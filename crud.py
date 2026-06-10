from decimal import Decimal

from sqlalchemy import delete, func, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from database import SessionLocal
from models import Department, Employee, Project, EmployeeProfile
from datetime import date

def create_department(name: str):
    with SessionLocal() as session:
        try:
            department = Department(name=name)
            session.add(department)
            session.commit()
            session.refresh(department)
            return department
        except IntegrityError:
            session.rollback()
            return None


def create_employee(
    name: str,
    salary: Decimal,
    department_id: int | None = None,
):
    with SessionLocal() as session:
        try:
            employee = Employee(
                name=name,
                salary=salary,
                department_id=department_id,
            )
            session.add(employee)
            session.commit()
            session.refresh(employee)
            return employee
        except IntegrityError:
            session.rollback()
            return None


def create_project(
    name: str,
    budget: Decimal,
    employee_id: int | None = None,
):
    with SessionLocal() as session:
        try:
            project = Project(
                name=name,
                budget=budget,
                employee_id=employee_id,
            )
            session.add(project)
            session.commit()
            session.refresh(project)
            return project
        except IntegrityError:
            session.rollback()
            return None


def get_all_departments():
    with SessionLocal() as session:
        stmt = select(Department)
        return session.execute(stmt).scalars().all()


def get_all_employees():
    with SessionLocal() as session:
        stmt = select(Employee)
        return session.execute(stmt).scalars().all()

def get_employee(emp_id: int):
    with SessionLocal() as session:
        emp = session.get(Employee, emp_id)

        stmt = select(Employee).options(joinedload(Employee.profile)).where(Employee.id == emp_id)

        return session.execute(stmt).scalar_one_or_none()

def create_employee_profile(emp_id):
    with SessionLocal() as session:
        emp = session.get(Employee, emp_id)

        if emp is None:
            return None

        profile = EmployeeProfile(
            employee_id=emp_id,
            phone="+70000000001",
            address="Moscow",
            birth_date=date(1995, 5, 20),
        )

        session.add(profile)
        session.commit()

        return profile


def get_all_projects():
    with SessionLocal() as session:
        stmt = select(Project)
        return session.execute(stmt).scalars().all()


def update_employee_salary(employee_id: int, new_salary: Decimal):
    with SessionLocal() as session:
        employee = session.get(Employee, employee_id)

        if employee is None:
            return None

        employee.salary = new_salary
        session.commit()
        session.refresh(employee)

        return employee


def deactivate_project(project_id: int):
    with SessionLocal() as session:
        project = session.get(Project, project_id)

        if project is None:
            return None

        project.is_active = False
        session.commit()
        session.refresh(project)

        return project


def delete_project(project_id: int):
    with SessionLocal() as session:
        project = session.get(Project, project_id)

        if project is None:
            return False

        session.delete(project)
        session.commit()

        return True


def get_employees_with_department_names():
    with SessionLocal() as session:
        stmt = (
            select(Employee.name, Department.name)
            .join(Department, Employee.department_id == Department.id)
        )

        return session.execute(stmt).all()


def get_projects_employees_departments():
    with SessionLocal() as session:
        stmt = (
            select(
                Project.name.label("project_name"),
                Employee.name.label("employee_name"),
                Department.name.label("department_name"),
            )
            .join(Employee, Project.employee_id == Employee.id)
            .join(Department, Employee.department_id == Department.id)
        )

        return session.execute(stmt).all()


def count_employees():
    with SessionLocal() as session:
        stmt = select(func.count(Employee.id))
        return session.execute(stmt).scalar()