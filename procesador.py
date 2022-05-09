from piezas import *
import time as time
from ventana import Master

class Procesador():

    sizex = 10
    sizey = 22
    id_min = 1
    id_max = 8

    def __init__(self):

        self.matrix         = Matrix(self.sizex, self.sizey)
        self.master         = Master(self.sizex, self.sizey)

        self.master.bind('<space>', lambda event: self.tap(0))
        self.master.bind('<Left>', lambda event: self.tap(-1))
        self.master.bind('<Right>', lambda event: self.tap(1))
        self.master.bind('<Down>', lambda event: self.tap(2))
        self.master.bind('<Escape>', lambda event: self.pausa())
        
        self.pieza          = Pieza.generar(np.random.randint(self.id_min, self.id_max), self.sizex, self.sizey)
        self.piezas         = list(np.random.randint(self.id_min, self.id_max, 3))
        self.pieza_cayendo  = True
        self.running        = True
        self.pausa_var      = False
        self.puntos         = 0

        self.t              = 0
        self.t0             = time.time_ns()
        self.tp             = self.t0
        self.tpi            = 0
        self.tpf            = 0
        self.tmax           = 1e15
        self.t              = time.time_ns()-self.t0
        dt                  = .4
        self.dt_ns          = dt*1e9
        self.conteo         = self.dt_ns

        print('JUGANDO')

        self.resultado      = self.bucle_principal()
                    
        self.game_over()


    def bucle_principal(self):

        while self.running and self.t<self.tmax:

            if not self.pieza_cayendo:

                out_Mf = self.matrix.fijar_matrizf(self.pieza)

                if out_Mf==-1:

                    return 1

                self.puntos += out_Mf*125

                if out_Mf==4: 
                    
                    self.puntos += 500

                self.master.marcador.suma(self.puntos)

                self.nueva_pieza()

                self.pieza_cayendo = True

            if not self.pausa_var:
                
                rdt = time.time_ns()-self.tp-self.t
                
                t = time.time_ns()-self.tp

                if t > self.conteo:

                    out_instante = self.instante()
                    self.conteo += self.dt_ns

            self.actualizar()
            
            # print('t: ', int(self.t/1e6), ' conteo: ', int(self.conteo/1e6), ' rdt: ', int(self.rdt/1e6))
            # print(self.matrix.M)
            
            time.sleep(0.01)

        return 0


    def instante(self):

        if self.pieza.descenso(self.matrix.Mf): self.pieza_cayendo = False

        return 0


    def tap(self, tap):

        if tap==0:      out_giro = self.pieza.giro(self.matrix.Mf)
        elif tap==2:    out_bajar = self.pieza.descenso(self.matrix.Mf)
        else:           out_movimiento = self.pieza.movimiento(tap, self.matrix.Mf)

        self.actualizar()

        # time.sleep(.1)


    def actualizar(self):

        self.matrix.actualizar_matriz(self.pieza)
        self.master.display.canvas.actualizar_canvas(self.matrix.M, self.matrix.Mf)

    
    def nueva_pieza(self):

        # print(self.piezas)

        self.pieza = Pieza.generar(self.piezas[0], self.sizex, self.sizey)
        self.piezas.pop(0)
        self.piezas.append(np.random.randint(self.id_min,self.id_max))


    def pausa(self):

        self.pausa_var = not self.pausa_var

        if self.pausa_var: self.tpi = time.time_ns()
        if not self.pausa_var:
            self.tpf = time.time_ns()
            self.tp += self.tpf-self.tpi
        

    
    def game_over(self):

        print('GAMEOVER')

        self.master.mainloop()


class Matrix():

    def __init__(self, sizex, sizey):

        self.sizex = sizex
        self.sizey = sizey

        self.M = np.zeros((sizey,sizex))
        self.Mf = np.zeros((sizey,sizex))


    def actualizar_matriz(self, pieza):

        self.M[:,:] = 0

        for i,j in pieza.forma:

            posx = pieza.posicion[0]+i
            posy = pieza.posicion[1]+j
            self.M[posy,posx] = pieza.id


    def fijar_matrizf(self, pieza):
        
        for i,j in pieza.forma:

            posx = pieza.posicion[0]+i
            posy = pieza.posicion[1]+j
            self.Mf[posy,posx] = pieza.id

            if posy==1: return -1

        combo = 0
        
        for j in range(self.sizey):

            if self.Mf[j,:].all()!=0:
                self.linea(j)
                combo += 1

        return combo

    def linea(self, linea):

        self.Mf[1:linea+1,:] = self.Mf[:linea,:]