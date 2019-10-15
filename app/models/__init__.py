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
    
    print(ArModels)
    return ArModels

def one_model(name):
    #print(globals().keys())
    if name in globals() and issubclass(type(globals()[name]), pw.ModelBase):
        #print(globals()[name])
        return globals()[name]
    else:
        return None