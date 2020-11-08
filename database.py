from jsonFile import Json

d = Json()
class Database:
    def __init__(self, dbName, filename, type='a'):
        self.dbname = dbName
        self.fileName = filename
        self.trans = Json()
        try:
            self.file = open(self.fileName, 'r')
            self.file = open(self.fileName, 'a')
            print("file opened successfully")
        except FileNotFoundError:
            print("error: file not found")
            res = str(input("create a new file[Y/n]: "))
            if res == 'y' or res == 'Y':
                self.file = open(self.fileName, 'a+')
                print("file created successfully !")
            else:
                print("exited")
                return
    def insert(self, document):
        with self.file as f:
            text = f.read()
        print(self.trans.string_to_dict(text))

achraf = Database('achraf', 'achraf.txt')
