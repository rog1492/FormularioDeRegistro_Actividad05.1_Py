import os
import re
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

COLOR_FONDO = "#EAF2F8"
COLOR_PANEL = "#FFFFFF"
COLOR_PRIMARIO = "#2563A6"
COLOR_GUARDAR = "#218838"
COLOR_BORRAR = "#D9534F"
COLOR_TEXTO = "#263238"

FUENTE = ("Segoe UI", 11)
FUENTE_TITULO = ("Segoe UI", 19, "bold")
FUENTE_ETIQUETA = ("Segoe UI", 10, "bold")

CARPETA = Path.home() / "Documents" / "FormularioPython"
ARCHIVO = CARPETA / "FormularioPython.txt"

def esEnteroValido(valor):
    try:
        int(valor)
        return True
    except ValueError:
        return False

def esDecimalValido(valor):
    valor = valor.replace(",", ".")
    return bool(re.fullmatch(r"\d+(\.\d+)?", valor))

def esNumerode10digitos(valor):
    return bool(re.fullmatch(r"\d{10}", valor))

def esTextoValido(valor):
    valor = valor.strip()

    if not valor:
        return False

    palabras = valor.split()

    return all(
        all(caracter.isalpha() or caracter in "'’-" for caracter in palabra)
        for palabra in palabras
    )

def Limpiar_Campos():
    tbNombre.delete(0, tk.END)
    tbApellidos.delete(0, tk.END)
    tbTelefono.delete(0, tk.END)
    tbEdad.delete(0, tk.END)
    tbEstatura.delete(0, tk.END)
    var_genero.set(0)
    tbNombre.focus_set()

def guardar_Valores():
    nombre = tbNombre.get().strip()
    apellidos = tbApellidos.get().strip()
    edad = tbEdad.get().strip()
    estatura = tbEstatura.get().strip().replace(",", ".")
    telefono = tbTelefono.get().strip()
    genero_seleccionado = var_genero.get()

    if not all([nombre, apellidos, edad, estatura, telefono]):
        messagebox.showwarning(
            "Campos incompletos",
            "Por favor, completa todos los campos."
        )
        return

    if not esTextoValido(nombre) or not esTextoValido(apellidos):
        messagebox.showerror(
            "Datos incorrectos",
            "El nombre y los apellidos solo deben contener "
            "letras, espacios, apostrofes o guiones."
        )
        return

    if not esEnteroValido(edad):
        messagebox.showerror(
            "Edad incorrecta",
            "La edad debe ser un numero entero."
        )
        return

    edad_numero = int(edad)

    if edad_numero < 1 or edad_numero > 120:
        messagebox.showerror(
            "Edad fuera de rango",
            "La edad debe estar entre 1 y 120 años."
        )
        return

    if not esDecimalValido(estatura):
        messagebox.showerror(
            "Estatura incorrecta",
            "Ingresa una estatura valida en centimetros."
        )
        return

    estatura_numero = float(estatura)

    if not 30 <= estatura_numero <= 250:
        messagebox.showerror(
            "Estatura fuera de rango",
            "La estatura debe estar entre 30 y 250 cm."
        )
        return

    if not esNumerode10digitos(telefono):
        messagebox.showerror(
            "Telefono incorrecto",
            "El telefono debe contener exactamente 10 digitos."
        )
        return

    generos = {
        1: "Hombre",
        2: "Mujer",
        3: "Otro"
    }

    if genero_seleccionado not in generos:
        messagebox.showwarning(
            "Falta seleccionar",
            "Selecciona una opcion de genero."
        )
        return

    genero = generos[genero_seleccionado]

    datos = (
        f"Nombre: {nombre}\n"
        f"Apellidos: {apellidos}\n"
        f"Edad: {edad_numero} años\n"
        f"Estatura: {estatura_numero:g} cm\n"
        f"Telefono: {telefono}\n"
        f"Genero: {genero}\n"
        f"{'-' * 35}\n"
    )

    try:
        CARPETA.mkdir(parents=True, exist_ok=True)

        with open(ARCHIVO, "a", encoding="utf-8") as archivo:
            archivo.write(datos)

    except OSError as error:
        messagebox.showerror(
            "Error al guardar",
            f"No se pudieron guardar los datos.\n\n{error}"
        )
        return

    messagebox.showinfo(
        "Registro guardado",
        f"Los datos se guardaron correctamente.\n\n{datos}"
        f"\nArchivo:\n{ARCHIVO}"
    )

    Limpiar_Campos()

