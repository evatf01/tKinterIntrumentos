from tkinter import ttk

from tkinter import *
from tkinter import messagebox
import csv


def noExiste(var):
    var_s = str(var)
    messagebox.showinfo("Instrumento no encontrado", var_s + ' ' + "no existe")


def write_instrument():
    messagebox.showinfo("Escribe un instrumento")


def borrar_instrumento(nombre):
    var_name = str(nombre)
    if var_name == '':
        write_instrument()
    else:
        search = messagebox.askquestion("¿Esta seguro de que desea eliminar este instrumento?\n" + var_name)
        if search == "yes":
            return True
        else:
            return False


def modificar_instrumento(instrumento):
    var_categoria = str(instrumento[0])
    var_marca = str(instrumento[1])
    var_modelo = str(instrumento[2])
    search = messagebox.askquestion("Modificar instrumento",
                                    "Desea modificar este instrumento: \n" + "categoria: " + var_categoria + "\nmarca: "
                                    + var_marca + "\nmodelo: " + var_modelo)
    if search == "yes":
        return True
    else:
        return False


# -----------------INTERFAZ GRÁFICA---------------------------------
class App():
    def __init__(self, raiz):
        self.window = raiz

        # ------Paneles-------
        panelInfo = LabelFrame(self.window, bg="#e3f2b3")
        panelInfo.grid(row=0, column=0, sticky=N)

        panelBotones = LabelFrame(self.window, bg="#e3f2b3")
        panelBotones.grid(row=2, column=0, sticky=S)

        panelContactos = LabelFrame(self.window, bg="#e3f2b3")
        panelContactos.grid(row=1, column=0, sticky=N)

        # ------Cuadros de texto-------
        Label(panelInfo, text='Categoria', bg="#e3f2b3").grid(row=0, column=0)
        inbox_categoria = Entry(panelInfo, width=35)
        inbox_categoria.grid(row=1, column=0)
        inbox_categoria.focus()

        Label(panelInfo, text='Marca', bg="#e3f2b3").grid(row=0, column=1)
        inbox_marca = Entry(panelInfo, width=32)
        inbox_marca.grid(row=1, column=1)

        Label(panelInfo, text='Modelo', bg="#e3f2b3", ).grid(row=0, column=2)
        inbox_modelo = Entry(panelInfo, width=32)
        inbox_modelo.grid(row=1, column=2)

        # ------Botones-------
        btAdd = Button(panelBotones, command=lambda: agregar(), text='Añadir ', width=15)
        btAdd.configure(bg="#969692", font=("Aldrich", "10", "normal"))
        btAdd.grid(row=0, column=0, sticky=S)

        btEliminar = Button(panelBotones, command=lambda: eliminar(), text='Eliminar', width=15)
        btEliminar.configure(bg="#c42912", font=("Aldrich", "10", "normal"))
        btEliminar.grid(row=0, column=1, sticky=S)

        btModificar = Button(panelBotones, command=lambda: modificar(), text='Modificar', width=15)
        btModificar.configure(bg="#969692", font=("Aldrich", "10", "normal"))
        btModificar.grid(row=0, column=2, sticky=S)

        btLimpiar = Button(panelBotones, command=lambda: limpiar(), text='Clear', width=15)
        btLimpiar.configure(bg="#969692", cursor='hand2', font=("Aldrich", "10", "normal"))
        btLimpiar.grid(row=1, column=0, sticky=S)

        btMostrar = Button(panelBotones, command=lambda: mostrar_instrumentos(), text='Mostrar', width=15)
        btMostrar.configure(bg="#969692", font=("Aldrich", "10", "normal"))
        btMostrar.grid(row=1, column=1, sticky=S)

        # -----ComboBox-------
        combo = ttk.Combobox(panelBotones, state='readonly', width=15, justify='center',
                             font=("Aldrich", "10", "normal"))
        combo["values"] = ['Categoria', 'Marca', 'Modelo']
        combo.grid(row=0, column=4)
        combo.current(0)

        # ------Tabla de instrumentos--------
        self.tree = ttk.Treeview(panelContactos, heigh=10, columns=("one", "two"))
        self.tree.grid(padx=5, pady=5, row=0, column=0, columnspan=1, sticky=N)
        self.tree.heading("#0", text='Categoria', anchor=CENTER)
        self.tree.heading("one", text='Marca', anchor=CENTER)
        self.tree.heading("two", text='Modelo', anchor=CENTER)

        # -------scroll de la tabla-----------
        scrollVert = Scrollbar(panelContactos, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollVert.set)
        scrollVert.grid(row=0, column=1, sticky="nsew")

        # ----------------------------------FUNCIONES------------------------------------

        def _limpiar_texto():
            inbox_categoria.delete(0, "end")
            inbox_marca.delete(0, "end")
            inbox_modelo.delete(0, "end")

        def _limpiar_lista():
            tree_list = self.tree.get_children()
            for item in tree_list:
                self.tree.delete(item)

        def _vista_csv():
            with open('Instrumentos.csv', 'r') as f:
                reader = csv.reader(f)
                for i, row in enumerate(reader):
                    categoria = str(row[0])
                    marca = str(row[1])
                    modelo = str(row[2])
                    self.tree.insert("", 0, text=categoria, values=(marca, modelo))

        def _guardar(categoria, marca, modelo):
            g_categoria = categoria
            g_marca = marca
            g_modelo = modelo
            with open('Instrumentos.csv', 'a') as f:
                writer = csv.writer(f, lineterminator='\r', delimiter=',')
                writer.writerow((g_categoria, g_marca, g_modelo))

        def _buscar(var_inbox, possition):
            list = []
            s_var_inbox = str(var_inbox)
            var_possition = int(possition)
            with open('Instrumentos.csv', 'r') as f:
                reader = csv.reader(f)
                for i, row in enumerate(reader):
                    if s_var_inbox == row[var_possition]:
                        list = [row[0], row[1], row[2]]
                        break
                    else:
                        continue
            return list

        def _check1(answer, var_search):
            val_modify = answer
            var = var_search
            if val_modify == []:
                noExiste(var)
            else:
                VentanaModificar(self.window, val_modify)

                # -----------Funciones de los botones---------------------------

        def agregar():
            categoria = inbox_categoria.get()
            marca = inbox_marca.get()
            modelo = inbox_modelo.get()
            instrumentos_check = [categoria, marca, modelo]
            if instrumentos_check == ['', '', '']:
                write_instrument()
            else:
                if categoria == '':
                    categoria = '<Default>'
                if marca == '':
                    marca = '<Default>'
                if modelo == '':
                    modelo = '<Default>'
                _guardar(categoria, marca, modelo)

                self.tree.insert("", 0, text=str(categoria), values=(str(marca), str(modelo)))
                self.tree.insert("", 0, text="Nueva categoria añadida",
                                 values=("Nueva marca añadida", "Nuevo modelo añadido"))

            instrumentos_check = []
            _limpiar_texto()

        def modificar():
            answer = []
            var_search = str(combo.get())
            if var_search == 'Categoria':
                var_inbox = inbox_categoria.get()
                possition = 0
                answer = _buscar(var_inbox, possition)
                _check1(answer, var_search)
            elif var_search == 'Marca':
                var_inbox = inbox_marca.get()
                possition = 1
                answer = _buscar(var_inbox, possition)
                _check1(answer, var_search)
            else:
                var_inbox = inbox_modelo.get()
                possition = 2
                answer = _buscar(var_inbox, possition)
                _check1(answer, var_search)
            _limpiar_texto()

        def mostrar_instrumentos():
            _vista_csv()

        def eliminar():
            categoria = str(inbox_categoria.get())
            a = borrar_instrumento(categoria)
            if a == True:
                with open('Instrumentos.csv', 'r') as f:
                    reader = list(csv.reader(f))
                with open('Instrumentos.csv', 'w') as f:
                    writer = csv.writer(f, lineterminator='\r', delimiter=',')
                    for i, row in enumerate(reader):
                        if categoria != row[0]:
                            writer.writerow(row)
            limpiar()
            mostrar_instrumentos()

        def limpiar():
            _limpiar_texto()
            _limpiar_lista()

            # ------Nueva clase para ventana modificar contacto--------


