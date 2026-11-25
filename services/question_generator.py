
import json
from pathlib import Path
from collections import Counter


BASE_DIR = Path(__file__).resolve().parents[1]

METADATA_DIR = BASE_DIR / "data" / "metadata"
OUTPUT_DIR = BASE_DIR / "data" / "questions"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_metadata(metadata_path: Path):

    with metadata_path.open("r", encoding="utf-8") as file:
        metadata = json.load(file)

    return metadata


def analyze_objects(metadata):

    objects = metadata["objects"]

    shape_counts = Counter()
    color_counts = Counter()

    for obj in objects:

        shape = obj["shape"]
        color = obj["color"]

        shape_counts[shape] += 1
        color_counts[color] += 1

    return {
        "total_objects": len(objects),
        "shape_counts": dict(shape_counts),
        "color_counts": dict(color_counts)
    }


def generate_questions(statistics):

    questions = []

    questions.append({
        "question": "How many objects are present in the image?",
        "answer": statistics["total_objects"],
        "category": "object_count"
    })

    for shape, count in statistics["shape_counts"].items():

        questions.append({
            "question": f"How many {shape}s are present?",
            "answer": count,
            "category": "shape_count"
        })

    for color, count in statistics["color_counts"].items():

        questions.append({
            "question": f"How many {color} objects are present?",
            "answer": count,
            "category": "color_count"
        })

    return questions


def generate_dataset_questions():

    for metadata_path in sorted(METADATA_DIR.glob("*.json")):

        metadata = load_metadata(metadata_path)

        statistics = analyze_objects(metadata)

        questions = generate_questions(statistics)

        output_path = OUTPUT_DIR / metadata_path.name

        with output_path.open("w", encoding="utf-8") as file:
            json.dump(questions, file, indent=4)

        print(f"Generated questions for {metadata_path.stem}")


if __name__ == "__main__":

    generate_dataset_questions()
