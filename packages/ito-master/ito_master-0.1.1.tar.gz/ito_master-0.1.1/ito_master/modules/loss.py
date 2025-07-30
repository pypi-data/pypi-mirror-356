"""
    Implementation of objective functions used in the task 'ITO-Master'
"""
import numpy as np
import torch
import torch.nn.functional as F
import torch.nn as nn
import auraloss

import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(currentdir))
from modules.front_back_end import FrontEnd



# Root Mean Squared Loss
#   penalizes the volume factor with non-linearlity
class RMSLoss(nn.Module):
    def __init__(self, reduce, loss_type="l2"):
        super(RMSLoss, self).__init__()
        self.weight_factor = 100.
        if loss_type=="l2":
            self.loss = nn.MSELoss(reduce=None)


    def forward(self, est_targets, targets):
        est_targets = est_targets.reshape(est_targets.shape[0]*est_targets.shape[1], est_targets.shape[2])
        targets = targets.reshape(targets.shape[0]*targets.shape[1], targets.shape[2])
        normalized_est = torch.sqrt(torch.mean(est_targets**2, dim=-1))
        normalized_tgt = torch.sqrt(torch.mean(targets**2, dim=-1))

        weight = torch.clamp(torch.abs(normalized_tgt-normalized_est), min=1/self.weight_factor) * self.weight_factor

        return torch.mean(weight**1.5 * self.loss(normalized_est, normalized_tgt))



# Multi-Scale Spectral Loss proposed at the paper "DDSP: DIFFERENTIABLE DIGITAL SIGNAL PROCESSING" (https://arxiv.org/abs/2001.04643)
#   we extend this loss by applying it to mid/side channels
class MultiScale_Spectral_Loss_MidSide_DDSP(nn.Module):
    def __init__(self, mode='midside', \
                        reduce=True, \
                        n_filters=None, \
                        windows_size=None, \
                        hops_size=None, \
                        window="hann", \
                        eps=1e-7, \
                        device=torch.device("cpu")):
        super(MultiScale_Spectral_Loss_MidSide_DDSP, self).__init__()
        self.mode = mode
        self.eps = eps
        self.mid_weight = 0.5   # value in the range of 0.0 ~ 1.0
        self.logmag_weight = 0.1

        if n_filters is None:
            n_filters = [4096, 2048, 1024, 512]
        if windows_size is None:
            windows_size = [4096, 2048, 1024, 512]
        if hops_size is None:
            hops_size = [1024, 512, 256, 128]

        self.multiscales = []
        for i in range(len(windows_size)):
            cur_scale = {'window_size' : float(windows_size[i])}
            if self.mode=='midside':
                cur_scale['front_end'] = FrontEnd(channel='mono', \
                                                    n_fft=n_filters[i], \
                                                    hop_length=hops_size[i], \
                                                    win_length=windows_size[i], \
                                                    window=window, \
                                                    device=device)
            elif self.mode=='ori':
                cur_scale['front_end'] = FrontEnd(channel='stereo', \
                                                    n_fft=n_filters[i], \
                                                    hop_length=hops_size[i], \
                                                    win_length=windows_size[i], \
                                                    window=window, \
                                                    device=device)
            self.multiscales.append(cur_scale)

        self.objective_l1 = nn.L1Loss(reduce=reduce)
        self.objective_l2 = nn.MSELoss(reduce=reduce)


    def forward(self, est_targets, targets):
        if self.mode=='midside':
            return self.forward_midside(est_targets, targets)
        elif self.mode=='ori':
            return self.forward_ori(est_targets, targets)


    def forward_ori(self, est_targets, targets):
        total_mag_loss = 0.0
        total_logmag_loss = 0.0
        for cur_scale in self.multiscales:
            est_mag = cur_scale['front_end'](est_targets, mode=["mag"])
            tgt_mag = cur_scale['front_end'](targets, mode=["mag"])

            mag_loss = self.magnitude_loss(est_mag, tgt_mag)
            logmag_loss = self.log_magnitude_loss(est_mag, tgt_mag)
            total_mag_loss += mag_loss
            total_logmag_loss += logmag_loss
        # return total_loss
        return (1-self.logmag_weight)*total_mag_loss + \
                (self.logmag_weight)*total_logmag_loss


    def forward_midside(self, est_targets, targets):
        est_mid, est_side = self.to_mid_side(est_targets)
        tgt_mid, tgt_side = self.to_mid_side(targets)
        total_mag_loss = 0.0
        total_logmag_loss = 0.0
        for cur_scale in self.multiscales:
            est_mid_mag = cur_scale['front_end'](est_mid, mode=["mag"])
            est_side_mag = cur_scale['front_end'](est_side, mode=["mag"])
            tgt_mid_mag = cur_scale['front_end'](tgt_mid, mode=["mag"])
            tgt_side_mag = cur_scale['front_end'](tgt_side, mode=["mag"])

            mag_loss = self.mid_weight*self.magnitude_loss(est_mid_mag, tgt_mid_mag) + \
                        (1-self.mid_weight)*self.magnitude_loss(est_side_mag, tgt_side_mag)
            logmag_loss = self.mid_weight*self.log_magnitude_loss(est_mid_mag, tgt_mid_mag) + \
                        (1-self.mid_weight)*self.log_magnitude_loss(est_side_mag, tgt_side_mag)
            total_mag_loss += mag_loss
            total_logmag_loss += logmag_loss
        # return total_loss
        return (1-self.logmag_weight)*total_mag_loss + \
                (self.logmag_weight)*total_logmag_loss


    def to_mid_side(self, stereo_in):
        mid = stereo_in[:,0] + stereo_in[:,1]
        side = stereo_in[:,0] - stereo_in[:,1]
        return mid, side


    def magnitude_loss(self, est_mag_spec, tgt_mag_spec):
        return torch.norm(self.objective_l1(est_mag_spec, tgt_mag_spec))


    def log_magnitude_loss(self, est_mag_spec, tgt_mag_spec):
        est_log_mag_spec = torch.log10(est_mag_spec+self.eps)
        tgt_log_mag_spec = torch.log10(tgt_mag_spec+self.eps)
        return self.objective_l2(est_log_mag_spec, tgt_log_mag_spec)



