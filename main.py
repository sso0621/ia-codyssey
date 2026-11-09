import json
import os
import sys

# 기본 퀴즈 데이터 (상식/IT 주제 5개)
DEFAULT_QUIZZES = [
    {
        "question": "파이썬(Python) 언어를 최초로 개발한 사람은 누구일까요?",
        "choices": ["귀도 반 로섬", "리누스 토발즈", "제임스 고슬링", "비야네 스트롭스트룹"],
        "answer": 1
    },
    {
        "question": "다음 중 파이썬의 불변(Immutable) 순서형 자료형은 무엇일까요?",
        "choices": ["List", "Dictionary", "Tuple", "Set"],
        "answer": 3
    },
    {
        "question": "파이썬에서 객체의 메모리 주소 또는 고유 식별값을 반환하는 함수는?",
        "choices": ["type()", "id()", "len()", "isinstance()"],
        "answer": 2
    },
    {
        "question": "HTTP 상태 코드 중 '404'가 의미하는 것은 무엇일까요?",
        "choices": ["OK (성공)", "Unauthorized (인증 필요)", "Internal Server Error", "Not Found (찾을 수 없음)"],
        "answer": 4
    },
    {
        "question": "Git에서 원격 저장소의 변경사항을 로컬로 가져와 병합하는 명령어는?",
        "choices": ["git fetch", "git pull", "git push", "git commit"],
        "answer": 2
    }
]


class Quiz:
    """개별 퀴즈 항목을 관리하는 클래스"""
    def __init__(self, question: str, choices: list[str], answer: int):
        self.question = question
        self.choices = choices
        self.answer = answer

    def is_correct(self, user_answer: int) -> bool:
        return self.answer == user_answer

    def display(self, index: int):
        print(f"\n[문제 {index}] {self.question}")
        for idx, choice in enumerate(self.choices, 1):
            print(f"  {idx}. {choice}")

    def to_dict(self) -> dict:
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data["question"], data["choices"], data["answer"])