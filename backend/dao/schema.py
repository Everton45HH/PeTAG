from connection import Database

class Schema(Database):
    def create_database(self):
        conn, cursor = self.get_connection()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Usuario (
                    userID SERIAL PRIMARY KEY,
                    nome TEXT NOT NULL,
                    telefone TEXT,
                    email TEXT UNIQUE NOT NULL,
                    senha TEXT NOT NULL
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Coleira (
                    idColeira SERIAL PRIMARY KEY,
                    userID INTEGER NOT NULL,
                    nomeColeira TEXT NOT NULL,
                    longitude REAL NOT NULL,
                    latitude REAL NOT NULL,
                    distanciaMaxima REAL,
                    FOREIGN KEY (userID) REFERENCES Usuario(userID),
                    UNIQUE (userID, nomeColeira)
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS HistoricoCoordenadas (
                    idHistorico SERIAL PRIMARY KEY,
                    idColeira INTEGER NOT NULL,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (idColeira) REFERENCES Coleira(idColeira)
                );
            """)

            conn.commit()
            print("Tabelas verificadas/criadas com sucesso!")
        except Exception as e:
            print(f"Erro ao criar tabelas: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()