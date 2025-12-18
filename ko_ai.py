import json
import os
import random

FILE = "ko.json"

if os.path.exists(FILE):
    with open(FILE, "r", encoding="utf-8") as f:
        brain = json.load(f)
else:
    brain = {}

mode = "일반"
messages = 0
trainings = 0

def save():
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(brain, f, ensure_ascii=False, indent=2)

def clean(text):
    return text.lower().strip()

def find_answer(phrase):
    words = phrase.split()
    counter = {}
    for word in words:
        if word in brain:
            for answer, weight in brain[word].items():
                counter[answer] = counter.get(answer, 0) + weight
    if not counter:
        return None
    best = max(counter.values())
    candidates = [a for a, w in counter.items() if w == best]
    return random.choice(candidates)

def train(phrase, answer):
    global trainings
    for word in phrase.split():
        if word not in brain:
            brain[word] = {}
        brain[word][answer] = brain[word].get(answer, 0) + 1
    trainings += 1
    save()

def commands(text):
    global mode
    if text == "/help":
        print("📌 명령어:")
        print("/help — 도움말")
        print("/stats — 통계")
        print("/mode — 모드 전환")
        print("/clear — 뇌 초기화")
        return True
    if text == "/stats":
        print(f"🧠 단어: {len(brain)}")
        print(f"💬 메시지: {messages}")
        print(f"📚 학습: {trainings}")
        print(f"⚙️ 모드: {mode}")
        return True
    if text == "/mode":
        mode = "재미" if mode == "일반" else "일반"
        print(f"⚙️ 모드 전환 → {mode}")
        return True
    if text == "/clear":
        brain.clear()
        save()
        print("🗑️ 뇌 초기화 완료")
        return True
    return False

print("🤖 학습 가능한 AI 시작")
print("/help 입력으로 명령 확인")

while True:
    user_input = input("당신: ")
    if user_input.lower() == "종료":
        break
    user_input = clean(user_input)
    messages += 1
    if user_input.startswith("/"):
        if commands(user_input):
            continue
    answer = find_answer(user_input)
    if answer:
        if mode == "재미":
            answer += " 😎"
        print("AI:", answer)
    else:
        print("AI: 모릅니다. 가르쳐 주세요.")
        new_answer = input("답변: ")
        train(user_input, clean(new_answer))
        print("AI: 학습 완료 🧠")
