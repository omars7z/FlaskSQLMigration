from app.Helpers.registry import register
from app.Mappers.user_mapper import UserMapper

@register("User", repo=("User","Role"))
class UserServices:
    
    def __init__(self, repositry):
        self.user = repositry.get("User")
        self.role = repositry.get("Role")

        
    def get_by_id(self, user_id: int):
        return self.user.get_by_id(user_id)
    
    def get(self, filters):
        return self.user.get(filters)
        
    def create_user(self, name, email):
        return self.user.create_user(name, email)
      
    def delete_user(self, id):
        user = self.user.get_by_id(id)
        if not user:
            raise ValueError(f"User with id={id} not found")  
        return self.user.delete_user(id)
    
    def assign_role(self, user_id: int, role_id: int):
        if not self.user.get_by_id(user_id) or not self.role.get_by_id(role_id):
            raise ValueError("user or role not found")
        return self.user.assign_role(user_id, role_id)
        
    
    def remove_role(self, user_id: int, role_id: int):
        user = self.user.get_by_id(user_id)
        role = self.role.get_by_id(role_id)
        if not user or not role:
            raise ValueError("user or role not found")
        if len(user.roles) <=1:
            raise ValueError("Cannt delete, User must have at least one role")
        return self.user.remove_role(user_id, role_id)