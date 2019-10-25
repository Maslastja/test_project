from peewee import Model
from playhouse.flask_utils import FlaskDB, get_object_or_404

class BaseModelClass(Model):
    # поиск по id
    @classmethod
    def get_by_id(self, id):
        result = get_object_or_404(self, self.id == id)
        #print(result)
        return result
    
db = FlaskDB(model_class=BaseModelClass)