class VentanaModificar():
    def __init__(self, raiz, val_modify):
        self.raiz_window = raiz
        self.val_modify = val_modify
        self.categoria = str(self.val_modify[0])
        self.marca = str(self.val_modify[1])
        self.modelo = str(self.val_modify[2])

        window_modify = Toplevel(self.raiz_window)
        window_modify.title("Modificar instrumento")
        window_modify.configure(bg="#e3f2b3")
        window_modify.geometry("615x130")
        window_modify.resizable(0, 0)

        panel_texto = LabelFrame(window_modify, bg="#e3f2b3")
        panel_texto.grid(row=0, column=0)

        bt_panel_texto = LabelFrame(window_modify, bg="#e3f2b3")
        bt_panel_texto.grid(row=2, column=0)
        # ------Dialogo de confirmacion-------------------
        Label(panel_texto, text="¿Quieres modificar este isnstrumento?", bg="#e3f2b3",
              font=("Alrich", "11", "normal")).grid(row=0, column=0, columnspan=3)
        Label(panel_texto, text=self.categoria, bg="#e3f2b3", font=("Alrich", "11", "normal")).grid(row=1, column=0)
        Label(panel_texto, text=self.marca, bg="#e3f2b3", font=("Alrich", "11", "normal")).grid(row=1, column=1)
        Label(panel_texto, text=self.modelo, bg="#e3f2b3", font=("Alrich", "11", "normal")).grid(row=1, column=2)

        # ------Cuadros de texto ventana modificar-------------------
        Label(panel_texto, text="Introduce una categoria", bg="#e3f2b3", font=("Alrich", "11", "normal")).grid(row=2,
                                                                                                               column=0)
        categoria = Entry(panel_texto, font=("Alrich", "11", "normal"), width=25)
        categoria.grid(row=3, column=0)
        categoria.focus()

        Label(panel_texto, text="Introduce una marca", bg="#e3f2b3", font=("Alrich", "11", "normal")).grid(row=2,
                                                                                                           column=1)
        marca = Entry(panel_texto, font=("Alrich", "11", "normal"), width=25)
        marca.grid(row=3, column=1)

        Label(panel_texto, text="Introduce un modelo", bg="#e3f2b3", font=("Alrich", "11", "normal")).grid(row=2,
                                                                                                           column=2)
        modelo = Entry(panel_texto, font=("Alrich", "11", "normal"), width=25)
        modelo.grid(row=3, column=2)

        # -------Botones----------------------------
        btOk = Button(bt_panel_texto, command=lambda: si(), text="Si", width=10)
        btOk.configure(bg="#969692", cursor='hand2', font=("Alrich", "11", "normal"))
        btOk.grid(row=1, column=0, padx=2, pady=3, sticky=W + E)

        btNo = Button(bt_panel_texto, command=window_modify.destroy, text="No", width=10, bg="yellow", cursor='hand2')
        btNo.configure(bg="#969692", cursor='hand2', font=("Alrich", "11", "normal"))
        btNo.grid(row=1, column=1, padx=2, pady=3, sticky=W + E)

        # ----Funciones de los botones-------

        def si():
            instrument = self.val_modify
            categoria_nueva = categoria.get()
            marca_nueva = marca.get()
            modelo_nuevo = modelo.get()
            a = modificar_instrumento(instrument)
            if a == True:
                _eliminar_antiguo(instrument[0])
                _agregar_nuevo(categoria_nueva, marca_nueva, modelo_nuevo)
            window_modify.destroy()

        def _agregar_nuevo(categoria, marca, modelo):
            g_categoria = categoria
            g_marca = marca
            g_modelo = modelo
            with open('Instrumentos.csv', 'a') as f:
                writer = csv.writer(f, lineterminator='\r', delimiter=',')
                writer.writerow((g_categoria, g_marca, g_modelo))

        def _eliminar_antiguo(categoria_antigua):
            categoria = categoria_antigua
            with open('Instrumentos.csv', 'r') as f:
                reader = list(csv.reader(f))
            with open('Instrumentos.csv', 'w') as f:
                writer = csv.writer(f, lineterminator='\r', delimiter=',')
                for i, row in enumerate(reader):
                    if categoria != row[0]:
                        writer.writerow(row)
