import json
import os
import random

FILE = "esp.json"

if os.path.exists(FILE):
    with open(FILE, "r", encoding="utf-8") as f:
        brain = json.load(f)
else:
    brain = {}

mode = "normal"
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
        print("📌 Comandos:")
        print("/help — ayuda")
        print("/stats — estadísticas")
        print("/mode — cambiar modo")
        print("/clear — limpiar cerebro")
        return True
    if text == "/stats":
        print(f"🧠 palabras: {len(brain)}")
        print(f"💬 mensajes: {messages}")
        print(f"📚 entrenamientos: {trainings}")
        print(f"⚙️ modo: {mode}")
        return True
    if text == "/mode":
        mode = "divertido" if mode == "normal" else "normal"
        print(f"⚙️ modo cambiado → {mode}")
        return True
    if text == "/clear":
        brain.clear()
        save()
        print("🗑️ cerebro limpiado")
        return True
    return False

print("🤖 IA entrenable iniciada")
print("Escribe /help para comandos")

while True:
    user_input = input("Tú: ")
    if user_input.lower() == "salir":
        break
    user_input = clean(user_input)
    messages += 1
    if user_input.startswith("/"):
        if commands(user_input):
            continue
    answer = find_answer(user_input)
    if answer:
        if mode == "divertido":
            answer += " 😎"
        print("IA:", answer)
    else:
        print("IA: no sé. Enséñame.")
        new_answer = input("Respuesta: ")
        train(user_input, clean(new_answer))
        print("IA: aprendido 🧠")
