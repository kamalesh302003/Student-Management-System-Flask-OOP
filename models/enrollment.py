class Enrollment:
    def __init__(self, student_id, course_id, grade=None, id=None):
        self.id = id
        self.student_id = student_id
        self.course_id = course_id
        self.grade = grade

    def get_details(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'course_id': self.course_id,
            'grade': self.grade
        }
