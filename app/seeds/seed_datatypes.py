import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.extensions import db
from app.models.datatype import Datatype

app = create_app("Development")

with app.app_context():
    default_data = [
        {"name": "Int", "info": "integer type"},
        {"name": "List", "info": "list type"},
        {"name": "Dict", "info": "Dict type"},
    ]

    for item in default_data:
        exists = Datatype.query.filter_by(name=item["name"]).first()
        if not exists:
            db.session.add(Datatype(**item))
        
        # stmt = insert(Datatype).values([
        # {"n..."},
        # ])
        # stmt = stmt.on_conflict_do_nothing(index_elements=["id"])  # or "name" if unique
        # db.session.execute(stmt)
        # db.session.commit()

    db.session.commit()
    print("added seed tables")

