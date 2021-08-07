x = 0
try:
    print("try")
    print(x)
    print(1 / x)
except ZeroDivisionError:
    print("except ZeroDivisionError")
    print("ERROR MESSAGE")
finally:
    print("finally")
    print(x + 1)

print(x + 2)
