from dataclasses import dataclass
from datastructures import LinkedStack
from datastructures import Array


@dataclass
class Answers:
    default: int
    choices: dict = None
    min: int = None
    max: int = None


@dataclass
class Question:
    category: str
    question: str
    answers: Answers


@dataclass
class Symptom:
    symptom_name: str
    question: Question


@dataclass
class Disease:
    disease_name: str
    possible_symptoms: LinkedStack()


class Patient:
    def __init__(self):
        self.basic_data = Array(10, None)
        self.symptoms_data = LinkedStack()
