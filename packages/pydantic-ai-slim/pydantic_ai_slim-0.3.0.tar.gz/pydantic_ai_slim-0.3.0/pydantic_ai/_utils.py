from __future__ import annotations as _annotations

import asyncio
import functools
import inspect
import time
import uuid
from collections.abc import AsyncIterable, AsyncIterator, Awaitable, Iterator
from contextlib import asynccontextmanager, suppress
from dataclasses import dataclass, fields, is_dataclass
from datetime import datetime, timezone
from functools import partial
from types import GenericAlias
from typing import TYPE_CHECKING, Any, Callable, Generic, TypeVar, Union, overload

from anyio.to_thread import run_sync
from pydantic import BaseModel, TypeAdapter
from pydantic.json_schema import JsonSchemaValue
from typing_extensions import ParamSpec, TypeAlias, TypeGuard, TypeIs, is_typeddict

from pydantic_graph._utils import AbstractSpan

AbstractSpan = AbstractSpan

if TYPE_CHECKING:
    from pydantic_ai.agent import AgentRun, AgentRunResult
    from pydantic_graph import GraphRun, GraphRunResult

    from . import messages as _messages
    from .tools import ObjectJsonSchema

_P = ParamSpec('_P')
_R = TypeVar('_R')


async def run_in_executor(func: Callable[_P, _R], *args: _P.args, **kwargs: _P.kwargs) -> _R:
    wrapped_func = partial(func, *args, **kwargs)
    return await run_sync(wrapped_func)


def is_model_like(type_: Any) -> bool:
    """Check if something is a pydantic model, dataclass or typedict.

    These should all generate a JSON Schema with `{"type": "object"}` and therefore be usable directly as
    function parameters.
    """
    return (
        isinstance(type_, type)
        and not isinstance(type_, GenericAlias)
        and (issubclass(type_, BaseModel) or is_dataclass(type_) or is_typeddict(type_))  # pyright: ignore[reportUnknownArgumentType]
    )


def check_object_json_schema(schema: JsonSchemaValue) -> ObjectJsonSchema:
    from .exceptions import UserError

    if schema.get('type') == 'object':
        return schema
    elif schema.get('$ref') is not None:
        maybe_result = schema.get('$defs', {}).get(schema['$ref'][8:])  # This removes the initial "#/$defs/".

        if "'$ref': '#/$defs/" in str(maybe_result):
            return schema  # We can't remove the $defs because the schema contains other references
        return maybe_result
    else:
        raise UserError('Schema must be an object')


T = TypeVar('T')


@dataclass
class Some(Generic[T]):
    """Analogous to Rust's `Option::Some` type."""

    value: T


Option: TypeAlias = Union[Some[T], None]
"""Analogous to Rust's `Option` type, usage: `Option[Thing]` is equivalent to `Some[Thing] | None`."""


class Unset:
    """A singleton to represent an unset value."""

    pass


UNSET = Unset()


def is_set(t_or_unset: T | Unset) -> TypeGuard[T]:
    return t_or_unset is not UNSET


@asynccontextmanager
async def group_by_temporal(
    aiterable: AsyncIterable[T], soft_max_interval: float | None
) -> AsyncIterator[AsyncIterable[list[T]]]:
    """Group items from an async iterable into lists based on time interval between them.

    Effectively, this debounces the iterator.

    This returns a context manager usable as an iterator so any pending tasks can be cancelled if an error occurs
    during iteration.

    Usage:

    ```python
    async with group_by_temporal(yield_groups(), 0.1) as groups_iter:
        async for groups in groups_iter:
            print(groups)
    ```

    Args:
        aiterable: The async iterable to group.
        soft_max_interval: Maximum interval over which to group items, this should avoid a trickle of items causing
            a group to never be yielded. It's a soft max in the sense that once we're over this time, we yield items
            as soon as `aiter.__anext__()` returns. If `None`, no grouping/debouncing is performed

    Returns:
        A context manager usable as an async iterable of lists of items produced by the input async iterable.
    """
    if soft_max_interval is None:

        async def async_iter_groups_noop() -> AsyncIterator[list[T]]:
            async for item in aiterable:
                yield [item]

        yield async_iter_groups_noop()
        return

    # we might wait for the next item more than once, so we store the task to await next time
    task: asyncio.Task[T] | None = None

    async def async_iter_groups() -> AsyncIterator[list[T]]:
        nonlocal task

        assert soft_max_interval is not None and soft_max_interval >= 0, 'soft_max_interval must be a positive number'
        buffer: list[T] = []
        group_start_time = time.monotonic()

        aiterator = aiterable.__aiter__()
        while True:
            if group_start_time is None:
                # group hasn't started, we just wait for the maximum interval
                wait_time = soft_max_interval
            else:
                # wait for the time remaining in the group
                wait_time = soft_max_interval - (time.monotonic() - group_start_time)

            # if there's no current task, we get the next one
            if task is None:
                # aiter.__anext__() returns an Awaitable[T], not a Coroutine which asyncio.create_task expects
                # so far, this doesn't seem to be a problem
                task = asyncio.create_task(aiterator.__anext__())  # pyright: ignore[reportArgumentType]

            # we use asyncio.wait to avoid cancelling the coroutine if it's not done
            done, _ = await asyncio.wait((task,), timeout=wait_time)

            if done:
                # the one task we waited for completed
                try:
                    item = done.pop().result()
                except StopAsyncIteration:
                    # if the task raised StopAsyncIteration, we're done iterating
                    if buffer:
                        yield buffer
                    task = None
                    break
                else:
                    # we got an item, add it to the buffer and set task to None to get the next item
                    buffer.append(item)
                    task = None
                    # if this is the first item in the group, set the group start time
                    if group_start_time is None:
                        group_start_time = time.monotonic()
            elif buffer:
                # otherwise if the task timeout expired and we have items in the buffer, yield the buffer
                yield buffer
                # clear the buffer and reset the group start time ready for the next group
                buffer = []
                group_start_time = None

    try:
        yield async_iter_groups()
    finally:  # pragma: no cover
        # after iteration if a tasks still exists, cancel it, this will only happen if an error occurred
        if task:
            task.cancel('Cancelling due to error in iterator')
            with suppress(asyncio.CancelledError):
                await task


def sync_anext(iterator: Iterator[T]) -> T:
    """Get the next item from a sync iterator, raising `StopAsyncIteration` if it's exhausted.

    Useful when iterating over a sync iterator in an async context.
    """
    try:
        return next(iterator)
    except StopIteration as e:
        raise StopAsyncIteration() from e


def now_utc() -> datetime:
    return datetime.now(tz=timezone.utc)


def guard_tool_call_id(t: _messages.ToolCallPart | _messages.ToolReturnPart | _messages.RetryPromptPart) -> str:
    """Type guard that either returns the tool call id or generates a new one if it's None."""
    return t.tool_call_id or generate_tool_call_id()


def generate_tool_call_id() -> str:
    """Generate a tool call id.

    Ensure that the tool call id is unique.
    """
    return f'pyd_ai_{uuid.uuid4().hex}'


class PeekableAsyncStream(Generic[T]):
    """Wraps an async iterable of type T and allows peeking at the *next* item without consuming it.

    We only buffer one item at a time (the next item). Once that item is yielded, it is discarded.
    This is a single-pass stream.
    """

    def __init__(self, source: AsyncIterable[T]):
        self._source = source
        self._source_iter: AsyncIterator[T] | None = None
        self._buffer: T | Unset = UNSET
        self._exhausted = False

    async def peek(self) -> T | Unset:
        """Returns the next item that would be yielded without consuming it.

        Returns None if the stream is exhausted.
        """
        if self._exhausted:
            return UNSET

        # If we already have a buffered item, just return it.
        if not isinstance(self._buffer, Unset):
            return self._buffer

        # Otherwise, we need to fetch the next item from the underlying iterator.
        if self._source_iter is None:
            self._source_iter = self._source.__aiter__()

        try:
            self._buffer = await self._source_iter.__anext__()
        except StopAsyncIteration:
            self._exhausted = True
            return UNSET

        return self._buffer

    async def is_exhausted(self) -> bool:
        """Returns True if the stream is exhausted, False otherwise."""
        return isinstance(await self.peek(), Unset)

    def __aiter__(self) -> AsyncIterator[T]:
        # For a single-pass iteration, we can return self as the iterator.
        return self

    async def __anext__(self) -> T:
        """Yields the buffered item if present, otherwise fetches the next item from the underlying source.

        Raises StopAsyncIteration if the stream is exhausted.
        """
        if self._exhausted:
            raise StopAsyncIteration

        # If we have a buffered item, yield it.
        if not isinstance(self._buffer, Unset):
            item = self._buffer
            self._buffer = UNSET
            return item

        # Otherwise, fetch the next item from the source.
        if self._source_iter is None:
            self._source_iter = self._source.__aiter__()

        try:
            return await self._source_iter.__anext__()
        except StopAsyncIteration:
            self._exhausted = True
            raise


def get_traceparent(x: AgentRun | AgentRunResult | GraphRun | GraphRunResult) -> str:
    return x._traceparent(required=False) or ''  # type: ignore[reportPrivateUsage]


def dataclasses_no_defaults_repr(self: Any) -> str:
    """Exclude fields with values equal to the field default."""
    kv_pairs = (
        f'{f.name}={getattr(self, f.name)!r}' for f in fields(self) if f.repr and getattr(self, f.name) != f.default
    )
    return f'{self.__class__.__qualname__}({", ".join(kv_pairs)})'


def number_to_datetime(x: int | float) -> datetime:
    return TypeAdapter(datetime).validate_python(x)


AwaitableCallable = Callable[..., Awaitable[T]]


@overload
def is_async_callable(obj: AwaitableCallable[T]) -> TypeIs[AwaitableCallable[T]]: ...


@overload
def is_async_callable(obj: Any) -> TypeIs[AwaitableCallable[Any]]: ...


def is_async_callable(obj: Any) -> Any:
    """Correctly check if a callable is async.

    This function was copied from Starlette:
    https://github.com/encode/starlette/blob/78da9b9e218ab289117df7d62aee200ed4c59617/starlette/_utils.py#L36-L40
    """
    while isinstance(obj, functools.partial):
        obj = obj.func

    return inspect.iscoroutinefunction(obj) or (callable(obj) and inspect.iscoroutinefunction(obj.__call__))  # type: ignore
