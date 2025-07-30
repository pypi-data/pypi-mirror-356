from subprocess import CalledProcessError, run
from typing import Tuple

import torch
import torchaudio
from torch import Tensor, nn

from typing import Union
import librosa
import io
import numpy as np
import soundfile as sf

SAMPLE_RATE = 16000


def load_audio(
    audio_path: str, sample_rate: int = SAMPLE_RATE, return_format: str = "float"
) -> Tensor:
    """
    Load an audio file and resample it to the specified sample rate.
    """
    cmd = [
        "ffmpeg",
        "-nostdin",
        "-threads",
        "0",
        "-i",
        audio_path,
        "-f",
        "s16le",
        "-ac",
        "1",
        "-acodec",
        "pcm_s16le",
        "-ar",
        str(sample_rate),
        "-",
    ]
    try:
        audio = run(cmd, capture_output=True, check=True).stdout
    except CalledProcessError as exc:
        raise RuntimeError("Failed to load audio") from exc

    if return_format == "float":
        return torch.frombuffer(audio, dtype=torch.int16).float() / 32768.0

    return torch.frombuffer(audio, dtype=torch.int16)

def load_audio_bytes(
    audio_source: Union[str, bytes, io.BytesIO], 
    sample_rate: int = SAMPLE_RATE, 
    return_format: str = "float"
) -> torch.Tensor:
    """
    Загружает аудио из файла, байтов или объекта BytesIO, преобразует 
    к заданной частоте дискретизации и возвращает Tensor.
    """
    try:
        if isinstance(audio_source, str):  # Путь к файлу
            audio, sr = librosa.load(audio_source, sr=sample_rate)
        elif isinstance(audio_source, bytes): # Байты
            audio, sr = sf.read(io.BytesIO(audio_source), dtype='float32') # или 'int16'
            if sr != sample_rate:
                audio = librosa.resample(audio, orig_sr=sr, target_sr=sample_rate)
        elif isinstance(audio_source, io.BytesIO): # BytesIO объект
            audio, sr = sf.read(audio_source, dtype='float32') # или 'int16'
            if sr != sample_rate:
                audio = librosa.resample(audio, orig_sr=sr, target_sr=sample_rate)
        else:
            raise TypeError("Неподдерживаемый тип аудиоисточника.")


        if return_format == "float":
            # Конвертируем NumPy array в Tensor и нормализуем
            return torch.from_numpy(audio).float()  # .float() важно для нормализации!
        else:
            return torch.from_numpy(audio).int() # Если нужен int16 Tensor

    except Exception as exc:
        raise RuntimeError("Ошибка при загрузке аудио") from exc
    
class SpecScaler(nn.Module):
    """
    Module that applies logarithmic scaling to spectrogram values.
    This module clamps the input values within a certain range and then applies a natural logarithm.
    """

    def forward(self, x: Tensor) -> Tensor:
        return torch.log(x.clamp_(1e-9, 1e9))


class FeatureExtractor(nn.Module):
    """
    Module for extracting Log-mel spectrogram features from raw audio signals.
    This module uses Torchaudio's MelSpectrogram transform to extract features
    and applies logarithmic scaling.
    """

    def __init__(self, sample_rate: int, features: int):
        super().__init__()
        self.hop_length = sample_rate // 100
        self.featurizer = nn.Sequential(
            torchaudio.transforms.MelSpectrogram(
                sample_rate=sample_rate,
                n_fft=sample_rate // 40,
                win_length=sample_rate // 40,
                hop_length=self.hop_length,
                n_mels=features,
            ),
            SpecScaler(),
        )

    def out_len(self, input_lengths: Tensor) -> Tensor:
        """
        Calculates the output length after the feature extraction process.
        """
        return input_lengths.div(self.hop_length, rounding_mode="floor").add(1).long()

    def forward(self, input_signal: Tensor, length: Tensor) -> Tuple[Tensor, Tensor]:
        """
        Extract Log-mel spectrogram features from the input audio signal.
        """
        return self.featurizer(input_signal), self.out_len(length)
