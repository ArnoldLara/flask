#permite representar archivos de plantilla HTML que existen en la carpeta templates
from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3
#Necesaria para devolver pagina 404 not found 
from werkzeug.exceptions import abort

#función que cree una conexión de base de datos y la devolverá
#la función devuelve el objeto de conexión conn que usará para acceder a la base de datos

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    #Conexión con la base de datos
    conn = get_db_connection()
    #Recuperar el dato con el id almacenado en post_id
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    #Cerrar conexión con base de datos
    conn.close()
    #Devolver 404 si no existe una entrada
    if post is None:
        #Responde con pagina de 404
        abort(404)
    return post

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

@app.route('/')
def index():
    #Abrir conexión con base de datos
    conn = get_db_connection()
    #consulta SQL para seleccionar todas las entradas de la tabla post
    posts = conn.execute('SELECT * FROM posts').fetchall()
    # Cierra la conexión con la base de datos
    conn.close()
    #Pasa la info de la base de datos a la plantilla HTML index
    return render_template('index.html', posts=posts)

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route('/create', methods=('GET', 'POST'))
def create():
    #Si es solicitud POST 
    if request.method == 'POST':
        # extrae el título enviado y el contenido desde el objeto request.form
        title = request.form['title']
        content = request.form['content']

        # Valida que el formulario tenga titulo
        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            # Confirma cambios en la base de datos
            conn.commit()
            conn.close()
            #redirige al cliente a la página de índice usando la función
            return redirect(url_for('index'))  

    return render_template('create.html')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))


# Para correr se deben usar los siguientes comandos:
# export FLASK_APP=main
# export FLASK_ENV=development
# flask run --host=0.0.0.0
