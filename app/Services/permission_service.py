from flask import current_app

from app.Helpers.registry import register

@register("Permission", repo="Permission")
class PermissionServices:
    
    
    def __init__(self, repositry):
        self.repo = repositry
        
    def get_by_id(self, id):
        return self.repo.get_by_id(id)

    def get(self, filters):
        return self.repo.get(filters)
    
    def create_permission(self,**kwargs):
        return self.repo.create_permission(**kwargs)
    
    def update_permission(self, id, data):
        return self.repo.update_permission(id, data)
    
    def delete_permission(self, perm_id):
        if not self.get_by_id(perm_id): 
            raise ValueError()
        return self.repo.delete_permission(perm_id)

    def assign_permission(self, role_id, perm_id):
        if not self.get_by_id(role_id) or not self.get_by_id(perm_id): 
            raise ValueError()
            # return None
        return self.repo.assign_permission(role_id, perm_id)
    
    def remove_permission(self, role_id, perm_id):
        if not self.get_by_id(role_id) or not self.get_by_id(perm_id):  
            raise ValueError()
        return self.repo.remove_permission(role_id, perm_id)