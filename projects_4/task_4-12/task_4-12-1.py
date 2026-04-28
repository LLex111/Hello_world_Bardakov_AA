array = [64, 34, 25, 12, 22, 11, 90]
n = len(array)

for i in range(n):
    swapped = False  # Флаг: была ли перестановка?
    for j in range(0, n - i - 1):
        if array[j] > array[j + 1]:
            array[j], array[j + 1] = array[j + 1], array[j]
            swapped = True 
            
    # Если за весь проход не было перестановок — выходим
    if not swapped:
        break

print("Отсортированный массив:", array)