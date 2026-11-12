import json
import os
import sys

# 기본 퀴즈 데이터 (대중적인 속담 및 사자성어 5개)
DEFAULT_QUIZZES = [
    {
        "question": "다음 중 '아무리 쉬운 일이라도 혼자 하는 것보다 협동하는 것이 낫다'는 의미의 속담은?",
        "choices": ["백지장도 맞들면 낫다", "티끌 모아 태산", "돌다리도 두들겨 보고 건너라", "가는 말이 고와야 오는 말이 곱다"],
        "answer": 1
    },
    {
        "question": "사자성어 '동문서답(東問西答)'의 뜻으로 올바른 것은 무엇일까요?",
        "choices": ["동쪽과 서쪽을 오가며 바쁘게 일함", "묻는 말에 아주 딴판인 전혀 다른 대답을 함", "서로 사이가 좋지 않아 항상 다툼", "동쪽과 서쪽의 문화를 모두 통달함"],
        "answer": 2
    },
    {
        "question": "다음 속담의 빈칸에 들어갈 말은? '낮말은 새가 듣고, (  )말은 쥐가 듣는다.'",
        "choices": ["밤", "속", "혼자", "큰"],
        "answer": 1
    },
    {
        "question": "사자성어 '일석이조(一石二鳥)'와 가장 의미가 비슷한 속담은 무엇일까요?",
        "choices": ["등 잔 밑이 어둡다", "꿩 먹고 알 먹는다", "우물 안 개구리", "쇠뿔도 단김에 빼라"],
        "answer": 2
    },
    {
        "question": "다음 속담의 빈칸에 들어갈 동물은? '(  )도 약에 쓰려면 없다.'",
        "choices": ["호랑이", "개구리", "개똥", "고양이"],
        "answer": 3
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


class QuizGame:
    """퀴즈 게임 전체 진행 및 데이터 영속성을 관리하는 클래스"""
    FILE_PATH = "state.json"

    def __init__(self):
        self.quizzes: list[Quiz] = []
        self.best_score: int = 0
        self.load_data()

    def get_valid_integer(self, prompt: str, min_val: int, max_val: int) -> int:
        """공통 예외 처리 메서드 (공백 제거, 숫자 변환, 범위 체크, Ctrl+C 방어)"""
        while True:
            try:
                raw_input = input(prompt).strip()
                if not raw_input:
                    print("⚠️ 빈 입력입니다. 다시 입력해 주세요.")
                    continue

                value = int(raw_input)
                if value < min_val or value > max_val:
                    print(f"⚠️ {min_val}~{max_val} 범위의 숫자를 입력해 주세요.")
                    continue

                return value
            except ValueError:
                print("⚠️ 올바른 숫자를 입력해 주세요.")
            except (KeyboardInterrupt, EOFError):
                print("\n\n⚠️ 입력이 중단되었습니다. 안전하게 저장 후 종료합니다.")
                self.save_data()
                sys.exit(0)

    def load_data(self):
        """state.json 데이터 로드 및 손상 시 안전 복구"""
        if not os.path.exists(self.FILE_PATH):
            print("📂 기존 데이터 파일이 없습니다. 기본 데이터를 생성합니다.")
            self._use_default_data()
            self.save_data()
            return

        try:
            with open(self.FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.quizzes = [Quiz.from_dict(q) for q in data.get("quizzes", [])]
                self.best_score = data.get("best_score", 0)

                if not self.quizzes:
                    self._use_default_data()
            print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {self.best_score}점)")
        except (json.JSONDecodeError, KeyError, Exception) as e:
            print(f"⚠️ 데이터 파일 손상 또는 읽기 오류가 발생했습니다: {e}")
            print("🔄 기본 데이터로 초기화합니다.")
            self._use_default_data()
            self.save_data()

    def _use_default_data(self):
        self.quizzes = [Quiz.from_dict(q) for q in DEFAULT_QUIZZES]
        self.best_score = 0

    def save_data(self):
        """현재 상태를 state.json에 UTF-8로 저장"""
        data = {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "best_score": self.best_score
        }
        try:
            with open(self.FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"⚠️ 저장 중 오류가 발생했습니다: {e}")

    def play_game(self):
        """퀴즈 풀기 기능"""
        if not self.quizzes:
            print("\n⚠️ 등록된 퀴즈가 없습니다.")
            return

        print(f"\n📝 퀴즈를 시작합니다! (총 {len(self.quizzes)}문제)")
        score = 0

        for idx, quiz in enumerate(self.quizzes, 1):
            quiz.display(idx)
            user_ans = self.get_valid_integer("👉 정답 입력 (1-4): ", 1, 4)

            if quiz.is_correct(user_ans):
                print("✅ 정답입니다!")
                score += 1
            else:
                print(f"❌ 오답입니다. (정답: {quiz.answer}번)")

        print("\n" + "=" * 40)
        print(f"🏆 결과: {len(self.quizzes)}문제 중 {score}문제 정답!")
        
        if score > self.best_score:
            print(f"🎉 축하합니다! 새로운 최고 점수 달성! ({self.best_score}점 -> {score}점)")
            self.best_score = score
            self.save_data()
        else:
            print(f"현재 최고 점수: {self.best_score}점")
        print("=" * 40)

    def add_quiz(self):
        """퀴즈 추가 기능"""
        print("\n📌 새로운 퀴즈를 추가합니다.")
        try:
            question = ""
            while not question:
                question = input("문제를 입력하세요: ").strip()
                if not question:
                    print("⚠️ 문제 내용은 비워둘 수 없습니다.")

            choices = []
            for i in range(1, 5):
                choice = ""
                while not choice:
                    choice = input(f"선택지 {i}: ").strip()
                    if not choice:
                        print("⚠️ 선택지 내용은 비워둘 수 없습니다.")
                choices.append(choice)

            answer = self.get_valid_integer("정답 번호 (1-4): ", 1, 4)

            new_quiz = Quiz(question, choices, answer)
            self.quizzes.append(new_quiz)
            self.save_data()
            print("✅ 퀴즈가 성공적으로 추가 및 저장되었습니다!")
        except (KeyboardInterrupt, EOFError):
            print("\n⚠️ 퀴즈 추가가 취소되었습니다.")

    def show_quiz_list(self):
        """퀴즈 목록 조회"""
        if not self.quizzes:
            print("\n⚠️ 등록된 퀴즈가 없습니다.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("-" * 40)
        for idx, quiz in enumerate(self.quizzes, 1):
            print(f"[{idx}] {quiz.question}")
        print("-" * 40)

    def show_score(self):
        """최고 점수 확인"""
        print("\n" + "=" * 40)
        print(f"🏆 현재 최고 점수: {self.best_score}점")
        print("=" * 40)

    def run(self):
        """메인 메뉴 실행 루프"""
        while True:
            print("\n" + "=" * 40)
            print("        🎯 나만의 퀴즈 게임 🎯")
            print("=" * 40)
            print(" 1. 퀴즈 풀기")
            print(" 2. 퀴즈 추가")
            print(" 3. 퀴즈 목록")
            print(" 4. 점수 확인")
            print(" 5. 종료")
            print("=" * 40)

            choice = self.get_valid_integer("선택: ", 1, 5)

            if choice == 1:
                self.play_game()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.show_quiz_list()
            elif choice == 4:
                self.show_score()
            elif choice == 5:
                print("\n게임 프로그램을 종료합니다. 감사합니다!")
                self.save_data()
                break


if __name__ == "__main__":
    try:
        game = QuizGame()
        game.run()
    except (KeyboardInterrupt, EOFError):
        print("\n\n⚠️ 프로그램이 안전하게 종료되었습니다.")