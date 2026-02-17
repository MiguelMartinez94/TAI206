from flask import Flask, render_template, request, jsonify
import requests
app = Flask(__name__)

@app.route('/')
def usuarios():
    respuesta = requests.get('http://127.0.0.1:8000/v1/usuarios/')
    usuarios = respuesta.json()
    
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/agregar', methods = ['POST'])
def agregar():
    id = request.form.get('id','').strip()
    nombre = request.form.get('nombre', '').strip()
    edad = request.form.get('edad', '').strip()
    
    
    usuario = {
        "id":id,
        "nombre":nombre,
        "edad":edad
    }
    
    respuesta = requests.post('http://127.0.0.1:8000/v1/usuarios/', json=usuario)
    
    
    return render_template('usuarios.html', respuesta=respuesta)

@app.route('/actualizar/{{id}}')
def actualizar(id: int):
    
    
    datos = requests.get('http://127.0.0.1:8000/v1/usuarios/')
    
    usuario = datos.json()
    
    if usuario['id'] == id:
    
        render_template('actualizar.html', usuario=usuario)
        
    return render_template('usuarios.html')        
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)