# Class of available loss functions
class Loss:
    def __init__(self, args, reduce=True):
        device = torch.device("cpu")
        if torch.cuda.is_available():
            device = torch.device(f"cuda:{args.gpu}")
        self.l1 = nn.L1Loss(reduce=reduce)
        self.mse = nn.MSELoss(reduce=reduce)
        self.ce = nn.CrossEntropyLoss()
        self.triplet = nn.TripletMarginLoss(margin=1., p=2)
        self.cos = nn.CosineSimilarity(eps=args.eps)
        self.cosemb = nn.CosineEmbeddingLoss()

        self.multi_scale_spectral_midside = MultiScale_Spectral_Loss_MidSide_DDSP(mode='midside', eps=args.eps, device=device)
        self.multi_scale_spectral_ori = MultiScale_Spectral_Loss_MidSide_DDSP(mode='ori', eps=args.eps, device=device)
        self.gain = RMSLoss(reduce=reduce)
        # perceptual weighting with mel scaled spectrograms
        self.mrs_mel_perceptual = auraloss.freq.MultiResolutionSTFTLoss(
            fft_sizes=[1024, 2048, 8192],
            hop_sizes=[256, 512, 2048],
            win_lengths=[1024, 2048, 8192],
            scale="mel",
            n_bins=128,
            sample_rate=args.sample_rate,
            perceptual_weighting=True,
        )


