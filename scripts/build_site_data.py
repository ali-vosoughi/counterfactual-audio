#!/usr/bin/env python3
"""Build the lightweight metadata bundle consumed by docs/app.js."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "docs" / "data" / "site-data.json"

RELEASES = [
    {
        "id": "audiocaps",
        "name": "AudioCaps",
        "split_label": "train release",
        "release_file": "audiocaps-train-counterfactual.json",
        "source_url": "https://github.com/cdjkim/audiocaps",
        "download_url": "https://audiocaps.github.io/",
        "path_pattern": "audio/<prefix>/<clip>.m4a",
        "notes": "One factual caption and one counterfactual caption per clip.",
        "example_paths": [
            "audio/--/---1_cCGK4M.m4a",
            "audio/--/---lTs1dxhU.m4a",
            "audio/--/--0PQM4-hqg.m4a",
            "audio/--/--299m5_DdE.m4a",
        ],
    },
    {
        "id": "clotho-dev",
        "name": "Clotho",
        "split_label": "development release",
        "release_file": "clotho-development-counterfactual.json",
        "source_url": "https://zenodo.org/records/3490684",
        "download_url": "https://github.com/audio-captioning/clotho-dataset",
        "path_pattern": "development/<file>.wav",
        "notes": "Five factual captions and five aligned counterfactual captions per clip.",
        "example_paths": [
            "development/Distorted AM Radio noise.wav",
            "development/Pipe hit.wav",
            "development/outdoors2.wav",
            "development/loud_japanese_diner_full_of_drunk_people_120-90surround.wav",
        ],
    },
    {
        "id": "clotho-val",
        "name": "Clotho",
        "split_label": "validation release",
        "release_file": "clotho-validation-counterfactual.json",
        "source_url": "https://zenodo.org/records/3490684",
        "download_url": "https://github.com/audio-captioning/clotho-dataset",
        "path_pattern": "validation/<file>.wav",
        "notes": (
            "In the current release, captions_counterfactual matches captions "
            "for every paired entry."
        ),
        "example_paths": [],
    },
    {
        "id": "macs",
        "name": "MACS",
        "split_label": "release",
        "release_file": "macs-counterfactual.json",
        "source_url": "https://zenodo.org/records/5114771",
        "download_url": "https://zenodo.org/record/2589280",
        "path_pattern": "development/audio/<file>.wav",
        "notes": "Multi-annotator captions paired with aligned counterfactual rewrites.",
        "example_paths": [
            "development/audio/airport-barcelona-0-0-a.wav",
            "development/audio/public_square-london-115-3352-a.wav",
            "development/audio/park-prague-1185-44120-a.wav",
            "development/audio/public_square-prague-1192-45104-a.wav",
        ],
    },
]


def load_json(path: Path):
    with path.open() as handle:
        return json.load(handle)


def captions_per_clip_summary(lengths: list[int]) -> str:
    values = sorted(set(lengths))
    if not values:
        return "0"
    if len(values) == 1:
        return str(values[0])
    return f"{values[0]}-{values[-1]}"


def round_or_none(value: float | None) -> float | None:
    if value is None:
        return None
    return round(value, 3)


def pick_examples(rows: list[dict], wanted_paths: list[str]) -> list[dict]:
    rows_by_path = {row["path"]: row for row in rows}
    picked = []

    for wanted_path in wanted_paths:
        row = rows_by_path[wanted_path]
        for factual, counterfactual in zip(
            row["captions"], row["captions_counterfactual"]
        ):
            if factual != counterfactual:
                picked.append(
                    {
                        "path": row["path"],
                        "factual": factual,
                        "counterfactual": counterfactual,
                    }
                )
                break

    return picked


def build_dataset_entry(release: dict) -> dict:
    rows = load_json(ROOT / release["release_file"])
    caption_lengths = [len(row.get("captions", [])) for row in rows]
    durations = [
        row["duration"]
        for row in rows
        if isinstance(row.get("duration"), (float, int))
    ]
    paired_caption_instances = sum(caption_lengths)
    identical_pairs = sum(
        1
        for row in rows
        for factual, counterfactual in zip(
            row.get("captions", []), row.get("captions_counterfactual", [])
        )
        if factual == counterfactual
    )

    return {
        "id": release["id"],
        "name": release["name"],
        "split_label": release["split_label"],
        "release_file": release["release_file"],
        "release_url": (
            "https://github.com/ali-vosoughi/counterfactual-audio/blob/main/"
            f"{release['release_file']}"
        ),
        "source_url": release["source_url"],
        "download_url": release["download_url"],
        "path_pattern": release["path_pattern"],
        "notes": release["notes"],
        "records": len(rows),
        "paired_caption_instances": paired_caption_instances,
        "captions_per_clip": captions_per_clip_summary(caption_lengths),
        "identical_pairs": identical_pairs,
        "duration_mean": round_or_none(sum(durations) / len(durations) if durations else None),
        "duration_min": round_or_none(min(durations) if durations else None),
        "duration_max": round_or_none(max(durations) if durations else None),
        "examples": pick_examples(rows, release["example_paths"]),
    }


def main() -> None:
    prompts = load_json(ROOT / "prompts_1.json")
    datasets = [build_dataset_entry(release) for release in RELEASES]

    payload = {
        "project": {
            "title": "Counterfactual Audio",
            "paper_title": "Learning Audio Concepts from Counterfactual Natural Language",
            "summary": (
                "Counterfactual caption release for AudioCaps, Clotho, and MACS, "
                "prepared for the ICASSP 2024 paper on audio-language learning "
                "with alternative linguistic scenarios."
            ),
            "repo_url": "https://github.com/ali-vosoughi/counterfactual-audio",
            "website_url": "https://ali-vosoughi.github.io/counterfactual-audio/",
            "arxiv_url": "https://arxiv.org/abs/2401.04935",
            "ieee_url": "https://ieeexplore.ieee.org/document/10446736",
            "venue": "ICASSP 2024",
            "retrieval_gain": "43%+ top-1 improvement on Clotho text-to-audio retrieval",
            "totals": {
                "records": sum(dataset["records"] for dataset in datasets),
                "paired_caption_instances": sum(
                    dataset["paired_caption_instances"] for dataset in datasets
                ),
            },
        },
        "prompts": prompts,
        "datasets": datasets,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")


if __name__ == "__main__":
    main()
