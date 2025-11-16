from app.Helpers.registry import register

@register("Role", repo=("Role", "Permission"))
class RoleServices:
    
    def __init__(self, repository):
        self.role = repository.get("Role")
        self.perm = repository.get("Permission")
    
    def get_by_id(self, id: int):
        return self.role.get_by_id(id)
    
    def get(self, filters: dict = None):
        return self.role.get(filters)
    
    def create_role(self, **kwargs):
        return self.role.create_role(**kwargs)
    
    def update_role(self, id: int, data: dict):
        if not self.role.get_by_id(id):
            raise ValueError(f"role id {id} not found")
        return self.role.update_role(id, data)
    
    def delete_role(self, role_id: int):
        if not self.role.get_by_id(role_id):
            raise ValueError(f"Role id {role_id} not found")
        return self.role.delete_role(role_id)
    
    def assign_permission(self, role_id, perm_id):
        if not self.role.get_by_id(role_id) or not self.perm.get_by_id(perm_id): 
            raise ValueError("No role_id or perm assigned ")
        return self.role.assign_permission(role_id, perm_id)
    
    def remove_permission(self, role_id, perm_id):
        if not self.role.get_by_id(role_id) or not self.perm.get_by_id(perm_id):  
            raise ValueError("Couldn't remove role_id or perm_id")
        return self.role.remove_permission(role_id, perm_id)
