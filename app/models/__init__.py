import peewee as pw
from app.models.group import Group
from app.models.student import Student
from app.models.users import User

def all_models():
    ArModels = []
    #независимые таблицы
    ArModels.append(User)
    
    #зависимые таблицы
    ArModels.append(Student)
    ArModels.append(Group)
    
    return ArModels

def one_model(name):
    ArModels = all_models()
    for mod in ArModels:
        if name == mod.__name__:
            #print(name)
            return mod
    else:
        return None