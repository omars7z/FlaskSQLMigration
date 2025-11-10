from app.Helpers.registry import register

@register("User", repo="User")
class UserServices:
    
    def __init__(self, repositry):
        self.user_repo = repositry.get("User")
        
    def get_by_id(self, id:int):
        return self.user_repo.get_by_id(id)
    
    def get(self, filters):
        return self.user_repo.get(filters)
        
    def create_user(self, name, email):
        return self.user_repo.create_user(name, email)
      
    def delete_user(self, id):
        return self.user_repo.delete_user(id)