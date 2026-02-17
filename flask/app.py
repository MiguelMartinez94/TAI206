from flask import Flask, render_template, request, jsonify, redirect, url_for
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

@app.route('/actualizar/<int:id>')
def actualizar(id):
    
    
    datos = requests.get('http://127.0.0.1:8000/v1/usuarios/')
    
    usuario = datos.json()
    
    usuario_encontrado = None
    for u in usuario:
        if u['id'] == id:
            usuario_encontrado = u
            
    if usuario_encontrado:
        return render_template('actualizar.html', usuario=usuario_encontrado)
    else:
        return "Usuario no encontrado", 404
        
@app.route('/update', methods = ['POST'])
def updateUsuario():
    id_usuario = request.form.get('id', '').strip()
    
    datos = {
        "nombre": request.form.get('nombre', '').strip(),
        "edad": request.form.get('edad', '').strip()
    }
    
    url_update = f"http://127.0.0.1:8000/v1/usuarios/{id_usuario}"
    requests.put(url_update, json=datos)
    
    return redirect(url_for('usuarios'))

@app.route('/eliminar/<int:id>', methods= ['POST'])
def eliminar(id):
    url_delete = f"http://127.0.0.1:8000/v1/usuarios/{id}"
    requests.delete(url_delete)
    
    return redirect(url_for('usuarios'))
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)