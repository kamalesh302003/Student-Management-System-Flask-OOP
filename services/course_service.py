from database.db import get_connection
from models.course import Course

class CourseService:
    @staticmethod
    def _row_to_course(row):
        if row is None:
            return None
        return Course(
            id=row['id'],
            title=row['title'],
            description=row['description'],
            code=row['code']
        )

    @staticmethod
    def get_all_courses():
        conn=get_connection()
        rows=conn.execute('SELECT * FROM courses ORDER BY id DESC').fetchall()
        conn.close()
        return [CourseService._row_to_course(row) for row in rows]

    @staticmethod
    def get_course_by_id(course_id):
        conn=get_connection()
        row=conn.execute(
            'SELECT * FROM courses WHERE id=?',(course_id,)
        ).fetchone()
        conn.close()
        return CourseService._row_to_course(row)

    @staticmethod
    def get_course_by_code(code):
        conn=get_connection()
        row=conn.execute(
            'SELECT * FROM courses WHERE code=?',(code,)
        ).fetchone()
        conn.close()
        return CourseService._row_to_course(row)

    @staticmethod
    def add_course(data):
        conn=get_connection()
        try:
            conn.execute('''
                INSERT INTO courses (title,description,code)
                VALUES (?,?,?)
            ''', (
                data['title'],
                data.get('description') or '',
                data['code']
            ))
            conn.commit()
            return True,'Course added successfully!'
        except conn.IntegrityError:
            return False,'Course code already exists.'
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    @staticmethod
    def update_course(course_id, data):
        conn=get_connection()
        try:
            conn.execute('''
                UPDATE courses
                SET title=?,description=?,code=?
                WHERE id=?
            ''', (
                data['title'],
                data.get('description') or '',
                data['code'],
                course_id
            ))
            conn.commit()
            return True,'Course updated successfully!'
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    @staticmethod
    def delete_course(course_id):
        conn=get_connection()
        try:
            cursor=conn.execute(
                'DELETE FROM courses WHERE id=?',(course_id,)
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    @staticmethod
    def get_course_count():
        conn=get_connection()
        count=conn.execute('SELECT COUNT(*) FROM courses').fetchone()[0]
        conn.close()
        return count
