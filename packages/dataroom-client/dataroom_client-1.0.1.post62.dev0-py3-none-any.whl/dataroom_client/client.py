import asyncio
import functools
import inspect
import threading
import atexit
from datetime import datetime
import json as json_module
import logging
import os
import uuid
from enum import Enum
from io import BytesIO
import mimetypes
from typing import List, TypedDict, Optional
from urllib.parse import urljoin
import httpx


mimetypes.add_type("image/webp", ".webp")
logger = logging.getLogger(__name__)


class DataRoomError(Exception):
    """Base exception class for DataRoomClient errors"""

    def __init__(self, *args, **kwargs):
        self.response = kwargs.pop("response", None)
        super().__init__(*args, **kwargs)

    def __str__(self):
        if self.response:
            return f"{super().__str__()}\n{self.response.status_code}\n{self.response.text}"
        else:
            return super().__str__()


class DataRoomFile:
    """A wrapper for a file-like object that can be used with DataRoomClient"""

    def __init__(self, bytes_io, content_type, path=None, extension=None):
        extension = (
            mimetypes.guess_extension(content_type) or "" if extension is None else extension
        )
        self.bytes_io = bytes_io
        self.content_type = content_type
        if extension[0] != ".":
            extension = f".{extension}"
        self.extension = extension
        self.name = f"{uuid.uuid4().hex}"
        self.filename = f"{self.name}{extension}"
        self.path = path

    @classmethod
    def from_path(cls, path: str):
        content_type, encoding = mimetypes.guess_type(path)
        if not content_type:
            raise DataRoomError(f"Could not guess content type for file: {path}")
        with open(path, "rb") as f:
            return DataRoomFile(
                bytes_io=BytesIO(f.read()),
                content_type=content_type,
                path=path,
            )

    @classmethod
    def from_bytesio(cls, bytes_io, extension):
        assert extension is not None, "Please provide a file extension"
        return DataRoomFile(
            bytes_io=bytes_io,
            extension=extension,
            content_type=None,
            path=None,
        )


class ClientDuplicateState(Enum):
    UNPROCESSED = 'None'
    ORIGINAL = 1
    DUPLICATE = 2


class LatentType(TypedDict, total=False):
    latent_type: str
    file: DataRoomFile


class ImageUpdate(TypedDict, total=False):
    id: str  # noqa: A003
    source: Optional[str]
    attributes: Optional[dict]
    tags: Optional[List[str]]
    coca_embedding: Optional[str]
    related_images: Optional[dict[str, str]]
    datasets: Optional[list[str]]


class ImageCreate(TypedDict, total=False):
    id: str  # noqa: A003
    source: str
    image_file: Optional[DataRoomFile]
    image_url: Optional[str]
    attributes: Optional[dict]
    tags: Optional[list[str]]
    related_images: Optional[dict[str, str]]
    datasets: Optional[list[str]]


def arg_deprecation_msg(arg_name, msg=''):
    return f'DEPRECATION WARNING: Argument "{arg_name}" is deprecated, and will be removed in the future. {msg}'


