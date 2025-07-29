import csv
import simplekml
import os

def exportar_csv(datos, carpeta_destino):
    archivo = os.path.join(carpeta_destino, "datos_publicos.csv")
    with open(archivo, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=datos[0].keys())
        writer.writeheader()
        writer.writerows(datos)
    print(f"✅ CSV exportado: {archivo}")

def exportar_kml(datos, carpeta_destino):
    kml = simplekml.Kml()
    for d in datos:
        kml.newpoint(name=str(d["DatoId"]), coords=[(float(d["Longitud"]), float(d["Latitud"]))])
    archivo = os.path.join(carpeta_destino, "datos_publicos.kml")
    kml.save(archivo)
    print(f"✅ KML exportado: {archivo}")
