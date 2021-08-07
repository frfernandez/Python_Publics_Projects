lst1 = "12,34"
print("Valor da variável lst1..:", lst1)
print("Tamanho da variável lst1:", len(lst1))

lst2 = lst1.split(',')
print("Valor da variável lst2..:", lst2)
print("Tamanho da variável lst2:", len(lst2))

print(len(lst1) < len(lst2))
