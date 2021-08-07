class A:
    def a(self):
        print("A",end='')

class B(A):
    def a(self):
        print("B",end='')

class C(B):
    def b(self):
        print("B",end='')

a = A()
b = B()
c = C()
a.a()
b.a()
c.b()