import laion_clap
import torchaudio
# CLAP feature loss
class CLAPFeatureLoss(nn.Module):
    def __init__(self):
        super(CLAPFeatureLoss, self).__init__()
        self.target_sample_rate = 48000  # CLAP expects 48kHz audio
        self.model = laion_clap.CLAP_Module(enable_fusion=False)
        self.model.load_ckpt()  # download the default pretrained checkpoint
        self.model.eval()

    def forward(self, input_audio, target, sample_rate, distance_fn='cosine'):
        # Process input audio
        input_embed = self.process_audio(input_audio, sample_rate)

        # Process target (audio or text)
        if isinstance(target, torch.Tensor):
            target_embed = self.process_audio(target, sample_rate)
        elif isinstance(target, str) or (isinstance(target, list) and isinstance(target[0], str)):
            target_embed = self.process_text(target)
        else:
            raise ValueError("Target must be either audio tensor or text (string or list of strings)")

        # Compute loss using the specified distance function
        loss = self.compute_distance(input_embed, target_embed, distance_fn)

        return loss

    def process_audio(self, audio, sample_rate):
        # Ensure input is in the correct shape (N, C, T)
        if audio.dim() == 2:
            audio = audio.unsqueeze(1)

        # Convert to mono if stereo
        if audio.shape[1] > 1:
            audio = audio.mean(dim=1, keepdim=True)
        # Resample if necessary
        if sample_rate != self.target_sample_rate:
            audio = self.resample(audio, sample_rate)
        audio = audio.squeeze(1)
        
        # Get CLAP embeddings
        embed = self.model.get_audio_embedding_from_data(x=audio, use_tensor=True)
        return embed

    def process_text(self, text):
        # Get CLAP embeddings for text
        # ensure input is a list of strings
        if not isinstance(text, list):
            text = [text]
        embed = self.model.get_text_embedding(text, use_tensor=True)
        return embed

    def compute_distance(self, x, y, distance_fn):
        if distance_fn == 'mse':
            return F.mse_loss(x, y)
        elif distance_fn == 'l1':
            return F.l1_loss(x, y)
        elif distance_fn == 'cosine':
            return 1 - F.cosine_similarity(x, y).mean()
        else:
            raise ValueError(f"Unsupported distance function: {distance_fn}")

    def resample(self, audio, input_sample_rate):
        resampler = torchaudio.transforms.Resample(
            orig_freq=input_sample_rate, new_freq=self.target_sample_rate
        ).to(audio.device)
        return resampler(audio)



"""
    Audio Feature Loss implementation 
        copied from https://github.com/sai-soum/Diff-MST/blob/main/mst/loss.py
"""

import librosa

from typing import List
from modules.filter import barkscale_fbanks




def compute_mid_side(x: torch.Tensor):
    x_mid = x[:, 0, :] + x[:, 1, :]
    x_side = x[:, 0, :] - x[:, 1, :]
    return x_mid, x_side


def compute_melspectrum(
    x: torch.Tensor,
    sample_rate: int = 44100,
    fft_size: int = 32768,
    n_bins: int = 128,
    **kwargs,
):
    """Compute mel-spectrogram.

    Args:
        x: (bs, 2, seq_len)
        sample_rate: sample rate of audio
        fft_size: size of fft
        n_bins: number of mel bins

    Returns:
        X: (bs, n_bins)

    """
    fb = librosa.filters.mel(sr=sample_rate, n_fft=fft_size, n_mels=n_bins)
    fb = torch.tensor(fb).unsqueeze(0).type_as(x)

    x = x.mean(dim=1, keepdim=True)
    X = torch.fft.rfft(x, n=fft_size, dim=-1)
    X = torch.abs(X)
    X = torch.mean(X, dim=1, keepdim=True)  # take mean over time
    X = X.permute(0, 2, 1)  # swap time and freq dims
    X = torch.matmul(fb, X)
    X = torch.log(X + 1e-8)

    return X


