class Person:
    def __init__(self, name, age, email):
        self.name=name
        self.age=age
        self.email=email

    def get_details(self):
        return {
            'name':self.name,
            'age':self.age,
            'email':self.email
        }

    def __repr__(self):
        return f"<Person {self.name}>"