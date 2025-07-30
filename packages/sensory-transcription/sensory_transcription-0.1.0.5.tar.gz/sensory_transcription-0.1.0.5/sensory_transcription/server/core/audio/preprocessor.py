# app/core/audio/preprocessor.py
import io, asyncio
from pydub import AudioSegment
from typing import Protocol
import noisereduce as nr            # pip install noisereduce (или любой метод NR)

class PreprocessorProtocol(Protocol):
    async def prepare(self, audio_b: bytes) -> bytes: ...

class AudioPreprocessor:

    def __init__(self,
                 target_sr: int = 16000,
                 channels: int = 1,
                 sample_width: int = 2,
                 apply_nr: bool = True,
                 normalize_dbfs: float | None = -14.0):
        self.target_sr = target_sr
        self.channels = channels
        self.sample_width = sample_width
        self.apply_nr = apply_nr
        self.normalize_dbfs = normalize_dbfs

    async def prepare(self, audio_b: bytes) -> bytes:
        return await asyncio.to_thread(self._sync_prepare, audio_b)

    def _sync_prepare(self, audio_b: bytes) -> bytes:
        seg = AudioSegment.from_file(io.BytesIO(audio_b))

        # 1. нормализация громкости
        if self.normalize_dbfs is not None:
            seg = seg.apply_gain(self.normalize_dbfs - seg.dBFS)

        # 2. шумоподавление (пример, можно заменить/выключить)
        if self.apply_nr:
            y = seg.get_array_of_samples()
            y = nr.reduce_noise(y=y, sr=seg.frame_rate)
            seg = seg._spawn(y.tobytes())

        # 3. приведение к целевым параметрам
        seg = (
            seg.set_frame_rate(self.target_sr)
               .set_channels(self.channels)
               .set_sample_width(self.sample_width)
        )

        out = io.BytesIO()
        seg.export(out, format="wav")
        return out.getvalue()