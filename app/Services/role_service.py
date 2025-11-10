from app.Helpers.registry import register

@register("Role", repo=("User", "Role"))
class RoleServices:
    
    def __init__(self, repository):
        self.user_repo = repository.get("User")
        self.role_repo = repository.get("Role")
    
    def get_by_id(self, id: int):
        return self.role_repo.get_by_id(id)
    
    def get(self, filters: dict = None):
        return self.role_repo.get(filters)
    
    def create_user(self, **kwargs):
        return self.role_repo.create_user(**kwargs)
    
    def update_user(self, id: int, data: dict):
        return self.role_repo.update_user(id, data)
    
    def delete_user(self, user_id: int):
        if not self.role_repo.get_by_id(user_id):
            raise ValueError()
        return self.role_repo.delete_user(user_id)
    
    def assign_role(self, user_id: int, role_id: int):
        if not self.get_by_id(user_id) or not self.role_repo.get_by_id(role_id):
            raise ValueError()
        return self.role_repo.assign_role(user_id, role_id)
    
    def remove_role(self, user_id: int, role_id: int):
        if not self.user_repo.get_by_id(user_id) or not self.role_repo.get_by_id(role_id):
            raise ValueError()
        return self.role_repo.remove_role(user_id, role_id)
