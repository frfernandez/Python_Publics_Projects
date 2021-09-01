from paises import sd


class Sulamericanos():

    def __init__(self):
        ''' Construtor'''
        self.members = sd

    def print_paises(self):
        print('Mostrando alguns paises sulamericanos')
        for member in self.members:
            print('\t%s ' % member)
