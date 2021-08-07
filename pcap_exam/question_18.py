for r in range(3):
    print(r)

lst = [[c for c in range(r)] for r in range(3)]
print()
print([[c for c in range(r)] for r in range(3)])
print()

for x in lst:
    for y in x:
        if y < 2:
            print('*', end='')

print()
print()
print("Imprimindo as variáveis")
print("lst:", lst)
print()

for x in lst:
    print("x:", x)
    print()

    for y in x:
        print("y:", y)
        if y < 2:
            print('*', end='')
