def gen():
    lst = range(5)
    for i in lst:
        yield i*i

for i in gen():
    print(i, end="")

print()
print("O comando yield trabalha como um acumulador numérico.")
