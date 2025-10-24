from app.models.flags import Flag
from app.services.registry import register

@register("Datatype")
class DatatypeService:
    
    def __init__(self, repository):
        self.repo = repository
             
    def get_by_id(self, id):
        return self.repo.get_by_id(id)
    
    def get_by_name(self, name: str):
        return self.repo.get_by_name(name)
    
    def get_all(self):
        return self.repo.get_all()

    def create(self, data: dict):
        return self.repo.create(data)

    
    def update(self, id, data: dict):
        dt = self.get_by_id(id)
        if not dt:
            return None
        flag_fields = {k: data[k] for k in data if k in Flag.DEFAULT_FLAGS}
        if flag_fields:
            flag_obj = Flag(flag_fields)
            data["flag"] = flag_obj.get_flag()
            #rmove flag fields from data before updating
            for k in flag_fields.keys():
                data.pop(k)
        return self.repo.update(id, data)  


    def delete(self, dt):
        self.repo.delete(dt)
