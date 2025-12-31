def explain(food, goal):
    if goal == "lose_weight":
        return f"{food['name']} چون پروتئین بالا و کالری مناسب دارد پیشنهاد شد."
    if goal == "gain_weight":
        return f"{food['name']} به دلیل کالری بالا برای افزایش وزن مناسب است."
    return f"{food['name']} گزینه متعادل برای حفظ وزن است."
