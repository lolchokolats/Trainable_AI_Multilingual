import json
import os
import random

FILE = "zh.json"

if os.path.exists(FILE):
    with open(FILE, "r", encoding="utf-8") as f:
        brain = json.load(f)
else:
    brain = {}

mode = "普通"
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
        print("📌 命令:")
        print("/help — 帮助")
        print("/stats — 统计")
        print("/mode — 切换模式")
        print("/clear — 清空脑子")
        return True
    if text == "/stats":
        print(f"🧠 单词: {len(brain)}")
        print(f"💬 消息: {messages}")
        print(f"📚 学习次数: {trainings}")
        print(f"⚙️ 模式: {mode}")
        return True
    if text == "/mode":
        mode = "搞笑" if mode == "普通" else "普通"
        print(f"⚙️ 模式切换 → {mode}")
        return True
    if text == "/clear":
        brain.clear()
        save()
        print("🗑️ 脑子清空完成")
        return True
    return False

print("🤖 可训练的人工智能启动")
print("输入 /help 获取命令")

while True:
    user_input = input("你: ")
    if user_input.lower() == "退出":
        break
    user_input = clean(user_input)
    messages += 1
    if user_input.startswith("/"):
        if commands(user_input):
            continue
    answer = find_answer(user_input)
    if answer:
        if mode == "搞笑":
            answer += " 😎"
        print("AI:", answer)
    else:
        print("AI: 我不知道。教我吧。")
        new_answer = input("回答: ")
        train(user_input, clean(new_answer))
        print("AI: 已学习 🧠")
