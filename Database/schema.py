from database.connection import Database

class Schema(Database):
    def create_database(self):
        conn, cursor = self.get_connection()
        conn.execute("PRAGMA foreign_keys = ON;")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Usuario (
                userID INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                telefone TEXT,
                email TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Coleira (
                idColeira INTEGER PRIMARY KEY AUTOINCREMENT,
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
                idHistorico INTEGER PRIMARY KEY AUTOINCREMENT,
                idColeira INTEGER NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (idColeira) REFERENCES Coleira(idColeira)
            );
        """)

        conn.commit()
        cursor.close()
        conn.close()