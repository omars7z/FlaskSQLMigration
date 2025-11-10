service_registry = {}

#decorator, a service can have multiple repos
def register(name:str, repo:str = None):
    def wrapper(cls):
        service_registry[name] = (cls, repo)
        return cls
    return wrapper

def init_services(app, repositories: dict):
    for name, (ServiceClass, repo_name) in service_registry.items():
        # print(str(ServiceClass) +' '+ repo_name)
        repo = repositories.get(repo_name)
        if not repo:
            raise ValueError(f"Repository '{repo}' not found")
        instance = ServiceClass(repo)
        setattr(app, f"{name.lower()}_service", instance)
    
    print("Registered services:", list(service_registry.keys()))

