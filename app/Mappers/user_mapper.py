
class UserMapper:

    @staticmethod
    def to_dict(user):
        if not user:
            return None

        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "flag": user.flag,
            "flags":  user.to_dict_flags(),
            "roles": [
                {
                    "id": role.id,
                    "name": role.name,
                    "permissions": [
                        {
                            "id": perm.id,
                            "name": perm.name,
                            "resource": perm.resource,
                            "action": perm.action,
                            "description": perm.description,
                        }
                        for perm in role.permissions
                    ],
                }
                for role in user.roles
            ],
        }

    @staticmethod
    def to_list(users):
        return [UserMapper.to_dict(user) for user in users]

