from ctypes.wintypes import RGB
from tkinter import *
from tkinter.font import BOLD
import numpy as np
from PIL import Image, ImageTk
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import cm
from piezas import *

class Master(Tk):

    def __init__(self, sizex, sizey):
        
        super().__init__()
        
        self.color_fondo = 'sky blue'

        self.iconbitmap('tetris.ico')
        self.title('TETRIS')
        self.resizable(False,False)

        self.marco_principal = Frame(self, bg=self.color_fondo, width=600, height=600)

        self.marco_principal.pack()

        # self.canvas = DisplayCanvas(self, sizex, sizey)
        self.display = DisplayFrame(self, sizex, sizey)
        self.marcador = FrameMarcador(self)

        rotulo = Label(self, text='TETRIS', bg=self.color_fondo, font=('Verdana', 32, BOLD))
        rotulo.place(relx=0.5, rely=0.05, anchor=CENTER)



class DisplayFrame(Frame):
    
    color_fondo_display = 'white'

    def __init__(self, master, sizex, sizey):

        super().__init__(master, bg='white', width=250, height=500)
        self.place(relx=0.7, rely=0.55, anchor=CENTER)
        self.canvas = DisplayCanvas(self, sizex, sizey)
        self.canvas.place(relx=0.5,rely=0.5, anchor=CENTER)



class DisplayCanvas(Canvas):

    colorlist = [(1,1,1), pieza_linea.color, pieza_piramide.color, pieza_zig.color, pieza_zag.color, pieza_ele.color, pieza_lel.color, pieza_cuadrado.color]
    cmap = LinearSegmentedColormap.from_list('Customizado', colorlist, 8)

    def __init__(self, frame, sizex, sizey):

        super().__init__(frame, width=250, height=500)

        represented_matrix = np.zeros((sizex,sizey))
        im = Image.fromarray(np.uint8(self.cmap(represented_matrix)*255))
        pixelado = ImageTk.PhotoImage(image=im.resize((250,500), Image.NEAREST))
        self.create_image(0, 0, anchor=NW, image=pixelado)


    def actualizar_canvas(self, M, Mf, color='blue'):

        represented_matrix = ((M[2:,:] + Mf[2:,:]))/7
        im = Image.fromarray(np.uint8(self.cmap(represented_matrix)*255))
        pixelado = ImageTk.PhotoImage(image=im.resize((250,500), Image.NEAREST))
        self.create_image(0, 0, anchor=NW, image=pixelado)
        self.update()

        # print(M)



class FrameMarcador(Frame):

    color_fondo = 'light sky blue'

    def __init__(self, master):

        super().__init__(master, bg=self.color_fondo, width=250, height=100)

        rotulo              = Label(self, text='POINTS:',   font=('Verdana', 24, BOLD), bg=self.color_fondo)
        self.puntos_label   = Label(self, text=0,           font=('Verdana', 24, BOLD), bg=self.color_fondo)
        rotulo.place(relx=.5, rely=.2, anchor=CENTER)
        self.puntos_label.place(relx=.5, rely=.7, anchor=CENTER)

        self.place(x=12.5, y=100)

    def suma(self, puntos):

        self.puntos_label.config(text=puntos, font=('Verdana', 24), bg=self.color_fondo)
    