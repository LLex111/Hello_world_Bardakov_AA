n = int(input())

count = 0
i = 1

while i <= n:
    x = int(input())
    if x > 0:
        count = count + 1
    i = i + 1

print(count)