from __future__ import annotations

from lt_tensor.model_zoo.audio_models.hifigan import ConvNets
from lt_utils.common import *
from lt_tensor.torch_commons import *
from lt_tensor.model_base import Model
from lt_tensor.model_zoo.convs import ConvNets
from torch.nn import functional as F
from torchaudio import transforms as T
from lt_tensor.processors import AudioProcessor, AudioProcessorConfig


MULTI_DISC_OUT_TYPE: TypeAlias = Tuple[
    List[Tensor],
    List[Tensor],
    List[List[Tensor]],
    List[List[Tensor]],
]


class MultiDiscriminatorWrapper(Model):
    def __init__(self, list_discriminator: List["_MultiDiscriminatorT"]):
        """Setup example:
        model_d = MultiDiscriminatorStep(
            [
                MultiEnvelopeDiscriminator(),
                MultiBandDiscriminator(),
                MultiResolutionDiscriminator(),
                MultiPeriodDiscriminator(0.5),
            ]
        )
        """
        super().__init__()
        self.disc: Sequence[_MultiDiscriminatorT] = nn.ModuleList(list_discriminator)
        self.total = len(self.disc)

    def forward(
        self,
        y: Tensor,
        y_hat: Tensor,
        step_type: Literal["discriminator", "generator"],
    ) -> Union[
        Tuple[Tensor, Tensor, List[float]], Tuple[Tensor, List[float], List[float]]
    ]:
        """
        It returns the content based on the choice of "step_type", being it a
        'discriminator' or 'generator'

        For generator it returns:
        Tuple[Tensor, Tensor, List[float]]
        "gen_loss, feat_loss, all_g_losses"

        For 'discriminator' it returns:
        Tuple[Tensor, List[float], List[float]]
        "disc_loss, disc_real_losses, disc_gen_losses"
        """
        if step_type == "generator":
            all_g_losses: List[float] = []
            feat_loss: Tensor = 0
            gen_loss: Tensor = 0
        else:
            disc_loss: Tensor = 0
            disc_real_losses: List[float] = []
            disc_gen_losses: List[float] = []

        for disc in self.disc:
            if step_type == "generator":
                #  feature loss, generator loss, list of generator losses (float)]
                f_loss, g_loss, g_losses = disc.gen_step(y, y_hat)
                gen_loss += g_loss
                feat_loss += f_loss
                all_g_losses.extend(g_losses)
            else:
                # [discriminator loss, (disc losses real, disc losses generated)]
                d_loss, (d_real_losses, d_gen_losses) = disc.disc_step(y, y_hat)
                disc_loss += d_loss
                disc_real_losses.extend(d_real_losses)
                disc_gen_losses.extend(d_gen_losses)

        if step_type == "generator":
            return gen_loss, feat_loss, all_g_losses
        return disc_loss, disc_real_losses, disc_gen_losses


def normalize_unit_norm(x: torch.Tensor, eps: float = 1e-5):
    norm = torch.norm(x, dim=-1, keepdim=True)
    return x / (norm + eps)


def normalize_minmax(x: torch.Tensor, eps: float = 1e-5):
    min_val = x.amin(dim=-1, keepdim=True)
    max_val = x.amax(dim=-1, keepdim=True)
    return (x - min_val) / (max_val - min_val + eps)


def normalize_zscore(x: torch.Tensor, eps: float = 1e-5):
    mean = x.mean(dim=-1, keepdim=True)
    std = x.std(dim=-1, keepdim=True)
    return (x - mean) / (std + eps)


def get_padding(kernel_size, dilation=1):
    return int((kernel_size * dilation - dilation) / 2)


