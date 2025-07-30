import io
import wave
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
from typing import Union, BinaryIO
import logging

logger = logging.getLogger(__name__)


class AudioConverter:
    """
    Класс для конвертации аудиофайлов в формат WAV в оперативной памяти.

    Поддерживает различные входные форматы, используя pydub.
    """

    def __init__(self, sample_rate: int = 16000, channels: int = 1, sample_width: int = 2):
        """
        Инициализирует конвертер с параметрами WAV по умолчанию.

        Args:
            sample_rate: Частота дискретизации (по умолчанию 16000 Гц).
            channels: Количество каналов (по умолчанию 1 - моно).
            sample_width:  Размер сэмпла в байтах (по умолчанию 2 - 16 бит).
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.sample_width = sample_width

    def convert_to_wav(self, audio_data: Union[bytes, BinaryIO]) -> bytes:
        """
        Конвертирует аудиоданные в формате bytes или BinaryIO в WAV (bytes).

        Args:
            audio_data: Аудиоданные в виде байтовой строки (bytes) или
                         файлоподобного объекта (BinaryIO).

        Returns:
            bytes: Аудиоданные в формате WAV (байтовая строка).

        Raises:
            CouldntDecodeError: Если pydub не смог декодировать входные данные.
            ValueError: Если входные данные не являются bytes или BinaryIO.
            Exception:  Другие ошибки при обработке.
        """
        try:
            # Определяем, является ли audio_data объектом BinaryIO
            if isinstance(audio_data, bytes):
                audio_stream = io.BytesIO(audio_data)
            elif hasattr(audio_data, 'read') and callable(audio_data.read):  # Duck typing
                audio_stream = audio_data
                # Важно: Если это BinaryIO, убеждаемся, что указатель в начале
                audio_stream.seek(0)
            else:
                raise ValueError("audio_data must be bytes or a BinaryIO object")

            # Используем try-except для обработки ошибок декодирования
            try:
                audio = AudioSegment.from_file(audio_stream)
            except CouldntDecodeError:
                # Пытаемся определить формат, если pydub не смог автоматически
                audio_stream.seek(0)  # Сбрасываем указатель
                try:
                  # Это место может потребовать дополнительной логики определения формата файла, если у вас есть такая информация
                  audio = AudioSegment.from_file(audio_stream, format='mp3') # or 'ogg', 'flv', etc.  Нужно определить явно
                except Exception as format_e:
                  logger.error(f"Pydub could not automatically detect the input file format. You might need to specify `format` manually (e.g. 'mp3', 'ogg'). Original decoding error: {format_e}")
                  raise


            # Применяем нужные параметры (частота, каналы, ширина)
            audio = audio.set_frame_rate(self.sample_rate)
            audio = audio.set_channels(self.channels)
            audio = audio.set_sample_width(self.sample_width)

            # Экспортируем в WAV в BytesIO
            wav_data = io.BytesIO()
            audio.export(wav_data, format="wav")
            return wav_data.getvalue()  # Возвращаем байты

        except Exception as e:
            logger.exception(f"Error during audio conversion: {e}")
            raise

