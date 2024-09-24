from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Модель таблицы для персонажей
class Character(Base):
    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True, index=True)
    birth_year = Column(String)
    eye_color = Column(String)
    films = Column(String)
    gender = Column(String)
    hair_color = Column(String)
    height = Column(String)
    homeworld = Column(String)
    mass = Column(String)
    name = Column(String)
    skin_color = Column(String)
    species = Column(String)
    starships = Column(String)
    vehicles = Column(String)


# Создание базы данных
def create_database():
    engine = create_engine('sqlite:///starwars.db')
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_database()
