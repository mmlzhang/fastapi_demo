"""HTTP Request And Response Generic Schema"""
from typing import Generic, Iterator, List, Optional, Type, TypeVar, Union

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.queryset import QuerySet

T = TypeVar("T")


class QueryParamSchema(BaseModel):
    page: int = Field(default=1, description="page number")
    size: int = Field(default=20, description="per page size, set -1 to disable paging")

    class Config:
        allow_mutation = False


class PagerSchema(GenericModel, Generic[T]):
    page: int = Field(description="current page size")
    page_size: int = Field(description="page size")
    items_count: int = Field(description="total items count")
    total_page: int = Field(description="per page size")
    items: List[T] = Field(description="objects list")

    class Config:
        allow_mutation = False

    @staticmethod
    async def from_queryset(
        queryset: QuerySet[T],
        schema: Optional[Type[BaseModel]] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> "PagerSchema[T]":
        items_count = await queryset.count()

        if page_size == 0:
            total_page = 1
            items = await pydantic_model_creator(queryset.model).from_queryset(queryset)
        else:
            total_page = (items_count // page_size) + 1 if items_count % page_size > 0 else items_count // page_size
            items = await pydantic_model_creator(queryset.model).from_queryset(queryset.offset((page - 1) * page_size).limit(page_size))

        if schema is not None:
            items = [schema(**item.dict()) for item in items]

        return PagerSchema(
            page=page,
            page_size=page_size,
            total_page=total_page,
            items_count=items_count,
            items=items,
        )

    @staticmethod
    async def from_list(
        items: Union[List[T], Iterator[T]],
        schema: Optional[Type[BaseModel]] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> "PagerSchema[T]":
        items = list(items)
        items_count = len(items)

        if page_size == 0:
            total_page = 1
        else:
            total_page = (items_count // page_size) + 1 if items_count % page_size > 0 else items_count // page_size
            items = items[(page - 1) * page_size : page * page_size]

        if schema is not None:
            items = [schema(**item) for item in items]

        return PagerSchema(
            page=page,
            page_size=page_size,
            total_page=total_page,
            items_count=items_count,
            items=items,
        )


class ResponseSchema(GenericModel, Generic[T]):
    code: int = 0
    message: Optional[str] = "SUCCESS"
    data: Optional[T] = None
