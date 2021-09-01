from paises import ed


class Europeus():

    def __init__(self):
        ''' Construtor '''
        self.members = ed

    def print_paises(self):
        print('Mostrando alguns paises europeus')
        for member in self.members:
            print('\t%s ' % member)
