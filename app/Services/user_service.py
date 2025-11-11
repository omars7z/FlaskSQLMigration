from app.Helpers.registry import register
from app.Mappers.user_mapper import UserMapper

@register("User", repo=("User","Role"))
class UserServices:
    
    def __init__(self, repositry):
        self.user_repo = repositry.get("User")
        self.role_repo = repositry.get("Role")

        
    def get_by_id(self, user_id: int):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return None
        return UserMapper.to_dict(user)
    
    def get(self, filters):
        user = self.user_repo.get(filters)
        if not user:
            return []
        return UserMapper.to_list(user)
        
    def create_user(self, name, email):
        return self.user_repo.create_user(name, email)
      
    def delete_user(self, id):
        user = self.user_repo.get_by_id(id)
        if not user:
            raise ValueError(f"User with id={id} not found")  
        return self.user_repo.delete_user(id)
    
    def assign_role(self, user_id: int, role_id: int):
        if not self.user_repo.get_by_id(user_id) or not self.role_repo.get_by_id(role_id):
            raise ValueError("ser or role not found")
        return self.user_repo.assign_role(user_id, role_id)
        
    
    def remove_role(self, user_id: int, role_id: int):
        user = self.user_repo.get_by_id(user_id)
        role = self.role_repo.get_by_id(role_id)
        if not user or not role:
            raise ValueError("ser or role not found")
        if len(user.roles) <=1:
            raise ValueError("Cannt delete, User must have at least one role")
        return self.user_repo.remove_role(user_id, role_id)