ventana = tk.Tk()
ventana.title("Formulario de Registro")
ventana.geometry("580x650")
ventana.minsize(520, 620)
ventana.configure(bg=COLOR_FONDO)

ventana.columnconfigure(0, weight=1)

encabezado = tk.Frame(
    ventana,
    bg=COLOR_PRIMARIO,
    padx=20,
    pady=16
)
encabezado.grid(row=0, column=0, sticky="ew")

tk.Label(
    encabezado,
    text="FORMULARIO DE REGISTRO",
    font=FUENTE_TITULO,
    fg="white",
    bg=COLOR_PRIMARIO
).pack()

tk.Label(
    encabezado,
    text="Ingresa los datos solicitados",
    font=("Segoe UI", 10),
    fg="#EAF2F8",
    bg=COLOR_PRIMARIO
).pack(pady=(4, 0))

panel = tk.Frame(
    ventana,
    bg=COLOR_PANEL,
    padx=30,
    pady=18
)
panel.grid(row=1, column=0, padx=25, pady=20, sticky="nsew")

panel.columnconfigure(0, weight=1)

var_genero = tk.IntVar(value=0)

def crear_campo(texto, fila):
    tk.Label(
        panel,
        text=texto,
        font=FUENTE_ETIQUETA,
        fg=COLOR_TEXTO,
        bg=COLOR_PANEL,
        anchor="w"
    ).grid(row=fila, column=0, sticky="ew", pady=(7, 3))

    entrada = tk.Entry(
        panel,
        font=FUENTE,
        relief="solid",
        bd=1
    )
    entrada.grid(row=fila + 1, column=0, sticky="ew", ipady=5)

    return entrada

tbNombre = crear_campo("Nombre(s):", 0)
tbApellidos = crear_campo("Apellidos:", 2)
tbTelefono = crear_campo("Telefono (10 digitos):", 4)
tbEdad = crear_campo("Edad:", 6)
tbEstatura = crear_campo("Estatura (cm):", 8)

tk.Label(
    panel,
    text="Genero:",
    font=FUENTE_ETIQUETA,
    fg=COLOR_TEXTO,
    bg=COLOR_PANEL,
    anchor="w"
).grid(row=10, column=0, sticky="ew", pady=(12, 5))

marco_genero = tk.Frame(panel, bg=COLOR_PANEL)
marco_genero.grid(row=11, column=0, sticky="w")

for texto, valor in [
    ("Hombre", 1),
    ("Mujer", 2),
    ("Otro", 3)
]:
    tk.Radiobutton(
        marco_genero,
        text=texto,
        variable=var_genero,
        value=valor,
        font=FUENTE,
        bg=COLOR_PANEL,
        activebackground=COLOR_PANEL
    ).pack(side="left", padx=(0, 12))

marco_botones = tk.Frame(panel, bg=COLOR_PANEL)
marco_botones.grid(row=12, column=0, sticky="ew", pady=(20, 0))

marco_botones.columnconfigure(0, weight=1)
marco_botones.columnconfigure(1, weight=1)

btnBorrar = tk.Button(
    marco_botones,
    text="Borrar campos",
    command=Limpiar_Campos,
    font=FUENTE,
    bg=COLOR_BORRAR,
    fg="white",
    activebackground="#C9302C",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    padx=10,
    pady=8
)
btnBorrar.grid(row=0, column=0, sticky="ew", padx=(0, 6))

btnGuardar = tk.Button(
    marco_botones,
    text="Guardar registro",
    command=guardar_Valores,
    font=("Segoe UI", 11, "bold"),
    bg=COLOR_GUARDAR,
    fg="white",
    activebackground="#19692C",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    padx=10,
    pady=8
)
btnGuardar.grid(row=0, column=1, sticky="ew", padx=(6, 0))

tk.Label(
    ventana,
    text="Los registros se guardan en un archivo de texto.",
    font=("Segoe UI", 9),
    fg="#526575",
    bg=COLOR_FONDO
).grid(row=2, column=0, pady=(0, 12))

ventana.bind("<Return>", lambda evento: guardar_Valores())
tbNombre.focus_set()
ventana.mainloop()