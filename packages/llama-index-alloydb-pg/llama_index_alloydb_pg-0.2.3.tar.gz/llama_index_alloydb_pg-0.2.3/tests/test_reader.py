# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os
import uuid
from typing import Sequence

import pytest
import pytest_asyncio
from llama_index.core.schema import Document
from sqlalchemy import RowMapping, text

from llama_index_alloydb_pg import AlloyDBEngine, AlloyDBReader

default_table_name_async = "async_reader_test_" + str(uuid.uuid4())
default_table_name_sync = "sync_reader_test_" + str(uuid.uuid4())


async def aexecute(
    engine: AlloyDBEngine,
    query: str,
) -> None:
    async def run(engine, query):
        async with engine._pool.connect() as conn:
            await conn.execute(text(query))
            await conn.commit()

    await engine._run_as_async(run(engine, query))


async def afetch(engine: AlloyDBEngine, query: str) -> Sequence[RowMapping]:
    async def run(engine, query):
        async with engine._pool.connect() as conn:
            result = await conn.execute(text(query))
            result_map = result.mappings()
            result_fetch = result_map.fetchall()
        return result_fetch

    return await engine._run_as_async(run(engine, query))


def get_env_var(key: str, desc: str) -> str:
    v = os.environ.get(key)
    if v is None:
        raise ValueError(f"Must set env var {key} to: {desc}")
    return v


