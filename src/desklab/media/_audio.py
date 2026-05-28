# fmt: off
import subprocess
from imageio_ffmpeg import get_ffmpeg_exe  # type: ignore
from io import BytesIO
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from desklab.exceptions import BytesReadingError
from desklab._check import type_check
# fmt: on


@type_check
class Audio:

    def __init__(self, audio: str | BytesIO) -> None:
        self.set(audio)

    def set(self, audio: str | BytesIO):
        if isinstance(audio, str):
            audio = self.__convert_to_wav(audio)
        try:
            self.__sound = pygame.mixer.Sound(audio)
        except pygame.error as e:
            raise BytesReadingError(str(e))

    def play(self, loops: int = 1):
        self.__sound.play(loops)

    def __convert_to_wav(self, audio: str) -> BytesIO:
        ffmpeg = get_ffmpeg_exe()

        process = subprocess.run([ffmpeg, "-i", audio, "-ac", "1",
                                  "-ar", "16000", "-sample_fmt", "s16",
                                  "-f", "wav", "-"],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.DEVNULL,
                                 check=True)

        wav_buffer = BytesIO(process.stdout)
        wav_buffer.seek(0)
        return wav_buffer