class _MultiDiscriminatorT(ConvNets):
    """Base for all multi-steps type of discriminators"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.leaky_relu = nn.LeakyReLU(kwargs.get("negative_slope", 0.1))

    def forward(self, y: Tensor, y_hat: Tensor) -> MULTI_DISC_OUT_TYPE:
        pass

    # for type hinting
    def __call__(self, *args, **kwds) -> MULTI_DISC_OUT_TYPE:
        return super().__call__(*args, **kwds)

    def gen_step(self, y: Tensor, y_hat: Tensor) -> tuple[Tensor, Tensor, List[float]]:
        """For generator loss step [feature loss, generator loss, list of generator losses (float)]"""
        _, y_hat_gen, feat_map_real, feat_map_gen = self.train_step(y, y_hat)
        loss_feat = self.feature_loss(feat_map_real, feat_map_gen)
        loss_generator, losses_gen_s = self.generator_loss(y_hat_gen)
        return loss_feat, loss_generator, losses_gen_s

    def disc_step(
        self, y: Tensor, y_hat: Tensor
    ) -> tuple[Tensor, tuple[List[float], List[float]]]:
        """For discriminator loss step [discriminator loss, (disc losses real, disc losses generated)]"""
        y_hat_real, y_hat_gen, _, _ = self.train_step(y, y_hat)

        loss_disc, losses_disc_real, losses_disc_generated = self.discriminator_loss(
            y_hat_real, y_hat_gen
        )
        return loss_disc, (losses_disc_real, losses_disc_generated)

    @staticmethod
    def discriminator_loss(
        disc_real_outputs, disc_generated_outputs
    ) -> Tuple[Tensor, List[float], List[float]]:
        loss = 0
        r_losses = []
        g_losses = []
        for dr, dg in zip(disc_real_outputs, disc_generated_outputs):
            r_loss = torch.mean((1 - dr) ** 2)
            g_loss = torch.mean(dg**2)
            loss += r_loss + g_loss
            r_losses.append(r_loss.item())
            g_losses.append(g_loss.item())

        return loss, r_losses, g_losses

    @staticmethod
    def feature_loss(fmap_r, fmap_g) -> Tensor:
        loss = 0
        for dr, dg in zip(fmap_r, fmap_g):
            for rl, gl in zip(dr, dg):
                loss += torch.mean(torch.abs(rl - gl))

        return loss * 2

    @staticmethod
    def generator_loss(disc_outputs) -> Tuple[Tensor, List[float]]:
        loss = 0
        gen_losses = []
        for dg in disc_outputs:
            l = torch.mean((1 - dg) ** 2)
            gen_losses.append(l.item())
            loss += l

        return loss, gen_losses


class DiscriminatorP(ConvNets):
    def __init__(
        self,
        period: List[int],
        discriminator_channel_mult: Number = 1,
        kernel_size: int = 5,
        stride: int = 3,
        use_spectral_norm: bool = False,
    ):
        super().__init__()
        self.period = period
        norm_f = weight_norm if not use_spectral_norm else spectral_norm
        dsc = lambda x: int(x * discriminator_channel_mult)
        self.convs = nn.ModuleList(
            [
                norm_f(
                    nn.Conv2d(
                        1,
                        dsc(32),
                        (kernel_size, 1),
                        (stride, 1),
                        padding=(get_padding(5, 1), 0),
                    )
                ),
                norm_f(
                    nn.Conv2d(
                        dsc(32),
                        dsc(128),
                        (kernel_size, 1),
                        (stride, 1),
                        padding=(get_padding(5, 1), 0),
                    )
                ),
                norm_f(
                    nn.Conv2d(
                        dsc(128),
                        dsc(512),
                        (kernel_size, 1),
                        (stride, 1),
                        padding=(get_padding(5, 1), 0),
                    )
                ),
                norm_f(
                    nn.Conv2d(
                        dsc(512),
                        dsc(1024),
                        (kernel_size, 1),
                        (stride, 1),
                        padding=(get_padding(5, 1), 0),
                    )
                ),
                norm_f(
                    nn.Conv2d(
                        dsc(1024),
                        dsc(1024),
                        (kernel_size, 1),
                        1,
                        padding=(2, 0),
                    )
                ),
            ]
        )
        self.conv_post = norm_f(nn.Conv2d(dsc(1024), 1, (3, 1), 1, padding=(1, 0)))

    def forward(self, x: Tensor) -> Tuple[Tensor, List[Tensor]]:
        fmap = []

        # 1d to 2d
        b, c, t = x.shape
        if t % self.period != 0:  # pad first
            n_pad = self.period - (t % self.period)
            x = F.pad(x, (0, n_pad), "reflect")
            t = t + n_pad
        x = x.view(b, c, t // self.period, self.period)

        for l in self.convs:
            x = l(x)
            x = F.leaky_relu(x, 0.1)
            fmap.append(x)
        x = self.conv_post(x)
        fmap.append(x)
        return x.flatten(1, -1), fmap


class MultiPeriodDiscriminator(_MultiDiscriminatorT):
    def __init__(
        self,
        discriminator_channel_mult: Number = 1,
        mpd_reshapes: list[int] = [2, 3, 5, 7, 11],
        use_spectral_norm: bool = False,
    ):
        super().__init__()
        self.mpd_reshapes = mpd_reshapes
        print(f"mpd_reshapes: {self.mpd_reshapes}")
        self.discriminators = nn.ModuleList(
            [
                DiscriminatorP(
                    rs,
                    use_spectral_norm=use_spectral_norm,
                    discriminator_channel_mult=discriminator_channel_mult,
                )
                for rs in self.mpd_reshapes
            ]
        )

    def forward(self, y: torch.Tensor, y_hat: torch.Tensor) -> MULTI_DISC_OUT_TYPE:
        y_d_rs = []
        y_d_gs = []
        fmap_rs = []
        fmap_gs = []
        for i, d in enumerate(self.discriminators):
            y_d_r, fmap_r = d(y)
            y_d_g, fmap_g = d(y_hat)
            y_d_rs.append(y_d_r)
            fmap_rs.append(fmap_r)
            y_d_gs.append(y_d_g)
            fmap_gs.append(fmap_g)

        return y_d_rs, y_d_gs, fmap_rs, fmap_gs


class EnvelopeExtractor(Model):
    """Extracts the amplitude envelope of the audio signal."""

    def __init__(self, kernel_size=101):
        super().__init__()
        # Lowpass filter for smoothing envelope (moving average)
        self.kernel_size = kernel_size
        self.register_buffer("kernel", torch.ones(1, 1, kernel_size) / kernel_size)

    def forward(self, x: Tensor):
        # x: (B, 1, T) -> abs(x)
        envelope = torch.abs(x)
        # Apply low-pass smoothing (via conv1d)
        envelope = F.pad(
            envelope, (self.kernel_size // 2, self.kernel_size // 2), mode="reflect"
        )
        envelope = F.conv1d(envelope, self.kernel)
        return envelope


class DiscriminatorEnvelope(ConvNets):
    def __init__(self, use_spectral_norm=False):
        super().__init__()
        norm_f = weight_norm if not use_spectral_norm else spectral_norm
        self.extractor = EnvelopeExtractor(kernel_size=101)
        self.convs = nn.ModuleList(
            [
                norm_f(nn.Conv1d(1, 64, 15, stride=1, padding=7)),
                norm_f(nn.Conv1d(64, 128, 41, stride=2, groups=4, padding=20)),
                norm_f(nn.Conv1d(128, 256, 41, stride=2, groups=16, padding=20)),
                norm_f(nn.Conv1d(256, 512, 41, stride=4, groups=16, padding=20)),
                norm_f(nn.Conv1d(512, 512, 41, stride=4, groups=16, padding=20)),
                norm_f(nn.Conv1d(512, 512, 5, stride=1, padding=2)),
            ]
        )
        self.conv_post = norm_f(nn.Conv1d(512, 1, 3, stride=1, padding=1))
        self.activation = nn.LeakyReLU(0.1)

    def forward(self, x):
        # Input: raw audio (B, 1, T)
        x = self.extractor(x)
        fmap = []
        for layer in self.convs:
            x = self.activation(layer(x))
            fmap.append(x)
        x = self.conv_post(x)
        fmap.append(x)
        return x.flatten(1), fmap


class MultiEnvelopeDiscriminator(_MultiDiscriminatorT):
    def __init__(self, use_spectral_norm: bool = False):
        super().__init__()
        self.discriminators = nn.ModuleList(
            [
                DiscriminatorEnvelope(use_spectral_norm),  # raw envelope
                DiscriminatorEnvelope(use_spectral_norm),  # downsampled once
                DiscriminatorEnvelope(use_spectral_norm),  # downsampled twice
            ]
        )
        self.meanpools = nn.ModuleList(
            [nn.AvgPool1d(4, 2, padding=2), nn.AvgPool1d(4, 2, padding=2)]
        )

    def forward(self, y, y_hat):
        y_d_rs, y_d_gs = [], []
        fmap_rs, fmap_gs = [], []
        for i, d in enumerate(self.discriminators):
            if i != 0:
                y = self.meanpools[i - 1](y)
                y_hat = self.meanpools[i - 1](y_hat)
            y_d_r, fmap_r = d(y)
            y_d_g, fmap_g = d(y_hat)
            y_d_rs.append(y_d_r)
            y_d_gs.append(y_d_g)
            fmap_rs.append(fmap_r)
            fmap_gs.append(fmap_g)

        return y_d_rs, y_d_gs, fmap_rs, fmap_gs


class DiscriminatorB(ConvNets):
    """
    Multi-band multi-scale STFT discriminator, with the architecture based on https://github.com/descriptinc/descript-audio-codec.
    and the modified code adapted from https://github.com/gemelo-ai/vocos.
    """

    def __init__(
        self,
        window_length: int,
        channels: int = 32,
        hop_factor: float = 0.25,
        bands: Tuple[Tuple[float, float], ...] = (
            (0.0, 0.1),
            (0.1, 0.25),
            (0.25, 0.5),
            (0.5, 0.75),
            (0.75, 1.0),
        ),
    ):
        super().__init__()
        self.window_length = window_length
        self.hop_factor = hop_factor
        self.spec_fn = T.Spectrogram(
            n_fft=window_length,
            hop_length=int(window_length * hop_factor),
            win_length=window_length,
            power=None,
        )
        n_fft = window_length // 2 + 1
        bands = [(int(b[0] * n_fft), int(b[1] * n_fft)) for b in bands]
        self.bands = bands
        convs = lambda: nn.ModuleList(
            [
                weight_norm(nn.Conv2d(2, channels, (3, 9), (1, 1), padding=(1, 4))),
                weight_norm(
                    nn.Conv2d(channels, channels, (3, 9), (1, 2), padding=(1, 4))
                ),
                weight_norm(
                    nn.Conv2d(channels, channels, (3, 9), (1, 2), padding=(1, 4))
                ),
                weight_norm(
                    nn.Conv2d(channels, channels, (3, 9), (1, 2), padding=(1, 4))
                ),
                weight_norm(
                    nn.Conv2d(channels, channels, (3, 3), (1, 1), padding=(1, 1))
                ),
            ]
        )
        self.band_convs = nn.ModuleList([convs() for _ in range(len(self.bands))])

        self.conv_post = weight_norm(
            nn.Conv2d(channels, 1, (3, 3), (1, 1), padding=(1, 1))
        )

    def spectrogram(self, x: Tensor) -> List[Tensor]:
        # Remove DC offset
        x = x - x.mean(dim=-1, keepdims=True)
        # Peak normalize the volume of input audio
        x = 0.8 * x / (x.abs().max(dim=-1, keepdim=True)[0] + 1e-9)
        x = self.spec_fn(x)
        x = torch.view_as_real(x)
        x = x.permute(0, 3, 2, 1)  # [B, F, T, C] -> [B, C, T, F]
        # Split into bands
        x_bands = [x[..., b[0] : b[1]] for b in self.bands]
        return x_bands

    def forward(self, x: Tensor) -> Tuple[Tensor, List[Tensor]]:
        x_bands = self.spectrogram(x.squeeze(1))
        fmap = []
        x = []

        for band, stack in zip(x_bands, self.band_convs):
            for i, layer in enumerate(stack):
                band = layer(band)
                band = torch.nn.functional.leaky_relu(band, 0.1)
                if i > 0:
                    fmap.append(band)
            x.append(band)

        x = torch.cat(x, dim=-1)
        x = self.conv_post(x)
        fmap.append(x)

        return x, fmap


class MultiBandDiscriminator(_MultiDiscriminatorT):
    """
    Multi-band multi-scale STFT discriminator, with the architecture based on https://github.com/descriptinc/descript-audio-codec.
    and the modified code adapted from https://github.com/gemelo-ai/vocos.
    """

    def __init__(
        self,
        mbd_fft_sizes: list[int] = [2048, 1024, 512],
    ):
        super().__init__()
        self.fft_sizes = mbd_fft_sizes
        self.discriminators = nn.ModuleList(
            [DiscriminatorB(window_length=w) for w in self.fft_sizes]
        )

    def forward(self, y: Tensor, y_hat: Tensor) -> MULTI_DISC_OUT_TYPE:

        y_d_rs = []
        y_d_gs = []
        fmap_rs = []
        fmap_gs = []

        for d in self.discriminators:

            y_d_r, fmap_r = d(x=y)
            y_d_g, fmap_g = d(x=y_hat)
            y_d_rs.append(y_d_r)
            fmap_rs.append(fmap_r)
            y_d_gs.append(y_d_g)
            fmap_gs.append(fmap_g)

        return y_d_rs, y_d_gs, fmap_rs, fmap_gs


class DiscriminatorR(ConvNets):
    def __init__(
        self,
        resolution: List[int],
        use_spectral_norm: bool = False,
        discriminator_channel_mult: int = 1,
    ):
        super().__init__()

        self.resolution = resolution
        assert (
            len(self.resolution) == 3
        ), f"MRD layer requires list with len=3, got {self.resolution}"
        self.lrelu_slope = 0.1

        self.register_buffer("window", torch.hann_window(self.resolution[-1]))

        norm_f = weight_norm if use_spectral_norm == False else spectral_norm

        self.convs = nn.ModuleList(
            [
                norm_f(
                    nn.Conv2d(
                        1, int(32 * discriminator_channel_mult), (3, 9), padding=(1, 4)
                    )
                ),
                norm_f(
                    nn.Conv2d(
                        int(32 * discriminator_channel_mult),
                        int(32 * discriminator_channel_mult),
                        (3, 9),
                        stride=(1, 2),
                        padding=(1, 4),
                    )
                ),
                norm_f(
                    nn.Conv2d(
                        int(32 * discriminator_channel_mult),
                        int(32 * discriminator_channel_mult),
                        (3, 9),
                        stride=(1, 2),
                        padding=(1, 4),
                    )
                ),
                norm_f(
                    nn.Conv2d(
                        int(32 * discriminator_channel_mult),
                        int(32 * discriminator_channel_mult),
                        (3, 9),
                        stride=(1, 2),
                        padding=(1, 4),
                    )
                ),
                norm_f(
                    nn.Conv2d(
                        int(32 * discriminator_channel_mult),
                        int(32 * discriminator_channel_mult),
                        (3, 3),
                        padding=(1, 1),
                    )
                ),
            ]
        )
        self.conv_post = norm_f(
            nn.Conv2d(int(32 * discriminator_channel_mult), 1, (3, 3), padding=(1, 1))
        )

    def forward(self, x: Tensor) -> Tuple[Tensor, List[Tensor]]:
        fmap = []
        x = self.spectrogram(x)
        x = x.unsqueeze(1)
        for l in self.convs:
            x = l(x)
            x = F.leaky_relu(x, self.lrelu_slope)
            fmap.append(x)
        x = self.conv_post(x)
        fmap.append(x)
        x = torch.flatten(x, 1, -1)

        return x, fmap

    def spectrogram(self, x: Tensor) -> Tensor:
        n_fft, hop_length, win_length = self.resolution
        x = F.pad(
            x,
            (int((n_fft - hop_length) / 2), int((n_fft - hop_length) / 2)),
            mode="reflect",
        )
        x = x.squeeze(1)
        x = torch.stft(
            x,
            n_fft=n_fft,
            hop_length=hop_length,
            win_length=win_length,
            center=False,
            return_complex=True,
            window=self.window,
        )
        x = torch.view_as_real(x)  # [B, F, TT, 2]
        mag = torch.norm(x, p=2, dim=-1)  # [B, F, TT]

        return mag


class MultiResolutionDiscriminator(_MultiDiscriminatorT):
    def __init__(
        self,
        use_spectral_norm: bool = False,
        discriminator_channel_mult: int = 1,
        resolutions: List[List[int]] = [
            [1024, 120, 600],
            [2048, 240, 1200],
            [512, 50, 240],
        ],
    ):
        super().__init__()
        self.resolutions = resolutions
        assert (
            len(self.resolutions) == 3
        ), f"MRD requires list of list with len=3, each element having a list with len=3. Got {self.resolutions}, type: {type(self.resolutions)}"
        self.discriminators = nn.ModuleList(
            [
                DiscriminatorR(
                    resolution, use_spectral_norm, discriminator_channel_mult
                )
                for resolution in self.resolutions
            ]
        )

    def forward(self, y: Tensor, y_hat: Tensor) -> MULTI_DISC_OUT_TYPE:
        y_d_rs = []
        y_d_gs = []
        fmap_rs = []
        fmap_gs = []
        for disc in self.discriminators:
            y_d_r, fmap_r = disc(x=y)
            y_d_g, fmap_g = disc(x=y_hat)
            y_d_rs.append(y_d_r)
            fmap_rs.append(fmap_r)
            y_d_gs.append(y_d_g)
            fmap_gs.append(fmap_g)
        return y_d_rs, y_d_gs, fmap_rs, fmap_gs


class MultiMelScaleLoss(Model):
    # TODO: Make the normalization an argument to be chosen by the dev
    def __init__(
        self,
        sample_rate: int,
        n_mels: List[int] = [5, 10, 20, 40, 80, 160, 320],
        window_lengths: List[int] = [32, 64, 128, 256, 512, 1024, 2048],
        n_ffts: List[int] = [32, 64, 128, 256, 512, 1024, 2048],
        hops: List[int] = [8, 16, 32, 64, 128, 256, 512],
        weight: float = 1.0,
        lambda_mel: float = 1.0,
        f_min: float = [0, 0, 0, 0, 0, 0, 0],
        f_max: Optional[float] = [None, None, None, None, None, None, None],
        loss_fn: Callable = nn.L1Loss(),
        center: bool = True,
        power: float = 1.0,
        normalized: bool = False,
        pad_mode: str = "reflect",
        onesided: Optional[bool] = None,
        std: int = 4,
        mean: int = -4,
        auto_interpolate: bool = True,
        use_istft_norm: bool = True,
        use_pitch_loss: bool = False,
        use_rms_loss: bool = False,
        lambda_pitch: float = 0.5,
        lambda_rms: float = 0.5,
    ):
        super().__init__()
        assert (
            len(n_mels)
            == len(window_lengths)
            == len(n_ffts)
            == len(hops)
            == len(f_min)
            == len(f_max)
        )
        self.loss_fn = loss_fn
        self.lambda_mel = lambda_mel
        self.weight = weight
        self.use_istft_norm = use_istft_norm
        self.auto_interpolate = auto_interpolate if not self.use_istft_norm else False
        self.use_pitch_loss = use_pitch_loss
        self.use_rms_loss = use_rms_loss
        self.lambda_pitch = lambda_pitch
        self.lambda_rms = lambda_rms

        self._setup_mels(
            sample_rate,
            n_mels,
            window_lengths,
            n_ffts,
            hops,
            f_min,
            f_max,
            center,
            power,
            normalized,
            pad_mode,
            onesided,
            std,
            mean,
        )

    def _setup_mels(
        self,
        sample_rate: int,
        n_mels: List[int],
        window_lengths: List[int],
        n_ffts: List[int],
        hops: List[int],
        f_min: List[float],
        f_max: List[Optional[float]],
        center: bool,
        power: float,
        normalized: bool,
        pad_mode: str = "reflect",
        onesided: Optional[bool] = None,
        std: int = 4,
        mean: int = -4,
    ):
        assert (
            len(n_mels)
            == len(window_lengths)
            == len(n_ffts)
            == len(hops)
            == len(f_min)
            == len(f_max)
        )
        _mel_kwargs = dict(
            sample_rate=sample_rate,
            center=center,
            onesided=onesided,
            normalized=normalized,
            power=power,
            pad_mode=pad_mode,
            std=std,
            mean=mean,
        )
        self.mel_spectrograms: List[AudioProcessor] = nn.ModuleList(
            [
                AudioProcessor(
                    AudioProcessorConfig(
                        **_mel_kwargs,
                        n_mels=mel,
                        n_fft=n_fft,
                        win_length=win,
                        hop_length=hop,
                        f_min=fmin,
                        f_max=fmax,
                    )
                )
                for mel, win, n_fft, hop, fmin, fmax in zip(
                    n_mels, window_lengths, n_ffts, hops, f_min, f_max
                )
            ]
        )

    def _process_tensor(
        self,
        input_wave: torch.Tensor,
        target_wave: torch.Tensor,
    ):
        if input_wave.shape[-1] != target_wave.shape[-1]:
            if input_wave.ndim < 3:
                # To be compatible with interpolatin
                if input_wave.ndim == 2:
                    input_wave = input_wave.unsqueeze(1)
                else:
                    input_wave = input_wave.unsqueeze(0).unsqueeze(0)
            input_wave = F.interpolate(input_wave, target_wave.shape[-1], mode="linear")
        return input_wave

    def forward(
        self, input_wave: torch.Tensor, target_wave: torch.Tensor
    ) -> torch.Tensor:
        assert (
            self.use_istft_norm
            or self.auto_interpolate
            or input_wave.shape[-1] == target_wave.shape[-1]
        )
        if self.auto_interpolate:
            input_wave = self._process_tensor(input_wave, target_wave)

        losses = 0.0
        for M in self.mel_spectrograms:
            # Apply normalization if requested
            if self.use_istft_norm:
                input_proc = M.istft_norm(input_wave, length=target_wave.shape[-1])
                target_proc = M.istft_norm(target_wave, length=target_wave.shape[-1])
            else:
                input_proc, target_proc = input_wave, target_wave

            x_mels = M(input_proc)
            y_mels = M(target_proc)

            loss = self.loss_fn(x_mels.squeeze(), y_mels.squeeze())
            losses += loss * self.lambda_mel

            # pitch/f0 loss
            if self.use_pitch_loss:
                x_pitch = normalize_unit_norm(M.compute_pitch(input_proc))
                y_pitch = normalize_unit_norm(M.compute_pitch(target_proc))
                f0_loss = self.loss_fn(x_pitch, y_pitch)
                losses += f0_loss * self.lambda_pitch

            # energy/rms loss
            if self.use_rms_loss:
                x_rms = normalize_unit_norm(M.compute_rms(input_proc, x_mels))
                y_rms = normalize_unit_norm(M.compute_rms(target_proc, y_mels))
                rms_loss = self.loss_fn(x_rms, y_rms)
                losses += rms_loss * self.lambda_rms

        return losses * self.weight
