
import random
import json
from pathlib import Path
from PIL import Image, ImageDraw


BASE_DIR = Path(__file__).resolve().parents[1]

IMAGE_DIR = BASE_DIR / "data" / "generated_images"
METADATA_DIR = BASE_DIR / "data" / "metadata"

IMAGE_DIR.mkdir(parents=True, exist_ok=True)
METADATA_DIR.mkdir(parents=True, exist_ok=True)


def generate_dataset_image(sample_id: int, shape_count: int = 6):

    width = 640
    height = 480

    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    shapes = ["circle", "rectangle", "triangle"]

    objects = []

    for index in range(shape_count):

        shape = random.choice(shapes)

        x1 = random.randint(30, 450)
        y1 = random.randint(30, 300)
        size = random.randint(40, 100)

        x2 = x1 + size
        y2 = y1 + size

        color = random.choice([
            "red", "blue", "green", "orange"
        ])

        if shape == "circle":
            draw.ellipse((x1, y1, x2, y2), fill=color)

        elif shape == "rectangle":
            draw.rectangle((x1, y1, x2, y2), fill=color)

        elif shape == "triangle":
            draw.polygon(
                [(x1, y2), (x1 + size // 2, y1), (x2, y2)],
                fill=color
            )

        objects.append({
            "id": index + 1,
            "shape": shape,
            "color": color,
            "position": {
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2
            }
        })

    image_path = IMAGE_DIR / f"sample_{sample_id:03}.png"
    metadata_path = METADATA_DIR / f"sample_{sample_id:03}.json"

    image.save(image_path)

    metadata = {
        "sample_id": sample_id,
        "image": str(image_path.relative_to(BASE_DIR)),
        "width": width,
        "height": height,
        "total_objects": len(objects),
        "objects": objects
    }

    with metadata_path.open("w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=4)

    return metadata


if __name__ == "__main__":

    for sample_id in range(1, 11):

        result = generate_dataset_image(
            sample_id=sample_id,
            shape_count=random.randint(4, 10)
        )

        print(f"Generated sample {sample_id}")
