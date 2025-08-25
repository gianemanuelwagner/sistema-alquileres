# Sistema de Gestión de Alquileres

Una aplicación web completa para la gestión de propiedades, inquilinos y contratos de alquiler.

## 🚀 Características

- **Gestión de Propiedades**: Agregar, editar y eliminar propiedades
- **Gestión de Inquilinos**: Administrar información de inquilinos
- **Gestión de Contratos**: Crear y gestionar contratos de alquiler
- **Sistema de Usuarios**: Autenticación y autorización
- **Dashboard**: Vista general con estadísticas
- **Sistema de Paquetes**: Diferentes niveles de servicio
- **Interfaz Responsiva**: Diseño moderno y adaptable

## 🛠️ Tecnologías Utilizadas

- **Backend**: Python Flask
- **Base de Datos**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Autenticación**: Werkzeug Security
- **UI Framework**: Bootstrap

## 📋 Requisitos

- Python 3.7+
- pip (gestor de paquetes de Python)

## 🔧 Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/sistema-alquileres.git
   cd sistema-alquileres
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar la aplicación**
   ```bash
   python app.py
   ```

4. **Acceder a la aplicación**
   - Abrir navegador en: `http://localhost:5000`
   - Usuario por defecto: `admin`
   - Contraseña por defecto: `admin123`

## 📊 Estructura del Proyecto

```
sistema-alquileres/
├── app.py                 # Aplicación principal Flask
├── requirements.txt       # Dependencias de Python
├── README.md             # Documentación
├── static/               # Archivos estáticos
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
└── templates/            # Plantillas HTML
    ├── base.html
    ├── index.html
    ├── login.html
    ├── register.html
    ├── propiedades.html
    ├── inquilinos.html
    ├── contratos.html
    └── ...
```

## 🗄️ Base de Datos

La aplicación utiliza SQLite con las siguientes tablas principales:

- **usuarios**: Información de usuarios del sistema
- **paquetes**: Diferentes niveles de servicio
- **propiedades**: Información de propiedades
- **inquilinos**: Datos de inquilinos
- **contratos**: Contratos de alquiler

## 🔐 Sistema de Autenticación

- Registro de nuevos usuarios
- Inicio de sesión seguro
- Protección de rutas
- Gestión de sesiones

## 📱 Funcionalidades Principales

### Dashboard
- Estadísticas generales
- Propiedades recientes
- Contratos activos
- Información del paquete

### Gestión de Propiedades
- Agregar nuevas propiedades
- Editar información existente
- Cambiar estado (disponible/alquilada)
- Eliminar propiedades

### Gestión de Inquilinos
- Registrar nuevos inquilinos
- Actualizar información personal
- Historial de inquilinos

### Gestión de Contratos
- Crear nuevos contratos
- Definir fechas de inicio y fin
- Establecer precios mensuales
- Gestionar estados de contratos

## 🎨 Interfaz de Usuario

- Diseño responsive
- Navegación intuitiva
- Formularios validados
- Mensajes de confirmación
- Alertas de error

## 🔧 Configuración

### Variables de Entorno
```bash
# Clave secreta para sesiones (cambiar en producción)
SECRET_KEY=tu_clave_secreta_aqui
```

### Base de Datos
La base de datos se crea automáticamente al ejecutar la aplicación por primera vez.

## 🚀 Despliegue

### Desarrollo Local
```bash
python app.py
```

### Producción
Para producción, se recomienda usar un servidor WSGI como Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## 📝 Licencia

Este proyecto está bajo la Licencia MIT.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o pull request.

## 📞 Soporte

Para soporte técnico, contacta a través de los issues del repositorio.

---

**Desarrollado con ❤️ para la gestión eficiente de alquileres** 