@pytest.mark.asyncio(loop_scope="class")
class TestAlloyDBReaderAsync:
    @pytest.fixture(scope="module")
    def db_project(self) -> str:
        return get_env_var("PROJECT_ID", "project id for google cloud")

    @pytest.fixture(scope="module")
    def db_region(self) -> str:
        return get_env_var("REGION", "region for AlloyDB instance")

    @pytest.fixture(scope="module")
    def db_cluster(self) -> str:
        return get_env_var("CLUSTER_ID", "cluster for AlloyDB")

    @pytest.fixture(scope="module")
    def db_instance(self) -> str:
        return get_env_var("INSTANCE_ID", "instance for AlloyDB")

    @pytest.fixture(scope="module")
    def db_name(self) -> str:
        return get_env_var("DATABASE_ID", "database name on AlloyDB instance")

    @pytest.fixture(scope="module")
    def user(self) -> str:
        return get_env_var("DB_USER", "database user for AlloyDB")

    @pytest.fixture(scope="module")
    def password(self) -> str:
        return get_env_var("DB_PASSWORD", "database password for AlloyDB")

    @pytest_asyncio.fixture(scope="class")
    async def async_engine(
        self,
        db_project,
        db_region,
        db_cluster,
        db_instance,
        db_name,
    ):
        async_engine = await AlloyDBEngine.afrom_instance(
            project_id=db_project,
            instance=db_instance,
            cluster=db_cluster,
            region=db_region,
            database=db_name,
        )

        yield async_engine

        await aexecute(
            async_engine, f'DROP TABLE IF EXISTS "{default_table_name_async}"'
        )

        await async_engine.close()

    async def _cleanup_table(self, engine):
        await aexecute(engine, f'DROP TABLE IF EXISTS "{default_table_name_async}"')

    async def _collect_async_items(self, docs_generator):
        """Collects items from an async generator."""
        docs = []
        async for doc in docs_generator:
            docs.append(doc)
        return docs

    async def test_create_reader_with_invalid_parameters(self, async_engine):
        with pytest.raises(ValueError):
            await AlloyDBReader.create(
                engine=async_engine,
            )
        with pytest.raises(ValueError):

            def fake_formatter():
                return None

            await AlloyDBReader.create(
                engine=async_engine,
                table_name=default_table_name_async,
                format="text",
                formatter=fake_formatter,
            )
        with pytest.raises(ValueError):
            await AlloyDBReader.create(
                engine=async_engine,
                table_name=default_table_name_async,
                format="fake_format",
            )

    async def test_load_from_query_default(self, async_engine):
        table_name = "test-table" + str(uuid.uuid4())
        query = f"""
                CREATE TABLE IF NOT EXISTS "{table_name}" (
                    fruit_id SERIAL PRIMARY KEY,
                    fruit_name VARCHAR(100) NOT NULL,
                    variety VARCHAR(50),
                    quantity_in_stock INT NOT NULL,
                    price_per_unit INT NOT NULL,
                    organic INT NOT NULL
                )
            """
        await aexecute(async_engine, query)

        insert_query = f"""
            INSERT INTO "{table_name}" (
                fruit_name, variety, quantity_in_stock, price_per_unit, organic
            ) VALUES ('Apple', 'Granny Smith', 150, 1, 1);
        """
        await aexecute(async_engine, insert_query)

        reader = await AlloyDBReader.create(
            engine=async_engine,
            table_name=table_name,
        )

        documents = await self._collect_async_items(reader.alazy_load_data())

        expected_document = Document(
            text="1",
            metadata={
                "fruit_name": "Apple",
                "variety": "Granny Smith",
                "quantity_in_stock": 150,
                "price_per_unit": 1,
                "organic": 1,
            },
        )

        assert documents[0].text == expected_document.text
        assert documents[0].metadata == expected_document.metadata

        await aexecute(async_engine, f'DROP TABLE IF EXISTS "{table_name}"')

    async def test_load_from_query_customized_content_customized_metadata(
        self, async_engine
    ):
        table_name = "test-table" + str(uuid.uuid4())
        expected_docs = [
            Document(
                text="Apple Smith 150 1 1",
                metadata={"fruit_id": 1},
            ),
            Document(
                text="Banana Cavendish 200 1 0",
                metadata={"fruit_id": 2},
            ),
            Document(
                text="Orange Navel 80 1 1",
                metadata={"fruit_id": 3},
            ),
        ]
        query = f"""
                CREATE TABLE IF NOT EXISTS "{table_name}" (
                    fruit_id SERIAL PRIMARY KEY,
                    fruit_name VARCHAR(100) NOT NULL,
                    variety VARCHAR(50),
                    quantity_in_stock INT NOT NULL,
                    price_per_unit INT NOT NULL,
                    organic INT NOT NULL
                )
            """
        await aexecute(async_engine, query)

        insert_query = f"""
            INSERT INTO "{table_name}" (fruit_name, variety, quantity_in_stock, price_per_unit, organic)
            VALUES ('Apple', 'Smith', 150, 0.99, 1),
                    ('Banana', 'Cavendish', 200, 0.59, 0),
                    ('Orange', 'Navel', 80, 1.29, 1);
        """
        await aexecute(async_engine, insert_query)

        reader = await AlloyDBReader.create(
            engine=async_engine,
            query=f'SELECT * FROM "{table_name}";',
            content_columns=[
                "fruit_name",
                "variety",
                "quantity_in_stock",
                "price_per_unit",
                "organic",
            ],
            metadata_columns=["fruit_id"],
        )

        documents = await self._collect_async_items(reader.alazy_load_data())

        # Compare the full list of documents to make sure all are in sync.
        for expected, actual in zip(expected_docs, documents):
            assert expected.text == actual.text
            assert expected.metadata == actual.metadata

        await aexecute(async_engine, f'DROP TABLE IF EXISTS "{table_name}"')

    async def test_load_from_query_customized_content_default_metadata(
        self, async_engine
    ):
        table_name = "test-table" + str(uuid.uuid4())
        query = f"""
                CREATE TABLE IF NOT EXISTS "{table_name}" (
                    fruit_id SERIAL PRIMARY KEY,
                    fruit_name VARCHAR(100) NOT NULL,
                    variety VARCHAR(50),
                    quantity_in_stock INT NOT NULL,
                    price_per_unit INT NOT NULL,
                    organic INT NOT NULL
                )
            """
        await aexecute(async_engine, query)

        insert_query = f"""
            INSERT INTO "{table_name}" (fruit_name, variety, quantity_in_stock, price_per_unit, organic)
            VALUES ('Apple', 'Granny Smith', 150, 1, 1);
        """
        await aexecute(async_engine, insert_query)

        reader = await AlloyDBReader.create(
            engine=async_engine,
            query=f'SELECT * FROM "{table_name}";',
            content_columns=[
                "variety",
                "quantity_in_stock",
                "price_per_unit",
            ],
        )

        documents = await self._collect_async_items(reader.alazy_load_data())

        expected_text_docs = [
            Document(
                text="Granny Smith 150 1",
                metadata={"fruit_id": 1, "fruit_name": "Apple", "organic": 1},
            )
        ]

        for expected, actual in zip(expected_text_docs, documents):
            assert expected.text == actual.text
            assert expected.metadata == actual.metadata

        reader = await AlloyDBReader.create(
            engine=async_engine,
            query=f'SELECT * FROM "{table_name}";',
            content_columns=[
                "variety",
                "quantity_in_stock",
                "price_per_unit",
            ],
            format="JSON",
        )

        actual_documents = await self._collect_async_items(reader.alazy_load_data())

        expected_docs = [
            Document(
                text='{"variety": "Granny Smith", "quantity_in_stock": 150, "price_per_unit": 1}',
                metadata={
                    "fruit_id": 1,
                    "fruit_name": "Apple",
                    "organic": 1,
                },
            )
        ]

        for expected, actual in zip(expected_docs, actual_documents):
            assert expected.text == actual.text
            assert expected.metadata == actual.metadata

        await aexecute(async_engine, f'DROP TABLE IF EXISTS "{table_name}"')

    async def test_load_from_query_with_json(self, async_engine):

        table_name = "test-table" + str(uuid.uuid4())
        query = f"""
            CREATE TABLE IF NOT EXISTS "{table_name}"(
                fruit_id SERIAL PRIMARY KEY,
                fruit_name VARCHAR(100) NOT NULL,
                variety JSON NOT NULL,
                quantity_in_stock INT NOT NULL,
                price_per_unit INT NOT NULL,
                li_metadata JSON NOT NULL
            )
            """
        await aexecute(async_engine, query)

        metadata = json.dumps({"organic": 1})
        variety = json.dumps({"type": "Granny Smith"})
        insert_query = f"""
            INSERT INTO "{table_name}"
            (fruit_name, variety, quantity_in_stock, price_per_unit, li_metadata)
            VALUES ('Apple', '{variety}', 150, 1, '{metadata}');"""
        await aexecute(async_engine, insert_query)

        reader = await AlloyDBReader.create(
            engine=async_engine,
            query=f'SELECT * FROM "{table_name}";',
            metadata_columns=[
                "variety",
            ],
        )

        documents = await self._collect_async_items(reader.alazy_load_data())

        expected_docs = [
            Document(
                text="1",
                metadata={
                    "variety": {"type": "Granny Smith"},
                    "organic": 1,
                },
            )
        ]

        for expected, actual in zip(expected_docs, documents):
            assert expected.text == actual.text
            assert expected.metadata == actual.metadata

        await aexecute(async_engine, f'DROP TABLE IF EXISTS "{table_name}"')

    async def test_load_from_query_customized_content_default_metadata_custom_formatter(
        self, async_engine
    ):

        table_name = "test-table" + str(uuid.uuid4())
        query = f"""
                CREATE TABLE IF NOT EXISTS "{table_name}" (
                    fruit_id SERIAL PRIMARY KEY,
                    fruit_name VARCHAR(100) NOT NULL,
                    variety VARCHAR(50),
                    quantity_in_stock INT NOT NULL,
                    price_per_unit INT NOT NULL,
                    organic INT NOT NULL
                )
            """
        await aexecute(async_engine, query)

        insert_query = f"""
                    INSERT INTO "{table_name}" (fruit_name, variety, quantity_in_stock, price_per_unit, organic)
                    VALUES ('Apple', 'Granny Smith', 150, 1, 1);
                    """
        await aexecute(async_engine, insert_query)

        def my_formatter(row, content_columns):
            return "-".join(
                str(row[column]) for column in content_columns if column in row
            )

        reader = await AlloyDBReader.create(
            engine=async_engine,
            query=f'SELECT * FROM "{table_name}";',
            content_columns=[
                "variety",
                "quantity_in_stock",
                "price_per_unit",
            ],
            formatter=my_formatter,
        )

        documents = await self._collect_async_items(reader.alazy_load_data())

        expected_documents = [
            Document(
                text="Granny Smith-150-1",
                metadata={
                    "fruit_id": 1,
                    "fruit_name": "Apple",
                    "organic": 1,
                },
            )
        ]

        for expected, actual in zip(expected_documents, documents):
            assert expected.text == actual.text
            assert expected.metadata == actual.metadata

        await aexecute(async_engine, f'DROP TABLE IF EXISTS "{table_name}"')

    async def test_load_from_query_customized_content_default_metadata_custom_page_content_format(
        self, async_engine
    ):
        table_name = "test-table" + str(uuid.uuid4())
        query = f"""
                CREATE TABLE IF NOT EXISTS "{table_name}" (
                    fruit_id SERIAL PRIMARY KEY,
                    fruit_name VARCHAR(100) NOT NULL,
                    variety VARCHAR(50),
                    quantity_in_stock INT NOT NULL,
                    price_per_unit INT NOT NULL,
                    organic INT NOT NULL
                )
            """
        await aexecute(async_engine, query)

        insert_query = f"""
                        INSERT INTO "{table_name}" (fruit_name, variety, quantity_in_stock, price_per_unit, organic)
                        VALUES ('Apple', 'Granny Smith', 150, 1, 1);
                    """
        await aexecute(async_engine, insert_query)

        reader = await AlloyDBReader.create(
            engine=async_engine,
            query=f'SELECT * FROM "{table_name}";',
            content_columns=[
                "variety",
                "quantity_in_stock",
                "price_per_unit",
            ],
            format="YAML",
        )

        documents = await self._collect_async_items(reader.alazy_load_data())

        expected_docs = [
            Document(
                text="variety: Granny Smith\nquantity_in_stock: 150\nprice_per_unit: 1",
                metadata={
                    "fruit_id": 1,
                    "fruit_name": "Apple",
                    "organic": 1,
                },
            )
        ]

        for expected, actual in zip(expected_docs, documents):
            assert expected.text == actual.text
            assert expected.metadata == actual.metadata

        await aexecute(async_engine, f'DROP TABLE IF EXISTS "{table_name}"')


