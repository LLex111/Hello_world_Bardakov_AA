n = int(input())

s = 0
count = 0
i = 1

while i <= n:
    x = int(input())
    if i % 2 == 0:
        s = s + x
        count = count + 1
    i = i + 1

if count > 0:
    avg = s / count
    print(avg)
else:
    print("Нет элементов с четными индексами")