# fmt: off
import subprocess
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from desklab._check import value_check, CheckRange
from desklab._utils import get_ffmpeg_exe
from desklab.exceptions import BytesReadingError
# fmt: on


class Audio:

    __ffmpeg: str = str(get_ffmpeg_exe())

    def __init__(self, audio: str | bytes) -> None:
        self.__sound: pygame.mixer.Sound
        self.set(audio)

    def set(self, audio: str | bytes) -> None:
        if isinstance(audio, str):
            audio_buffer: bytes = self.__convert_to_wav(audio)
        else:
            audio_buffer = audio

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            self.__sound = pygame.mixer.Sound(audio_buffer)
        except (pygame.error, ValueError) as e:
            raise BytesReadingError(f"Failed to read audio source: {e}")

    @value_check(loops=CheckRange(-1, variable_name="loops"))
    def play(self, loops: int = 1) -> None:
        loops = loops - 1 if loops > 0 else loops
        self.__sound.play(loops=loops)

    def stop(self) -> None:
        self.__sound.stop()

    def __convert_to_wav(self, audio_path: str) -> bytes:
        try:
            process = subprocess.run(
                [
                    self.__ffmpeg, "-y", "-i", audio_path,
                    "-ac", "1", "-ar", "16000",
                    "-sample_fmt", "s16", "-f", "wav", "-"
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            error = f"Conversion to .wav failed for '{audio_path}': {e}"
            raise BytesReadingError(error)
        return process.stdout
