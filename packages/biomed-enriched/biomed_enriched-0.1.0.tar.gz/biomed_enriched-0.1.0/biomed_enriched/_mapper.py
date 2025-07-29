"""Load pre-built PMID→XML index."""
from __future__ import annotations

import functools
import logging
from typing import Optional

from datasets import load_dataset

logger = logging.getLogger(__name__)

_DEFAULT_INDEX_DATASET = "rntc/pmid-xml-index"


# noqa: D101  # private class


class _IndexLoader:
    """Load the Parquet index hosted on the Hub or from disk."""

    def __init__(
        self,
        index_dataset: Optional[str] = None,
        *,
        split: str = "train",
        lookup: Optional[dict[str, str]] = None,
    ) -> None:
        """Create a loader.

        If *lookup* is provided, we use it directly — useful for unit tests.
        Otherwise we download *index_dataset* via 🤗 *datasets*.
        """

        if lookup is not None:
            _lookup_dict = {str(k): str(v) for k, v in lookup.items()}
            logger.debug("IndexLoader initialised from in-memory dict (%s entries)", len(_lookup_dict))
        else:
            dataset_id = index_dataset or _DEFAULT_INDEX_DATASET

            logger.info("Loading PMID→XML index from %s (split=%s)…", dataset_id, split)
            try:
                ds = load_dataset(dataset_id, split=split, streaming=False)
            except Exception:  # pragma: no cover  # pylint: disable=broad-except
                logger.exception("Failed to load index dataset '%s'.", dataset_id)
                raise

            # Expect columns pmid (string) and xml_path (string).
            missing_cols = {"pmid", "xml_path"} - set(ds.column_names)
            if missing_cols:
                raise ValueError(
                    f"Index dataset '{dataset_id}' is missing expected columns: {missing_cols}"
                )

            _lookup_dict = {record["pmid"]: record["xml_path"] for record in ds}
            logger.info("Loaded %s PMID mappings into memory.", len(_lookup_dict))

        # Single assignment to satisfy type checkers
        self._lookup: dict[str, str] = _lookup_dict

    # Public helpers
    @functools.lru_cache(maxsize=2**14)  # memoise most-used IDs
    def get_xml_path(self, pmid: str) -> str | None:  # noqa: D401  # simple method
        """Return the XML filepath for *pmid* or ``None`` if absent."""

        return self._lookup.get(str(pmid)) 