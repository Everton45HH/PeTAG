from dao.connection import Database
from psycopg2.errors import UniqueViolation
from utils.error_messages import AppError

class ColeiraDAO(Database):

    def _execute(self, query, params=None, fetchone=False, fetchall=False):
        conn, cursor = self.get_connection()
        try:
            cursor.execute(query, params)
            result = None
            if fetchone:
                result = cursor.fetchone()
            elif fetchall:
                result = cursor.fetchall()
            conn.commit()
            return result
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def create(self, data):
        query = """
            INSERT INTO coleiras (nome, usuario_id, longitude, latitude, distancia_maxima)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id AS "idColeira"
        """
        try:
            return self._execute(
            query,
            (
                data["nomeColeira"],
                data["userID"],
                data["longitude"],
                data["latitude"],
                data["distanciaMaxima"],
            ),
            fetchone=True,
        )
        except UniqueViolation:
                raise AppError("COLLAR_EXISTS")

    def get_by_id(self, id_coleira):
        query = """
            SELECT id AS "idColeira",
                usuario_id AS "userID",
                nome AS "nomeColeira",
                longitude,
                latitude,
                distancia_maxima AS "distanciaMaxima"
            FROM coleiras
            WHERE id = %s
        """
        return self._execute(query, (id_coleira,), fetchone=True)

    def get_all_coleiras_by_user(self, user_id):
        query = """
            SELECT id AS "idColeira",
                usuario_id AS "userID",
                nome AS "nomeColeira",
                longitude,
                latitude,
                distancia_maxima AS "distanciaMaxima"
            FROM coleiras
            WHERE usuario_id = %s
        """
        return self._execute(query, (user_id,), fetchall=True)

    def delete(self, id_coleira, user_id):
        query = """
            DELETE FROM coleiras
            WHERE id = %s
            AND usuario_id = %s
            RETURNING id AS "idColeira"
        """
        return self._execute(query, (id_coleira, user_id), fetchone=True)

    def update_settings(self, id_coleira, user_id, data):
        query = """
            UPDATE coleiras
            SET nome = %s,
                distancia_maxima = %s
            WHERE id = %s
            AND usuario_id = %s
            RETURNING id AS "idColeira"
        """
        try:
            return self._execute(
            query,
            (data["nomeColeira"], data["distanciaMaxima"], id_coleira, user_id),
            fetchone=True,
        )
        except UniqueViolation:
            raise AppError("COLLAR_EXISTS")
            

    def update_coords(self, id_coleira, data):
        query = """
            UPDATE coleiras
            SET longitude = %s,
                latitude = %s
            WHERE id = %s
            RETURNING id AS "idColeira"
        """
        return self._execute(
            query,
            (data["longitude"], data["latitude"], id_coleira),
            fetchone=True,
        )