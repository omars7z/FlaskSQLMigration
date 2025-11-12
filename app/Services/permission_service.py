from app.Helpers.registry import register

@register("Permission", repo=("Permission", "Role"))
class PermissionServices:
    
    def __init__(self, repositry):
        self.perm_repo = repositry.get("Permission")
        self.role_repo = repositry.get("Role")
        
    def get_by_id(self, id):
        return self.perm_repo.get_by_id(id)

    def get(self, filters):
        return self.perm_repo.get(filters)
    
    def create_permission(self,**kwargs):
        return self.perm_repo.create_permission(**kwargs)
    
    def update_permission(self, id, data):
        if not self.get_by_id(id):
            raise ValueError(f"Permission with id={id} not found")
        return self.perm_repo.update_permission(id, data)
    
    def delete_permission(self, perm_id):
        if not self.get_by_id(perm_id): 
            raise ValueError(f"Permission with id={perm_id} not found")
        return self.perm_repo.delete_permission(perm_id)

    