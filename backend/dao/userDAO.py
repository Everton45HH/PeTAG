from .connection import Database

class UserDAO(Database):
    # POST
    def addUserDAO(self, user):
        conn, cursor = self.get_connection()
        try:
            query = "INSERT INTO Usuario (nome, telefone, email, senha) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (user["nome"], user["telefone"], user["email"], user["senha"]))
            conn.commit()
            return "Usuario criado com sucesso", None
        except Exception as e:
            print(f"Erro BDD: {e}")
            return "Algo deu errado (BDD)", 500
        finally:
            cursor.close()
            conn.close()

    # GET (todos)
    def listAllUsersDAO(self):
        conn, cursor = self.get_connection()
        try:    
            cursor.execute("SELECT userID, nome, telefone, email, senha FROM Usuario")
            rows = cursor.fetchall()
            users = [{'userID': row[0], 'nome': row[1], 'telefone': row[2], 'email': row[3], 'senha': row[4]} for row in rows]
            return (users, None) if users else (None, "Users not found")
        except Exception as e:
            return None, f"Database error: {e}"
        finally:
            cursor.close()
            conn.close()

    # GET (por id)
    def getUserByIdDAO(self, id):
        conn, cursor = self.get_connection()
        try:
            cursor.execute("SELECT userID, nome, email, senha, telefone FROM Usuario WHERE userID = %s", (id,))
            user = cursor.fetchone()
            if user:
                return {'userID': user[0], 'nome': user[1], 'email': user[2], 'senha': user[3], 'telefone': user[4]}, None
            return None, "User not found"
        except Exception as e:
            return None, f"Database error: {e}"
        finally:
            cursor.close()
            conn.close()
    
    def getUserByEmailDAO(self, email):
        conn, cursor = self.get_connection()
        try:
            cursor.execute("SELECT userID, nome, email, senha, telefone FROM Usuario WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user:
                return {'userID': user[0], 'nome': user[1], 'email': user[2], 'senha': user[3], 'telefone': user[4]}, None
            return None, "User not found"
        except Exception as e:
            return None, f"Database error: {e}"
        finally:
            cursor.close()
            conn.close()

    def updateUserDAO(self, id, new_info):
        conn, cursor = self.get_connection()
        try:
            user_exists, _ = self.getUserByIdDAO(id)
            if not user_exists:
                return None, "User not found"

            fields = []
            values = []
            for key, value in new_info.items():
                fields.append(f"{key} = %s")
                values.append(value)
            values.append(id)

            query = f"UPDATE Usuario SET {', '.join(fields)} WHERE userID = %s"
            cursor.execute(query, values)
            conn.commit()

            return self.getUserByIdDAO(id)
        except Exception as e:
            conn.rollback()
            return None, f"Update error: {e}"
        finally:
            cursor.close()
            conn.close()

    def deleteUserDAO(self, id):
        conn, cursor = self.get_connection()
        try:
            cursor.execute("DELETE FROM Usuario WHERE userID = %s", (id,))
            conn.commit()
            return "Removido com sucesso", None
        except Exception as e:
            conn.rollback()
            return None, f"Delete error: {e}"
        finally:
            cursor.close()
            conn.close()