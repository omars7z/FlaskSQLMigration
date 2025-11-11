from typing import List, Dict, Any
from app.Models.role import Role

class RoleMapper:

    @staticmethod
    def to_dict(role: Role) -> Dict[str, Any]:
        if not role:
            return None

        return {
            "id": role.id,
            "name": role.name,
            "description": role.description,
            "permissions": [
                {
                    "id": perm.id,
                    "name": perm.name,
                    "resource": perm.resource,
                    "action": perm.action,
                    "description": getattr(perm, "description", None),
                }
                for perm in role.permissions
            ],
            "users": [
                {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email
                }
                for user in getattr(role, "users", [])
            ]
        }

    @staticmethod
    def to_list(roles: List[Role]) -> List[Dict[str, Any]]:
        return [RoleMapper.to_dict(role) for role in roles]
