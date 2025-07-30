"""Base SQLAlchemy model with CRUD operations."""

from functools import wraps

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import desc, asc, and_, delete
from sqlalchemy.inspection import inspect
from sqlalchemy.orm.attributes import InstrumentedAttribute
from lecrapaud.db.session import get_db


def with_db(func):
    """Decorator to allow passing an optional db session"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        db = kwargs.pop("db", None)
        if db:
            return func(*args, db=db, **kwargs)
        with get_db() as db:
            return func(*args, db=db, **kwargs)

    return wrapper


# declarative base class
class Base(DeclarativeBase):
    @classmethod
    @with_db
    def create(cls, db, **kwargs):
        instance = cls(**kwargs)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance

    @classmethod
    @with_db
    def get(cls, id: int, db=None):
        return db.get(cls, id)

    @classmethod
    @with_db
    def find_by(cls, db=None, **kwargs):
        return db.query(cls).filter_by(**kwargs).first()

    @classmethod
    @with_db
    def get_all(
        cls, raw=False, db=None, limit: int = 100, order: str = "desc", **kwargs
    ):
        order_by_field = (
            desc(cls.created_at) if order == "desc" else asc(cls.created_at)
        )

        query = db.query(cls)

        # Apply filters from kwargs
        for key, value in kwargs.items():
            if hasattr(cls, key):
                query = query.filter(getattr(cls, key) == value)

        results = query.order_by(order_by_field).limit(limit).all()

        if raw:
            return [
                {
                    column.name: getattr(row, column.name)
                    for column in cls.__table__.columns
                }
                for row in results
            ]

        return results

    @classmethod
    @with_db
    def filter(cls, db=None, **kwargs):
        filters = []

        for key, value in kwargs.items():
            if "__" in key:
                field, op = key.split("__", 1)
            else:
                field, op = key, "eq"

            if not hasattr(cls, field):
                raise ValueError(f"{field} is not a valid field on {cls.__name__}")

            column: InstrumentedAttribute = getattr(cls, field)

            if op == "eq":
                filters.append(column == value)
            elif op == "in":
                filters.append(column.in_(value))
            elif op == "gt":
                filters.append(column > value)
            elif op == "lt":
                filters.append(column < value)
            elif op == "gte":
                filters.append(column >= value)
            elif op == "lte":
                filters.append(column <= value)
            else:
                raise ValueError(f"Unsupported operator: {op}")

        return db.query(cls).filter(and_(*filters)).all()

    @classmethod
    @with_db
    def update(cls, id: int, db=None, **kwargs):
        instance = db.get(cls, id)
        if not instance:
            return None
        for key, value in kwargs.items():
            setattr(instance, key, value)
        db.commit()
        db.refresh(instance)
        return instance

    @classmethod
    @with_db
    def upsert(cls, match_fields: list[str], db=None, **kwargs):
        """
        Upsert an instance of the model: update if found, else create.

        :param match_fields: list of field names to use for matching
        :param kwargs: all fields for creation or update
        """
        filters = [
            getattr(cls, field) == kwargs[field]
            for field in match_fields
            if field in kwargs
        ]

        instance = db.query(cls).filter(*filters).first()

        if instance:
            for key, value in kwargs.items():
                setattr(instance, key, value)
        else:
            instance = cls(**kwargs)
            db.add(instance)

        db.commit()
        db.refresh(instance)
        return instance

    @classmethod
    @with_db
    def delete(cls, id: int, db=None):
        instance = db.get(cls, id)
        if instance:
            db.delete(instance)
            db.commit()
            return True
        return False

    @classmethod
    @with_db
    def delete_all(cls, db=None, **kwargs):
        stmt = delete(cls)

        for key, value in kwargs.items():
            if hasattr(cls, key):
                stmt = stmt.where(getattr(cls, key) == value)

        db.execute(stmt)
        db.commit()
        return True

    @with_db
    def save(self, db=None):
        self = db.merge(self)
        db.add(self)
        db.commit()
        db.refresh(self)
        return self

    def to_json(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
