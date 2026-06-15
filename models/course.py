class Course:
    def __init__(self, title, description, code, id=None):
        self.id = id
        self.title = title
        self.description = description
        self.code = code

    def get_details(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'code': self.code
        }
