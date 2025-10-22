from sqlalchemy import event
from app.models.datatype import Datatype 
from app.models.flags import Flag
        
        
# @event.listens_for(Datatype, "before_insert")
# def validate_on_insert(mapper, connection, target):
#     if target.flag < 0:
#         raise ValueError("Flag cannot be negative")

@event.listens_for(Datatype, "before_delete")
def prevent_default_delete(mapper, connection, target):
    if not target.can_delete:
        raise ValueError(f"Cannot delete datatype '{target.name}' due to flag restriction")

    if target.flag & Flag.CAN_ADD:
        print(f"'{target.name}' + add operation")
       

