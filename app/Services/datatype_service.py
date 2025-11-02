from app.Helpers.registry import register

@register("Datatype")
class DatatypeService:
    
    def __init__(self, repository):
        self.repo = repository
    
    def get(self, filters):
        return self.repo.get(filters)
    
    def create(self, data: dict):
        return self.repo.create(data)
    
    def update(self, id, data: dict):
        return self.repo.update(id, data)  

    def delete(self, dt):
        if dt.get_flag() & 1:
            raise ValueError("Can't delete this datatype (protected by flag=1)")
        self.repo.delete(dt)
