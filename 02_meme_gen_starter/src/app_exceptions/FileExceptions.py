import sys
class FileExceptions(Exception):
    def __init__(self, path, msg=None):
        if msg is None:
            msg = "Error with the file"
        #super(FileExceptions,self).__init__(msg)
        self.path = path
        self.msg = msg
    @property
    def show(self):
        full_msg = self.msg +": "+ self.path
        print(full_msg, file=sys.stderr)
        return full_msg
      

class FilePathInvalid(FileExceptions, FileNotFoundError):
    def __init__(self, path, msg="File path not found"):
        super(FilePathInvalid, self).__init__(path, msg)

class InvalidFile(FileExceptions):
    def __init__(self, path, msg= "Invalid file extension"):
        super(InvalidFile, self).__init__(path, msg)
