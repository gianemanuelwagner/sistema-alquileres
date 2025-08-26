from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import sqlite3
from datetime import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'tu_clave_secreta_aqui')

# Configuración de la base de datos
DATABASE = 'alquileres.db'

def init_db():
    """Inicializar la base de datos"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Tabla de paquetes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS paquetes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            max_propiedades INTEGER NOT NULL,
            max_inquilinos INTEGER NOT NULL,
            max_contratos INTEGER NOT NULL,
            precio DECIMAL(10,2) NOT NULL,
            descripcion TEXT,
            activo BOOLEAN DEFAULT 1
        )
    ''')
    
    # Tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            paquete_id INTEGER,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ultimo_acceso TIMESTAMP,
            activo BOOLEAN DEFAULT 1,
            es_admin BOOLEAN DEFAULT 0,
            FOREIGN KEY (paquete_id) REFERENCES paquetes (id)
        )
    ''')
    
    # Tabla de propiedades (agregar user_id)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS propiedades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            direccion TEXT NOT NULL,
            tipo TEXT NOT NULL,
            habitaciones INTEGER,
            baños INTEGER,
            precio DECIMAL(10,2),
            estado TEXT DEFAULT 'disponible',
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES usuarios (id)
        )
    ''')
    
    # Tabla de inquilinos (agregar user_id)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inquilinos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            email TEXT,
            telefono TEXT,
            dni TEXT,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES usuarios (id)
        )
    ''')
    
    # Tabla de contratos (agregar user_id)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contratos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            propiedad_id INTEGER,
            inquilino_id INTEGER,
            fecha_inicio DATE,
            fecha_fin DATE,
            precio_mensual DECIMAL(10,2),
            estado TEXT DEFAULT 'activo',
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES usuarios (id),
            FOREIGN KEY (propiedad_id) REFERENCES propiedades (id),
            FOREIGN KEY (inquilino_id) REFERENCES inquilinos (id)
        )
    ''')
    
    # Insertar paquetes por defecto
    cursor.execute('''
        INSERT OR IGNORE INTO paquetes (id, nombre, max_propiedades, max_inquilinos, max_contratos, precio, descripcion)
        VALUES 
        (1, 'Básico', 5, 10, 15, 0.00, 'Ideal para comenzar. Hasta 5 propiedades, 10 inquilinos y 15 contratos.'),
        (2, 'Profesional', 20, 50, 100, 29.99, 'Para profesionales. Hasta 20 propiedades, 50 inquilinos y 100 contratos.'),
        (3, 'Empresarial', 100, 250, 500, 99.99, 'Para empresas. Hasta 100 propiedades, 250 inquilinos y 500 contratos.')
    ''')
    
    # Crear usuario admin por defecto
    admin_password = generate_password_hash('admin123')
    cursor.execute('''
        INSERT OR IGNORE INTO usuarios (id, username, email, password_hash, nombre, apellido, paquete_id, es_admin)
        VALUES (1, 'admin', 'admin@alquileres.com', ?, 'Administrador', 'Sistema', 3, 1)
    ''', (admin_password,))
    
    conn.commit()
    conn.close()

def get_db_connection():
    """Obtener conexión a la base de datos"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    """Decorador para requerir login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión para acceder a esta página.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorador para requerir permisos de admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión para acceder a esta página.', 'warning')
            return redirect(url_for('login'))
        
        conn = get_db_connection()
        user = conn.execute('SELECT es_admin FROM usuarios WHERE id = ?', (session['user_id'],)).fetchone()
        conn.close()
        
        if not user or not user['es_admin']:
            flash('No tienes permisos para acceder a esta página.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def check_limits(user_id, tipo):
    """Verificar límites del paquete del usuario"""
    conn = get_db_connection()
    
    # Obtener información del usuario y su paquete
    user_info = conn.execute('''
        SELECT u.id, p.max_propiedades, p.max_inquilinos, p.max_contratos
        FROM usuarios u
        JOIN paquetes p ON u.paquete_id = p.id
        WHERE u.id = ?
    ''', (user_id,)).fetchone()
    
    if not user_info:
        conn.close()
        return False, "Usuario no encontrado"
    
    # Contar elementos actuales
    if tipo == 'propiedades':
        current_count = conn.execute('SELECT COUNT(*) FROM propiedades WHERE user_id = ?', (user_id,)).fetchone()[0]
        max_count = user_info['max_propiedades']
    elif tipo == 'inquilinos':
        current_count = conn.execute('SELECT COUNT(*) FROM inquilinos WHERE user_id = ?', (user_id,)).fetchone()[0]
        max_count = user_info['max_inquilinos']
    elif tipo == 'contratos':
        current_count = conn.execute('SELECT COUNT(*) FROM contratos WHERE user_id = ?', (user_id,)).fetchone()[0]
        max_count = user_info['max_contratos']
    else:
        conn.close()
        return False, "Tipo no válido"
    
    conn.close()
    
    if current_count >= max_count:
        return False, f"Has alcanzado el límite de {tipo} para tu paquete ({max_count})"
    
    return True, f"Puedes agregar {max_count - current_count} {tipo} más"

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM usuarios WHERE username = ? AND activo = 1', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['nombre'] = user['nombre']
            session['es_admin'] = user['es_admin']
            
            # Actualizar último acceso
            conn = get_db_connection()
            conn.execute('UPDATE usuarios SET ultimo_acceso = CURRENT_TIMESTAMP WHERE id = ?', (user['id'],))
            conn.commit()
            conn.close()
            
            flash(f'¡Bienvenido, {user["nombre"]}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Cerrar sesión"""
    session.clear()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Página de registro"""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        paquete_id = request.form['paquete_id']
        
        if password != confirm_password:
            flash('Las contraseñas no coinciden.', 'danger')
            return render_template('register.html')
        
        conn = get_db_connection()
        
        # Verificar si el usuario ya existe
        existing_user = conn.execute('SELECT id FROM usuarios WHERE username = ? OR email = ?', (username, email)).fetchone()
        if existing_user:
            flash('El usuario o email ya existe.', 'danger')
            conn.close()
            return render_template('register.html')
        
        # Crear nuevo usuario
        password_hash = generate_password_hash(password)
        conn.execute('''
            INSERT INTO usuarios (username, email, password_hash, nombre, apellido, paquete_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (username, email, password_hash, nombre, apellido, paquete_id))
        conn.commit()
        conn.close()
        
        flash('Usuario registrado correctamente. Puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))
    
    # Obtener paquetes disponibles
    conn = get_db_connection()
    paquetes = conn.execute('SELECT * FROM paquetes WHERE activo = 1').fetchall()
    conn.close()
    
    return render_template('register.html', paquetes=paquetes)

@app.route('/')
@login_required
def index():
    """Página principal con dashboard"""
    conn = get_db_connection()
    
    # Estadísticas básicas del usuario
    total_propiedades = conn.execute('SELECT COUNT(*) FROM propiedades WHERE user_id = ?', (session['user_id'],)).fetchone()[0]
    propiedades_disponibles = conn.execute('SELECT COUNT(*) FROM propiedades WHERE user_id = ? AND estado = "disponible"', (session['user_id'],)).fetchone()[0]
    total_inquilinos = conn.execute('SELECT COUNT(*) FROM inquilinos WHERE user_id = ?', (session['user_id'],)).fetchone()[0]
    contratos_activos = conn.execute('SELECT COUNT(*) FROM contratos WHERE user_id = ? AND estado = "activo"', (session['user_id'],)).fetchone()[0]
    
    # Propiedades recientes
    propiedades_recientes = conn.execute('''
        SELECT * FROM propiedades 
        WHERE user_id = ?
        ORDER BY fecha_creacion DESC 
        LIMIT 5
    ''', (session['user_id'],)).fetchall()
    
    # Contratos recientes
    contratos_recientes = conn.execute('''
        SELECT c.*, p.direccion, i.nombre, i.apellido 
        FROM contratos c
        JOIN propiedades p ON c.propiedad_id = p.id
        JOIN inquilinos i ON c.inquilino_id = i.id
        WHERE c.user_id = ?
        ORDER BY c.fecha_creacion DESC 
        LIMIT 5
    ''', (session['user_id'],)).fetchall()
    
    # Información del paquete del usuario
    user_info = conn.execute('''
        SELECT u.*, p.nombre as paquete_nombre, p.max_propiedades, p.max_inquilinos, p.max_contratos, p.precio as paquete_precio
        FROM usuarios u
        JOIN paquetes p ON u.paquete_id = p.id
        WHERE u.id = ?
    ''', (session['user_id'],)).fetchone()
    
    conn.close()
    
    return render_template('index.html', 
                         total_propiedades=total_propiedades,
                         propiedades_disponibles=propiedades_disponibles,
                         total_inquilinos=total_inquilinos,
                         contratos_activos=contratos_activos,
                         propiedades_recientes=propiedades_recientes,
                         contratos_recientes=contratos_recientes,
                         user_info=user_info)

# Rutas para propiedades
@app.route('/propiedades')
@login_required
def propiedades():
    """Lista de propiedades"""
    conn = get_db_connection()
    propiedades = conn.execute('SELECT * FROM propiedades WHERE user_id = ? ORDER BY fecha_creacion DESC', (session['user_id'],)).fetchall()
    conn.close()
    return render_template('propiedades.html', propiedades=propiedades)

@app.route('/propiedades/nueva', methods=['GET', 'POST'])
@login_required
def nueva_propiedad():
    """Crear nueva propiedad"""
    # Verificar límites del paquete
    can_add, message = check_limits(session['user_id'], 'propiedades')
    if not can_add:
        flash(message, 'warning')
        return redirect(url_for('propiedades'))
    
    if request.method == 'POST':
        try:
            direccion = request.form['direccion']
            tipo = request.form['tipo']
            habitaciones = request.form['habitaciones']
            baños = request.form['baños']
            precio = request.form['precio']
            
            # Validar datos requeridos
            if not direccion or not tipo or not precio:
                flash('Por favor completa todos los campos requeridos.', 'danger')
                return render_template('nueva_propiedad.html')
            
            conn = get_db_connection()
            conn.execute('''
                INSERT INTO propiedades (user_id, direccion, tipo, habitaciones, baños, precio)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (session['user_id'], direccion, tipo, habitaciones, baños, precio))
            conn.commit()
            conn.close()
            
            flash('Propiedad creada exitosamente', 'success')
            return redirect(url_for('propiedades'))
        except Exception as e:
            print(f"Error al crear propiedad: {e}")
            flash('Error al crear la propiedad. Por favor intenta nuevamente.', 'danger')
            return render_template('nueva_propiedad.html')
    
    return render_template('nueva_propiedad.html')

@app.route('/propiedades/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_propiedad(id):
    """Editar propiedad"""
    conn = get_db_connection()
    
    if request.method == 'POST':
        direccion = request.form['direccion']
        tipo = request.form['tipo']
        habitaciones = request.form['habitaciones']
        baños = request.form['baños']
        precio = request.form['precio']
        estado = request.form['estado']
        
        conn.execute('''
            UPDATE propiedades 
            SET direccion = ?, tipo = ?, habitaciones = ?, baños = ?, precio = ?, estado = ?
            WHERE id = ? AND user_id = ?
        ''', (direccion, tipo, habitaciones, baños, precio, estado, id, session['user_id']))
        conn.commit()
        conn.close()
        
        flash('Propiedad actualizada exitosamente', 'success')
        return redirect(url_for('propiedades'))
    
    propiedad = conn.execute('SELECT * FROM propiedades WHERE id = ? AND user_id = ?', (id, session['user_id'])).fetchone()
    conn.close()
    
    if propiedad is None:
        flash('Propiedad no encontrada', 'error')
        return redirect(url_for('propiedades'))
    
    return render_template('editar_propiedad.html', propiedad=propiedad)

@app.route('/propiedades/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_propiedad(id):
    """Eliminar propiedad"""
    conn = get_db_connection()
    conn.execute('DELETE FROM propiedades WHERE id = ? AND user_id = ?', (id, session['user_id']))
    conn.commit()
    conn.close()
    
    flash('Propiedad eliminada exitosamente', 'success')
    return redirect(url_for('propiedades'))

# Rutas para inquilinos
@app.route('/inquilinos')
@login_required
def inquilinos():
    """Lista de inquilinos"""
    conn = get_db_connection()
    inquilinos = conn.execute('SELECT * FROM inquilinos WHERE user_id = ? ORDER BY fecha_creacion DESC', (session['user_id'],)).fetchall()
    conn.close()
    return render_template('inquilinos.html', inquilinos=inquilinos)

@app.route('/inquilinos/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_inquilino():
    """Crear nuevo inquilino"""
    # Verificar límites del paquete
    can_add, message = check_limits(session['user_id'], 'inquilinos')
    if not can_add:
        flash(message, 'warning')
        return redirect(url_for('inquilinos'))
    
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            email = request.form['email']
            telefono = request.form['telefono']
            dni = request.form['dni']
            
            # Validar datos requeridos
            if not nombre or not apellido or not dni:
                flash('Por favor completa todos los campos requeridos.', 'danger')
                return render_template('nuevo_inquilino.html')
            
            conn = get_db_connection()
            conn.execute('''
                INSERT INTO inquilinos (user_id, nombre, apellido, email, telefono, dni)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (session['user_id'], nombre, apellido, email, telefono, dni))
            conn.commit()
            conn.close()
            
            flash('Inquilino creado exitosamente', 'success')
            return redirect(url_for('inquilinos'))
        except Exception as e:
            print(f"Error al crear inquilino: {e}")
            flash('Error al crear el inquilino. Por favor intenta nuevamente.', 'danger')
            return render_template('nuevo_inquilino.html')
    
    return render_template('nuevo_inquilino.html')

@app.route('/inquilinos/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_inquilino(id):
    """Editar inquilino"""
    conn = get_db_connection()
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        telefono = request.form['telefono']
        dni = request.form['dni']
        
        conn.execute('''
            UPDATE inquilinos 
            SET nombre = ?, apellido = ?, email = ?, telefono = ?, dni = ?
            WHERE id = ? AND user_id = ?
        ''', (nombre, apellido, email, telefono, dni, id, session['user_id']))
        conn.commit()
        conn.close()
        
        flash('Inquilino actualizado exitosamente', 'success')
        return redirect(url_for('inquilinos'))
    
    inquilino = conn.execute('SELECT * FROM inquilinos WHERE id = ? AND user_id = ?', (id, session['user_id'])).fetchone()
    conn.close()
    
    if inquilino is None:
        flash('Inquilino no encontrado', 'error')
        return redirect(url_for('inquilinos'))
    
    return render_template('editar_inquilino.html', inquilino=inquilino)

@app.route('/inquilinos/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_inquilino(id):
    """Eliminar inquilino"""
    conn = get_db_connection()
    conn.execute('DELETE FROM inquilinos WHERE id = ? AND user_id = ?', (id, session['user_id']))
    conn.commit()
    conn.close()
    
    flash('Inquilino eliminado exitosamente', 'success')
    return redirect(url_for('inquilinos'))

# Rutas para contratos
@app.route('/contratos')
@login_required
def contratos():
    """Lista de contratos"""
    conn = get_db_connection()
    contratos = conn.execute('''
        SELECT c.*, p.direccion, i.nombre, i.apellido 
        FROM contratos c
        JOIN propiedades p ON c.propiedad_id = p.id
        JOIN inquilinos i ON c.inquilino_id = i.id
        WHERE c.user_id = ?
        ORDER BY c.fecha_creacion DESC
    ''', (session['user_id'],)).fetchall()
    conn.close()
    return render_template('contratos.html', contratos=contratos)

@app.route('/contratos/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_contrato():
    """Crear nuevo contrato"""
    # Verificar límites del paquete
    can_add, message = check_limits(session['user_id'], 'contratos')
    if not can_add:
        flash(message, 'warning')
        return redirect(url_for('contratos'))
    
    conn = get_db_connection()
    
    if request.method == 'POST':
        try:
            propiedad_id = request.form['propiedad_id']
            inquilino_id = request.form['inquilino_id']
            fecha_inicio = request.form['fecha_inicio']
            fecha_fin = request.form['fecha_fin']
            precio_mensual = request.form['precio_mensual']
            
            # Validar datos requeridos
            if not propiedad_id or not inquilino_id or not fecha_inicio or not fecha_fin or not precio_mensual:
                flash('Por favor completa todos los campos requeridos.', 'danger')
                return render_template('nuevo_contrato.html', propiedades=propiedades, inquilinos=inquilinos)
            
            conn.execute('''
                INSERT INTO contratos (user_id, propiedad_id, inquilino_id, fecha_inicio, fecha_fin, precio_mensual)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (session['user_id'], propiedad_id, inquilino_id, fecha_inicio, fecha_fin, precio_mensual))
            
            # Actualizar estado de la propiedad
            conn.execute('UPDATE propiedades SET estado = "alquilada" WHERE id = ? AND user_id = ?', (propiedad_id, session['user_id']))
            
            conn.commit()
            conn.close()
            
            flash('Contrato creado exitosamente', 'success')
            return redirect(url_for('contratos'))
        except Exception as e:
            print(f"Error al crear contrato: {e}")
            flash('Error al crear el contrato. Por favor intenta nuevamente.', 'danger')
            return render_template('nuevo_contrato.html', propiedades=propiedades, inquilinos=inquilinos)
    
    propiedades = conn.execute('SELECT * FROM propiedades WHERE estado = "disponible" AND user_id = ?', (session['user_id'],)).fetchall()
    inquilinos = conn.execute('SELECT * FROM inquilinos WHERE user_id = ?', (session['user_id'],)).fetchall()
    conn.close()
    
    return render_template('nuevo_contrato.html', propiedades=propiedades, inquilinos=inquilinos)

@app.route('/contratos/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_contrato(id):
    """Editar contrato"""
    conn = get_db_connection()
    
    if request.method == 'POST':
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']
        precio_mensual = request.form['precio_mensual']
        estado = request.form['estado']
        
        conn.execute('''
            UPDATE contratos 
            SET fecha_inicio = ?, fecha_fin = ?, precio_mensual = ?, estado = ?
            WHERE id = ? AND user_id = ?
        ''', (fecha_inicio, fecha_fin, precio_mensual, estado, id, session['user_id']))
        conn.commit()
        conn.close()
        
        flash('Contrato actualizado exitosamente', 'success')
        return redirect(url_for('contratos'))
    
    contrato = conn.execute('''
        SELECT c.*, p.direccion, i.nombre, i.apellido 
        FROM contratos c
        JOIN propiedades p ON c.propiedad_id = p.id
        JOIN inquilinos i ON c.inquilino_id = i.id
        WHERE c.id = ? AND c.user_id = ?
    ''', (id, session['user_id'])).fetchone()
    
    propiedades = conn.execute('SELECT * FROM propiedades WHERE user_id = ?', (session['user_id'],)).fetchall()
    inquilinos = conn.execute('SELECT * FROM inquilinos WHERE user_id = ?', (session['user_id'],)).fetchall()
    conn.close()
    
    if contrato is None:
        flash('Contrato no encontrado', 'error')
        return redirect(url_for('contratos'))
    
    return render_template('editar_contrato.html', contrato=contrato, propiedades=propiedades, inquilinos=inquilinos)

@app.route('/contratos/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_contrato(id):
    """Eliminar contrato"""
    conn = get_db_connection()
    
    # Obtener información del contrato antes de eliminarlo
    contrato = conn.execute('SELECT propiedad_id FROM contratos WHERE id = ? AND user_id = ?', (id, session['user_id'])).fetchone()
    
    conn.execute('DELETE FROM contratos WHERE id = ? AND user_id = ?', (id, session['user_id']))
    
    # Actualizar estado de la propiedad si existe
    if contrato:
        conn.execute('UPDATE propiedades SET estado = "disponible" WHERE id = ? AND user_id = ?', (contrato['propiedad_id'], session['user_id']))
    
    conn.commit()
    conn.close()
    
    flash('Contrato eliminado exitosamente', 'success')
    return redirect(url_for('contratos'))

if __name__ == '__main__':
    init_db()
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
