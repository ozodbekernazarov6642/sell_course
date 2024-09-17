from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
        )

    async def execute(
            self,
            command,
            *args,
            fetch: bool = False,
            fetchval: bool = False,
            fetchrow: bool = False,
            execute: bool = False,
    ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_sell_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS sell_course_user (
        id VARCHAR NOT NULL,
        full_name VARCHAR(255) NOT NULL,
        phone_number VARCHAR(20) NOT NULL,
        description VARCHAR(255) NOT NULL,
        course_sell_time VARCHAR NOT NULL,
        user_name VARCHAR(255) NOT NULL,
        price VARCHAR(255) NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args_sell_course_user(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def add_sell_course_user(self, id: str, full_name: str, phone_number: str, description: str,
                                   course_sell_time: str, user_name: str, price: str):
        sql = "INSERT INTO sell_course_user (id, full_name, phone_number, description, course_sell_time, user_name, price) VALUES($1, $2, $3, $4, $5, $6, $7) returning *"
        return await self.execute(sql, id, full_name, phone_number, description, course_sell_time, user_name, price,
                                  fetchrow=True)

    async def select_all_sell_course_users(self):
        sql = "SELECT * FROM sell_course_user"
        return await self.execute(sql, fetch=True)

    async def select_sell_course_user(self, **kwargs):
        sql = "SELECT * FROM sell_course_user WHERE "
        sql, parameters = self.format_args_user(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_sell_course_users(self):
        sql = "SELECT COUNT(*) FROM sell_course_user"
        return await self.execute(sql, fetchval=True)

    async def delete_sell_course_users(self):
        await self.execute("DELETE FROM sell_course_user WHERE TRUE", execute=True)

    async def drop_sell_course_users(self):
        await self.execute("DROP TABLE sell_course_user", execute=True)

    async def create_table_con_sell_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS con_sell_course_user (
        id VARCHAR NOT NULL,
        full_name VARCHAR(255) NOT NULL,
        phone_number VARCHAR(20) NOT NULL,
        description VARCHAR(255) NOT NULL,
        course_sell_time VARCHAR NOT NULL,
        user_name VARCHAR(255) NOT NULL,
        price VARCHAR(255) NOT NULL,
        con_time VARCHAR(255) NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args_con_sell_course_user(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def add_con_sell_course_user(self, id: str, full_name: str, phone_number: str, description: str,
                                       course_sell_time: str, user_name: str, price: str, con_time: str):
        sql = "INSERT INTO con_sell_course_user (id, full_name, phone_number, description, course_sell_time, user_name, price, con_time) VALUES($1, $2, $3, $4, $5, $6, $7, $8) returning *"
        return await self.execute(sql, id, full_name, phone_number, description, course_sell_time, user_name, price,
                                  con_time,
                                  fetchrow=True)

    async def select_all_con_sell_course_users(self):
        sql = "SELECT * FROM con_sell_course_user"
        return await self.execute(sql, fetch=True)

    async def select_con_sell_course_user(self, **kwargs):
        sql = "SELECT * FROM con_sell_course_user WHERE "
        sql, parameters = self.format_args_user(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_con_sell_course_users(self):
        sql = "SELECT COUNT(*) FROM con_sell_course_user"
        return await self.execute(sql, fetchval=True)

    async def delete_con_sell_course_users(self):
        await self.execute("DELETE FROM con_sell_course_user WHERE TRUE", execute=True)

    async def drop_con_sell_course_users(self):
        await self.execute("DROP TABLE con_sell_course_user", execute=True)

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users(
            id VARCHAR PRIMARY KEY,
            full_name VARCHAR(255) NOT NULL,
            phone_number VARCHAR(20) NOT NULL,
            date_time VARCHAR NOT NULL,
            user_name VARCHAR(255) NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args_user(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def add_user(self, id: str, full_name: str, phone_number: str, date_time: str,
                       user_name: str):
        sql = "INSERT INTO Users (id, full_name, phone_number, date_time, user_name) VALUES($1, $2, $3, $4, $5) returning *"
        return await self.execute(sql, id, full_name, phone_number, date_time, user_name, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args_user(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)

