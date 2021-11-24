from tkinter import *
import intrumentos


if __name__ == '__main__':
    raiz = Tk()
    raiz.title("Instrumentos")
    raiz.config(bg="#e3f2b3")
    raiz.geometry("750x400")

    intrumentos.App(raiz)
    raiz.mainloop()
