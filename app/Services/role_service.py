from app.Helpers.registry import register
from app.Mappers.role_mapper import RoleMapper

@register("Role", repo=("Role", "Permission"))
class RoleServices:
    
    def __init__(self, repository):
        self.role_repo = repository.get("Role")
        self.perm_repo = repository.get("Permission")
    
    def get_by_id(self, id: int):
        return self.role_repo.get_by_id(id)
    
    def get(self, filters: dict = None):
        return self.role_repo.get(filters)
    
    def create_role(self, **kwargs):
        return self.role_repo.create_role(**kwargs)
    
    def update_role(self, id: int, data: dict):
        return self.role_repo.update_role(id, data)
    
    def delete_role(self, role_id: int):
        if not self.role_repo.get_by_id(role_id):
            raise ValueError()
        return self.role_repo.delete_role(role_id)
    
    def assign_permission(self, role_id, perm_id):
        if not self.role_repo.get_by_id(role_id) or not self.perm_repo.get_by_id(perm_id): 
            raise ValueError("No role_id or perm assigned ")
        return self.perm_repo.assign_permission(role_id, perm_id)
    
    def remove_permission(self, role_id, perm_id):
        if not self.role_repo.get_by_id(role_id) or not self.perm_repo.get_by_id(perm_id):  
            raise ValueError("Couldn't assign role_id or perm_id")
        return self.perm_repo.remove_permission(role_id, perm_id)
