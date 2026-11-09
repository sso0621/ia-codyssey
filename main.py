class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question  # 문제 내용
        self.choices = choices    # 선택지 리스트 (4개)
        self.answer = answer      # 정답 번호 (1~4)

    def display(self):
        """퀴즈 문제와 선택지를 출력하는 메서드"""
        print(f"\n[문제] {self.question}")
        for idx, choice in enumerate(self.choices, 1):
            print(f"  {idx}. {choice}")

    def check_answer(self, user_answer):
        """사용자가 입력한 정답이 맞는지 확인"""
        return user_answer == self.answer

    def to_dict(self):
        """JSON 저장을 위해 딕셔너리 형태로 변환"""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }