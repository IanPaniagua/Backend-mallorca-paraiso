import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from database import SQLALCHEMY_DATABASE_URL

def init_database():
    # Extraer el nombre de la base de datos de la URL
    db_name = SQLALCHEMY_DATABASE_URL.split('/')[-1].split('?')[0]
    
    # Conectar a PostgreSQL
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='postgres',
        host='localhost',
        port='5432'
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    try:
        # Crear la base de datos si no existe
        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
        exists = cur.fetchone()
        
        if not exists:
            cur.execute(f"CREATE DATABASE {db_name} WITH ENCODING = 'UTF8'")
            print(f"Base de datos '{db_name}' creada exitosamente.")
        else:
            print(f"La base de datos '{db_name}' ya existe.")
            
    except Exception as e:
        print(f"Error al crear la base de datos: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    init_database() 