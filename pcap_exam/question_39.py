file = open("test.txt")

print("file.readlines()")
print(file.readlines())

print()
print("for l in file")
file.seek(0)
for l in file:
    print(l)

print()
print("file.read()")
file.seek(0)
print(file.read())

file.close()
