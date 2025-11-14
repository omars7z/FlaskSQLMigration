service_registry = {}

#decorator, a service can have multiple repos
def register(name:str, repo:str = None):
    def wrapper(cls):
        service_registry[name] = (cls, repo)
        return cls
    return wrapper

def init_services(app, repositories: dict):
    for name, (ServiceClass, repo_names) in service_registry.items():
        if isinstance(repo_names, str):
            repo_dict = {repo_names: repositories.get(repo_names)}
        elif isinstance(repo_names, tuple):
            repo_dict = {r: repositories.get(r) for r in repo_names}
        else:
            repo_dict = {}

        if None in repo_dict.values():
            missing = [r for r, v in repo_dict.items() if v is None]
            print(f"Repository '{missing}' not found")

        instance = ServiceClass(repo_dict)
        setattr(app, f"{name.lower()}_service", instance)

    print("Registered services:", list(service_registry.keys()))


