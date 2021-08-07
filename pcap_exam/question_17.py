print("O programa causará uma exceção ao ser executado.")
lst = [i // i for i in range(0, 4)]
sum = 0
for n in lst:
    sum += n

print(sum)
