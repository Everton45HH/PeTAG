from schema import Schema

try:
    print("Sincronizando tabelas...")
    Schema().create_database()
    print("Tudo pronto no banco de dados!")
except Exception as e:
    print(f"Erro no schema: {e}")