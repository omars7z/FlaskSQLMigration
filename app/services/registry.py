service_registry = {}
# service_registry = {'Datatype': <class 'app.services.datatype_service.DatatypeService'>},
# name = 'Datatype'

#decorator
def register(name: str): 
    def wrapper(cls):
        service_registry[name] = cls
        return cls
    return wrapper


def init_services(app, repositories: dict):
    for name, ServiceClass in service_registry.items():
        repo = repositories.get(name)
        print(" REGistered so far: ", repo)
        if not repo:
            raise ValueError(f"Repository '{name}' not found")

        instance = ServiceClass(repo) #dependency inversion
        setattr(app, f"{name.lower()}_service", instance)
