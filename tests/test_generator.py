
import json

from PIL import Image

from backend.generator.synthetic_generator import generate_dataset


def test_dataset_generation(tmp_path, monkeypatch):
    import backend.generator.synthetic_generator as generator

    monkeypatch.setattr(generator, "IMAGE_DIR", tmp_path / "images")
    monkeypatch.setattr(generator, "DATASET_DIR", tmp_path / "datasets")

    result = generate_dataset(
        number_of_images=5,
        seed=42,
    )

    assert result["number_of_images"] == 5
    assert len(result["images"]) == 5

    dataset_file = tmp_path / "datasets" / "dataset.json"

    assert dataset_file.exists()

    with dataset_file.open(encoding="utf-8") as file:
        saved_data = json.load(file)

    assert len(saved_data["images"]) == 5


def test_generated_images_are_valid(tmp_path, monkeypatch):
    import backend.generator.synthetic_generator as generator

    monkeypatch.setattr(generator, "IMAGE_DIR", tmp_path / "images")
    monkeypatch.setattr(generator, "DATASET_DIR", tmp_path / "datasets")

    result = generate_dataset(
        number_of_images=3,
        seed=42,
    )

    for item in result["images"]:
        image_path = tmp_path / item["image_path"].replace(
            "data/images/",
            "",
        )

        # Image path is checked separately below using the patched directory.
        image_path = tmp_path / "images" / f'{item["image_id"]}.png'

        assert image_path.exists()

        with Image.open(image_path) as image:
            assert image.size == (512, 512)
            assert image.mode == "RGB"


def test_object_metadata_is_valid(tmp_path, monkeypatch):
    import backend.generator.synthetic_generator as generator

    monkeypatch.setattr(generator, "IMAGE_DIR", tmp_path / "images")
    monkeypatch.setattr(generator, "DATASET_DIR", tmp_path / "datasets")

    result = generate_dataset(
        number_of_images=5,
        seed=42,
    )

    for item in result["images"]:
        assert item["total_objects"] == len(item["objects"])

        for obj in item["objects"]:
            assert obj["shape"] in ["circle", "square", "triangle"]
            assert obj["color"] in generator.COLORS

    def test_generated_objects_do_not_overlap(tmp_path, monkeypatch):
        monkeypatch.setattr(generator, "IMAGE_DIR", tmp_path / "images")
        monkeypatch.setattr(generator, "DATASET_DIR", tmp_path / "datasets")

        result = generator.generate_dataset(number_of_images=20, seed=42)

        gap = 10

        for image_data in result["images"]:
            objects = image_data["objects"]

            for i, first in enumerate(objects):
                for second in objects[i + 1:]:
                    x1 = first["position"]["x"]
                    y1 = first["position"]["y"]
                    s1 = first["size"]

                    x2 = second["position"]["x"]
                    y2 = second["position"]["y"]
                    s2 = second["size"]

                    separated = (
                        x1 + s1 + gap <= x2
                        or x2 + s2 + gap <= x1
                        or y1 + s1 + gap <= y2
                        or y2 + s2 + gap <= y1
                    )

                    assert separated, (
                        f"Objects overlap in {image_data['image_id']}"
                    )
   

def test_generated_objects_do_not_overlap(tmp_path, monkeypatch):
    import backend.generator.synthetic_generator as generator

    monkeypatch.setattr(generator, "IMAGE_DIR", tmp_path / "images")
    monkeypatch.setattr(generator, "DATASET_DIR", tmp_path / "datasets")

    result = generator.generate_dataset(number_of_images=20, seed=42)
    gap = 10

    for image_data in result["images"]:
        objects = image_data["objects"]

        for i, first in enumerate(objects):
            for second in objects[i + 1:]:
                x1 = first["position"]["x"]
                y1 = first["position"]["y"]
                s1 = first["size"]

                x2 = second["position"]["x"]
                y2 = second["position"]["y"]
                s2 = second["size"]

                separated = (
                    x1 + s1 + gap <= x2
                    or x2 + s2 + gap <= x1
                    or y1 + s1 + gap <= y2
                    or y2 + s2 + gap <= y1
                )

                assert separated, (
                    f"Objects overlap in {image_data['image_id']}"
                )
