n = int(input())

s = 0
i = 1

while i <= n:
    x = int(input())
    if x % 2 != 0:
        s = s + x
    i = i + 1

print(s)