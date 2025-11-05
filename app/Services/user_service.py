from app.Helpers.registry import register

@register("User", repo="User")
class UserServices:
    
    def __init__(self, repositry):
        self.repo = repositry
        
    def get_by_id(self, id:int):
        return self.repo.get_by_id(id)
    
    def get(self, filters):
        return self.repo.get(filters)
        
    def create_user(self, name, email, current_user):
        if current_user and not current_user.to_dict_flags().get("isSuperAdmin"):
            raise PermissionError("can't create user unless Super Admin")
        return self.repo.create_user(name, email)
      
    
    def delete_user(self, id):
        return self.repo.delete_user(id)