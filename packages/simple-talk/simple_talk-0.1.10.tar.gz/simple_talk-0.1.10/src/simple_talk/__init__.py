from __future__ import annotations

import multiprocessing
import sys
from enum import StrEnum
from os import path
from pathlib import Path
from shutil import move
from subprocess import run
from tempfile import gettempdir
from typing import Any
from uuid import uuid4

from extratools_av.audio import normalize as normalize_volume
from moviepy.audio.io.AudioFileClip import AudioFileClip

from .helpers import text_to_sentences_with_min_duration


class Synthesizer(StrEnum):
    AMAZON_POLLY = "AMAZON_POLLY"
    ESPEAK_NG = "ESPEAK_NG"
    MAC_OS = "MAC_OS"


class SimpleTalk:
    def __init__(
        self,
        *,
        voice: str | None = None,
        synthesizer: Synthesizer = Synthesizer.MAC_OS,
        engine: str | None = None,
        normalize_volume: bool = True,
    ) -> None:
        if synthesizer == Synthesizer.MAC_OS and sys.platform != "darwin":
            msg = "You must run the specified synthesizer on macOS."
            raise ValueError(msg)

        if synthesizer == Synthesizer.AMAZON_POLLY:
            import boto3  # noqa: PLC0415
            self.__polly_client = boto3.client("polly")

            if not voice or not engine:
                msg = "You must specify engine and voice for Amazon Polly."
                raise ValueError(msg)

        self.__voice: str | None = voice
        self.__synthesizer: Synthesizer = synthesizer
        self.__normalize_volume: bool = normalize_volume

    def talk(
        self,
        text: str,
        filename_prefix: str | None = None,
    ) -> str | AudioFileClip:
        return_clip: bool = filename_prefix is None
        filename_prefix = filename_prefix or path.join(gettempdir(), str(uuid4()))

        filename: str
        match self.__synthesizer:
            case Synthesizer.MAC_OS:
                filename = self.__talk_macos(text, filename_prefix)
            case Synthesizer.ESPEAK_NG:
                filename = self.__talk_espeak(text, filename_prefix)
            case Synthesizer.AMAZON_POLLY:
                filename = self.__talk_polly(text, filename_prefix)
            case _:
                msg = "The specified synthesizer is not implemented yet."
                raise NotImplementedError(msg)

        if self.__normalize_volume:
            normalized_clip = normalize_volume(filename)

            temp_filename: str = filename_prefix + ".tmp.mp3"
            normalized_clip.write_audiofile(temp_filename)

            Path(filename).unlink()

            filename = filename_prefix + ".mp3"
            move(temp_filename, filename)

        return AudioFileClip(filename) if return_clip else filename

    def talk_by_sentence(
        self,
        text: str,
        filename_prefix: str | None = None,
        *,
        parallel_factor: int | None = None,
    ) -> list[tuple[str, str | AudioFileClip]]:
        return_clip: bool = filename_prefix is None
        # Must explicitly set filename prefix here
        # Otherwise, `AudioClip` is returned by it cannot be pickled for `multiprocessing`.
        # As a bonus, all the temporary files will also share same filename prefix.
        filename_prefix = filename_prefix or path.join(gettempdir(), str(uuid4())) + "_s"

        args: list[tuple[str, str | None]] = [
            (
                sentence,
                f"{filename_prefix}{i}",
            )
            for i, sentence in enumerate(
                # MoviePy cannot handle audio clip less than one second
                text_to_sentences_with_min_duration(text, 1, buffer=0.2),
                start=1,
            )
        ]

        with multiprocessing.Pool(processes=parallel_factor) as pool:
            return [
                (sentence, AudioFileClip(audio) if return_clip else audio)
                for (sentence, _), audio in zip(
                    args,
                    pool.starmap(self.talk, args),
                    strict=True,
                )
            ]

    def __talk_macos(
        self,
        text: str,
        filename_prefix: str,
    ) -> str:
        run(
            args=[
                "say",
                text,
                # Specify voice if necessary
                *(
                    [
                        "-v",
                        self.__voice,
                    ] if self.__voice
                    else []
                ),
                "--file-format=mp4f",
                "-o",
                filename_prefix + ".mp4",
            ],
            check=True,
        )

        return filename_prefix + ".mp4"

    def __talk_espeak(
        self,
        text: str,
        filename_prefix: str,
    ) -> str:
        run(
            args=[
                "espeak-ng",
                text,
                # Specify voice if necessary
                *(
                    [
                        "-v",
                        self.__voice,
                    ] if self.__voice
                    else []
                ),
                "-w",
                filename_prefix + ".wav",
            ],
            check=True,
        )

        return filename_prefix + ".wav"

    def __talk_polly(
        self,
        text: str,
        filename_prefix: str,
    ) -> str:
        response: dict[str, Any] = self.__polly_client.synthesize_speech(
            OutputFormat="mp3",
            Text=text,
            VoiceId=self.__voice,
        )

        Path(filename_prefix + ".mp3").write_bytes(response["AudioStream"].read())

        return filename_prefix + ".mp3"
