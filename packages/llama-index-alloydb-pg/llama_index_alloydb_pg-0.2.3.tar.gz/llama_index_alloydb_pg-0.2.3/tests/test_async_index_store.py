# Copyright 2024 Google LLC
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

import os
import uuid
import warnings
from typing import Sequence

import pytest
import pytest_asyncio
from llama_index.core.data_structs.data_structs import (
    IndexDict,
    IndexGraph,
    IndexList,
    IndexStruct,
)
from sqlalchemy import RowMapping, text

from llama_index_alloydb_pg import AlloyDBEngine
from llama_index_alloydb_pg.async_index_store import AsyncAlloyDBIndexStore

default_table_name_async = "index_store_" + str(uuid.uuid4())
sync_method_exception_str = "Sync methods are not implemented for AsyncAlloyDBIndexStore . Use AlloyDBIndexStore  interface instead."


async def aexecute(engine: AlloyDBEngine, query: str) -> None:
    async with engine._pool.connect() as conn:
        await conn.execute(text(query))
        await conn.commit()


async def afetch(engine: AlloyDBEngine, query: str) -> Sequence[RowMapping]:
    async with engine._pool.connect() as conn:
        result = await conn.execute(text(query))
        result_map = result.mappings()
        result_fetch = result_map.fetchall()
    return result_fetch


def get_env_var(key: str, desc: str) -> str:
    v = os.environ.get(key)
    if v is None:
        raise ValueError(f"Must set env var {key} to: {desc}")
    return v


@pytest.mark.asyncio(loop_scope="class")
class TestAsyncAlloyDBIndexStore:
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
        self, db_project, db_region, db_cluster, db_instance, db_name
    ):
        async_engine = await AlloyDBEngine.afrom_instance(
            project_id=db_project,
            instance=db_instance,
            cluster=db_cluster,
            region=db_region,
            database=db_name,
        )

        yield async_engine

        await async_engine.close()

    @pytest_asyncio.fixture(scope="class")
    async def index_store(self, async_engine):
        await async_engine._ainit_index_store_table(table_name=default_table_name_async)

        index_store = await AsyncAlloyDBIndexStore.create(
            engine=async_engine, table_name=default_table_name_async
        )

        yield index_store

        query = f'DROP TABLE IF EXISTS "{default_table_name_async}"'
        await aexecute(async_engine, query)

    async def test_init_with_constructor(self, async_engine):
        key = object()
        with pytest.raises(Exception):
            AsyncAlloyDBIndexStore(
                key, engine=async_engine, table_name=default_table_name_async
            )

    async def test_create_without_table(self, async_engine):
        with pytest.raises(ValueError):
            await AsyncAlloyDBIndexStore.create(
                engine=async_engine, table_name="non-existent-table"
            )

    async def test_add_and_delete_index(self, index_store, async_engine):
        index_struct = IndexGraph()
        index_id = index_struct.index_id
        index_type = index_struct.get_type()
        await index_store.aadd_index_struct(index_struct)

        query = f"""select * from "public"."{default_table_name_async}" where index_id = '{index_id}';"""
        results = await afetch(async_engine, query)
        result = results[0]
        assert result.get("type") == index_type

        await index_store.adelete_index_struct(index_id)
        query = f"""select * from "public"."{default_table_name_async}" where index_id = '{index_id}';"""
        results = await afetch(async_engine, query)
        assert results == []

    async def test_get_index(self, index_store):
        index_struct = IndexGraph()
        index_id = index_struct.index_id
        index_type = index_struct.get_type()
        await index_store.aadd_index_struct(index_struct)

        ind_struct = await index_store.aget_index_struct(index_id)

        assert index_struct == ind_struct

    async def test_aindex_structs(self, index_store):
        index_dict_struct = IndexDict()
        index_list_struct = IndexList()
        index_graph_struct = IndexGraph()

        await index_store.aadd_index_struct(index_dict_struct)
        await index_store.async_add_index_struct(index_graph_struct)
        await index_store.aadd_index_struct(index_list_struct)

        indexes = await index_store.aindex_structs()

        assert index_dict_struct in indexes
        assert index_list_struct in indexes
        assert index_graph_struct in indexes

    async def test_warning(self, index_store):
        index_dict_struct = IndexDict()
        index_list_struct = IndexList()

        await index_store.aadd_index_struct(index_dict_struct)
        await index_store.aadd_index_struct(index_list_struct)

        with warnings.catch_warnings(record=True) as w:
            index_struct = await index_store.aget_index_struct()

            assert len(w) == 1
            assert "No struct_id specified and more than one struct exists." in str(
                w[-1].message
            )

    async def test_index_structs(self, index_store):
        with pytest.raises(Exception, match=sync_method_exception_str):
            index_store.index_structs()

    async def test_add_index_struct(self, index_store):
        index_struct = IndexGraph()
        with pytest.raises(Exception, match=sync_method_exception_str):
            index_store.add_index_struct(index_struct)

    async def test_delete_index_struct(self, index_store):
        with pytest.raises(Exception, match=sync_method_exception_str):
            index_store.delete_index_struct("non_existent_key")

    async def test_get_index_struct(self, index_store):
        with pytest.raises(Exception, match=sync_method_exception_str):
            index_store.get_index_struct(struct_id="non_existent_id")
