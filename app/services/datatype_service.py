from app.models.flags import Flag

class DatatypeService():
    
    def __init__(self, repository):
        self.repo = repository
             
    def get_by_id(self, id):
        return self.repo.get_by_id(id)
    
    def get_by_name(self, name: str):
        return self.repo.get_by_name(name)
    
    def get_all(self):
        return self.repo.get_all()

    def create(self, data: dict):
        return self.repo.create(data)

        # Flag({ can_delete: data.can_delete }) ... permissions 
        # flag_fields = {k: data[k] for k in data if k in Flag.DEFAULT_FLAGS}
        
        # flag_obj = Flag(flag_fields)
        # data["flag"] = flag_obj.get_flag()
        
        # for key in flag_fields.keys():
        #     data.pop(key)
        
    

    def update(self, id, data: dict):
        dt = self.get_by_id(id)
        if not dt:
            return None
        flag_fields = {k: data[k] for k in data if k in Flag.DEFAULT_FLAGS}
        if flag_fields:
            flag_obj = Flag(flag_fields)
            data["flag"] = flag_obj.get_flag()
            #rmove flag fields from data before updating
            for k in flag_fields.keys():
                data.pop(k)
        return self.repo.update(id, data)  


    def delete(self, dt):
        if not dt.can_delete:
            raise ValueError(f"Cannot delete datatype '{dt.name}' due to flag restriction")
        self.repo.delete(dt)
