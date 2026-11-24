
import json
import random
from pathlib import Path

from PIL import Image, ImageDraw

# Project directories
BASE_DIR = Path(__file__).resolve().parents[2]

IMAGE_DIR = BASE_DIR / "data" / "images"
DATASET_DIR = BASE_DIR / "data" / "datasets"

# Image configuration
IMAGE_SIZE = 512

COLORS = {
    "red": (255, 0, 0),
    "blue": (0, 0, 255),
    "green": (0, 180, 0),
    "yellow": (255, 220, 0),
    "purple": (150, 0, 200),
    "orange": (255, 140, 0),
}

SHAPES = ["circle", "square", "triangle"]



def generate_object(draw, rng, existing_objects, max_attempts=100):
    shape = rng.choice(SHAPES)
    color_name = rng.choice(list(COLORS.keys()))
    color = COLORS[color_name]

    size = rng.randint(50, 100)
    gap = 10

    for _ in range(max_attempts):
        x = rng.randint(10, IMAGE_SIZE - size - 10)
        y = rng.randint(10, IMAGE_SIZE - size - 10)

        candidate = (x, y, x + size, y + size)

        overlaps = any(
            not (
                candidate[2] + gap <= obj["position"]["x"]
                or obj["position"]["x"] + obj["size"] + gap <= candidate[0]
                or candidate[3] + gap <= obj["position"]["y"]
                or obj["position"]["y"] + obj["size"] + gap <= candidate[1]
            )
            for obj in existing_objects
        )

        if not overlaps:
            break
    else:
        return None

    if shape == "circle":
        draw.ellipse(
            candidate,
            fill=color,
            outline="black",
            width=2,
        )

    elif shape == "square":
        draw.rectangle(
            candidate,
            fill=color,
            outline="black",
            width=2,
        )

    elif shape == "triangle":
        points = [
            (x + size // 2, y),
            (x + size, y + size),
            (x, y + size),
        ]
        draw.polygon(points, fill=color, outline="black")

    return {
        "shape": shape,
        "color": color_name,
        "position": {"x": x, "y": y},
        "size": size,
    }



def generate_image(image_id, object_count, rng):
    image = Image.new(
        "RGB",
        (IMAGE_SIZE, IMAGE_SIZE),
        "white",
    )

    draw = ImageDraw.Draw(image)

    objects = []

    for _ in range(object_count):
        obj = generate_object(draw, rng, objects)
        if obj is not None:
            objects.append(obj)

    image_path = IMAGE_DIR / f"{image_id}.png"

    image.save(image_path)

    return {
        "image_id": image_id,
        "image_path": (
    str(image_path.relative_to(BASE_DIR))
    if image_path.is_relative_to(BASE_DIR)
    else str(image_path)
),
        "image_size": IMAGE_SIZE,
        "objects": objects,
        "total_objects": len(objects),
    }


def generate_dataset(number_of_images=10, seed=42):
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    DATASET_DIR.mkdir(parents=True, exist_ok=True)

    rng = random.Random(seed)

    dataset = {
        "dataset_name": "VisionBench Synthetic Dataset",
        "seed": seed,
        "number_of_images": number_of_images,
        "images": [],
    }

    for index in range(1, number_of_images + 1):
        image_id = f"scene_{index:04d}"

        object_count = rng.randint(2, 6)

        metadata = generate_image(
            image_id,
            object_count,
            rng,
        )

        dataset["images"].append(metadata)

    dataset_path = DATASET_DIR / "dataset.json"

    with dataset_path.open("w", encoding="utf-8") as file:
        json.dump(dataset, file, indent=4)

    return dataset


if __name__ == "__main__":
    result = generate_dataset(
        number_of_images=10,
        seed=42,
    )

    print("Dataset generated successfully!")
    print("Total images:", result["number_of_images"])
    print("Dataset location:", DATASET_DIR / "dataset.json")
