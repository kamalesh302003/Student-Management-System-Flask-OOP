from models.person import Person
class Student(Person):
    def __init__(self,name,age,email,student_id,course,grade=None,id=None):
        super().__init__(name,age,email)
        self.id=id
        self.student_id=student_id
        self.course=course
        self.grade=grade

    def get_details(self):# Method overriding
        details=super().get_details()
        details.update({
            'id':self.id,
            'student_id':self.student_id,
            'course':self.course,
            'grade':self.grade
        })
        return details

    def is_passing(self):
        return self.grade in ['A','B','C'] if self.grade else None

    def __repr__(self):
        return f"<Student {self.name} | {self.student_id}>"