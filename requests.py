import asyncio
import aiohttp
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import insert
from models import Character

# Подключение к базе данных
DATABASE_URL = 'sqlite+aiosqlite:///starwars.db'
engine = create_async_engine(DATABASE_URL, echo=True)

# Асинхронная сессия
async_session = sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)


# Функция для выполнения запроса по URL и извлечения названия
async def fetch_name(session, url):
    async with session.get(url) as response:
        data = await response.json()
        return data.get("title") or data.get("name")


# Функция для преобразования списка URL в строку с названиями через запятую
async def fetch_names(session, urls):
    names = []
    for url in urls:
        name = await fetch_name(session, url)
        names.append(name)
    return ', '.join(names)


# Функция для получения данных о персонаже
async def fetch_character(session, url):
    async with session.get(url) as response:
        return await response.json()


# Функция для преобразования данных из API в нужный формат
async def transform_data(session, data):
    films = await fetch_names(session, data.get("films", []))
    species = await fetch_names(session, data.get("species", []))
    starships = await fetch_names(session, data.get("starships", []))
    vehicles = await fetch_names(session, data.get("vehicles", []))

    # Получаем название планеты
    homeworld = await fetch_name(session, data.get("homeworld"))

    return {
        "id": data.get("id"),
        "birth_year": data.get("birth_year"),
        "eye_color": data.get("eye_color"),
        "films": films,
        "gender": data.get("gender"),
        "hair_color": data.get("hair_color"),
        "height": data.get("height"),
        "homeworld": homeworld,
        "mass": data.get("mass"),
        "name": data.get("name"),
        "skin_color": data.get("skin_color"),
        "species": species,
        "starships": starships,
        "vehicles": vehicles,
    }


# Асинхронная функция для загрузки данных в базу
async def save_character(character_data, session):
    async with session.begin():
        stmt = insert(Character).values(**character_data)
        await session.execute(stmt)


# Основная асинхронная функция для загрузки всех персонажей
async def main():
    async with aiohttp.ClientSession() as session:
        character_url = 'https://swapi.dev/api/people/'
        async with async_session() as db_session:
            while character_url:
                async with session.get(character_url) as response:
                    character_data = await response.json()
                    for character in character_data['results']:
                        transformed_data = await transform_data(session, character)
                        await save_character(transformed_data, db_session)
                # Переход на следующую страницу
                character_url = character_data.get('next')

# Запуск
if __name__ == '__main__':
    asyncio.run(main())
