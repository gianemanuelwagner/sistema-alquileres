# Sistema de Alquileres - Flask

Un sistema completo de administración de alquileres desarrollado con Flask y Python. Permite gestionar propiedades, inquilinos y contratos de manera eficiente y profesional.

## 🚀 Características

- **Dashboard Interactivo**: Resumen general con estadísticas y actividad reciente
- **Gestión de Propiedades**: CRUD completo para propiedades con filtros y búsqueda
- **Gestión de Inquilinos**: Registro y administración de inquilinos
- **Gestión de Contratos**: Creación y seguimiento de contratos de alquiler
- **Interfaz Moderna**: Diseño responsive con Bootstrap 5 y CSS personalizado
- **Funcionalidades Avanzadas**: Búsqueda, filtros, exportación y validaciones
- **Base de Datos SQLite**: Fácil de configurar y mantener

## 📋 Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## 🛠️ Instalación

1. **Clona o descarga el proyecto**
   ```bash
   git clone <url-del-repositorio>
   cd alquileres
   ```

2. **Instala las dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecuta la aplicación**
   ```bash
   python app.py
   ```

4. **Abre tu navegador**
   ```
   http://localhost:5000
   ```

## 📁 Estructura del Proyecto

```
alquileres/
├── app.py                 # Aplicación principal Flask
├── requirements.txt       # Dependencias del proyecto
├── README.md             # Este archivo
├── alquileres.db         # Base de datos SQLite (se crea automáticamente)
├── templates/            # Plantillas HTML
│   ├── base.html         # Plantilla base
│   ├── index.html        # Dashboard principal
│   ├── propiedades.html  # Lista de propiedades
│   ├── nueva_propiedad.html
│   ├── editar_propiedad.html
│   ├── inquilinos.html   # Lista de inquilinos
│   ├── nuevo_inquilino.html
│   ├── editar_inquilino.html
│   ├── contratos.html    # Lista de contratos
│   └── nuevo_contrato.html
└── static/               # Archivos estáticos
    ├── css/
    │   └── style.css     # Estilos personalizados
    └── js/
        └── main.js       # JavaScript personalizado
```

## 🎯 Funcionalidades Principales

### Dashboard
- Estadísticas en tiempo real
- Actividad reciente
- Acciones rápidas
- Información del sistema

### Propiedades
- Lista con filtros y búsqueda
- Agregar nuevas propiedades
- Editar información existente
- Estados: disponible, alquilada, mantenimiento
- Características: tipo, habitaciones, baños, precio

### Inquilinos
- Registro completo de inquilinos
- Información de contacto
- DNI y datos personales
- Contacto de emergencia
- Documentación requerida

### Contratos
- Creación de contratos
- Selección de propiedad e inquilino
- Fechas de inicio y fin
- Precio mensual y depósito
- Estados: activo, vencido, cancelado
- Alertas de vencimiento

## 🎨 Características de la Interfaz

- **Diseño Responsive**: Funciona en desktop, tablet y móvil
- **Tema Moderno**: Gradientes, sombras y animaciones
- **Iconografía**: Bootstrap Icons para mejor UX
- **Validaciones**: Formularios con validación en tiempo real
- **Notificaciones**: Alertas y mensajes de confirmación
- **Accesibilidad**: Navegación por teclado y lectores de pantalla

## 🔧 Configuración Avanzada

### Variables de Entorno
Puedes configurar las siguientes variables:

```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
export SECRET_KEY=tu_clave_secreta_aqui
```

### Base de Datos
La aplicación usa SQLite por defecto. Para cambiar a otra base de datos:

1. Modifica la configuración en `app.py`
2. Actualiza las consultas SQL según sea necesario
3. Instala el driver correspondiente

## 📊 Base de Datos

### Tablas Principales

**propiedades**
- id, direccion, tipo, habitaciones, baños, precio, estado, fecha_creacion

**inquilinos**
- id, nombre, apellido, email, telefono, dni, fecha_creacion

**contratos**
- id, propiedad_id, inquilino_id, fecha_inicio, fecha_fin, precio_mensual, estado, fecha_creacion

## 🚀 Despliegue

### Desarrollo Local
```bash
python app.py
```

### Producción (Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker (opcional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 🔒 Seguridad

- Validación de formularios
- Sanitización de datos
- Protección CSRF (implementar según necesidades)
- Autenticación (agregar según requerimientos)

## 📈 Próximas Mejoras

- [ ] Sistema de autenticación
- [ ] Reportes y estadísticas avanzadas
- [ ] Notificaciones por email
- [ ] Subida de imágenes de propiedades
- [ ] API REST
- [ ] Aplicación móvil
- [ ] Integración con sistemas de pago
- [ ] Backup automático de base de datos

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte

Si tienes problemas o preguntas:

1. Revisa la documentación
2. Busca en los issues existentes
3. Crea un nuevo issue con detalles del problema

## 🙏 Agradecimientos

- Flask por el framework web
- Bootstrap por el framework CSS
- Bootstrap Icons por los iconos
- La comunidad de desarrolladores

---

**Desarrollado con ❤️ y Flask**
"# alquileres" 
