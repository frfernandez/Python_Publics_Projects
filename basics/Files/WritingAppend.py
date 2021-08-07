'''
r - read
w - write
a - append
r+ - read/write
'''

employee_file = open("Append.txt", "a");

employee_file.write("Toby - Human Resources");
employee_file.write("\nKelly - Customer Service");

employee_file.close();
