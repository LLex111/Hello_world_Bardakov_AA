V = int(input("Нужный объем раствора (в мл): "))
M = V * 0.009
with open("recipe.txt", "w", encoding="utf-8") as file:
    file.write(f"ОТЧЕТ ПО ПРИГОТОВЛЕНИЮ:\n{"-" * 23}\nОбщий объем:\t{V}\tмл\nМасса соли:\t{M:.2f}\tг\nОбъем воды:\t{V}\tмл")
