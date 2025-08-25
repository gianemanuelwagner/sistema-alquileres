# Desplegar en Render

## Pasos para desplegar tu aplicación Flask en Render

### 1. Preparación del proyecto

Tu proyecto ya está configurado con los archivos necesarios:
- ✅ `requirements.txt` (con gunicorn agregado)
- ✅ `render.yaml` (configuración de Render)
- ✅ `app.py` (configurado para producción)

### 2. Crear cuenta en Render

1. Ve a [render.com](https://render.com)
2. Crea una cuenta gratuita
3. Conecta tu cuenta de GitHub

### 3. Desplegar la aplicación

#### Opción A: Usando render.yaml (Recomendado)

1. **Sube tu código a GitHub** (si no lo has hecho ya):
   ```bash
   git add .
   git commit -m "Configuración para Render"
   git push origin main
   ```

2. **En Render Dashboard**:
   - Haz clic en "New +"
   - Selecciona "Blueprint"
   - Conecta tu repositorio de GitHub
   - Render detectará automáticamente el archivo `render.yaml`
   - Haz clic en "Apply"

#### Opción B: Configuración manual

1. **En Render Dashboard**:
   - Haz clic en "New +"
   - Selecciona "Web Service"
   - Conecta tu repositorio de GitHub
   - Selecciona el repositorio

2. **Configuración del servicio**:
   - **Name**: `alquileres-app` (o el nombre que prefieras)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free

3. **Variables de entorno** (opcional):
   - `SECRET_KEY`: Una clave secreta segura para Flask
   - `PYTHON_VERSION`: `3.9.16`

### 4. Configuración de la base de datos

**IMPORTANTE**: Tu aplicación usa SQLite local. Para producción, considera:

1. **Usar PostgreSQL** (recomendado para Render):
   - En Render, crea un nuevo servicio "PostgreSQL"
   - Modifica tu código para usar PostgreSQL en lugar de SQLite

2. **O mantener SQLite** (para desarrollo/pruebas):
   - La base de datos se reiniciará cada vez que se despliegue
   - No es recomendable para producción

### 5. Verificar el despliegue

1. Una vez desplegado, Render te dará una URL como:
   `https://tu-app.onrender.com`

2. Tu aplicación estará disponible en esa URL

### 6. Configuración adicional

#### Variables de entorno recomendadas:
```
SECRET_KEY=tu_clave_secreta_muy_segura_aqui
FLASK_ENV=production
```

#### Dominio personalizado (opcional):
- En la configuración del servicio, puedes agregar un dominio personalizado

### 7. Monitoreo

- Render proporciona logs en tiempo real
- Puedes ver el estado de tu aplicación en el dashboard
- Configura alertas si es necesario

### 8. Actualizaciones

Para actualizar tu aplicación:
1. Haz cambios en tu código
2. Haz commit y push a GitHub
3. Render automáticamente detectará los cambios y redeployará

### Notas importantes:

- **Plan gratuito**: Tiene limitaciones de tiempo de ejecución
- **Base de datos**: Considera migrar a PostgreSQL para producción
- **Archivos estáticos**: Render los sirve automáticamente desde la carpeta `static/`
- **Logs**: Revisa los logs en Render si hay problemas

### Solución de problemas comunes:

1. **Error de build**: Revisa que todas las dependencias estén en `requirements.txt`
2. **Error de inicio**: Verifica que el comando `gunicorn app:app` funcione localmente
3. **Base de datos**: Asegúrate de que la base de datos se inicialice correctamente

¡Tu aplicación estará lista para usar en Render!
