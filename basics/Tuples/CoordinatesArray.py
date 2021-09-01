coordinates = [(4, 5), (6, 7), (80, 34)];
print(coordinates[0]);
print(coordinates[1]);
print(coordinates[2]);

print(coordinates[0][0]);
print(coordinates[0][1]);

print(coordinates[1][0]);
print(coordinates[1][1]);

print(coordinates[2][0]);
print(coordinates[2][1]);

print()
for line in coordinates:
    for column in line:
        print(line, column)

ini = [("Conection", "database_type"),
       ("Conection", "protocol"),
       ("Conection", "database"),
       ("Conection", "path"),
       ("Conection", "server"),
       ("Conection", "port"),
       ("Conection", "user"),
       ("Conection", "password")]

ini.append(("Teste", "testando"))

key = True
print()
for line in ini:
    for column in line:
        if key:
            print("section", column)
            key = False
        else:
            print("key", column)
            key = True
