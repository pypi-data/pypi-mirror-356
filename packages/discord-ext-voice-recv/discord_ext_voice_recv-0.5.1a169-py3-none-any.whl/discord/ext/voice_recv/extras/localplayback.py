# -*- coding: utf-8 -*-

from __future__ import annotations

import logging

from typing import TYPE_CHECKING


from ..sinks import AudioSink

if TYPE_CHECKING:
    from typing import Optional

    from ..opus import VoiceData
    from ..types import MemberOrUser


__all__ = [
    'LocalPlaybackSink',
]

log = logging.getLogger(__name__)

try:
    import pyaudio
except ImportError:

    def LocalPlaybackSink(**kwargs) -> AudioSink:
        """A stub for when the pyaudio module isn't found."""
        raise RuntimeError('The pyaudio module is required to use this sink.')

else:
    if TYPE_CHECKING:
        pass

    class LocalPlaybackSink(AudioSink):  # type: ignore
        pa: pyaudio.PyAudio = None  # type: ignore

        def __init__(self, *, py_audio: Optional[pyaudio.PyAudio] = None):
            self._init_pa(py_audio)

        @classmethod
        def _init_pa(cls, pa: Optional[pyaudio.PyAudio]):
            if pa is None:
                if cls.pa is None:
                    cls.pa = pyaudio.PyAudio()
            else:
                if cls.pa is None:
                    cls.pa = pa
                elif cls.pa is not pa:
                    ...  # ??? reinit?

        def wants_opus(self) -> bool:
            return False

        def write(self, user: Optional[MemberOrUser], data: VoiceData):
            pass

        def cleanup(self):
            pass
