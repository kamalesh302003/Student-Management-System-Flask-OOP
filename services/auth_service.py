from database.db import get_connection
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

class AuthService:
    @staticmethod
    def _row_to_user(row):
        if row is None:
            return None
        return User(
            id=row['id'],
            username=row['username'],
            email=row['email'],
            password=row['password']
        )

    @staticmethod
    def authenticate(username, password):
        conn=get_connection()
        row=conn.execute(
            'SELECT * FROM users WHERE username=?',(username,)
        ).fetchone()
        conn.close()
        
        if row is None:
            return False
        
        user=AuthService._row_to_user(row)
        return check_password_hash(user.password, password)

    @staticmethod
    def get_user_by_username(username):
        conn=get_connection()
        row=conn.execute(
            'SELECT * FROM users WHERE username=?',(username,)
        ).fetchone()
        conn.close()
        return AuthService._row_to_user(row)

    @staticmethod
    def get_user_by_id(user_id):
        conn=get_connection()
        row=conn.execute(
            'SELECT * FROM users WHERE id=?',(user_id,)
        ).fetchone()
        conn.close()
        return AuthService._row_to_user(row)

    @staticmethod
    def register_user(username, email, password):
        conn=get_connection()
        try:
            hashed_password=generate_password_hash(password)
            conn.execute('''
                INSERT INTO users (username,email,password)
                VALUES (?,?,?)
            ''', (username, email, hashed_password))
            conn.commit()
            return True,'User registered successfully!'
        except conn.IntegrityError:
            return False,'Username or email already exists.'
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    @staticmethod
    def change_password(user_id, old_password, new_password):
        user=AuthService.get_user_by_id(user_id)
        if user is None:
            return False, 'User not found.'
        
        if not check_password_hash(user.password, old_password):
            return False, 'Old password is incorrect.'
        
        conn=get_connection()
        try:
            hashed_password=generate_password_hash(new_password)
            conn.execute(
                'UPDATE users SET password=? WHERE id=?',
                (hashed_password, user_id)
            )
            conn.commit()
            return True,'Password changed successfully!'
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()
