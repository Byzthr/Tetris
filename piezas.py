import numpy as np

class Pieza():

    def __init__(self, sizex, sizey):

        self.sizex = sizex
        self.sizey = sizey

        self.posicion = [4, 1]

    @staticmethod
    def generar(id, sizex, sizey):

        if id == 7: return pieza_cuadrado(sizex, sizey)
        if id == 1: return pieza_linea(sizex, sizey)
        if id == 2: return pieza_piramide(sizex, sizey)
        if id == 3: return pieza_zig(sizex, sizey)
        if id == 4: return pieza_zag(sizex, sizey)
        if id == 5: return pieza_ele(sizex, sizey)
        if id == 6: return pieza_lel(sizex, sizey)

    def descenso(self, Mf):

        for i,j in self.forma:
            posx = self.posicion[0]+i
            posy = self.posicion[1]+j
            if posy == self.sizey-1: return 1
            if Mf[posy+1,posx]: return 1

        self.posicion[1] += 1

        return 0

    def giro(self, Mf):

        c = 0

        for i,j in self.forma:
            nposx = self.posicion[0]-j
            nposy = self.posicion[1]+i
            if nposx < 0: return 1
            if nposx >= self.sizex: return 1
            if nposy >= self.sizey: return 1
            if Mf[nposy,nposx]: return 1

        for i,j in self.forma:
            self.forma[c] = (-j,i)
            c+=1

        return 0

    def movimiento(self, sentido, Mf):

        for i,j in self.forma:
            posx = self.posicion[0]+i
            posy = self.posicion[1]+j
            if posx+sentido <0 or posx+sentido >=self.sizex: return 1
            if Mf[posy,posx+sentido]: return 1

        self.posicion[0] += sentido

        return 0


class pieza_cuadrado(Pieza):
    
    color = 'yellow'

    def __init__(self, sizex, sizey):

        super().__init__(sizex, sizey)
        
        self.id = 7
        self.forma = [(0,0),(0,1),(1,0),(1,1)]
        self.limites = [0,0,1,1]


class pieza_linea(Pieza):
    
    color = 'cyan'

    def __init__(self, sizex, sizey):

        super().__init__(sizex, sizey)

        self.id = 1
        self.forma = [(0,-1),(0,0),(0,1),(0,2)]
        self.limites = [0,-1,0,2]


class pieza_piramide(Pieza):

    color = 'purple'

    def __init__(self, sizex, sizey):

        super().__init__(sizex, sizey)

        self.id = 2
        self.forma = [(0,-1),(-1,0),(0,0),(1,0)]
        self.limites = [-1,-1,1,0]


class pieza_zig(Pieza):

    color = 'green'

    def __init__(self, sizex, sizey):

        super().__init__(sizex, sizey)

        self.id = 3
        self.forma = [(0,-1),(0,0),(1,0),(1,1)]
        self.limites = [0,-1,1,1]


class pieza_zag(Pieza):
    
    color = 'red'

    def __init__(self, sizex, sizey):

        super().__init__(sizex, sizey)

        self.id = 4
        self.forma = [(1,-1),(1,0),(0,0),(0,1)]
        self.limites = [0,-1,1,1]


class pieza_ele(Pieza):
    
    color = 'orange'

    def __init__(self, sizex, sizey):

        super().__init__(sizex, sizey)

        self.id = 5
        self.forma = [(0,-1),(0,0),(0,1),(1,1)]
        self.limites = [0,-1,1,1]
        self.color = 'orange'


class pieza_lel(Pieza):

    color = 'blue'

    def __init__(self, sizex, sizey):

        super().__init__(sizex, sizey)

        self.id = 6
        self.forma = [(0,-1),(0,0),(0,1),(-1,1)]
        self.limites = [-1,-1,0,1]
        self.color = 'blue'