class DataRoomClient:
    """
    The official client of the DataRoom API. See notebooks for usage examples.
    """

    def __init__(self, api_key=None, api_url=None, timeout=120):
        """
        @param api_key: API key for DataRoom API
        @param api_url: URL of the DataRoom backend API
        """
        self.api_key = api_key or os.environ.get("DATAROOM_API_KEY")
        self.api_url = (
            api_url
            or os.environ.get("DATAROOM_API_URL")
        )
        if not self.api_url:
            raise DataRoomError("DataRoom api_url is not set")
        self.client = httpx.AsyncClient()
        self.timeout = timeout

    # -------------------- Private methods --------------------

    async def _make_request(
        self, url, params=None, method="GET", json=None, files=None, headers=None,
    ):
        absolute_url = urljoin(self.api_url, url)
        if headers is None:
            headers = {}
        headers.update({
            "Authorization": f"Token {self.api_key}",
        })
        try:
            response = await self.client.request(
                method=method,
                url=absolute_url,
                params=params,
                json=json,
                files=files,
                headers=headers,
                timeout=self.timeout,
            )
            response.raise_for_status()
        except httpx.HTTPError as e:
            response = None
            if hasattr(e, "response"):
                response = e.response
            raise DataRoomError(e, response=response) from e
        else:
            if response.content:
                return response.json()

    async def _make_paginated_request(
        self, url, limit=1000, params=None, method="GET", json=None, headers=None,
    ):
        items = []
        next_url = url
        while next_url:
            response = await self._make_request(
                next_url, params=params, method=method, json=json, headers=headers,
            )
            if "results" not in response:
                raise NotImplementedError(f'No "results" in response to {url}')
            if "next" not in response:
                raise NotImplementedError(f'No "next" in response to {url}')
            next_url = response["next"]
            items += response["results"]
            if limit is not None and len(items) >= limit:
                break

        if limit is not None:
            return items[:limit]
        return items

    async def _make_paginated_request_iter(
        self, url, limit=1000, params=None, method="GET", json=None, headers=None,
    ):
        next_url = url
        returned_items = 0
        while next_url:
            response = await self._make_request(
                next_url, params=params, method=method, json=json, headers=headers,
            )
            if "results" not in response:
                raise NotImplementedError(f'No "results" in response to {url}')
            if "next" not in response:
                raise NotImplementedError(f'No "next" in response to {url}')
            next_url = response["next"]
            for item in response["results"]:
                yield item
                returned_items += 1
                if limit is not None and returned_items >= limit:
                    break
            if limit is not None and returned_items >= limit:
                break

    @staticmethod
    def _dict_filter_none(d: dict):
        return {k: v for k, v in d.items() if v is not None}

    @staticmethod
    def _get_attributes_filter(attributes: dict | None):
        if not attributes:
            return None
        for key, val in attributes.items():
            val = str(val)
            if "," in key or "," in val:
                raise DataRoomError(
                    "Commas are not allowed in attribute keys or values"
                )
            if ":" in key or ":" in val:
                raise DataRoomError(
                    "Colons are not allowed in attribute keys or values"
                )
        attrs_str = ",".join([f"{key}:{val}" for key, val in attributes.items()])
        return attrs_str

    @staticmethod
    def _validate_vector(vector: str):
        err_msg = "Argument vector must be a string representing a list of 768 floats."
        if not isinstance(vector, str) or not len(vector) > 0:
            raise DataRoomError(f"{err_msg} Not a string.")
        if vector[0] != "[" or vector[-1] != "]":
            raise DataRoomError(f"{err_msg} Not a list.")
        if len(vector[1:-1].split(',')) != 768:
            raise DataRoomError(f"{err_msg} Incorrect length.")

    # -------------------- Utils --------------------

    @classmethod
    async def download_image_from_url(cls, image_url: str) -> DataRoomFile:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(image_url)
                response.raise_for_status()
        except httpx.HTTPError as e:
            response = None
            if hasattr(e, "response"):
                response = e.response
            raise DataRoomError(e, response=response) from e
        else:
            content_type = response.headers.get("Content-Type")
            return DataRoomFile(
                bytes_io=BytesIO(response.content),
                content_type=content_type,
            )

    # -------------------- Image API methods --------------------

    async def get_images(
        self,
        limit: int | None = 1000,
        page_size: int = None,
        fields: List[str] = None,
        include_fields: List[str] = None,
        exclude_fields: List[str] = None,
        all_fields: bool = False,
        return_latents: List[str] = None,
        cache_ttl: int = None,
        partitions_count: int = None,
        partition: int = None,
        # filters
        short_edge: int = None,
        short_edge__gt: int = None,
        short_edge__gte: int = None,
        short_edge__lt: int = None,
        short_edge__lte: int = None,
        pixel_count: int = None,
        pixel_count__gt: int = None,
        pixel_count__gte: int = None,
        pixel_count__lt: int = None,
        pixel_count__lte: int = None,
        aspect_ratio_fraction: str = None,
        aspect_ratio: float = None,
        aspect_ratio__gt: float = None,
        aspect_ratio__gte: float = None,
        aspect_ratio__lt: float = None,
        aspect_ratio__lte: float = None,
        source: str = None,
        sources: List[str] = None,
        sources__ne: List[str] = None,
        attributes: dict = None,
        has_attributes: list = None,
        lacks_attributes: list = None,
        has_latents: List[str] = None,
        lacks_latents: List[str] = None,
        has_masks: List[str] = None,
        lacks_masks: List[str] = None,
        tags: list = None,
        tags__ne: list = None,
        tags__all: list = None,
        tags__ne_all: list = None,
        tags__empty: bool = None,
        coca_embedding__empty: bool = None,
        duplicate_state: ClientDuplicateState = None,
        date_created__gt: datetime = None,
        date_created__gte: datetime = None,
        date_created__lt: datetime = None,
        date_created__lte: datetime = None,
        date_updated__gt: datetime = None,
        date_updated__gte: datetime = None,
        date_updated__lt: datetime = None,
        date_updated__lte: datetime = None,
        datasets: list = None,
        datasets__ne: list = None,
        datasets__all: list = None,
        datasets__ne_all: list = None,
        datasets__empty: bool = None,
    ):
        headers = {}
        if cache_ttl:
            headers["Cache-Control"] = f"max-age={cache_ttl}"

        if source is not None:
            sources = [source]
            logger.warning(arg_deprecation_msg('source', 'Please use "sources" instead.'))

        return await self._make_paginated_request(
            url="images/",
            limit=limit,
            params=self._dict_filter_none(
                {
                    "fields": ",".join(fields) if fields else None,
                    "include_fields": ",".join(include_fields) if include_fields else None,
                    "exclude_fields": ",".join(exclude_fields) if exclude_fields else None,
                    "all_fields": all_fields if all_fields else None,
                    "return_latents": ",".join(return_latents) if return_latents else None,
                    "page_size": page_size,
                    "partitions_count": partitions_count,
                    "partition": partition,
                    # filters
                    "short_edge": short_edge,
                    "short_edge__gt": short_edge__gt,
                    "short_edge__gte": short_edge__gte,
                    "short_edge__lt": short_edge__lt,
                    "short_edge__lte": short_edge__lte,
                    "pixel_count": pixel_count,
                    "pixel_count__gt": pixel_count__gt,
                    "pixel_count__gte": pixel_count__gte,
                    "pixel_count__lt": pixel_count__lt,
                    "pixel_count__lte": pixel_count__lte,
                    "aspect_ratio_fraction": aspect_ratio_fraction,
                    "aspect_ratio": aspect_ratio,
                    "aspect_ratio__gt": aspect_ratio__gt,
                    "aspect_ratio__gte": aspect_ratio__gte,
                    "aspect_ratio__lt": aspect_ratio__lt,
                    "aspect_ratio__lte": aspect_ratio__lte,
                    "sources": ",".join(sources) if sources else None,
                    "sources__ne": ",".join(sources__ne) if sources__ne else None,
                    "attributes": self._get_attributes_filter(attributes),
                    "has_attributes": ",".join(has_attributes) if has_attributes else None,
                    "lacks_attributes": ",".join(lacks_attributes) if lacks_attributes else None,
                    "has_latents": ",".join(has_latents) if has_latents else None,
                    "lacks_latents": ",".join(lacks_latents) if lacks_latents else None,
                    "has_masks": ",".join(has_masks) if has_masks else None,
                    "lacks_masks": ",".join(lacks_masks) if lacks_masks else None,
                    "tags": ",".join(tags) if tags else None,
                    "tags__ne": ",".join(tags__ne) if tags__ne else None,
                    "tags__all": ",".join(tags__all) if tags__all else None,
                    "tags__ne_all": ",".join(tags__ne_all) if tags__ne_all else None,
                    "tags__empty": tags__empty,
                    "coca_embedding__empty": coca_embedding__empty,
                    "duplicate_state": duplicate_state.value if duplicate_state else None,
                    "date_created__gt": date_created__gt.isoformat() if date_created__gt else None,
                    "date_created__gte": date_created__gte.isoformat() if date_created__gte else None,
                    "date_created__lt": date_created__lt.isoformat() if date_created__lt else None,
                    "date_created__lte": date_created__lte.isoformat() if date_created__lte else None,
                    "date_updated__gt": date_updated__gt.isoformat() if date_updated__gt else None,
                    "date_updated__gte": date_updated__gte.isoformat() if date_updated__gte else None,
                    "date_updated__lt": date_updated__lt.isoformat() if date_updated__lt else None,
                    "date_updated__lte": date_updated__lte.isoformat() if date_updated__lte else None,
                    "datasets": ",".join(datasets) if datasets else None,
                    "datasets__ne": ",".join(datasets__ne) if datasets__ne else None,
                    "datasets__all": ",".join(datasets__all) if datasets__all else None,
                    "datasets__ne_all": ",".join(datasets__ne_all) if datasets__ne_all else None,
                    "datasets__empty": datasets__empty,
                }
            ),
            headers=headers,
        )

    async def get_images_iter(
        self,
        limit: int | None = 1000,
        page_size: int = None,
        fields: List[str] = None,
        include_fields: List[str] = None,
        exclude_fields: List[str] = None,
        all_fields: bool = False,
        return_latents: List[str] = None,
        cache_ttl: int = None,
        partitions_count: int = None,
        partition: int = None,
        # filters
        short_edge: int = None,
        short_edge__gt: int = None,
        short_edge__gte: int = None,
        short_edge__lt: int = None,
        short_edge__lte: int = None,
        pixel_count: int = None,
        pixel_count__gt: int = None,
        pixel_count__gte: int = None,
        pixel_count__lt: int = None,
        pixel_count__lte: int = None,
        aspect_ratio_fraction: str = None,
        aspect_ratio: float = None,
        aspect_ratio__gt: float = None,
        aspect_ratio__gte: float = None,
        aspect_ratio__lt: float = None,
        aspect_ratio__lte: float = None,
        source: str = None,
        sources: List[str] = None,
        sources__ne: List[str] = None,
        attributes: dict = None,
        has_attributes: list = None,
        lacks_attributes: list = None,
        has_latents: List[str] = None,
        lacks_latents: List[str] = None,
        has_masks: List[str] = None,
        lacks_masks: List[str] = None,
        tags: list = None,
        tags__ne: list = None,
        tags__all: list = None,
        tags__ne_all: list = None,
        tags__empty: bool = None,
        coca_embedding__empty: bool = None,
        duplicate_state: ClientDuplicateState = None,
        date_created__gt: datetime = None,
        date_created__gte: datetime = None,
        date_created__lt: datetime = None,
        date_created__lte: datetime = None,
        date_updated__gt: datetime = None,
        date_updated__gte: datetime = None,
        date_updated__lt: datetime = None,
        date_updated__lte: datetime = None,
        datasets: list = None,
        datasets__ne: list = None,
        datasets__all: list = None,
        datasets__ne_all: list = None,
        datasets__empty: bool = None,
    ):
        headers = {}
        if cache_ttl:
            headers["Cache-Control"] = f"max-age={cache_ttl}"

        if source is not None:
            sources = [source]
            logger.warning(arg_deprecation_msg('source', 'Please use "sources" instead.'))

        async for item in self._make_paginated_request_iter(
            url="images/",
            limit=limit,
            params=self._dict_filter_none(
                {
                    "fields": ",".join(fields) if fields else None,
                    "include_fields": ",".join(include_fields) if include_fields else None,
                    "exclude_fields": ",".join(exclude_fields) if exclude_fields else None,
                    "all_fields": all_fields if all_fields else None,
                    "return_latents": ",".join(return_latents) if return_latents else None,
                    "page_size": page_size,
                    "partitions_count": partitions_count,
                    "partition": partition,
                    # filters
                    "short_edge": short_edge,
                    "short_edge__gt": short_edge__gt,
                    "short_edge__gte": short_edge__gte,
                    "short_edge__lt": short_edge__lt,
                    "short_edge__lte": short_edge__lte,
                    "pixel_count": pixel_count,
                    "pixel_count__gt": pixel_count__gt,
                    "pixel_count__gte": pixel_count__gte,
                    "pixel_count__lt": pixel_count__lt,
                    "pixel_count__lte": pixel_count__lte,
                    "aspect_ratio_fraction": aspect_ratio_fraction,
                    "aspect_ratio": aspect_ratio,
                    "aspect_ratio__gt": aspect_ratio__gt,
                    "aspect_ratio__gte": aspect_ratio__gte,
                    "aspect_ratio__lt": aspect_ratio__lt,
                    "aspect_ratio__lte": aspect_ratio__lte,
                    "sources": ",".join(sources) if sources else None,
                    "sources__ne": ",".join(sources__ne) if sources__ne else None,
                    "attributes": self._get_attributes_filter(attributes),
                    "has_attributes": ",".join(has_attributes) if has_attributes else None,
                    "lacks_attributes": ",".join(lacks_attributes) if lacks_attributes else None,
                    "has_latents": ",".join(has_latents) if has_latents else None,
                    "lacks_latents": ",".join(lacks_latents) if lacks_latents else None,
                    "has_masks": ",".join(has_masks) if has_masks else None,
                    "lacks_masks": ",".join(lacks_masks) if lacks_masks else None,
                    "tags": ",".join(tags) if tags else None,
                    "tags__ne": ",".join(tags__ne) if tags__ne else None,
                    "tags__all": ",".join(tags__all) if tags__all else None,
                    "tags__ne_all": ",".join(tags__ne_all) if tags__ne_all else None,
                    "tags__empty": tags__empty,
                    "coca_embedding__empty": coca_embedding__empty,
                    "duplicate_state": duplicate_state.value if duplicate_state else None,
                    "date_created__gt": date_created__gt.isoformat() if date_created__gt else None,
                    "date_created__gte": date_created__gte.isoformat() if date_created__gte else None,
                    "date_created__lt": date_created__lt.isoformat() if date_created__lt else None,
                    "date_created__lte": date_created__lte.isoformat() if date_created__lte else None,
                    "date_updated__gt": date_updated__gt.isoformat() if date_updated__gt else None,
                    "date_updated__gte": date_updated__gte.isoformat() if date_updated__gte else None,
                    "date_updated__lt": date_updated__lt.isoformat() if date_updated__lt else None,
                    "date_updated__lte": date_updated__lte.isoformat() if date_updated__lte else None,
                    "datasets": ",".join(datasets) if datasets else None,
                    "datasets__ne": ",".join(datasets__ne) if datasets__ne else None,
                    "datasets__all": ",".join(datasets__all) if datasets__all else None,
                    "datasets__ne_all": ",".join(datasets__ne_all) if datasets__ne_all else None,
                    "datasets__empty": datasets__empty,
                }
            ),
            headers=headers,
        ):
            yield item

    async def get_random_images(
        self,
        limit: int | None = 1000,
        page_size: int = None,
        fields: List[str] = None,
        include_fields: List[str] = None,
        exclude_fields: List[str] = None,
        all_fields: bool = False,
        return_latents: List[str] = None,
        cache_ttl: int = None,
        prefix_length: int = None,
        num_prefixes: int = None,
        # filters
        short_edge: int = None,
        short_edge__gt: int = None,
        short_edge__gte: int = None,
        short_edge__lt: int = None,
        short_edge__lte: int = None,
        pixel_count: int = None,
        pixel_count__gt: int = None,
        pixel_count__gte: int = None,
        pixel_count__lt: int = None,
        pixel_count__lte: int = None,
        aspect_ratio_fraction: str = None,
        aspect_ratio: float = None,
        aspect_ratio__gt: float = None,
        aspect_ratio__gte: float = None,
        aspect_ratio__lt: float = None,
        aspect_ratio__lte: float = None,
        source: str = None,
        sources: List[str] = None,
        sources__ne: List[str] = None,
        attributes: dict = None,
        has_attributes: list = None,
        lacks_attributes: list = None,
        has_latents: List[str] = None,
        lacks_latents: List[str] = None,
        has_masks: List[str] = None,
        lacks_masks: List[str] = None,
        tags: list = None,
        tags__ne: list = None,
        tags__all: list = None,
        tags__ne_all: list = None,
        tags__empty: bool = None,
        coca_embedding__empty: bool = None,
        duplicate_state: ClientDuplicateState = None,
        date_created__gt: datetime = None,
        date_created__gte: datetime = None,
        date_created__lt: datetime = None,
        date_created__lte: datetime = None,
        date_updated__gt: datetime = None,
        date_updated__gte: datetime = None,
        date_updated__lt: datetime = None,
        date_updated__lte: datetime = None,
        datasets: list = None,
        datasets__ne: list = None,
        datasets__all: list = None,
        datasets__ne_all: list = None,
        datasets__empty: bool = None,
    ):
        """
        Get a list of random images.

        Random sampling works by filtering image_hash by a number of random hex prefixes. Use prefix_length and
        num_prefixes to adjust the randomness factor. In general, a smaller prefix_length will give you more samples,
        but less random and a higher num_prefixes will give you more samples, but slow down the query. The default
        values are prefix_length=5 and num_prefixes=100.
        """
        headers = {}
        if cache_ttl:
            headers["Cache-Control"] = f"max-age={cache_ttl}"

        if source is not None:
            sources = [source]
            logger.warning(arg_deprecation_msg('source', 'Please use "sources" instead.'))

        return await self._make_paginated_request(
            url="images/random/",
            limit=limit,
            params=self._dict_filter_none(
                {
                    "fields": ",".join(fields) if fields else None,
                    "include_fields": ",".join(include_fields) if include_fields else None,
                    "exclude_fields": ",".join(exclude_fields) if exclude_fields else None,
                    "all_fields": all_fields if all_fields else None,
                    "return_latents": ",".join(return_latents) if return_latents else None,
                    "page_size": page_size,
                    "prefix_length": prefix_length,
                    "num_prefixes": num_prefixes,
                    # filters
                    "short_edge": short_edge,
                    "short_edge__gt": short_edge__gt,
                    "short_edge__gte": short_edge__gte,
                    "short_edge__lt": short_edge__lt,
                    "short_edge__lte": short_edge__lte,
                    "pixel_count": pixel_count,
                    "pixel_count__gt": pixel_count__gt,
                    "pixel_count__gte": pixel_count__gte,
                    "pixel_count__lt": pixel_count__lt,
                    "pixel_count__lte": pixel_count__lte,
                    "aspect_ratio_fraction": aspect_ratio_fraction,
                    "aspect_ratio": aspect_ratio,
                    "aspect_ratio__gt": aspect_ratio__gt,
                    "aspect_ratio__gte": aspect_ratio__gte,
                    "aspect_ratio__lt": aspect_ratio__lt,
                    "aspect_ratio__lte": aspect_ratio__lte,
                    "sources": ",".join(sources) if sources else None,
                    "sources__ne": ",".join(sources__ne) if sources__ne else None,
                    "attributes": self._get_attributes_filter(attributes),
                    "has_attributes": ",".join(has_attributes) if has_attributes else None,
                    "lacks_attributes": ",".join(lacks_attributes) if lacks_attributes else None,
                    "has_latents": ",".join(has_latents) if has_latents else None,
                    "lacks_latents": ",".join(lacks_latents) if lacks_latents else None,
                    "has_masks": ",".join(has_masks) if has_masks else None,
                    "lacks_masks": ",".join(lacks_masks) if lacks_masks else None,
                    "tags": ",".join(tags) if tags else None,
                    "tags__ne": ",".join(tags__ne) if tags__ne else None,
                    "tags__all": ",".join(tags__all) if tags__all else None,
                    "tags__ne_all": ",".join(tags__ne_all) if tags__ne_all else None,
                    "tags__empty": tags__empty,
                    "coca_embedding__empty": coca_embedding__empty,
                    "duplicate_state": duplicate_state.value if duplicate_state else None,
                    "date_created__gt": date_created__gt.isoformat() if date_created__gt else None,
                    "date_created__gte": date_created__gte.isoformat() if date_created__gte else None,
                    "date_created__lt": date_created__lt.isoformat() if date_created__lt else None,
                    "date_created__lte": date_created__lte.isoformat() if date_created__lte else None,
                    "date_updated__gt": date_updated__gt.isoformat() if date_updated__gt else None,
                    "date_updated__gte": date_updated__gte.isoformat() if date_updated__gte else None,
                    "date_updated__lt": date_updated__lt.isoformat() if date_updated__lt else None,
                    "date_updated__lte": date_updated__lte.isoformat() if date_updated__lte else None,
                    "datasets": ",".join(datasets) if datasets else None,
                    "datasets__ne": ",".join(datasets__ne) if datasets__ne else None,
                    "datasets__all": ",".join(datasets__all) if datasets__all else None,
                    "datasets__ne_all": ",".join(datasets__ne_all) if datasets__ne_all else None,
                    "datasets__empty": datasets__empty,
                }
            ),
            headers=headers,
        )

    async def count_images(
        self,
        partitions_count: int = None,
        partition: int = None,
        # filters
        short_edge: int | None = None,
        short_edge__gt: int = None,
        short_edge__gte: int = None,
        short_edge__lt: int = None,
        short_edge__lte: int = None,
        pixel_count: int | None = None,
        pixel_count__gt: int = None,
        pixel_count__gte: int = None,
        pixel_count__lt: int = None,
        pixel_count__lte: int = None,
        aspect_ratio_fraction: str = None,
        aspect_ratio: float = None,
        aspect_ratio__gt: float = None,
        aspect_ratio__gte: float = None,
        aspect_ratio__lt: float = None,
        aspect_ratio__lte: float = None,
        source: str = None,
        sources: List[str] = None,
        sources__ne: List[str] = None,
        attributes: dict = None,
        has_attributes: list = None,
        lacks_attributes: list = None,
        has_latents: List[str] = None,
        lacks_latents: List[str] = None,
        has_masks: List[str] = None,
        lacks_masks: List[str] = None,
        tags: list = None,
        tags__ne: list = None,
        tags__all: list = None,
        tags__ne_all: list = None,
        tags__empty: bool = None,
        coca_embedding__empty: bool = None,
        duplicate_state: ClientDuplicateState = None,
        date_created__gt: datetime = None,
        date_created__gte: datetime = None,
        date_created__lt: datetime = None,
        date_created__lte: datetime = None,
        date_updated__gt: datetime = None,
        date_updated__gte: datetime = None,
        date_updated__lt: datetime = None,
        date_updated__lte: datetime = None,
        datasets: list = None,
        datasets__ne: list = None,
        datasets__all: list = None,
        datasets__ne_all: list = None,
        datasets__empty: bool = None,
    ):

        if source is not None:
            sources = [source]
            logger.warning(arg_deprecation_msg('source', 'Please use "sources" instead.'))

        response = await self._make_request(
            url="images/count/",
            params=self._dict_filter_none(
                {
                    "partitions_count": partitions_count,
                    "partition": partition,
                    # filters
                    "short_edge": short_edge,
                    "short_edge__gt": short_edge__gt,
                    "short_edge__gte": short_edge__gte,
                    "short_edge__lt": short_edge__lt,
                    "short_edge__lte": short_edge__lte,
                    "pixel_count": pixel_count,
                    "pixel_count__gt": pixel_count__gt,
                    "pixel_count__gte": pixel_count__gte,
                    "pixel_count__lt": pixel_count__lt,
                    "pixel_count__lte": pixel_count__lte,
                    "aspect_ratio_fraction": aspect_ratio_fraction,
                    "aspect_ratio": aspect_ratio,
                    "aspect_ratio__gt": aspect_ratio__gt,
                    "aspect_ratio__gte": aspect_ratio__gte,
                    "aspect_ratio__lt": aspect_ratio__lt,
                    "aspect_ratio__lte": aspect_ratio__lte,
                    "sources": ",".join(sources) if sources else None,
                    "sources__ne": ",".join(sources__ne) if sources__ne else None,
                    "attributes": self._get_attributes_filter(attributes),
                    "has_attributes": ",".join(has_attributes) if has_attributes else None,
                    "lacks_attributes": ",".join(lacks_attributes) if lacks_attributes else None,
                    "has_latents": ",".join(has_latents) if has_latents else None,
                    "lacks_latents": ",".join(lacks_latents) if lacks_latents else None,
                    "has_masks": ",".join(has_masks) if has_masks else None,
                    "lacks_masks": ",".join(lacks_masks) if lacks_masks else None,
                    "tags": ",".join(tags) if tags else None,
                    "tags__ne": ",".join(tags__ne) if tags__ne else None,
                    "tags__all": ",".join(tags__all) if tags__all else None,
                    "tags__ne_all": ",".join(tags__ne_all) if tags__ne_all else None,
                    "tags__empty": tags__empty,
                    "coca_embedding__empty": coca_embedding__empty,
                    "duplicate_state": duplicate_state.value if duplicate_state else None,
                    "date_created__gt": date_created__gt.isoformat() if date_created__gt else None,
                    "date_created__gte": date_created__gte.isoformat() if date_created__gte else None,
                    "date_created__lt": date_created__lt.isoformat() if date_created__lt else None,
                    "date_created__lte": date_created__lte.isoformat() if date_created__lte else None,
                    "date_updated__gt": date_updated__gt.isoformat() if date_updated__gt else None,
                    "date_updated__gte": date_updated__gte.isoformat() if date_updated__gte else None,
                    "date_updated__lt": date_updated__lt.isoformat() if date_updated__lt else None,
                    "date_updated__lte": date_updated__lte.isoformat() if date_updated__lte else None,
                    "datasets": ",".join(datasets) if datasets else None,
                    "datasets__ne": ",".join(datasets__ne) if datasets__ne else None,
                    "datasets__all": ",".join(datasets__all) if datasets__all else None,
                    "datasets__ne_all": ",".join(datasets__ne_all) if datasets__ne_all else None,
                    "datasets__empty": datasets__empty,
                }
            ),
        )
        return response["count"]

    async def get_image(
        self,
        image_id: str,
        fields: List[str] = None,
        include_fields: List[str] = None,
        exclude_fields: List[str] = None,
        all_fields: bool = False,
        return_latents: List[str] = None,
    ):
        return await self._make_request(
            url=f"images/{image_id}/",
            params=self._dict_filter_none({
                "fields": ",".join(fields) if fields else None,
                "include_fields": ",".join(include_fields) if include_fields else None,
                "exclude_fields": ",".join(exclude_fields) if exclude_fields else None,
                "all_fields": all_fields if all_fields else None,
                "return_latents": ",".join(return_latents) if return_latents else None,
            }),
        )

    async def create_image(
        self,
        image_id: str = None,
        source: str = None,
        image_file: DataRoomFile = None,
        image_url: str = None,
        attributes: dict = None,
        tags: list[str] = None,
        related_images: dict[str, str] | None = None,
        datasets: list[str] = None,
    ):
        if not image_file and not image_url:
            raise DataRoomError('Please provide either an "image_file" or "image_url" field')
        
        if not image_id and not image_url:
            raise DataRoomError('Please provide either an "image_id" or "image_url" field')
        
        if not source:
            raise DataRoomError('Please provide a "source" field')

        json_data = self._dict_filter_none(
            {
                "id": image_id,
                "image_url": image_url,
                "source": source,
                "attributes": attributes,
                "tags": tags,
                "related_images": related_images,
                "datasets": datasets,
            }
        )

        if image_file:
            # when uploading an image, we need to send a multipart/form-data request, not JSON
            # the image is sent as a file, and the rest of the data is sent as text/plain
            if not isinstance(image_file, DataRoomFile):
                raise DataRoomError("Argument image_file must be a DataRoomFile")
            files = {
                "image": (
                    image_file.filename,
                    image_file.bytes_io,
                    image_file.content_type,
                ),
                "json": (None, json_module.dumps(json_data), "text/plain"),
            }
            return await self._make_request(url="images/", method="POST", files=files)
        else:
            # application/json request
            return await self._make_request(
                url="images/",
                method="POST",
                json=json_data,
            )

    async def create_images(
        self,
        images: List[ImageCreate],
    ):
        files = []
        for i, image in enumerate(images):
            if 'id' not in image:
                raise DataRoomError("Missing 'id' field in image")
            if 'source' not in image:
                raise DataRoomError("Missing 'source' field in image")
            if 'image_file' not in image and 'image_url' not in image:
                raise DataRoomError('Please provide either an "image_file" or "image_url" field')

            image_file = image.get('image_file')
            if image_file and not isinstance(image_file, DataRoomFile):
                raise DataRoomError("Argument image_file must be a DataRoomFile")

            if image_file:
                files.append((
                    f"image_{i}",
                    (
                        image_file.filename,
                        image_file.bytes_io,
                        image_file.content_type,
                    ),
                ))

            json_data = self._dict_filter_none({
                "id": image['id'],
                "source": image['source'],
                "image_url": image.get('image_url'),
                "attributes": image.get('attributes'),
                "tags": image.get('tags'),
                "related_images": image.get('related_images'),
                "datasets": image.get('datasets'),
            })
            files.append((
                f"json_{i}",
                (None, json_module.dumps(json_data), "text/plain")
            ))

        return await self._make_request(url="images/", method="POST", files=files)

    async def update_image(
        self,
        image_id: str,
        source: str = None,
        attributes: dict = None,
        latents: List[LatentType] = None,
        tags: list[str] = None,
        coca_embedding: str = None,
        related_images: dict[str, str] | None = None,
        datasets: list[str] = None,
    ):
        """
        Update the image:
         * overwrite tags
         * merge attributes
         * merge latents
         * merge related_images
         * merge datasets
        """

        if coca_embedding:
            self._validate_vector(coca_embedding)

        if latents:
            files = []
            for i, latent in enumerate(latents):
                if 'latent_type' not in latent:
                    raise DataRoomError("Missing 'latent_type' field in latent")
                if 'file' not in latent:
                    raise DataRoomError("Missing 'file' field in latent")
                if not isinstance(latent['file'], DataRoomFile):
                    raise DataRoomError("Property 'file' must be a DataRoomFile")

                latent_file = latent['file']
                files.append((
                    f"latent_{i}",
                    (
                        latent_file.filename,
                        latent_file.bytes_io,
                        latent_file.content_type,
                    ),
                ))

                json_data = self._dict_filter_none({
                    "latent_type": latent['latent_type'],
                })
                files.append((
                    f"latent_json_{i}",
                    (None, json_module.dumps(json_data), "text/plain")
                ))

            image_data = self._dict_filter_none({
                "source": source,
                "attributes": attributes,
                "tags": tags,
                "coca_embedding": coca_embedding,
                "related_images": related_images,
                "datasets": datasets,
            })
            files.append((
                "json",
                (None, json_module.dumps(image_data), "text/plain")
            ))
            return await self._make_request(url=f"images/{image_id}/", method="PUT", files=files)
        else:
            return await self._make_request(
                url=f"images/{image_id}/",
                method="PUT",
                json=self._dict_filter_none({
                    "source": source,
                    "attributes": attributes,
                    "tags": tags,
                    "coca_embedding": coca_embedding,
                    "related_images": related_images,
                    "datasets": datasets,
                }),
            )

    async def update_images(
        self,
        images: List[ImageUpdate],
    ):
        """
        Bulk update images:
         * overwrite tags
         * merge attributes
         * merge latents
         * merge related_images
         * merge datasets
        """
        for image in images:
            if 'id' not in image:
                raise DataRoomError("Missing 'id' field in image")
            image.setdefault('source', None)
            image.setdefault('attributes', None)
            image.setdefault('tags', None)
            image.setdefault('coca_embedding', None)
            image.setdefault('related_images', None)
            image.setdefault('datasets', None)
        
        return await self._make_request(
            url=f"images/bulk_update/",
            method="PUT",
            json=[
                self._dict_filter_none({
                    "id": image['id'],
                    "source": image['source'],
                    "attributes": image['attributes'],
                    "tags": image['tags'],
                    "coca_embedding": image['coca_embedding'],
                    "related_images": image['related_images'],
                    "datasets": image['datasets'],
                })
                for image in images
            ],
        )

    async def add_image_attributes(
        self,
        image_id: str,
        attributes: dict,
    ):
        """
        Update attributes of an image, merging them with the existing attributes.
        """
        logger.warning(
            'DEPRECATION WARNING: Method "add_image_attributes" is deprecated, and will be removed in the future. '
            'Please use "update_image" instead.'
        )

        return await self._make_request(
            url=f"images/{image_id}/add_attributes/",
            method="PUT",
            json={
                "attributes": attributes,
            },
        )

    async def add_image_attributes_in_bulk(
        self,
        ids_to_attributes: dict[str, dict],
    ):
        """
        Update attributes of a list of images, merging them with the existing attributes.
        """
        logger.warning(
            'DEPRECATION WARNING: Method "add_image_attributes_in_bulk" is deprecated, '
            'and will be removed in the future. Please use "update_image" instead.'
        )

        return await self._make_request(
            url=f"images/add_attributes_bulk/",
            method="POST",
            json=[
                {"image_id": key, "attributes": val}
                for key, val in ids_to_attributes.items()
            ],
        )

    async def delete_image(self, image_id: str):
        return await self._make_request(
            url=f"images/{image_id}/",
            method="DELETE",
        )

    async def get_image_audit_logs(self, image_id: str):
        return await self._make_request(
            url=f"images/{image_id}/audit_logs/",
        )

    async def get_image_similarity(self, image_id_1: str, image_id_2: str):
        response = await self._make_request(
            url=f"images/{image_id_1}/similarity/",
            method="POST",
            json={
                "image_id": image_id_2,
            },
        )
        return response["similarity"]

    async def get_similar_images(
        self,
        # similarity by
        image_id: str = None,
        image_file: DataRoomFile = None,
        image_vector: str = None,
        image_text: str = None,
        # options
        number=5,
        fields: List[str] = None,
        include_fields: List[str] = None,
        exclude_fields: List[str] = None,
        all_fields: bool = False,
        return_latents: List[str] = None,
        # filters
        short_edge: int | None = None,
        short_edge__gt: int = None,
        short_edge__gte: int = None,
        short_edge__lt: int = None,
        short_edge__lte: int = None,
        pixel_count: int | None = None,
        pixel_count__gt: int = None,
        pixel_count__gte: int = None,
        pixel_count__lt: int = None,
        pixel_count__lte: int = None,
        aspect_ratio_fraction: str = None,
        aspect_ratio: float = None,
        aspect_ratio__gt: float = None,
        aspect_ratio__gte: float = None,
        aspect_ratio__lt: float = None,
        aspect_ratio__lte: float = None,
        sources: List[str] = None,
        sources__ne: List[str] = None,
        attributes: dict = None,
        has_attributes: list = None,
        lacks_attributes: list = None,
        has_latents: List[str] = None,
        lacks_latents: List[str] = None,
        has_masks: List[str] = None,
        lacks_masks: List[str] = None,
        tags: list = None,
        tags__ne: list = None,
        tags__all: list = None,
        tags__ne_all: list = None,
        tags__empty: bool = None,
        coca_embedding__empty: bool = None,
        duplicate_state: ClientDuplicateState = None,
        date_created__gt: datetime = None,
        date_created__gte: datetime = None,
        date_created__lt: datetime = None,
        date_created__lte: datetime = None,
        date_updated__gt: datetime = None,
        date_updated__gte: datetime = None,
        date_updated__lt: datetime = None,
        date_updated__lte: datetime = None,
        datasets: list = None,
        datasets__ne: list = None,
        datasets__all: list = None,
        datasets__ne_all: list = None,
        datasets__empty: bool = None,
    ):
        search_args = {
            'image_id': image_id, 'image_file': image_file, 'image_vector': image_vector, 'image_text': image_text,
        }
        if sum([bool(arg) for arg in search_args.values()]) != 1:
            raise DataRoomError(f'Please provide one of the following arguments: {", ".join(search_args.keys())}')

        params = self._dict_filter_none({
            "fields": ",".join(fields) if fields else None,
            "include_fields": ",".join(include_fields) if include_fields else None,
            "exclude_fields": ",".join(exclude_fields) if exclude_fields else None,
            "all_fields": all_fields if all_fields else None,
            "return_latents": ",".join(return_latents) if return_latents else None,
            # filters
            "short_edge": short_edge,
            "short_edge__gt": short_edge__gt,
            "short_edge__gte": short_edge__gte,
            "short_edge__lt": short_edge__lt,
            "short_edge__lte": short_edge__lte,
            "pixel_count": pixel_count,
            "pixel_count__gt": pixel_count__gt,
            "pixel_count__gte": pixel_count__gte,
            "pixel_count__lt": pixel_count__lt,
            "pixel_count__lte": pixel_count__lte,
            "aspect_ratio_fraction": aspect_ratio_fraction,
            "aspect_ratio": aspect_ratio,
            "aspect_ratio__gt": aspect_ratio__gt,
            "aspect_ratio__gte": aspect_ratio__gte,
            "aspect_ratio__lt": aspect_ratio__lt,
            "aspect_ratio__lte": aspect_ratio__lte,
            "sources": ",".join(sources) if sources else None,
            "sources__ne": ",".join(sources__ne) if sources__ne else None,
            "attributes": self._get_attributes_filter(attributes),
            "has_attributes": ",".join(has_attributes) if has_attributes else None,
            "lacks_attributes": ",".join(lacks_attributes) if lacks_attributes else None,
            "has_latents": ",".join(has_latents) if has_latents else None,
            "lacks_latents": ",".join(lacks_latents) if lacks_latents else None,
            "has_masks": ",".join(has_masks) if has_masks else None,
            "lacks_masks": ",".join(lacks_masks) if lacks_masks else None,
            "tags": ",".join(tags) if tags else None,
            "tags__ne": ",".join(tags__ne) if tags__ne else None,
            "tags__all": ",".join(tags__all) if tags__all else None,
            "tags__ne_all": ",".join(tags__ne_all) if tags__ne_all else None,
            "tags__empty": tags__empty,
            "coca_embedding__empty": coca_embedding__empty,
            "duplicate_state": duplicate_state.value if duplicate_state else None,
            "date_created__gt": date_created__gt.isoformat() if date_created__gt else None,
            "date_created__gte": date_created__gte.isoformat() if date_created__gte else None,
            "date_created__lt": date_created__lt.isoformat() if date_created__lt else None,
            "date_created__lte": date_created__lte.isoformat() if date_created__lte else None,
            "date_updated__gt": date_updated__gt.isoformat() if date_updated__gt else None,
            "date_updated__gte": date_updated__gte.isoformat() if date_updated__gte else None,
            "date_updated__lt": date_updated__lt.isoformat() if date_updated__lt else None,
            "date_updated__lte": date_updated__lte.isoformat() if date_updated__lte else None,
            "datasets": ",".join(datasets) if datasets else None,
            "datasets__ne": ",".join(datasets__ne) if datasets__ne else None,
            "datasets__all": ",".join(datasets__all) if datasets__all else None,
            "datasets__ne_all": ",".join(datasets__ne_all) if datasets__ne_all else None,
            "datasets__empty": datasets__empty,
        })

        if image_file:
            # by image file
            if not isinstance(image_file, DataRoomFile):
                raise DataRoomError("Argument image_file must be a DataRoomFile")
            json_data = {
                "number": number,
            }
            files = {
                "image": (
                    image_file.filename,
                    image_file.bytes_io,
                    image_file.content_type,
                ),
                "json": (None, json_module.dumps(json_data), "text/plain"),
            }
            return await self._make_request(
                url=f"images/similar_to_file/",
                method="POST",
                files=files,
                params=params,
            )
        elif image_id:
            # by image id
            response = await self._make_request(
                url=f"images/{image_id}/similar/",
                params={
                    "number": number,
                    **params,
                },
            )
            return response
        elif image_vector:
            # by image vector
            self._validate_vector(image_vector)
            return await self._make_request(
                url=f"images/similar_to_vector/",
                method="POST",
                json={
                    "vector": image_vector,
                    "number": number,
                },
                params=params,
            )
        elif image_text:
            # by text
            return await self._make_request(
                url=f"images/similar_to_text/",
                method="POST",
                json={
                    "text": image_text,
                    "number": number,
                },
                params=params,
            )
        else:
            raise DataRoomError("Invalid arguments")
        
    async def get_related_images(
        self,
        image_id: str,
        # options
        fields: List[str] = None,
        include_fields: List[str] = None,
        exclude_fields: List[str] = None,
        all_fields: bool = False,
        return_latents: List[str] = None,
    ):
        params = self._dict_filter_none({
            "fields": ",".join(fields) if fields else None,
            "include_fields": ",".join(include_fields) if include_fields else None,
            "exclude_fields": ",".join(exclude_fields) if exclude_fields else None,
            "all_fields": all_fields if all_fields else None,
            "return_latents": ",".join(return_latents) if return_latents else None,
        })
        return await self._make_request(
            url=f"images/{image_id}/related/",
            params=params,
        )

    async def set_image_latent(
        self,
        image_id: str,
        latent_file: DataRoomFile,
        latent_type: str,
        is_mask=None,
    ):
        logger.warning(
            'DEPRECATION WARNING: Method "set_image_latent" is deprecated, and will be removed in the future. '
            'Please use "update_image" instead.'
        )

        if not isinstance(latent_file, DataRoomFile):
            raise DataRoomError("Argument latent_file must be a DataRoomFile")

        if is_mask is not None:
            logger.warning(arg_deprecation_msg('is_mask'))

        json_data = {
            "latent_type": latent_type,
        }
        files = {
            "file": (
                latent_file.filename,
                latent_file.bytes_io,
                latent_file.content_type,
            ),
            "json": (None, json_module.dumps(json_data), "text/plain"),
        }
        return await self._make_request(
            url=f"images/{image_id}/set_latent/",
            method="POST",
            files=files,
        )

    async def delete_image_latent(self, image_id: str, latent_type: str):
        return await self._make_request(
            url=f"images/{image_id}/delete_latent/",
            method="POST",
            json={
                "latent_type": latent_type,
            },
        )

    async def set_image_coca_embedding(self, image_id: str, vector: str):
        logger.warning(
            'DEPRECATION WARNING: Method "set_image_coca_embedding" is deprecated, and will be removed in the future. '
            'Please use "update_image" instead.'
        )
        self._validate_vector(vector)
        return await self._make_request(
            url=f"images/{image_id}/",
            method="PUT",
            json={
                "coca_embedding": vector,
            },
        )
    
    async def aggregate_images(self, field, type):
        return await self._make_request(
            url="images/aggregate/",
            method="POST",
            json={
                "field": field,
                "type": type,
            },
        )
    
    async def bucket_images(self, field, size):
        return await self._make_request(
            url="images/bucket/",
            method="POST",
            json={
                "field": field,
                "size": size,
            },
        )

    # -------------------- Tag API methods --------------------

    async def get_tags(self, limit: int = 1000):
        return await self._make_paginated_request(
            url=f"tags/",
            limit=limit,
        )

    async def get_tag(self, tag_id: str):
        return await self._make_request(
            url=f"tags/{tag_id}/",
        )

    async def create_tag(self, name: str, description: str = None):
        return await self._make_request(
            url="tags/",
            method="POST",
            json=self._dict_filter_none(
                {
                    "name": name,
                    "description": description,
                }
            ),
        )

    async def tag_images(self, image_ids: List[str], tag_names: List[str]):
        return await self._make_request(
            url="tags/tag_images/",
            method="PUT",
            json={
                "image_ids": image_ids,
                "tag_names": tag_names,
            },
        )

    # -------------------- Dataset API methods --------------------

    async def get_datasets(self, slug: str = None, limit: int = 1000):
        return await self._make_paginated_request(
            url=f"datasets/",
            params=self._dict_filter_none({
                "slug": slug,
            }),
            limit=limit,
        )

    async def get_dataset(self, slug_version: str):
        return await self._make_request(
            url=f"datasets/{slug_version}/",
        )

    async def create_dataset(self, name: str, slug: str, description: str = None):
        return await self._make_request(
            url=f"datasets/",
            method="POST",
            json={
                "name": name,
                "slug": slug,
                "description": description if description else "",
            },
        )
    
    async def freeze_dataset(self, slug_version: str):
        return await self._make_request(
            url=f"datasets/{slug_version}/freeze/",
            method="POST",
        )
    
    async def unfreeze_dataset(self, slug_version: str):
        return await self._make_request(
            url=f"datasets/{slug_version}/unfreeze/",
            method="POST",
        )

    async def dataset_add_images(self, slug_version: str, image_ids: List[str]):
        return await self._make_request(
            url=f"datasets/{slug_version}/images/",
            method="POST",
            json={
                "image_ids": image_ids,
            },
        )

    async def dataset_remove_images(self, slug_version: str, image_ids: List[str]):
        return await self._make_request(
            url=f"datasets/{slug_version}/images/",
            method="DELETE",
            json={
                "image_ids": image_ids,
            },
        )



