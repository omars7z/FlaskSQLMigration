
class PermMapper:
    @staticmethod
    def to_dict(permission):
        if not permission:
            return None

        return {
            "id": permission.id,
            "name": permission.name,
            "resource": permission.resource,
            "action": permission.action,
            "flag": permission.flag,
            "description": permission.description,
        }

    @staticmethod
    def to_list(permissions):
        if not permissions:
            return []
        return [PermMapper.to_dict(p) for p in permissions]
