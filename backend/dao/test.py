from connection import Database
def test():
    try:
        db = Database()
        conn, cursor = db.get_connection()
        
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        
        print("Conexão com o Neon estabelecida!")
        print(f"Versão do Postgres: {db_version['version']}")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao conectar: {e}")

if __name__ == "__main__":
    test()