class AsyncRunner:
    """
    Manages a single, shared event loop in a background thread
    to run async functions from a synchronous context using classmethods.

    The shutdown method is automatically registered to be called on exit.
    """
    _loop: asyncio.AbstractEventLoop | None = None
    _thread: threading.Thread | None = None
    _lock = threading.Lock() # To ensure thread-safe initialization

    @classmethod
    def _initialize(cls):
        """Initializes the background event loop and thread if not already done."""
        with cls._lock:
            if cls._thread is not None:
                return

            cls._loop = asyncio.new_event_loop()
            cls._thread = threading.Thread(
                target=cls._loop.run_forever,
                daemon=True,
                name="ClassAsyncRunnerThread"
            )
            cls._thread.start()
            # Register the shutdown method to be called when the program exits.
            # This is done here to ensure it's only registered once.
            atexit.register(cls.shutdown)
            logger.debug("Initialized ClassAsyncRunner background thread")

    @classmethod
    def run(cls, coro):
        """
        Runs a coroutine on the shared background event loop and returns the result.
        Initializes the loop on the first call.
        """
        if cls._thread is None:
            cls._initialize()

        future = asyncio.run_coroutine_threadsafe(coro, cls._loop)
        return future.result()

    @classmethod
    def shutdown(cls):
        """
        Cleanly stops the shared event loop.
        This is registered with atexit and called automatically.
        """
        # The check for cls._loop is important because atexit might call this
        # even if the runner was never initialized.
        if cls._loop and cls._loop.is_running():
            logger.debug("Shutting down ClassAsyncRunner background thread...")
            cls._loop.call_soon_threadsafe(cls._loop.stop)
            # It's good practice to have a timeout on join
            cls._thread.join(timeout=5) 
            cls._loop.close()
            logger.debug("ClassAsyncRunner has been shut down.")
        
        cls._loop = None
        cls._thread = None


