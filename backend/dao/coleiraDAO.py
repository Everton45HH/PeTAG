from dao.connection import Database

class ColeiraDAO(Database):

    def createColeiraDAO(self, coleira):
        conn, cursor = self.get_connection()
        try:
            # Verifica se já existe uma coleira com este nome para este usuário
            # Nota: Ajustado para buscar por nome dentro do contexto do usuário
            query_check = "SELECT idColeira FROM Coleira WHERE nomeColeira = %s AND userID = %s"
            cursor.execute(query_check, (coleira["nomeColeira"], coleira["userID"]))
            if cursor.fetchone():
                return None, "device_already_exists"

            query = """
                INSERT INTO Coleira (nomeColeira, userID, longitude, latitude, distanciaMaxima) 
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                coleira["nomeColeira"], 
                coleira["userID"], 
                coleira["longitude"], 
                coleira["latitude"],
                coleira["distanciaMaxima"]
            ))
            conn.commit()
            return "Coleira criada com sucesso", None
        except Exception as e:
            print(f"Erro ao criar coleira: {e}")
            conn.rollback()
            return "Algo deu errado (BDD)", 500
        finally:
            cursor.close()
            conn.close()

    def getColeirasDAO(self, id_coleira):
        conn, cursor = self.get_connection()
        try:
            # Placeholder alterado para %s
            query = "SELECT idColeira, userID, nomeColeira, longitude, latitude, distanciaMaxima FROM Coleira WHERE idColeira = %s"
            cursor.execute(query, (id_coleira,))
            row = cursor.fetchone()

            if row:
                coleira = {
                    'idColeira': row[0],
                    'userID': row[1],
                    'nomeColeira': row[2],
                    'longitude': row[3],
                    'latitude': row[4],
                    'distanciaMaxima': row[5]
                }
                return coleira, None
            return None, 404
        except Exception as e:
            print(f"Erro ao buscar coleira: {e}")
            return None, 500
        finally:
            cursor.close()
            conn.close()

    def getAllColeirasDAO(self, user_id):
        conn, cursor = self.get_connection()
        try:
            query = "SELECT idColeira, userID, nomeColeira, longitude, latitude, distanciaMaxima FROM Coleira WHERE userID = %s"
            cursor.execute(query, (user_id,))
            rows = cursor.fetchall()
            
            coleiras = [
                {
                    'idColeira': row[0], 
                    'userID': row[1], 
                    'nomeColeira': row[2], 
                    'longitude': row[3], 
                    'latitude': row[4], 
                    'distanciaMaxima': row[5]
                } for row in rows
            ]
            return coleiras, None
        except Exception as e:
            print(f"Erro ao listar coleiras: {e}")
            return None, 500
        finally:
            cursor.close()
            conn.close()
            
    def deleteColeiraDAO(self, id_coleira, userID):
        conn, cursor = self.get_connection()
        try:
            query = "DELETE FROM Coleira WHERE idColeira = %s AND userID = %s"
            cursor.execute(query, (id_coleira, userID))
            conn.commit()

            if cursor.rowcount == 0:
                return None, "device_not_found"

            return "Coleira deletada com sucesso", None
        except Exception as e:
            print(f"Erro ao deletar coleira: {e}")
            conn.rollback()
            return None, "internal_error"
        finally:
            cursor.close()
            conn.close()

    def updateSettingsColeiraDAO(self, id_coleira, data, userID):
        conn, cursor = self.get_connection()
        try:
            query = """
                UPDATE Coleira
                SET nomeColeira = %s, distanciaMaxima = %s
                WHERE idColeira = %s AND userID = %s
            """
            cursor.execute(query, (
                data["nomeColeira"],
                data["distanciaMaxima"],
                id_coleira,
                userID
            ))
            conn.commit()

            if cursor.rowcount == 0:
                return None, 404

            return {"message": "Dados da coleira atualizados"}, None
        except Exception as e:
            print(f"Erro no updateSettings: {e}")
            conn.rollback()
            return None, 500
        finally:
            cursor.close()
            conn.close()

    def updateCoordsColeiraDAO(self, id_coleira, data, userID):
        conn, cursor = self.get_connection()
        try:
            query = """
                UPDATE Coleira
                SET longitude = %s, latitude = %s
                WHERE idColeira = %s AND userID = %s
            """
            cursor.execute(query, (
                data["longitude"],
                data["latitude"],
                id_coleira,
                userID
            ))
            conn.commit()

            if cursor.rowcount == 0:
                return None, 404

            return {"message": "Coordenadas atualizadas"}, None
        except Exception as e:
            print(f"Erro no updateCoords: {e}")
            conn.rollback()
            return None, 500
        finally:
            cursor.close()
            conn.close()