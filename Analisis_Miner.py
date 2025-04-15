import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('agg')
from io import BytesIO
import base64


def numero_ingresar():      #**
    # Solicitar al usuario que ingrese un número
    Numero_fila = input("Por favor, ingresa un número: ")

    # Convertir el valor ingresado a un número entero (si es necesario)
    try:
        Numero_fila = int(Numero_fila)
        print("Número ingresado:", Numero_fila)
    except ValueError:
        print("Por favor, asegúrate de ingresar un número válido.")
    return Numero_fila

def preparar_datos(Numero_fila):
    # Intenta leer el archivo CSV con diferentes encodings
    encodings = ['latin1', 'ISO-8859-1', 'cp1252']
    for encoding in encodings:
        #try:
            df = pd.read_csv("./data/Toneladas.csv", encoding=encoding, delimiter=';')
            
            nombre_empresa = df.loc[Numero_fila,'Empresa/Anio']
            # Se convierten los datos de las columnas a datos numéricos
            for column in df.columns:
              df[column] = pd.to_numeric(df[column], errors='coerce')

            return df,nombre_empresa
            #except UnicodeDecodeError:
            #print("No se pudo leer el archivo CSV con encoding:", encoding)
           

def Promedio(df, Numero_fila):
    # Se calcula el promedio de toneladas de la fila seleccionada
    promedio_toneladas = df.iloc[Numero_fila].mean()
    return promedio_toneladas

def graficar_datos(fila_numerica, nombre_empresa):
    # Convertir los datos a tipos numéricos
    fila_numerica = pd.to_numeric(fila_numerica, errors='coerce')

    # Limpieza de los valores en blanco
    fila_numerica = fila_numerica.dropna()

    # Graficar los datos convertidos
    fila_numerica.plot(kind='line', marker='o', figsize=(15, 6), title=nombre_empresa)
    plt.ylabel('Toneladas de cobre')
    plt.xlabel('Produccion en el tiempo')
    plt.xticks(range(len(fila_numerica.index)), fila_numerica.index)

    # Convertir el gráfico a una imagen codificada en base64
    img_data = BytesIO()
    plt.savefig(img_data, format='png')
    img_data.seek(0)
    encoded_img = base64.b64encode(img_data.getvalue()).decode()

    # Limpiar la figura para que no se superpongan los gráficos
    plt.clf()

    return encoded_img


def main():

    # Se solicita al usuario que ingrese un número
    Numero_fila = numero_ingresar()

    # Se preparan los datos del archivo CSV
    df,nombre_empresa = preparar_datos(Numero_fila)
   

    if df is None:
        return

    # Se procesan los datos y se obtiene el promedio y el nombre de la empresa
    promedio= Promedio(df, Numero_fila)


    # Se imprime el promedio de la empresa seleccionada
    print("Promedio de producción de", nombre_empresa, "en [1998-2019] es", promedio, "Toneladas")

    # Se grafican los datos
    graficar_datos(df.iloc[Numero_fila], nombre_empresa)

if __name__ == "__main__":
    main()
