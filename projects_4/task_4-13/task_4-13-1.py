a = int(input())
b = int(input())
c = int(input())
d = int(input())

m = a
if b < m:
    m = b
if c < m:
    m = c
if d < m:
    m = d

print(m)