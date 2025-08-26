#!/usr/bin/env python3
"""
Script de prueba simple para verificar que la aplicación funciona correctamente
"""

import sqlite3
import os

def test_database():
    """Probar la conexión a la base de datos"""
    try:
        conn = sqlite3.connect('alquileres.db')
        cursor = conn.cursor()
        
        # Verificar que las tablas existen
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Tablas encontradas: {[table[0] for table in tables]}")
        
        # Verificar usuarios
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        user_count = cursor.fetchone()[0]
        print(f"Usuarios en la base de datos: {user_count}")
        
        # Verificar propiedades
        cursor.execute("SELECT COUNT(*) FROM propiedades")
        prop_count = cursor.fetchone()[0]
        print(f"Propiedades en la base de datos: {prop_count}")
        
        # Verificar inquilinos
        cursor.execute("SELECT COUNT(*) FROM inquilinos")
        inquilino_count = cursor.fetchone()[0]
        print(f"Inquilinos en la base de datos: {inquilino_count}")
        
        # Verificar contratos
        cursor.execute("SELECT COUNT(*) FROM contratos")
        contrato_count = cursor.fetchone()[0]
        print(f"Contratos en la base de datos: {contrato_count}")
        
        conn.close()
        print("✅ Conexión a la base de datos exitosa")
        return True
        
    except Exception as e:
        print(f"❌ Error en la base de datos: {e}")
        return False

def test_flask_app():
    """Probar que Flask puede importarse y crear la aplicación"""
    try:
        from app import app, init_db
        
        # Inicializar la base de datos
        init_db()
        print("✅ Aplicación Flask creada correctamente")
        print("✅ Base de datos inicializada")
        return True
        
    except Exception as e:
        print(f"❌ Error al crear la aplicación Flask: {e}")
        return False

def main():
    """Función principal de prueba"""
    print("=== PRUEBA DEL SISTEMA DE ALQUILERES ===\n")
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists('app.py'):
        print("❌ Error: No se encontró app.py. Asegúrate de estar en el directorio correcto.")
        return
    
    print("1. Probando base de datos...")
    db_ok = test_database()
    
    print("\n2. Probando aplicación Flask...")
    flask_ok = test_flask_app()
    
    print("\n=== RESULTADOS ===")
    if db_ok and flask_ok:
        print("✅ Todo está funcionando correctamente")
        print("\nPara ejecutar la aplicación:")
        print("python app.py")
        print("\nLuego abre tu navegador en: http://localhost:5000")
        print("Usuario admin: admin")
        print("Contraseña admin: admin123")
    else:
        print("❌ Hay problemas que necesitan ser solucionados")

if __name__ == "__main__":
    main()

