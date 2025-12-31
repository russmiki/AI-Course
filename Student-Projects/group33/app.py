from flask import Flask, render_template, request
import pandas as pd
import random

app = Flask(__name__)

# دیتاست
foods_df = pd.read_csv('data/foods.csv')

@app.route("/", methods=["GET", "POST"])
def index():
    meal_plan = {}
    if request.method == "POST":
        # ورودی کاربر
        weight = float(request.form.get("weight"))
        height = float(request.form.get("height"))
        age = int(request.form.get("age"))
        gender = request.form.get("gender")
        goal = request.form.get("goal")

        # کالری روزانه تقریبی (BMR + TDEE ساده)
        if gender == "مرد":
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        else:
            bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

        if goal == "کاهش وزن":
            calories = bmr * 1.2 - 500
        elif goal == "افزایش وزن":
            calories = bmr * 1.2 + 500
        else:
            calories = bmr * 1.2

        # بخش‌بندی وعده‌ها و انتخاب ۲ تا ۳ غذا به صورت تصادفی
        for meal in ["صبحانه", "میان‌وعده", "ناهار", "میان‌وعده دوم", "شام"]:
            options = foods_df[foods_df["وعده"] == meal]
            if not options.empty:
                num_items = random.randint(2, min(3, len(options)))
                meal_plan[meal] = options.sample(num_items).to_dict(orient="records")
            else:
                meal_plan[meal] = []

    return render_template("index.html", meal_plan=meal_plan)

if __name__ == "__main__":
    app.run(debug=True)
