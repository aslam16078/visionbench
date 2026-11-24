
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

DATASET_PATH = BASE_DIR / "data" / "datasets" / "dataset.json"
OUTPUT_PATH = BASE_DIR / "data" / "datasets" / "questions.json"


def generate_questions(image_data):
    objects = image_data["objects"]
    questions = []

    # Question 1: Total object count
    questions.append({
        "question": "How many objects are in the image?",
        "answer": len(objects),
        "question_type": "object_count",
    })

    # Question 2: Count objects by color
    colors = {obj["color"] for obj in objects}

    for color in sorted(colors):
        count = sum(
            1 for obj in objects
            if obj["color"] == color
        )

        questions.append({
            "question": f"How many {color} objects are present?",
            "answer": count,
            "question_type": "color_count",
        })

    # Question 3: Count objects by shape
    shapes = {obj["shape"] for obj in objects}

    for shape in sorted(shapes):
        count = sum(
            1 for obj in objects
            if obj["shape"] == shape
        )

        questions.append({
            "question": f"How many {shape} objects are present?",
            "answer": count,
            "question_type": "shape_count",
        })

    # Question 4: List available colors
    questions.append({
        "question": "Which colors are present in the image?",
        "answer": sorted(colors),
        "question_type": "color_list",
    })

    return questions


def generate_question_dataset():
    with DATASET_PATH.open("r", encoding="utf-8") as file:
        dataset = json.load(file)

    question_dataset = {
        "dataset_name": "VisionBench Visual Questions",
        "total_images": len(dataset["images"]),
        "images": [],
    }

    for image_data in dataset["images"]:
        question_data = {
            "image_id": image_data["image_id"],
            "image_path": image_data["image_path"],
            "questions": generate_questions(image_data),
        }

        question_dataset["images"].append(question_data)

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        json.dump(question_dataset, file, indent=4)

    return question_dataset


if __name__ == "__main__":
    result = generate_question_dataset()

    total_questions = sum(
        len(item["questions"])
        for item in result["images"]
    )

    print("Question dataset generated successfully!")
    print("Total images:", result["total_images"])
    print("Total questions:", total_questions)
    print("Saved to:", OUTPUT_PATH)
