import json
import os
import random

FILE = "rus.json"

if os.path.exists(FILE):
    with open(FILE, "r", encoding="utf-8") as f:
        brain = json.load(f)
else:
    brain = {}

mode = "норм"
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
        print("📌 Команды:")
        print("/help — помощь")
        print("/stats — статистика")
        print("/mode — режимы")
        print("/clear — очистить мозг")
        return True
    if text == "/stats":
        print(f"🧠 слов: {len(brain)}")
        print(f"💬 сообщений: {messages}")
        print(f"📚 обучений: {trainings}")
        print(f"⚙️ режим: {mode}")
        return True
    if text == "/mode":
        mode = "рофл" if mode == "норм" else "норм"
        print(f"⚙️ режим переключён → {mode}")
        return True
    if text == "/clear":
        brain.clear()
        save()
        print("🗑️ мозг очищен")
        return True
    return False

print("🤖 Обучаемый ИИ запущен")
print("Напиши /help для команд")

while True:
    user_input = input("Ты: ")
    if user_input.lower() == "выход":
        break
    user_input = clean(user_input)
    messages += 1
    if user_input.startswith("/"):
        if commands(user_input):
            continue
    answer = find_answer(user_input)
    if answer:
        if mode == "рофл":
            answer += " 😎"
        print("ИИ:", answer)
    else:
        print("ИИ: не знаю. Научи меня.")
        new_answer = input("Ответ: ")
        train(user_input, clean(new_answer))
        print("ИИ: принято 🧠")
