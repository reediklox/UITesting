import json

class JsonWorkException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None
            
    def __str__(self):
        if 'class' in self.message:
            return f'ClassInstanceException: {self.message}'
        elif 'path' in self.message:
            return f'InvalidPathException: {self.message}'
        else:
            return 'Something went wrong in jsonWork.py module'

class CreateObjectError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args


class JWork():
    def __init__(self):
        raise JsonWorkException('You can not create the instance of this class')
     
    @classmethod
    def __pathValidate(cls, path:str):
        if '.' in path and path.split('.')[1] == 'json':
            return path
        else:
            raise JsonWorkException('Something wrong with the path. Check the format!')
    
    @classmethod
    def getData(cls, key:str, path:str) -> str:
        path = JWork.__pathValidate(path)
            
        with open(path, 'r') as j:
            data = json.load(j)
        
        return data[key]
        
    @classmethod
    def ChangePass(cls, path:str, password:str, key:str):
        with open(path, 'r') as r:
            data = json.load(r)
            
        data[key]['password'] = password
        
        with open(path, 'w') as w:
            json.dump(data, w)