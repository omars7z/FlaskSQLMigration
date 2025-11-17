
class RoleMapper:

    @staticmethod
    def to_dict(role):
        if not role:
            return None

        return {
            "id": role.id,
            "name": role.name,
            "flags": role.to_dict_flags(),
            "flag": role.flag,
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
            ]
        }

    @staticmethod
    def to_list(roles):
        if not roles:
            return []
        return [RoleMapper.to_dict(role) for role in roles]
