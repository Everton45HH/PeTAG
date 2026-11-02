from .connection import Database
from psycopg2.errors import UniqueViolation
from utils.error_messages import AppError
from psycopg2.extras import RealDictRow


class UserDAO(Database):

    def _execute(self, query, params=None, fetchone=False):
        conn, cursor = self.get_connection()
        try:
            cursor.execute(query, params)
            result = cursor.fetchone() if fetchone else None
            conn.commit()
            return result
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def create(self, user):
        query = """
            INSERT INTO usuarios (nome, email, senha)
            VALUES (%s, %s, %s)
            RETURNING id
        """
        try:
            return self._execute(
                query,
                (user["nome"], user["email"], user["senha"]),
                fetchone=True,
            )
        except UniqueViolation:
            raise AppError("EMAIL_EXISTS")

    def get_by_email(self, email):
        query = """
            SELECT id, email, senha
            FROM usuarios 
            WHERE "email" = %s
        """
        return self._execute(query, (email,), fetchone=True)

    def user_exists(self, user_id):
        query = """SELECT 1 FROM usuarios WHERE id" = %s"""
        return self._execute(query, (user_id,), fetchone=True)

    def update(self, user_id, data):
        fields = ", ".join(f'"{k}" = %s' for k in data)
        values = list(data.values()) + [user_id]

        query = f"""
            UPDATE usuarios
            SET {fields}
            WHERE id = %s
        """
        return self._execute(query, values, fetchone=True)

    def delete(self, user_id):
        print(user_id)
        query = """
            DELETE FROM usuarios
            WHERE id = %s
            RETURNING id
        """
        return self._execute(query, (user_id,), fetchone=True)
