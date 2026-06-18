from database.db import get_connection
from models.student import Student

class StudentService:
    @staticmethod
    def _parse_attendance(value):
        if value is None or str(value).strip() == '':
            return None
        try:
            attendance = int(value)
            return max(0, min(100, attendance))
        except ValueError:
            return None

    @staticmethod
    def _row_to_student(row):
        if row is None:
            return None
        return Student(
            id=row['id'],
            name=row['name'],
            age=row['age'],
            email=row['email'],
            student_id=row['student_id'],
            course=row['course'],
            grade=row['grade'],
            attendance=row['attendance']
        )

    @staticmethod
    def get_all_students():
        conn=get_connection()
        rows=conn.execute('SELECT * FROM students ORDER BY id DESC').fetchall()
        conn.close()
        return [StudentService._row_to_student(row) for row in rows]

    @staticmethod
    def get_student_by_id(student_id):
        conn=get_connection()
        row=conn.execute(
            'SELECT * FROM students WHERE student_id=?',(student_id,)
        ).fetchone()
        conn.close()
        return StudentService._row_to_student(row)

    @staticmethod
    def add_student(data):
        attendance = StudentService._parse_attendance(data.get('attendance'))
        if data.get('attendance') and attendance is None:
            return False, 'Attendance must be a whole number between 0 and 100.'

        conn=get_connection()
        try:
            conn.execute('''
                INSERT INTO students (name,age,email,student_id,course,grade,attendance)
                VALUES (?,?,?,?,?,?,?)
            ''', (
                data['name'],
                int(data['age']),
                data['email'],
                data['student_id'],
                data['course'],
                data.get('grade') or None,
                attendance
            ))
            conn.commit()
            return True,'Student added successfully!'
        except conn.IntegrityError:
            return False,'Student ID or Email already exists.'
        finally:
            conn.close()

    @staticmethod
    def update_student(student_id, data):
        attendance = StudentService._parse_attendance(data.get('attendance'))
        if data.get('attendance') and attendance is None:
            return False, 'Attendance must be a whole number between 0 and 100.'

        conn=get_connection()
        try:
            conn.execute('''
                UPDATE students
                SET name=?,age=?,email=?,course=?,grade=?,attendance=?
                WHERE student_id=?
            ''', (
                data['name'],
                int(data['age']),
                data['email'],
                data['course'],
                data.get('grade') or None,
                attendance,
                student_id
            ))
            conn.commit()
            return True,'Student updated successfully!'
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    @staticmethod
    def delete_student(student_id):
        conn=get_connection()
        cursor=conn.execute(
            'DELETE FROM students WHERE student_id=?',(student_id,)
        )
        conn.commit()
        conn.close()
        return cursor.rowcount >0  # True if a row was deleted

    @staticmethod
    def get_student_count():
        conn=get_connection()
        count=conn.execute('SELECT COUNT(*) FROM students').fetchone()[0]
        conn.close()
        return count

    @staticmethod
    def get_average_attendance():
        conn=get_connection()
        row=conn.execute('SELECT AVG(attendance) as avg_attendance FROM students WHERE attendance IS NOT NULL').fetchone()
        conn.close()
        return round(row['avg_attendance'], 1) if row and row['avg_attendance'] is not None else 0

    @staticmethod
    def get_recent_students(limit=5):
        conn=get_connection()
        rows=conn.execute('SELECT * FROM students ORDER BY id DESC LIMIT ?', (limit,)).fetchall()
        conn.close()
        return [StudentService._row_to_student(row) for row in rows]