@pytest.mark.asyncio(loop_scope="class")
class TestAlloyDBReaderSync:
    @pytest.fixture(scope="module")
    def db_project(self) -> str:
        return get_env_var("PROJECT_ID", "project id for google cloud")

    @pytest.fixture(scope="module")
    def db_region(self) -> str:
        return get_env_var("REGION", "region for AlloyDB instance")

    @pytest.fixture(scope="module")
    def db_cluster(self) -> str:
        return get_env_var("CLUSTER_ID", "cluster for AlloyDB")

    @pytest.fixture(scope="module")
    def db_instance(self) -> str:
        return get_env_var("INSTANCE_ID", "instance for AlloyDB")

    @pytest.fixture(scope="module")
    def db_name(self) -> str:
        return get_env_var("DATABASE_ID", "database name on AlloyDB instance")

    @pytest.fixture(scope="module")
    def user(self) -> str:
        return get_env_var("DB_USER", "database user for AlloyDB")

    @pytest.fixture(scope="module")
    def password(self) -> str:
        return get_env_var("DB_PASSWORD", "database password for AlloyDB")

    @pytest_asyncio.fixture(scope="class")
    async def sync_engine(
        self,
        db_project,
        db_region,
        db_cluster,
        db_instance,
        db_name,
    ):
        sync_engine = await AlloyDBEngine.afrom_instance(
            project_id=db_project,
            instance=db_instance,
            cluster=db_cluster,
            region=db_region,
            database=db_name,
        )

        yield sync_engine

        await aexecute(
            sync_engine, f'DROP TABLE IF EXISTS "{default_table_name_async}"'
        )

        await sync_engine.close()

    async def _cleanup_table(self, engine):
        await aexecute(engine, f'DROP TABLE IF EXISTS "{default_table_name_async}"')

    def _collect_items(self, docs_generator):
        """Collects items from a generator."""
        docs = []
        for doc in docs_generator:
            docs.append(doc)
        return docs

    async def test_create_reader_with_invalid_parameters(self, sync_engine):
        with pytest.raises(ValueError):
            AlloyDBReader.create_sync(
                engine=sync_engine,
            )
        with pytest.raises(ValueError):

            def fake_formatter():
                return None

            AlloyDBReader.create_sync(
                engine=sync_engine,
                table_name=default_table_name_async,
                format="text",
                formatter=fake_formatter,
            )
        with pytest.raises(ValueError):
            AlloyDBReader.create_sync(
                engine=sync_engine,
                table_name=default_table_name_async,
                format="fake_format",
            )

    async def test_load_from_query_default(self, sync_engine):
        table_name = "test-table" + str(uuid.uuid4())
        query = f"""
                CREATE TABLE IF NOT EXISTS "{table_name}" (
                    fruit_id SERIAL PRIMARY KEY,
                    fruit_name VARCHAR(100) NOT NULL,
                    variety VARCHAR(50),
                    quantity_in_stock INT NOT NULL,
                    price_per_unit INT NOT NULL,
                    organic INT NOT NULL
                )
            """
        await aexecute(sync_engine, query)

        insert_query = f"""
            INSERT INTO "{table_name}" (
                fruit_name, variety, quantity_in_stock, price_per_unit, organic
            ) VALUES ('Apple', 'Granny Smith', 150, 1, 1);
        """
        await aexecute(sync_engine, insert_query)

        reader = AlloyDBReader.create_sync(
            engine=sync_engine,
            table_name=table_name,
        )

        documents = self._collect_items(reader.lazy_load_data())

        expected_document = Document(
            text="1",
            metadata={
                "fruit_name": "Apple",
                "variety": "Granny Smith",
                "quantity_in_stock": 150,
                "price_per_unit": 1,
                "organic": 1,
            },
        )

        assert documents[0].text == expected_document.text
        assert documents[0].metadata == expected_document.metadata

        await aexecute(sync_engine, f'DROP TABLE IF EXISTS "{table_name}"')

    async def test_load_from_query_customized_content_customized_metadata(
        self, sync_engine
    ):
        table_name = "test-table" + str(uuid.uuid4())
        expected_docs = [
            Document(
                text="Apple Smith 150 1 1",
                metadata={"fruit_id": 1},
            ),
            Document(
                text="Banana Cavendish 200 1 0",
                metadata={"fruit_id": 2},
            ),
            Document(
                text="Orange Navel 80 1 1",
                metadata={"fruit_id": 3},
            ),
        ]
        query = f"""
                CREATE TABLE IF NOT EXISTS "{table_name}" (
                    fruit_id SERIAL PRIMARY KEY,
                    fruit_name VARCHAR(100) NOT NULL,
                    variety VARCHAR(50),
                    quantity_in_stock INT NOT NULL,
                    price_per_unit INT NOT NULL,
                    organic INT NOT NULL
                )
            """
        await aexecute(sync_engine, query)

        insert_query = f"""
            INSERT INTO "{table_name}" (fruit_name, variety, quantity_in_stock, price_per_unit, organic)
            VALUES ('Apple', 'Smith', 150, 0.99, 1),
                    ('Banana', 'Cavendish', 200, 0.59, 0),
                    ('Orange', 'Navel', 80, 1.29, 1);
        """
        await aexecute(sync_engine, insert_query)

        reader = AlloyDBReader.create_sync(
            engine=sync_engine,
            query=f'SELECT * FROM "{table_name}";',
            content_columns=[
                "fruit_name",
                "variety",
                "quantity_in_stock",
                "price_per_unit",
                "organic",
            ],
            metadata_columns=["fruit_id"],
        )

        documents = self._collect_items(reader.lazy_load_data())

        # Compare the full list of documents to make sure all are in sync.
        for expected, actual in zip(expected_docs, documents):
            assert expected.text == actual.text
            assert expected.metadata == actual.metadata

        await aexecute(sync_engine, f'DROP TABLE IF EXISTS "{table_name}"')

    async def test_load_from_query_customized_content_default_metadata(
        self, sync_engine
    ):
        table_name = "test-table" + str(uuid.uuid4())
        query = f"""
                CREATE TABLE IF NOT EXISTS "{table_name}" (
                    fruit_id SERIAL PRIMARY KEY,
                    fruit_name VARCHAR(100) NOT NULL,
                    variety VARCHAR(50),
                    quantity_in_stock INT NOT NULL,
                    price_per_unit INT NOT NULL,
                    organic INT NOT NULL
                )
            """
        await aexecute(sync_engine, query)

        insert_query = f"""
            INSERT INTO "{table_name}" (fruit_name, variety, quantity_in_stock, price_per_unit, organic)
            VALUES ('Apple', 'Granny Smith', 150, 1, 1);
        """
        await aexecute(sync_engine, insert_query)

        reader = AlloyDBReader.create_sync(
            engine=sync_engine,
            query=f'SELECT * FROM "{table_name}";',
            content_columns=[
                "variety",
                "quantity_in_stock",
                "price_per_unit",
            ],
        )

        documents = self._collect_items(reader.lazy_load_data())

        expected_text_docs = [
            Document(
                text="Granny Smith 150 1",
                metadata={"fruit_id": 1, "fruit_name": "Apple", "organic": 1},
            )
        ]

        for expected, actual in zip(expected_text_docs, documents):
            assert expected.text == actual.text
            assert expected.metadata == actual.metadata

        reader = AlloyDBReader.create_sync(
            engine=sync_engine,
            query=f'SELECT * FROM "{table_name}";',
            content_columns=[
                "variety",
                "quantity_in_stock",
                "price_per_unit",
            ],
            format="JSON",
        )

        actual_documents = self._collect_items(reader.lazy_load_data())

        expected_docs = [
            Document(
                text='{"variety": "Granny Smith", "quantity_in_stock": 150, "price_per_unit": 1}',
                metadata={
                    "fruit_id": 1,
                    "fruit_name": "Apple",
                    "organic": 1,
                },
            )
        ]

        for expected, actual in zip(expected_docs, actual_documents):
            assert expected.text == actual.text
            assert expected.metadata == actual.metadata

        await aexecute(sync_engine, f'DROP TABLE IF EXISTS "{table_name}"')

    async def test_load_from_query_with_json(self, sync_engine):

        table_name = "test-table" + str(uuid.uuid4())
        query = f"""
            CREATE TABLE IF NOT EXISTS "{table_name}"(
                fruit_id SERIAL PRIMARY KEY,
                fruit_name VARCHAR(100) NOT NULL,
                variety JSON NOT NULL,
                quantity_in_stock INT NOT NULL,
                price_per_unit INT NOT NULL,
                li_metadata JSON NOT NULL
            )
            """
        await aexecute(sync_engine, query)

        metadata = json.dumps({"organic": 1})
        variety = json.dumps({"type": "Granny Smith"})
        insert_query = f"""
            INSERT INTO "{table_name}"
            (fruit_name, variety, quantity_in_stock, price_per_unit, li_metadata)
            VALUES ('Apple', '{variety}', 150, 1, '{metadata}');"""
        await aexecute(sync_engine, insert_query)

        reader = AlloyDBReader.create_sync(
            engine=sync_engine,
            query=f'SELECT * FROM "{table_name}";',
            metadata_columns=[
                "variety",
            ],
        )

        documents = self._collect_items(reader.lazy_load_data())

        expected_docs = [
            Document(
                text="1",
                metadata={
                    "variety": {"type": "Granny Smith"},
                    "organic": 1,
                },
            )
        ]

        for expected, actual in zip(expected_docs, documents):
            assert expected.text == actual.text
            assert expected.metadata == actual.metadata

        await aexecute(sync_engine, f'DROP TABLE IF EXISTS "{table_name}"')

    async def test_load_from_query_customized_content_default_metadata_custom_formatter(
        self, sync_engine
    ):

        table_name = "test-table" + str(uuid.uuid4())
        query = f"""
                CREATE TABLE IF NOT EXISTS "{table_name}" (
                    fruit_id SERIAL PRIMARY KEY,
                    fruit_name VARCHAR(100) NOT NULL,
                    variety VARCHAR(50),
                    quantity_in_stock INT NOT NULL,
                    price_per_unit INT NOT NULL,
                    organic INT NOT NULL
                )
            """
        await aexecute(sync_engine, query)

        insert_query = f"""
                    INSERT INTO "{table_name}" (fruit_name, variety, quantity_in_stock, price_per_unit, organic)
                    VALUES ('Apple', 'Granny Smith', 150, 1, 1);
                    """
        await aexecute(sync_engine, insert_query)

        def my_formatter(row, content_columns):
            return "-".join(
                str(row[column]) for column in content_columns if column in row
            )

        reader = AlloyDBReader.create_sync(
            engine=sync_engine,
            query=f'SELECT * FROM "{table_name}";',
            content_columns=[
                "variety",
                "quantity_in_stock",
                "price_per_unit",
            ],
            formatter=my_formatter,
        )

        documents = self._collect_items(reader.lazy_load_data())

        expected_documents = [
            Document(
                text="Granny Smith-150-1",
                metadata={
                    "fruit_id": 1,
                    "fruit_name": "Apple",
                    "organic": 1,
                },
            )
        ]

        for expected, actual in zip(expected_documents, documents):
            assert expected.text == actual.text
            assert expected.metadata == actual.metadata

        await aexecute(sync_engine, f'DROP TABLE IF EXISTS "{table_name}"')

    async def test_load_from_query_customized_content_default_metadata_custom_page_content_format(
        self, sync_engine
    ):
        table_name = "test-table" + str(uuid.uuid4())
        query = f"""
                CREATE TABLE IF NOT EXISTS "{table_name}" (
                    fruit_id SERIAL PRIMARY KEY,
                    fruit_name VARCHAR(100) NOT NULL,
                    variety VARCHAR(50),
                    quantity_in_stock INT NOT NULL,
                    price_per_unit INT NOT NULL,
                    organic INT NOT NULL
                )
            """
        await aexecute(sync_engine, query)

        insert_query = f"""
                        INSERT INTO "{table_name}" (fruit_name, variety, quantity_in_stock, price_per_unit, organic)
                        VALUES ('Apple', 'Granny Smith', 150, 1, 1);
                    """
        await aexecute(sync_engine, insert_query)

        reader = AlloyDBReader.create_sync(
            engine=sync_engine,
            query=f'SELECT * FROM "{table_name}";',
            content_columns=[
                "variety",
                "quantity_in_stock",
                "price_per_unit",
            ],
            format="YAML",
        )

        documents = self._collect_items(reader.lazy_load_data())

        expected_docs = [
            Document(
                text="variety: Granny Smith\nquantity_in_stock: 150\nprice_per_unit: 1",
                metadata={
                    "fruit_id": 1,
                    "fruit_name": "Apple",
                    "organic": 1,
                },
            )
        ]

        for expected, actual in zip(expected_docs, documents):
            assert expected.text == actual.text
            assert expected.metadata == actual.metadata

        await aexecute(sync_engine, f'DROP TABLE IF EXISTS "{table_name}"')
