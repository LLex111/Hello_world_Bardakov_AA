weight = float(input("Введите  ваш вес (кг): "))
height = float(input("Введите ваш рост (см): "))
bmi = weight / (height / 100) ** 2
print(f"--- Отчет о состоянии здоровья ---\nРост:\t{height:.1f} см\nВес:\t{weight:.1f} кг\nИндекс массы тела:	{bmi:.2f}")