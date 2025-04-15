from flask import Flask, render_template
from flask import request  #Contiene toda la data enviada por el usuario
import pandas as pd
import Analisis_Miner as f
import matplotlib
matplotlib.use('agg')

app = Flask(__name__)

# Variable global para almacenar el número de usuario
numero_usuario_global = None


@app.route('/')  #Esto se ejecuta en la URL principal, ruta principal
def index(): #Nombre de la vista 
    return render_template('index.html') #Ingresa al archivo HTML para mostrar

#Ruta de tipo POST que recibe datos del usuario para guardar el dato entregado por el usuario y guardarlo
#Ademas muestra el promedio total recibido 
@app.route('/procesar', methods=['POST'])
def procesar():
    global numero_usuario_global
    try:
        numero_usuario = request.form['numero_usuario']
        if not numero_usuario:
            raise ValueError('El campo número de usuario está vacío.')  #Arreglar caso, que muestre una alerta de datos 
        
        numero_usuario = int(numero_usuario)
        df, nombre_empresa = f.preparar_datos(numero_usuario)
        prom = f.Promedio(df,numero_usuario)
        img = f.graficar_datos(df.iloc[numero_usuario], nombre_empresa)
        # Almacena el número de usuario en la variable global
        numero_usuario_global = numero_usuario
        return render_template('index.html', img=img, prom=prom)
    except ValueError as e:
        return render_template('error.html', error=str(e))


    
if __name__ == '__main__':
    app.run()

#Activar el debugger de la consola.