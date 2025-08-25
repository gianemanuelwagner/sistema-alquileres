# 🚀 Guía para Subir tu Aplicación a GitHub

## Paso 1: Crear un Token de Acceso Personal en GitHub

1. Ve a [GitHub Settings > Tokens](https://github.com/settings/tokens)
2. Haz clic en "Generate new token (classic)"
3. Dale un nombre como "Sistema Alquileres"
4. Selecciona los siguientes permisos:
   - ✅ `repo` (todos los permisos de repositorio)
   - ✅ `workflow` (opcional, para GitHub Actions)
5. Haz clic en "Generate token"
6. **IMPORTANTE**: Copia el token generado (solo se muestra una vez)

## Paso 2: Crear el Repositorio en GitHub

### Opción A: Usando el Script Automático
```bash
python create_github_repo.py
```
Cuando te pida el token, pégalo y presiona Enter.

### Opción B: Manualmente
1. Ve a [GitHub](https://github.com)
2. Haz clic en el botón "+" y selecciona "New repository"
3. Nombre del repositorio: `sistema-alquileres`
4. Descripción: `Sistema completo de gestión de alquileres desarrollado con Flask y Python`
5. Selecciona "Public"
6. **NO** marques "Add a README file" (ya tenemos uno)
7. Haz clic en "Create repository"

## Paso 3: Conectar tu Repositorio Local con GitHub

Si usaste el script automático, este paso ya está hecho. Si no, ejecuta:

```bash
# Reemplaza TU_USUARIO con tu nombre de usuario de GitHub
git remote add origin https://github.com/TU_USUARIO/sistema-alquileres.git
git branch -M main
git push -u origin main
```

## Paso 4: Verificar que Todo Funcione

1. Ve a tu repositorio en GitHub: `https://github.com/TU_USUARIO/sistema-alquileres`
2. Deberías ver todos los archivos subidos
3. El README.md se mostrará en la página principal

## 🎉 ¡Listo! Tu Aplicación está en GitHub

### URL de tu Repositorio:
```
https://github.com/TU_USUARIO/sistema-alquileres
```

### Para Clonar en Otro Computador:
```bash
git clone https://github.com/TU_USUARIO/sistema-alquileres.git
cd sistema-alquileres
pip install -r requirements.txt
python app.py
```

## 🌐 Opciones para Desplegar en Vivo

### 1. Railway (Recomendado - Gratis)
1. Ve a [Railway](https://railway.app)
2. Conecta tu cuenta de GitHub
3. Selecciona tu repositorio `sistema-alquileres`
4. Railway detectará automáticamente que es una app Flask
5. ¡Listo! Tu app estará disponible en una URL como: `https://tu-app.railway.app`

### 2. Render
1. Ve a [Render](https://render.com)
2. Conecta tu cuenta de GitHub
3. Crea un nuevo "Web Service"
4. Selecciona tu repositorio
5. Configura:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`

### 3. Heroku
1. Ve a [Heroku](https://heroku.com)
2. Crea una nueva app
3. Conecta tu repositorio de GitHub
4. Configura las variables de entorno si es necesario

## 📝 Archivos Importantes

- `app.py` - Aplicación principal
- `requirements.txt` - Dependencias de Python
- `README.md` - Documentación del proyecto
- `.gitignore` - Archivos que no se suben a GitHub

## 🔧 Comandos Útiles

```bash
# Ver el estado del repositorio
git status

# Ver los cambios
git diff

# Agregar cambios
git add .

# Hacer commit
git commit -m "Descripción de los cambios"

# Subir cambios
git push

# Ver el historial
git log --oneline
```

## 🆘 Si Algo Sale Mal

1. **Error de autenticación**: Verifica que tu token sea correcto
2. **Error de permisos**: Asegúrate de que el token tenga permisos de `repo`
3. **Repositorio ya existe**: Cambia el nombre en el script o crea uno manualmente
4. **Error de push**: Verifica que tengas permisos de escritura en el repositorio

---

**¡Tu aplicación de gestión de alquileres está lista para ser compartida con el mundo! 🌍**
