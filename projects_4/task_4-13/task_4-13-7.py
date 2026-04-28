n = int(input())

s = 0
i = 1

while i <= n:
    x = float(input())
    s = s + x
    i = i + 1

avg = s / n
print(avg)