import sqlite3

from flask import json


class UserDAO:
    def create_database(self):
        conn , cursor = self.get_connection()
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Usuario(
                userID INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                telefone TEXT,
                email TEXT,
                senha TEXT
            );''')
        cursor.execute('''

            CREATE TABLE IF NOT EXISTS Coleira(
                idColeira INTEGER PRIMARY KEY AUTOINCREMENT,
                userID INTERGER ,
                nomeColeira TEXT,
                longitude REAL,
                latitude REAL,
                distanciaMaxima REAL
            );''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS HistoricoCoordenadas (
                idHistorico INTEGER PRIMARY KEY AUTOINCREMENT,
                idColeira INTEGER,
                latitude REAL,
                longitude REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (idColeira) REFERENCES Coleira(idColeira)
            );''')
        
        conn.commit()
        cursor.close()
        conn.close()


    def get_connection(self):
        conn = sqlite3.connect("Database/databasePeTAG.db")
        cursor = conn.cursor()
        return conn, cursor

    # POST
    def addUserDAO(self, user):
        conn, cursor = self.get_connection()

        try:
            query = "INSERT INTO Usuario (nome, telefone, email, senha) VALUES (?, ?, ?, ?)"
            cursor.execute(query, (user["nome"], user["telefone"], user["email"], user["senha"]))
            conn.commit()
            return "Usuario criado com sucesso" , None
        except Exception as e:
            return "Algo deu errado (BDD)" , 404
        finally:
            cursor.close()
            conn.close()

    # GET (todos)
    def listAllUsersDAO(self):
        conn , cursor = self.get_connection()
        try:    
            cursor.execute("SELECT * FROM Usuario")
            rows = cursor.fetchall()
            users = [{'userID': row[0], 'nome': row[1], 'telefone': row[2], 'email': row[3], 'senha': row[4].decode('utf-8')} for row in rows]
            if users:
                return users, None
            else:
                return None, "Users not found"
        except Exception:
            return None, "Database error"
        finally:
            cursor.close()
            conn.close()

    # GET (por id)
    def getUserByIdDAO(self, id):
        conn , cursor = self.get_connection()
        try:
            cursor.execute("SELECT * FROM Usuario WHERE userID = ?", (id,))
            user = cursor.fetchone()
            if user:
                user_dict = {'userID': user[0], 'nome': user[1], 'email': user[2], 'senha': user[3], 'telefone': user[4]}
                return user_dict, None
            else:
                return None, "User not found"
        except Exception:
            return None, "Database error"
        finally:
            cursor.close()
            conn.close()
    
    def getUserByEmailDAO(self, email):
        conn , cursor = self.get_connection()
        try:
            cursor.execute("SELECT userID , nome , email , senha , telefone FROM Usuario WHERE email = ?", (email,))
            user = cursor.fetchone()
            if user:
                user_dict = {'userID': user[0], 'nome': user[1], 'email': user[2], 'senha': user[3].decode('utf-8'), 'telefone': user[4]}
                return user_dict, None
            else:
                return None, "User not found"
        except Exception:
            return None, "Database error"
        finally:
            cursor.close()
            conn.close()

    
    def updateUserDAO(self, id, new_info):
        conn , cursor = self.get_connection()
        try:
            response = self.getUserByIdDAO(id)
            if not response:
                return None, "User not found"
            
            if 'email' in new_info:
                response = self.getUserByEmailDAO(new_info['email'])
                if response:
                    return "Email already exists" , 404

            fields = []
            values = []
            for key, value in new_info.items():
                fields.append(f"{key} = ?")
                values.append(value)
            values.append(id)

            query = f"UPDATE Usuario SET {', '.join(fields)} WHERE userID = ?"
            cursor.execute(query, values)
            conn.commit()

            updated_user, error = self.getUserByIdDAO(id)
            if updated_user:
                return updated_user, None
            else:
                return None, error
        finally:
            cursor.close()
            conn.close()

    def deleteUserDAO(self, id):
        conn , cursor = self.get_connection()
        try:
            user = self.getUserByIdDAO(id)
            if not user:
                return None, "User not found"
            
            cursor.execute("DELETE FROM Usuario WHERE userID = ?", (id,))
            conn.commit()
            return "Atualizado", None
        except Exception as e:
            return None, "Database error"
        finally:
            cursor.close()
            conn.close()

DAO = UserDAO()
DAO.create_database()