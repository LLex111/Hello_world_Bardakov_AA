n = int(input())

x = int(input())
max = x

i = 2
while i <= n:
    x = int(input())
    if x > max:
        max = x
    i = i + 1

print(max)