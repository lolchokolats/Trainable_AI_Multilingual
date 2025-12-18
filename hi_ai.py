import json
import os
import random

FILE = "hi.json"

if os.path.exists(FILE):
    with open(FILE, "r", encoding="utf-8") as f:
        brain = json.load(f)
else:
    brain = {}

mode = "सामान्य"
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
        print("📌 कमांड:")
        print("/help — मदद")
        print("/stats — सांख्यिकी")
        print("/mode — मोड बदलें")
        print("/clear — दिमाग साफ़ करें")
        return True
    if text == "/stats":
        print(f"🧠 शब्द: {len(brain)}")
        print(f"💬 संदेश: {messages}")
        print(f"📚 प्रशिक्षण: {trainings}")
        print(f"⚙️ मोड: {mode}")
        return True
    if text == "/mode":
        mode = "मज़ेदार" if mode == "सामान्य" else "सामान्य"
        print(f"⚙️ मोड बदला → {mode}")
        return True
    if text == "/clear":
        brain.clear()
        save()
        print("🗑️ दिमाग साफ़ किया गया")
        return True
    return False

print("🤖 प्रशिक्षण योग्य एआई चालू")
print("/help टाइप करके कमांड देखें")

while True:
    user_input = input("आप: ")
    if user_input.lower() == "बाहर":
        break
    user_input = clean(user_input)
    messages += 1
    if user_input.startswith("/"):
        if commands(user_input):
            continue
    answer = find_answer(user_input)
    if answer:
        if mode == "मज़ेदार":
            answer += " 😎"
        print("AI:", answer)
    else:
        print("AI: मुझे नहीं पता। मुझे सिखाएँ।")
        new_answer = input("उत्तर: ")
        train(user_input, clean(new_answer))
        print("AI: सीखा 🧠")
