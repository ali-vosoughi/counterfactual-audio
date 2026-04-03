#!/usr/bin/env python3
"""Build the lightweight metadata bundle consumed by docs/app.js."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "docs" / "data" / "site-data.json"

BIBTEX = """@inproceedings{vosoughi2024counterfactualaudio,
  title={Learning Audio Concepts from Counterfactual Natural Language},
  author={Vosoughi, Ali and Bondi, Luca and Wu, Ho-Hsiang and Xu, Chenliang},
  booktitle={2024 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)},
  year={2024},
  url={https://ieeexplore.ieee.org/document/10446736}
}"""

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

SHOWCASE_VIEWS = [
    {
        "id": "source-event-swaps",
        "label": "Source / event swaps",
        "title": "When the clip stays fixed but the core source changes",
        "description": (
            "These pairs mostly alter a salient source or event while leaving the "
            "caption format natural and compact."
        ),
        "note": (
            "This view is useful for researchers who want text-first hard negatives "
            "that stay close to the original caption style."
        ),
        "items": [
            {
                "dataset_id": "audiocaps",
                "path": "audio/--/--L22BmDI6E.m4a",
                "caption_index": 0,
                "tag": "source swap",
                "focus": "dog whimpering to violin melody",
            },
            {
                "dataset_id": "audiocaps",
                "path": "audio/--/--Z3ciOmwZQ.m4a",
                "caption_index": 0,
                "tag": "event swap",
                "focus": "water bubbling to music playback",
            },
            {
                "dataset_id": "clotho-dev",
                "path": "development/Pipe hit.wav",
                "caption_index": 0,
                "tag": "source swap",
                "focus": "metal strike to natural ambience",
            },
            {
                "dataset_id": "clotho-dev",
                "path": "development/Distorted AM Radio noise.wav",
                "caption_index": 2,
                "tag": "event swap",
                "focus": "radio static to gentle rainfall",
            },
            {
                "dataset_id": "macs",
                "path": "development/audio/airport-barcelona-0-0-a.wav",
                "caption_index": 0,
                "tag": "source swap",
                "focus": "whistling and singing to violin and clock",
            },
            {
                "dataset_id": "macs",
                "path": "development/audio/public_square-london-115-3352-a.wav",
                "caption_index": 1,
                "tag": "hard negative",
                "focus": "public-space chatter to dog bark and loud music",
            },
        ],
    },
    {
        "id": "scene-level-rewrites",
        "label": "Scene-level rewrites",
        "title": "When the counterfactual changes the whole scene",
        "description": (
            "These examples shift multiple sound sources at once, turning the same "
            "audio path into a linguistically different scene."
        ),
        "note": (
            "This view highlights why counterfactual language is stronger than a "
            "generic random mismatch: the alternatives are still fluent scene descriptions."
        ),
        "items": [
            {
                "dataset_id": "audiocaps",
                "path": "audio/--/---lTs1dxhU.m4a",
                "caption_index": 0,
                "tag": "scene rewrite",
                "focus": "vehicle pass-by to children in a park",
            },
            {
                "dataset_id": "audiocaps",
                "path": "audio/--/--299m5_DdE.m4a",
                "caption_index": 0,
                "tag": "scene rewrite",
                "focus": "water and child to wind and distant guitar",
            },
            {
                "dataset_id": "clotho-dev",
                "path": "development/outdoors2.wav",
                "caption_index": 0,
                "tag": "scene rewrite",
                "focus": "door, leaves, and speech to bells, birds, and whistle",
            },
            {
                "dataset_id": "clotho-dev",
                "path": "development/loud_japanese_diner_full_of_drunk_people_120-90surround.wav",
                "caption_index": 0,
                "tag": "scene rewrite",
                "focus": "restaurant crowd to emergency-report scene",
            },
            {
                "dataset_id": "macs",
                "path": "development/audio/public_square-prague-1192-45104-a.wav",
                "caption_index": 0,
                "tag": "scene rewrite",
                "focus": "urban crowd to storm scene",
            },
            {
                "dataset_id": "macs",
                "path": "development/audio/public_square-london-115-3352-a.wav",
                "caption_index": 2,
                "tag": "scene rewrite",
                "focus": "public square to traffic and construction",
            },
        ],
    },
    {
        "id": "dataset-specific",
        "label": "Dataset-specific examples",
        "title": "Representative pairs from AudioCaps, Clotho, and MACS",
        "description": (
            "This view shows how the release differs by source dataset, from "
            "single-caption AudioCaps clips to multi-caption Clotho and multi-annotator MACS."
        ),
        "note": (
            "The current Clotho validation release is excluded here because its "
            "counterfactual field mirrors the factual captions."
        ),
        "items": [
            {
                "dataset_id": "audiocaps",
                "path": "audio/--/---1_cCGK4M.m4a",
                "caption_index": 0,
                "tag": "AudioCaps",
                "focus": "single-caption pair",
            },
            {
                "dataset_id": "audiocaps",
                "path": "audio/--/--RBwc_VFYA.m4a",
                "caption_index": 0,
                "tag": "AudioCaps",
                "focus": "single-caption pair with natural ambience shift",
            },
            {
                "dataset_id": "clotho-dev",
                "path": "development/Distorted AM Radio noise.wav",
                "caption_index": 0,
                "tag": "Clotho",
                "focus": "one of five aligned caption pairs",
            },
            {
                "dataset_id": "clotho-dev",
                "path": "development/loud_japanese_diner_full_of_drunk_people_120-90surround.wav",
                "caption_index": 2,
                "tag": "Clotho",
                "focus": "multi-caption contrast on the same clip",
            },
            {
                "dataset_id": "macs",
                "path": "development/audio/airport-barcelona-0-0-a.wav",
                "caption_index": 1,
                "tag": "MACS",
                "focus": "multi-annotator caption pair",
            },
            {
                "dataset_id": "macs",
                "path": "development/audio/park-prague-1185-44120-a.wav",
                "caption_index": 1,
                "tag": "MACS",
                "focus": "same scene, different textual alternative",
            },
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


def build_dataset_entry(release: dict, rows: list[dict]) -> dict:
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


def build_showcases(
    loaded_rows: dict[str, list[dict]], dataset_names: dict[str, str]
) -> list[dict]:
    rows_by_dataset = {
        dataset_id: {row["path"]: row for row in rows}
        for dataset_id, rows in loaded_rows.items()
    }

    showcases = []

    for view in SHOWCASE_VIEWS:
        examples = []

        for item in view["items"]:
            row = rows_by_dataset[item["dataset_id"]][item["path"]]
            factual = row["captions"][item["caption_index"]]
            counterfactual = row["captions_counterfactual"][item["caption_index"]]

            if factual == counterfactual:
                raise ValueError(
                    f"Showcase item {item['path']} index={item['caption_index']} "
                    "is not counterfactual."
                )

            examples.append(
                {
                    "dataset": dataset_names[item["dataset_id"]],
                    "path": item["path"],
                    "tag": item["tag"],
                    "focus": item["focus"],
                    "factual": factual,
                    "counterfactual": counterfactual,
                }
            )

        showcases.append(
            {
                "id": view["id"],
                "label": view["label"],
                "title": view["title"],
                "description": view["description"],
                "note": view["note"],
                "examples": examples,
            }
        )

    return showcases


def main() -> None:
    prompts = load_json(ROOT / "prompts_1.json")
    loaded_rows = {
        release["id"]: load_json(ROOT / release["release_file"]) for release in RELEASES
    }
    datasets = [
        build_dataset_entry(release, loaded_rows[release["id"]]) for release in RELEASES
    ]
    dataset_names = {dataset["id"]: dataset["name"] for dataset in datasets}
    showcases = build_showcases(loaded_rows, dataset_names)

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
            "authors": [
                "Ali Vosoughi",
                "Luca Bondi",
                "Ho-Hsiang Wu",
                "Chenliang Xu",
            ],
            "acceptance_note": "Accepted at IEEE ICASSP 2024",
            "novelty_statement": (
                "This release adds counterfactual language for the same audio clip, "
                "not just factual caption matching."
            ),
            "bibtex": BIBTEX,
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
        "showcases": showcases,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")


if __name__ == "__main__":
    main()
