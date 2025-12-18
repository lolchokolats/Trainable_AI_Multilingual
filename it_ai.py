import json
import os
import random

FILE = "it.json"

if os.path.exists(FILE):
    with open(FILE, "r", encoding="utf-8") as f:
        brain = json.load(f)
else:
    brain = {}

mode = "normale"
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
        print("📌 Comandi:")
        print("/help — aiuto")
        print("/stats — statistiche")
        print("/mode — cambia modalità")
        print("/clear — cancella cervello")
        return True
    if text == "/stats":
        print(f"🧠 parole: {len(brain)}")
        print(f"💬 messaggi: {messages}")
        print(f"📚 addestramenti: {trainings}")
        print(f"⚙️ modalità: {mode}")
        return True
    if text == "/mode":
        mode = "divertente" if mode == "normale" else "normale"
        print(f"⚙️ modalità cambiata → {mode}")
        return True
    if text == "/clear":
        brain.clear()
        save()
        print("🗑️ cervello cancellato")
        return True
    return False

print("🤖 IA addestrabile avviata")
print("Scrivi /help per comandi")

while True:
    user_input = input("Tu: ")
    if user_input.lower() == "exit":
        break
    user_input = clean(user_input)
    messages += 1
    if user_input.startswith("/"):
        if commands(user_input):
            continue
    answer = find_answer(user_input)
    if answer:
        if mode == "divertente":
            answer += " 😎"
        print("IA:", answer)
    else:
        print("IA: non so. Insegnami.")
        new_answer = input("Risposta: ")
        train(user_input, clean(new_answer))
        print("IA: memorizzato 🧠")
