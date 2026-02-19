print("=== Анализ последовательности ДНК ===")
dna = input("Введите последовательность ДНК: ").upper()
A = dna.count("A")
T = dna.count("T")
G = dna.count("G")
C = dna.count("C")
lenth = A + T + G + C
print(f"Подсчёт нуклеотидов:\nA:\t{A}\nT:\t{T}\nG:\t{G}\nC:\t{C}\n\nОбщая длина: {lenth} нуклеотидов")