def compute_barkspectrum(
    x: torch.Tensor,
    fft_size: int = 32768,
    n_bands: int = 24,
    sample_rate: int = 44100,
    f_min: float = 20.0,
    f_max: float = 20000.0,
    mode: str = "mid-side",
    **kwargs,
):
    """Compute bark-spectrogram.

    Args:
        x: (bs, 2, seq_len)
        fft_size: size of fft
        n_bands: number of bark bins
        sample_rate: sample rate of audio
        f_min: minimum frequency
        f_max: maximum frequency
        mode: "mono", "stereo", or "mid-side"

    Returns:
        X: (bs, 24)

    """
    # compute filterbank
    fb = barkscale_fbanks((fft_size // 2) + 1, f_min, f_max, n_bands, sample_rate)
    fb = fb.unsqueeze(0).type_as(x)
    fb = fb.permute(0, 2, 1)

    if mode == "mono":
        x = x.mean(dim=1)  # average over channels
        signals = [x]
    elif mode == "stereo":
        signals = [x[:, 0, :], x[:, 1, :]]
    elif mode == "mid-side":
        x_mid = x[:, 0, :] + x[:, 1, :]
        x_side = x[:, 0, :] - x[:, 1, :]
        signals = [x_mid, x_side]
    else:
        raise ValueError(f"Invalid mode {mode}")

    outputs = []
    for signal in signals:
        X = torch.stft(
            signal,
            n_fft=fft_size,
            hop_length=fft_size // 4,
            return_complex=True,
            window=torch.hann_window(fft_size).to(x.device),
        )  # compute stft
        X = torch.abs(X)  # take magnitude
        X = torch.mean(X, dim=-1, keepdim=True)  # take mean over time
        # X = X.permute(0, 2, 1)  # swap time and freq dims
        X = torch.matmul(fb, X)  # apply filterbank
        X = torch.log(X + 1e-8)
        # X = torch.cat([X, X_log], dim=-1)
        outputs.append(X)

    # stack into tensor
    X = torch.cat(outputs, dim=-1)

    return X


def compute_rms(x: torch.Tensor, **kwargs):
    """Compute root mean square energy.

    Args:
        x: (bs, 1, seq_len)

    Returns:
        rms: (bs, )
    """
    rms = torch.sqrt(torch.mean(x**2, dim=-1).clamp(min=1e-8))
    return rms


def compute_crest_factor(x: torch.Tensor, **kwargs):
    """Compute crest factor as ratio of peak to rms energy in dB.

    Args:
        x: (bs, 2, seq_len)

    """
    num = torch.max(torch.abs(x), dim=-1)[0]
    den = compute_rms(x).clamp(min=1e-8)
    cf = 20 * torch.log10((num / den).clamp(min=1e-8))
    return cf


def compute_stereo_width(x: torch.Tensor, **kwargs):
    """Compute stereo width as ratio of energy in sum and difference signals.

    Args:
        x: (bs, 2, seq_len)

    """
    bs, chs, seq_len = x.size()

    assert chs == 2, "Input must be stereo"

    # compute sum and diff of stereo channels
    x_sum = x[:, 0, :] + x[:, 1, :]
    x_diff = x[:, 0, :] - x[:, 1, :]

    # compute power of sum and diff
    sum_energy = torch.mean(x_sum**2, dim=-1)
    diff_energy = torch.mean(x_diff**2, dim=-1)

    # compute stereo width as ratio
    stereo_width = diff_energy / sum_energy.clamp(min=1e-8)

    return stereo_width


def compute_stereo_imbalance(x: torch.Tensor, **kwargs):
    """Compute stereo imbalance as ratio of energy in left and right channels.

    Args:
        x: (bs, 2, seq_len)

    Returns:
        stereo_imbalance: (bs, )

    """
    left_energy = torch.mean(x[:, 0, :] ** 2, dim=-1)
    right_energy = torch.mean(x[:, 1, :] ** 2, dim=-1)

    stereo_imbalance = (right_energy - left_energy) / (
        right_energy + left_energy
    ).clamp(min=1e-8)

    return stereo_imbalance


class AudioFeatureLoss(torch.nn.Module):
    def __init__(
        self,
        weights: List[float],
        sample_rate: int,
        stem_separation: bool = False,
        use_clap: bool = False,
    ) -> None:
        """Compute loss using a set of differentiable audio features.

        Args:
            weights: weights for each feature
            sample_rate: sample rate of audio
            stem_separation: whether to compute loss on stems or mix

        Based on features proposed in:

        Man, B. D., et al.
        "An analysis and evaluation of audio features for multitrack music mixtures."
        (2014).

        """
        super().__init__()
        self.weights = weights
        self.sample_rate = sample_rate
        self.stem_separation = stem_separation
        self.sources_list = ["mix"]
        self.source_weights = [1.0]
        self.use_clap = use_clap

        self.transforms = [
            compute_rms,
            compute_crest_factor,
            compute_stereo_width,
            compute_stereo_imbalance,
            compute_barkspectrum,
        ]

        assert len(self.transforms) == len(weights)

    def forward(self, input: torch.Tensor, target: torch.Tensor):
        losses = {}

        # reshape for example stem dim
        input_stems = input.unsqueeze(1)
        target_stems = target.unsqueeze(1)

        n_stems = input_stems.shape[1]

        # iterate over each stem compute loss for each transform
        for stem_idx in range(n_stems):
            input_stem = input_stems[:, stem_idx, ...]
            target_stem = target_stems[:, stem_idx, ...]

            for transform, weight in zip(self.transforms, self.weights):
                transform_name = "_".join(transform.__name__.split("_")[1:])
                key = f"{self.sources_list[stem_idx]}-{transform_name}"
                input_transform = transform(input_stem, sample_rate=self.sample_rate)
                target_transform = transform(target_stem, sample_rate=self.sample_rate)
                val = torch.nn.functional.mse_loss(input_transform, target_transform)
                losses[key] = weight * val * self.source_weights[stem_idx]

        return losses

