"""Extract text from a PMC XML file."""
from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import List, Tuple

from lxml import etree

logger = logging.getLogger(__name__)

_PATH_TOKEN_RE = re.compile(r"^(?P<tag>\w+)\[(?P<index>\d+)]$")


class _XmlParagraphExtractor:
    """Navigate the XML tree using a simple `tag[index]` path syntax."""

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------
    def __init__(self, xml_path: str | Path):
        self.xml_path = Path(xml_path)
        if not self.xml_path.is_file():  # pragma: no cover
            raise FileNotFoundError(self.xml_path)

        parser = etree.XMLParser(recover=True, huge_tree=True)
        with self.xml_path.open("rb") as fp:
            self._tree = etree.parse(fp, parser)

        self._body = self._tree.find(".//body") or self._tree.getroot()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def extract(self, hf_path: str) -> str | None:  # noqa: D401  # simple method
        """Return paragraph text for a Hugging Face *path* or ``None``.

        The returned string is stripped and whitespace-normalised.
        """
        try:
            segments = self._parse_path(hf_path)
        except ValueError as err:
            logger.warning("Invalid path '%s': %s", hf_path, err)
            return None

        element = self._navigate(self._body, segments)
        if element is None:
            return None

        # Join text nodes with whitespace
        text = " ".join(element.itertext())
        return " ".join(text.split()) if text else None

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------
    @staticmethod
    def _parse_path(path: str) -> List[Tuple[str, int]]:
        """Convert ``sec[0]/p[1]`` into ``[("sec", 0), ("p", 1)]``.

        Raises
        ------
        ValueError
            If the path cannot be parsed.
        """
        if not path:
            raise ValueError("Empty path")

        segments: List[Tuple[str, int]] = []
        for token in path.split("/"):
            m = _PATH_TOKEN_RE.match(token)
            if m is None:
                raise ValueError(f"Malformed token: '{token}'")
            segments.append((m.group("tag"), int(m.group("index"))))
        return segments

    @staticmethod
    def _navigate(root: etree._Element, segments: List[Tuple[str, int]]) -> etree._Element | None:
        current = root
        for tag, idx in segments:
            children = current.findall(tag)
            if idx >= len(children):
                return None
            current = children[idx]
        return current 