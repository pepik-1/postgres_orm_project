from database import SessionLocal
from models import Department

def create_departament(name:str):
    with SessionLocal() as session:
        department = Department(name=name)
        
        session.add(department)
        session.commit()
        session.refresh(department)

        return department

department = create_departament('Test')
print(department.id,department.name)