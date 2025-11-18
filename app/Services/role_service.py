from app.Helpers.registry import register

@register("Role", repo=("Role", "Permission"))
class RoleService:

    def __init__(self, repository):
        self.role_repo = repository.get("Role")
        self.perm_repo = repository.get("Permission")

    def get_by_id(self, role_id: int):
        role = self.role_repo.get_by_id(role_id)
        if not role:
            return False
        return role

    def get(self, filters: dict = None):
        return self.role_repo.get(filters)

    def create_role(self, **kwargs):
        return self.role_repo.create_role(**kwargs)

    def update_role(self, role_id: int, data: dict):
        if not self.role_repo.get_by_id(role_id):
            raise ValueError(f"Role id {role_id} not found")
        return self.role_repo.update_role(role_id, data)

    def delete_role(self, role_id: int):
        if not self.role_repo.get_by_id(role_id):
            raise ValueError(f"Role id {role_id} not found")
        return self.role_repo.delete_role(role_id)


    def assign_permission(self, role_id: int, perm_id: int):
        role = self.role_repo.get_by_id(role_id)
        perm = self.perm_repo.get_by_id(perm_id)
        if not role or not perm:
            raise ValueError("Role or permission not found")
        return self.role_repo.assign_permission(role_id, perm_id)


    def remove_permission(self, role_id: int, perm_id: int):
        role = self.role_repo.get_by_id(role_id)
        perm = self.perm_repo.get_by_id(perm_id)
        if not role or not perm:
            raise ValueError("Role or permission not found")
        return self.role_repo.remove_permission(role_id, perm_id)
