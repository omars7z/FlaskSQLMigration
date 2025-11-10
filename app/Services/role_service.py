from app.Helpers.registry import register

@register("Role", repo="Role")
class RoleServices:
    def __init__(self, repositry):
        self.repo = repositry

    def get_by_id(self, id:int):
        return self.repo.get_by_id(id)
    
    def get(self, filters):
        return self.repo.get(filters)
    

    def create_role(self,**kwargs):
        return self.repo.create_role(**kwargs)
    
    def update_role(self, id, data):
        return self.repo.update_role(id, data)
    
    def delete_role(self, role_id):
        if not role_id:  
            return None
        return self.repo.delete_role(role_id)

    def assign_role(self, user_id, role_id):
        #...
        return self.repo.assign_role(user_id, role_id)
    
    def remove_role(self, user_id, role_id):
        if not self.get_by_id(user_id) or not self.get_by_id(role_id):  
            raise ValueError()
        return self.repo.remove_role(user_id, role_id)