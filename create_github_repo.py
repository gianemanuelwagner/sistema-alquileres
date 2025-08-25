import requests
import json
import subprocess
import sys
import os

def create_github_repo():
    """Create a GitHub repository and push the code"""
    
    print("🚀 Creando repositorio en GitHub...")
    print("=" * 50)
    
    # Solicitar token de GitHub
    print("Para crear el repositorio, necesitas un token de acceso personal de GitHub.")
    print("1. Ve a https://github.com/settings/tokens")
    print("2. Haz clic en 'Generate new token (classic)'")
    print("3. Selecciona 'repo' para permisos completos")
    print("4. Copia el token generado")
    print()
    
    token = input("Ingresa tu token de GitHub: ").strip()
    
    if not token:
        print("❌ Token requerido para continuar")
        return
    
    # Configurar headers para la API de GitHub
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # Datos del repositorio
    repo_data = {
        'name': 'sistema-alquileres',
        'description': 'Sistema completo de gestión de alquileres desarrollado con Flask y Python',
        'homepage': '',
        'private': False,
        'has_issues': True,
        'has_wiki': True,
        'has_downloads': True,
        'auto_init': False
    }
    
    try:
        # Crear el repositorio
        print("📝 Creando repositorio...")
        response = requests.post(
            'https://api.github.com/user/repos',
            headers=headers,
            data=json.dumps(repo_data)
        )
        
        if response.status_code == 201:
            repo_info = response.json()
            repo_url = repo_info['html_url']
            clone_url = repo_info['clone_url']
            
            print(f"✅ Repositorio creado exitosamente!")
            print(f"🌐 URL: {repo_url}")
            print()
            
            # Configurar el remote y hacer push
            print("📤 Subiendo código al repositorio...")
            
            # Agregar remote
            subprocess.run(['git', 'remote', 'add', 'origin', clone_url], check=True)
            
            # Hacer push
            subprocess.run(['git', 'branch', '-M', 'main'], check=True)
            subprocess.run(['git', 'push', '-u', 'origin', 'main'], check=True)
            
            print("✅ Código subido exitosamente!")
            print()
            print("🎉 ¡Tu aplicación está ahora en GitHub!")
            print(f"🔗 URL del repositorio: {repo_url}")
            print()
            print("📋 Para ver tu aplicación en vivo, puedes usar:")
            print("   - GitHub Pages (para frontend estático)")
            print("   - Heroku, Vercel, o Railway (para la aplicación completa)")
            print()
            print("🔧 Para ejecutar localmente:")
            print("   git clone " + clone_url)
            print("   cd sistema-alquileres")
            print("   pip install -r requirements.txt")
            print("   python app.py")
            
        else:
            print(f"❌ Error al crear el repositorio: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al ejecutar comando Git: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    create_github_repo()