class DataRoomClientSync:
    """
    The official client of the DataRoom API using synchronous method and requests.
    """

    def __init__(self, api_key=None, api_url=None, timeout=120):
        """
        @param api_key: API key for DataRoom API
        @param api_url: URL of the DataRoom backend API
        """
        self.api_key = api_key or os.environ.get("DATAROOM_API_KEY")
        self.api_url = (
            api_url
            or os.environ.get("DATAROOM_API_URL")
        )
        if not self.api_url:
            raise DataRoomError("DataRoom api_url is not set")
        self._async_client = DataRoomClient(api_key=self.api_key, api_url=self.api_url, timeout=timeout)

    def __getattr__(self, name):
        """
        Dynamically create sync methods for all methods of the async client.
        """
        attr = getattr(self._async_client, name)

        if not callable(attr):
            return attr

        @functools.wraps(attr)
        def sync_wrapper(*args, **kwargs):
            result = attr(*args, **kwargs)
            if inspect.isawaitable(result):
                return AsyncRunner.run(result)
            return result

        return sync_wrapper

    def __dir__(self) -> List[str]:
        """
        Provide a list of attributes for introspection and autocompletion in tools like IPython.
        """
        return sorted(list(set(super().__dir__()) | set(dir(self._async_client))))

    @classmethod
    def download_image_from_url(cls, *args, **kwargs) -> DataRoomFile:
        return AsyncRunner.run(DataRoomClient.download_image_from_url(*args, **kwargs))