from .connection import Database
from psycopg2.extras import RealDictRow

class UserDAO(Database):

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
            # Retornamos a string do erro para o Flask conseguir serializar em JSON
            return None, str(e)

        finally:
            cursor.close()
            conn.close()

    def create(self, user):
        query = """
            INSERT INTO "Usuario" ("nome", "email", "senha")
            VALUES (%s, %s, %s)
            RETURNING "userID" AS "userID"
        """
        return self._execute(
            query,
            (user["nome"], user["email"], user["senha"]),
            fetchone=True
        )

    def get_by_email(self, email):
        query = """
            SELECT "userID" AS "userID", "email", "senha" 
            FROM "Usuario" 
            WHERE "email" = %s
        """
        return self._execute(query, (email,), fetchone=True)

    def user_exists(self, user_id):
        query = """SELECT 1 FROM "Usuario" WHERE "userID" = %s"""
        return self._execute(query, (user_id,), fetchone=True)

    def update(self, user_id, data):
        fields = ", ".join(f'"{k}" = %s' for k in data)
        values = list(data.values()) + [user_id]

        query = f"""
            UPDATE "Usuario"
            SET {fields}
            WHERE "userID" = %s
            RETURNING "userID" AS "userID"
        """
        return self._execute(query, values, fetchone=True)

    def delete(self, user_id):
        query = """
            DELETE FROM "Usuario"
            WHERE "userID" = %s
            RETURNING "userID" AS "userID"
        """
        return self._execute(query, (user_id,), fetchone=True)