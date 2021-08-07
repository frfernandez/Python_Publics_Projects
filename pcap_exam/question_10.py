print("Exemplo 1")
for i in range(1, 4, 2):
    print("*")

print()
print("Exemplo 2")
for i in range(1, 4, 2):
    print("*", end="")

print()
print("Exemplo 3")
for i in range(1, 4, 2):
    print("*", end="**")

print()
print("Exemplo 4")
for i in range(1, 4, 2):
    print("*", end="**")

print("***")
print()
print("A função range possui três parâmetros:")
print("01) Parâmetro do início da contagem.")
print("02) Parâmetro do fim da contagem menos 1 (um).")
print("03) Parâmetro de passos que serão realizados na contagem.")

print()
print("Exemplo sem passos iniciando do 1 (um) e indo até 10 (dez): ")
for i in range(1, 10):
    print(i)

print()
print("Exemplo com passos iniciando do 1 (um) e indo até 10 (dez) andando de 2 (dois): ")
for i in range(1, 10, 2):
    print(i)
