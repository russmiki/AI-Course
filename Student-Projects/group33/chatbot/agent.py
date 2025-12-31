import re
from joblib import load
from nlp.preprocess import preprocess
from chatbot.memory import UserMemory

model = load("models/intent_model.pkl")
vectorizer = load("models/vectorizer.pkl")

class DietAgent:
    def __init__(self):
        self.memory = UserMemory()

    def detect_intent(self, text):
        text = preprocess(text)
        vec = vectorizer.transform([text])
        return model.predict(vec)[0]

    def extract_number(self, text):
        nums = re.findall(r"\d+", text)
        return int(nums[0]) if nums else None

    def reply(self, text):
        if not self.memory.has("goal"):
            intent = self.detect_intent(text)
            if intent in ["lose_weight", "gain_weight", "maintain_weight"]:
                self.memory.update("goal", intent)
                return "وزنت رو به کیلو بگو"
            return "هدفت چیه؟ (کاهش، افزایش یا حفظ وزن)"

        if not self.memory.has("weight"):
            num = self.extract_number(text)
            if num:
                self.memory.update("weight", num)
                return "قدت رو به سانتی‌متر بگو"
            return "وزن رو عددی بگو"

        if not self.memory.has("height"):
            num = self.extract_number(text)
            if num:
                self.memory.update("height", num)
                return "سنت رو بگو"
            return "قد رو عددی بگو"

        if not self.memory.has("age"):
            num = self.extract_number(text)
            if num:
                self.memory.update("age", num)
                return "دارم رژیم رو محاسبه می‌کنم..."
            return "سن رو عددی بگو"

        return "اطلاعات کامل شد"
