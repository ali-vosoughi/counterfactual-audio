#!/usr/bin/env python3
"""Resolve released counterfactual annotations to local audio paths.

This helper flattens one release JSON file into JSON Lines. Each output record
contains the resolved audio path, the factual caption, and the corresponding
counterfactual caption.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Iterable


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--release",
        type=Path,
        required=True,
        help="Path to one of the released JSON files in this repository.",
    )
    parser.add_argument(
        "--dataset-root",
        type=Path,
        required=True,
        help="Root directory that contains the original dataset audio tree.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional maximum number of flattened caption pairs to emit.",
    )
    parser.add_argument(
        "--check-files",
        action="store_true",
        help="Add an 'audio_exists' field after checking the resolved path.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional output JSONL path. Defaults to stdout.",
    )
    return parser.parse_args()


def load_rows(path: Path) -> list[dict]:
    with path.open() as handle:
        data = json.load(handle)

    if not isinstance(data, list):
        raise ValueError(f"{path} does not contain a top-level JSON list.")

    return data


def iter_flattened_rows(
    rows: list[dict],
    dataset_root: Path,
    check_files: bool,
) -> Iterable[dict]:
    for row in rows:
        factual_captions = row.get("captions", [])
        counterfactual_captions = row.get("captions_counterfactual", [])

        if len(factual_captions) != len(counterfactual_captions):
            raise ValueError(
                f"Caption length mismatch for path={row.get('path')!r}: "
                f"{len(factual_captions)} factual vs "
                f"{len(counterfactual_captions)} counterfactual"
            )

        audio_path = (dataset_root / row["path"]).resolve()
        base_fields = {
            key: value
            for key, value in row.items()
            if key not in {"captions", "captions_counterfactual"}
        }
        base_fields["audio_path"] = str(audio_path)

        if check_files:
            base_fields["audio_exists"] = audio_path.exists()

        for caption_index, (caption, counterfactual_caption) in enumerate(
            zip(factual_captions, counterfactual_captions)
        ):
            yield {
                **base_fields,
                "caption_index": caption_index,
                "caption": caption,
                "counterfactual_caption": counterfactual_caption,
            }


def write_jsonl(records: Iterable[dict], output: Path | None, limit: int | None) -> None:
    handle = output.open("w") if output else sys.stdout
    should_close = output is not None

    try:
        for index, record in enumerate(records):
            if limit is not None and index >= limit:
                break
            handle.write(json.dumps(record, ensure_ascii=True) + "\n")
    finally:
        if should_close:
            handle.close()


def main() -> None:
    args = parse_args()
    rows = load_rows(args.release)
    records = iter_flattened_rows(rows, args.dataset_root, args.check_files)
    write_jsonl(records, args.output, args.limit)


if __name__ == "__main__":
    main()
