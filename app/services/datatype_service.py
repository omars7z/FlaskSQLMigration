from app.services.registry import register

@register("Datatype")
class DatatypeService:
    
    def __init__(self, repository):
        self.repo = repository
             
    def get_by_id(self, id:int):
        return self.repo.get_by_id(id)
    
    def get_by_name(self, name: str, case_sens: bool):
        return self.repo.get_by_name(name, case_sens)
    
    def get_all(self):
        return self.repo.get_all()

    def create(self, data: dict):
        return self.repo.create(data)
    
    def update(self, id, data: dict):
        return self.repo.update(id, data)  

    def delete(self, dt):
        if dt.flag_val & 1:
            raise ValueError("Can't delete this datatype (protected by flag=1)")
        self.repo.delete(dt)
