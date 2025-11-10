from app.Helpers.registry import register
from flask import g

@register("Datatype", repo="Datatype")
class DatatypeService:
    
    def __init__(self, repository):
        self.repo = repository.get("Datatype")
    
    def get_by_id(self, id):
        return self.repo.get_by_id(id)
    
    def get(self, filters):
        return self.repo.get(filters)
    
    def create(self, data: dict):
        return self.repo.create(data)
    
    def update(self, id, data: dict):
        dt = self.get_by_id(id)
        if not dt:
            return None
        return self.repo.update(dt, data)  

    def delete(self, id):
        dt = self.repo.get_by_id(id)
        if not dt:
            raise ValueError(f"Datatype with id={id} not found")
        if dt.get_flag() & 1:
            raise ValueError("Cannot delete protected datatype (flag=1)")
        if dt.creator_id != g.current_user.id:
            raise PermissionError("You are not allowed to delete this datatype")

        self.repo.delete(dt)
        return dt  
