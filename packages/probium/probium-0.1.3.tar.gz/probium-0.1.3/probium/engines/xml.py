from __future__ import annotations
from ..types import Candidate, Result
from .base import EngineBase
from ..registry import register

@register
class XMLEngine(EngineBase):
    name = "xml"
    cost = 0.05
    _MAGIC = [b'\xEF\xBB\xBF', b'\xFF\xFE', b'\xFE\xFF', b"<?xml"]

    def sniff(self, payload: bytes) -> Result:
        window = payload[:64]
        cand = []

        for magic in self._MAGIC:
            idx = window.find(magic)
            if idx != -1:
                conf = 1.0 if idx == 0 else 0.90 - min(idx / (1 << 20), 0.1)
                cand.append(
                    Candidate(
                        media_type="application/xml",
                        extension="xml",
                        confidence=conf,
                    )
                )
                break

        if not cand and window.lstrip().startswith(b"<") and b">" in window:
            cand.append(
                Candidate(
                    media_type="application/xml",
                    extension="xml",
                    confidence=0.6,
                )
            )

        return Result(candidates=cand)
