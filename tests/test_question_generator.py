
from backend.generator.question_generator import generate_questions


def test_total_object_count():
    image_data = {
        "objects": [
            {"shape": "circle", "color": "red"},
            {"shape": "square", "color": "blue"},
            {"shape": "triangle", "color": "red"},
        ]
    }

    questions = generate_questions(image_data)

    count_question = next(
        q for q in questions
        if q["question_type"] == "object_count"
    )

    assert count_question["answer"] == 3


def test_color_count():
    image_data = {
        "objects": [
            {"shape": "circle", "color": "red"},
            {"shape": "square", "color": "blue"},
            {"shape": "triangle", "color": "red"},
        ]
    }

    questions = generate_questions(image_data)

    red_question = next(
        q for q in questions
        if q["question"] == "How many red objects are present?"
    )

    assert red_question["answer"] == 2


def test_shape_count():
    image_data = {
        "objects": [
            {"shape": "circle", "color": "red"},
            {"shape": "circle", "color": "blue"},
            {"shape": "square", "color": "green"},
        ]
    }

    questions = generate_questions(image_data)

    circle_question = next(
        q for q in questions
        if q["question"] == "How many circle objects are present?"
    )

    assert circle_question["answer"] == 2


def test_color_list():
    image_data = {
        "objects": [
            {"shape": "circle", "color": "red"},
            {"shape": "square", "color": "blue"},
            {"shape": "triangle", "color": "red"},
        ]
    }

    questions = generate_questions(image_data)

    color_question = next(
        q for q in questions
        if q["question_type"] == "color_list"
    )

    assert color_question["answer"] == ["blue", "red"]
