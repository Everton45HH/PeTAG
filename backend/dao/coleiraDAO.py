from dao.connection import Database
from psycopg2.extras import RealDictRow

class ColeiraDAO(Database):

    def _execute(self, query, params=(), fetchone=False, fetchall=False):
        conn, cursor = self.get_connection()
        try:
            cursor.execute(query, params)

            if fetchone:
                result = cursor.fetchone()
            elif fetchall:
                result = cursor.fetchall()
            else:
                result = None

            conn.commit()
            return result, None

        except Exception as e:
            conn.rollback()
            return None, str(e)

        finally:
            cursor.close()
            conn.close()

    def create(self, data):
        query = """
            INSERT INTO "Coleira" ("nomeColeira", "userID", "longitude", "latitude", "distanciaMaxima")
            VALUES (%s, %s, %s, %s, %s)
            RETURNING "idColeira" AS "idColeira"
        """
        return self._execute(
            query,
            (
                data["nomeColeira"],
                data["userID"],
                data["longitude"],
                data["latitude"],
                data["distanciaMaxima"]
            ),
            fetchone=True
        )

    def get_by_id(self, id_coleira):
        query = """
            SELECT "idColeira" AS "idColeira", "userID" AS "userID", "nomeColeira" AS "nomeColeira", 
                   "longitude", "latitude", "distanciaMaxima" AS "distanciaMaxima"
            FROM "Coleira"
            WHERE "idColeira" = %s
        """
        return self._execute(query, (id_coleira,), fetchone=True)

    def get_all_coleiras_by_user(self, user_id):
        query = """
            SELECT "idColeira" AS "idColeira", "userID" AS "userID", "nomeColeira" AS "nomeColeira", 
                   "longitude", "latitude", "distanciaMaxima" AS "distanciaMaxima"
            FROM "Coleira"
            WHERE "userID" = %s
        """
        return self._execute(query, (user_id,), fetchall=True)
            
    def delete(self, id_coleira):
        query = """
            DELETE FROM "Coleira"
            WHERE "idColeira" = %s
            RETURNING "idColeira" AS "idColeira"
        """
        return self._execute(query, (id_coleira,), fetchone=True)

    def update_settings(self, id_coleira, data, user_id):
        query = """
            UPDATE "Coleira"
            SET "nomeColeira" = %s,
                "distanciaMaxima" = %s
            WHERE "idColeira" = %s
            AND "userID" = %s
            RETURNING "idColeira" AS "idColeira"
        """
        return self._execute(
            query,
            (
                data["nomeColeira"],
                data["distanciaMaxima"],
                id_coleira,
                user_id
            ),
            fetchone=True
        )

    def update_coords(self, data, id_coleira):
        query = """
            UPDATE "Coleira"
            SET "longitude" = %s, "latitude" = %s
            WHERE "idColeira" = %s
            RETURNING "idColeira" AS "idColeira"
        """
        return self._execute(
            query,
            (data["longitude"], data["latitude"], id_coleira),
            fetchone=True
        )