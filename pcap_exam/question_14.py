lst = ["A", "B", "C", 2, 4]
print("Valor da variável lst.............:", lst)
print("Largura da variável lst...........:", len(lst))
print("Primeiro carácter.................:", lst[0])
print("Último carácter...................:", lst[4])
print("Todos caracteres..................:", lst[0:5])
print("Vazio para o primeiro carácter....:", lst[:5])
print("Vazio para o último carácter......:", lst[0:])
del lst[0:-2]
print(lst)
