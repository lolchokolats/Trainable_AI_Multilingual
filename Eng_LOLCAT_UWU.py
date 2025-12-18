import json
import os
import random

FILE = "lolcat_eng.json"

if os.path.exists(FILE):
    with open(FILE, "r", encoding="utf-8") as f:
        brain = json.load(f)
else:
    brain = {}

mode = "normul"
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
        print("📌 Commaz:")
        print("/help — halp")
        print("/stats — statz")
        print("/mode — modez")
        print("/clear — cleer brane")
        return True
    if text == "/stats":
        print(f"🧠 wordz: {len(brain)}")
        print(f"💬 messajes: {messages}")
        print(f"📚 traininz: {trainings}")
        print(f"⚙️ mode: {mode}")
        return True
    if text == "/mode":
        mode = "funz" if mode == "normul" else "normul"
        print(f"⚙️ mode changed → {mode}")
        return True
    if text == "/clear":
        brain.clear()
        save()
        print("🗑️ brane cleered")
        return True
    return False

print("🤖 trainabul AI startd")
print("type /help 4 commandz")

while True:
    user_input = input("u: ")
    if user_input.lower() == "exit":
        break
    user_input = clean(user_input)
    messages += 1
    if user_input.startswith("/"):
        if commands(user_input):
            continue
    answer = find_answer(user_input)
    if answer:
        if mode == "funz":
            answer += " 😹"
        print("AI:", answer)
    else:
        print("AI: i dunno. teach me pls.")
        new_answer = input("responz: ")
        train(user_input, clean(new_answer))
        print("AI: lerned 🧠")
