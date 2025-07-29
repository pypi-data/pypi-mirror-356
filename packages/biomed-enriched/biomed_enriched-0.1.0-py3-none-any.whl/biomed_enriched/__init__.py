"""BioMed-Enriched public API."""
from __future__ import annotations

from pathlib import Path
from typing import Optional, TYPE_CHECKING

from ._mapper import _IndexLoader  # noqa: F401 (re-exported for power users)
from ._extractor import _XmlParagraphExtractor  # noqa: F401
from ._enricher import _Enricher

__all__ = [
    "populate",
    "_IndexLoader",
    "_XmlParagraphExtractor",
]

if TYPE_CHECKING:  # pragma: no cover
    import datasets  # type: ignore

def populate(
    dataset_path: str | Path,
    xml_root: str | Path,
    output_path: str | Path | None = None,
    cache: Optional[str] = None,
    *,
    splits: str | list[str] | None = "non-comm",
    index_dataset: str | None = None,
    num_proc: int | None = None,
) -> "datasets.Dataset":
    """Return an enriched dataset with a `text` column added."""

    import datasets  # local import to keep startup time low

    dataset_path = Path(dataset_path)

    try:
        raw = datasets.load_from_disk(str(dataset_path))
    except (FileNotFoundError, ValueError):
        raw = datasets.load_dataset(str(dataset_path))

    # Determine splits to process
    if isinstance(raw, datasets.DatasetDict):
        if splits in (None, "all"):
            split_names = list(raw.keys())
        elif isinstance(splits, str):
            split_names = [splits]
        else:
            split_names = list(splits)

        missing = set(split_names) - set(raw.keys())
        if missing:
            raise ValueError(f"Splits not found in dataset: {missing}")

        enriched_dict = {}
        enricher = _Enricher(xml_root, index_loader=_IndexLoader(index_dataset=index_dataset), num_proc=num_proc)
        for split in split_names:
            enriched_dict[split] = enricher.enrich_dataset(raw[split])

        enriched_ds = datasets.DatasetDict(enriched_dict)
    else:
        # Single split dataset
        enricher = _Enricher(xml_root, index_loader=_IndexLoader(index_dataset=index_dataset), num_proc=num_proc)
        enriched_ds = enricher.enrich_dataset(raw)

    target_dir = Path(output_path or dataset_path)

    if target_dir == dataset_path:
        tmp_dir = dataset_path.with_name(dataset_path.name + "_enrich_tmp")
        if tmp_dir.exists():
            import shutil; shutil.rmtree(tmp_dir)

        enriched_ds.save_to_disk(str(tmp_dir))

        import os, shutil; shutil.rmtree(dataset_path); os.rename(tmp_dir, dataset_path)
    else:
        enriched_ds.save_to_disk(str(target_dir))
    
    return enriched_ds
