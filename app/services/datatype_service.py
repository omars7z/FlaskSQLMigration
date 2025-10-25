from app.models.flags import Flag
from app.services.registry import register

@register("Datatype")
class DatatypeService:
    
    def __init__(self, repository):
        self.repo = repository
             
    def get_by_id(self, id:int):
        return self.repo.get_by_id(id)
    
    def get_by_name(self, name: str):
        return self.repo.get_by_name(name)
    
    def get_all(self):
        return self.repo.get_all()

    def create(self, data: dict):
        return self.repo.create(data)

    
    def update(self, id, data: dict):
        dt = self.get_by_id(id)
        print(dt)
        
        return self.repo.update(id, data)  


    def delete(self, dt):
        if Flag().get_flag() == 1:
            raise ValueError("cant delete default flag")
        self.repo.delete(dt)
