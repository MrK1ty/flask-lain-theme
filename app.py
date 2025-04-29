from flask import Flask, render_template, request, flash, redirect
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necesario para mostrar mensajes flash
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Crear la carpeta de uploads si no existe
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No se encontró ningún archivo')
        return redirect('/')
    
    file = request.files['file']
    if file.filename == '':
        flash('No seleccionaste ningún archivo')
        return redirect('/')
    
    if not file.filename.lower().endswith('.csv'):
        flash('El archivo debe ser un CSV')
        return redirect('/')

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        try:
            df = pd.read_csv(filepath)
        except Exception as e:
            flash(f'Error al leer el archivo: {str(e)}')
            return redirect('/')

        if df.shape[1] < 2:
            flash('El archivo CSV debe tener al menos dos columnas (ej: Nombre, Valor)')
            return redirect('/')

        labels = df.iloc[:, 0].tolist()  # Primera columna
        values = df.iloc[:, 1].tolist()  # Segunda columna

        return render_template('index.html', labels=labels, values=values)

if __name__ == '__main__':
    app.run(debug=True)