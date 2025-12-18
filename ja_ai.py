import json
import os
import random

FILE = "ja.json"

if os.path.exists(FILE):
    with open(FILE, "r", encoding="utf-8") as f:
        brain = json.load(f)
else:
    brain = {}

mode = "通常"
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
        print("📌 コマンド:")
        print("/help — ヘルプ")
        print("/stats — 統計")
        print("/mode — モード切替")
        print("/clear — 脳をクリア")
        return True
    if text == "/stats":
        print(f"🧠 単語: {len(brain)}")
        print(f"💬 メッセージ: {messages}")
        print(f"📚 学習: {trainings}")
        print(f"⚙️ モード: {mode}")
        return True
    if text == "/mode":
        mode = "楽しい" if mode == "通常" else "通常"
        print(f"⚙️ モード切替 → {mode}")
        return True
    if text == "/clear":
        brain.clear()
        save()
        print("🗑️ 脳をクリアしました")
        return True
    return False

print("🤖 学習可能なAI起動")
print("コマンドは /help を入力")

while True:
    user_input = input("あなた: ")
    if user_input.lower() == "終了":
        break
    user_input = clean(user_input)
    messages += 1
    if user_input.startswith("/"):
        if commands(user_input):
            continue
    answer = find_answer(user_input)
    if answer:
        if mode == "楽しい":
            answer += " 😎"
        print("AI:", answer)
    else:
        print("AI: わかりません。教えてください。")
        new_answer = input("回答: ")
        train(user_input, clean(new_answer))
        print("AI: 学習済み 🧠")
