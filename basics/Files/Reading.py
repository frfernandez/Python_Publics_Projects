'''
r - read
w - write
a - append
r+ - read/write
'''

employee_file = open("employees.txt", "r");

print(employee_file.readable());

print("");
print(employee_file.read());

employee_file.close();
employee_file = open("employees.txt", "r");
print("");
print(employee_file.readline());
print(employee_file.readline());

employee_file.close();
employee_file = open("employees.txt", "r");
print("");
print(employee_file.readlines());

employee_file.close();
employee_file = open("employees.txt", "r");
print("");
print(employee_file.readlines()[1]);

employee_file.close();
employee_file = open("employees.txt", "r");
print("");
for employee in employee_file.readlines():
    print(employee);

employee_file.close();