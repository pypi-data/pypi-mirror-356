"""Dataset enrichment helpers."""
from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Optional

import datasets
import functools

from ._extractor import _XmlParagraphExtractor
from ._mapper import _IndexLoader

logger = logging.getLogger(__name__)


class _Enricher:
    """Populate missing paragraph text given a dataset and an XML corpus."""

    def __init__(
        self,
        xml_root: str | Path,
        *,
        index_loader: Optional[_IndexLoader] = None,
        num_proc: Optional[int] = None,
    ) -> None:
        self.xml_root = Path(xml_root)
        if not self.xml_root.exists():
            raise FileNotFoundError(self.xml_root)

        self.index_loader = index_loader or _IndexLoader()
        self.num_proc = num_proc or os.cpu_count() or 1

    # Public API
    def enrich_dataset(self, ds: datasets.Dataset) -> datasets.Dataset:  # noqa: D401
        """Return a **new** dataset with a `text` column added."""

        if not {"article_id", "path"}.issubset(ds.column_names):
            missing = {"article_id", "path"} - set(ds.column_names)
            raise ValueError(f"Input dataset missing required columns: {missing}")

        logger.info("Starting enrichment on %s rows (num_proc=%s)…", len(ds), self.num_proc)

        # Map-function executed for each row; must be top-level to be picklable.
        def _process_row(row):  # noqa: D401, WPS430
            pmid = str(row["article_id"])
            rel_xml_path = self.index_loader.get_xml_path(pmid)
            if rel_xml_path is None:
                return {"text": None}

            xml_path = self.xml_root / rel_xml_path
            try:
                extractor = _get_extractor_cached(xml_path)
                text = extractor.extract(row["path"])
                return {"text": text}
            except Exception as exc:  # pragma: no cover  # pylint: disable=broad-except
                logger.debug("Extraction failed for pmid=%s: %s", pmid, exc)
                return {"text": None}

        enriched: datasets.Dataset = ds.map(
            _process_row,
            num_proc=self.num_proc,
            desc="Enriching",
        )

        # Ensure column order
        desired_prefix = ["article_id", "path", "text"]
        ordered_cols = desired_prefix + [c for c in enriched.column_names if c not in desired_prefix]
        enriched = enriched.select_columns(ordered_cols)

        return enriched


# Helpers


@functools.lru_cache(maxsize=128)
def _get_extractor_cached(xml_path: Path) -> _XmlParagraphExtractor:  # noqa: D401
    """Return an extractor cached by *xml_path*."""

    return _XmlParagraphExtractor(xml_path) 