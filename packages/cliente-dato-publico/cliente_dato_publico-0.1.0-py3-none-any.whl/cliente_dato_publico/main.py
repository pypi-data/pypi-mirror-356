import requests
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from cliente_dato_publico.api_config import API_URL
from cliente_dato_publico.utils.exportador import exportar_csv, exportar_kml


def obtener_datos():
    try:
        resp = requests.get(API_URL)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        messagebox.showerror("Error", f"❌ Error conectando al API:\n{str(e)}")
        return []

def seleccionar_carpeta():
    carpeta = filedialog.askdirectory(title="Seleccione una carpeta para guardar")
    return carpeta

def exportar():
    root = tk.Tk()
    root.withdraw()  # Oculta ventana principal

    datos = obtener_datos()
    if not datos:
        messagebox.showinfo("Información", "No se encontraron datos.")
        return

    # Mostrar resumen de los primeros 5 datos
    resumen = f"🔍 Total de datos públicos: {len(datos)}\n"
    for d in datos[:5]:
        resumen += f"- DatoId: {d['DatoId']}, Especie: {d['EspeCod']}, Lat: {d['Latitud']}, Long: {d['Longitud']}\n"
    messagebox.showinfo("Resumen de datos", resumen)

    # Preguntar tipo de exportación
    opcion = simpledialog.askstring("Exportar", "Seleccione una opción:\n1. Exportar a CSV\n2. Exportar a KML")
    if opcion not in ["1", "2"]:
        messagebox.showerror("Error", "Opción no válida.")
        return

    # Seleccionar carpeta
    carpeta = seleccionar_carpeta()
    if not carpeta:
        messagebox.showwarning("Advertencia", "No se seleccionó ninguna carpeta.")
        return

    # Exportar
    if opcion == "1":
        exportar_csv(datos, carpeta)
    elif opcion == "2":
        exportar_kml(datos, carpeta)

if __name__ == "__main__":
    exportar()
