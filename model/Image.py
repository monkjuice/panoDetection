from model.database import connect

class Image:
    def __init__(self, id=None, name=None, path=None):
        self.id = id
        self.name = name
        self.path = path

    def get(self):
        db = connect()
        cursor = db.cursor()
        sql = 'Select * from images where id = %s limit 1'
        id = (self.id,)

        cursor.execute(sql,id)

        tempimg = cursor.fetchone()

        self.name = tempimg[1]
        self.path = tempimg[2]

        return self
