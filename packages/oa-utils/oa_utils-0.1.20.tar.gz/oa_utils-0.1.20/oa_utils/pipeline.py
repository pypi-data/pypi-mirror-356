from __future__ import annotations
import functools
import itertools
import more_itertools
import json
from pprint import pprint, pformat
from tabulate import tabulate
from collections import defaultdict
from typing import IO, Callable, Iterable, Sequence, Literal, TypeVar, Any, overload
from dataclasses import dataclass
from multiprocessing import Pool
import random

default_json_encoder = lambda obj: vars(obj) if hasattr(obj, '__dict__') else str(obj)

T_co = TypeVar("T_co", covariant=True)
T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")
K = TypeVar("K")

class Pipeline(tuple[T_co, ...]):
    """This class is useful for programming in the *collection pipeline* style.
    It wraps a homogenous variadic tuple and exposes a fluent interface with 
    common functional programming operations. Why a tuple and not a "lazy" iterator? 
    Because a tuple is relatively immutable and because, in my opinion, 
    reified collections are much easier to reason about than stateful iterators
    (at the expense of performance).
        
    >>> hamming_distance = (
    ...     Pipeline("karolin") # ('k', 'a', 'r', 'o', 'l', 'i', 'n')
    ...     .zip_with(lambda a, b: int(a != b), "kathrin") # (0, 0, 1, 1, 1, 0, 0)
    ...     .sum() # 3
    ... )
    
    >>> hamming_distance
    3
    """

    def map(self, fn: Callable[[T_co], U]) -> Pipeline[U]:
        """Apply *fn* to every element.
        
        >>> Pipeline([1, 2, 3]).map(lambda x: x * 2)
        (2, 4, 6)
        """
        return Pipeline(map(fn, self))

    def par_map(self, fn: Callable[[T_co], U], 
               processes: int | None = None,
               maxtasksperchild: int | None = None,
               chunksize: int | None = None) -> Pipeline[U]:
        """Apply *fn* to every element in parallel using a pool of processes.
        *fn* must be picklable, so it can't be a lambda function.
        
        >>> Pipeline(range(1, 11)).par_map(square, processes=2)
        (1, 4, 9, 16, 25, 36, 49, 64, 81, 100)
        """
        with Pool(processes=processes, maxtasksperchild=maxtasksperchild) as pool:
            return Pipeline(pool.map(fn, self, chunksize))

    def filter(self, pred: Callable[[T_co], bool]) -> Pipeline[T_co]:
        """Keep only elements for which *pred* returns True.
        
        >>> Pipeline([1, 2, 3, 4]).filter(lambda x: x % 2 == 0)
        (2, 4)
        """
        return Pipeline(filter(pred, self))

    def zip(self, other: Iterable[U], strict: bool = False) -> Pipeline[tuple[T_co, U]]:
        """Pair each element with the corresponding element from *other* (like :func:`zip`).
        
        >>> Pipeline([1, 2]).zip([10, 20])
        ((1, 10), (2, 20))
        """
        return Pipeline(zip(self, other, strict=strict))

    def zip_longest(self, other: Iterable[U], fillvalue: V) -> Pipeline[tuple[T_co | V, U | V]]:
        """Zip two iterables, filling missing positions with *fillvalue* (like :func:`itertools.zip_longest`).
        
        >>> Pipeline([1, 2]).zip_longest([10, 20, 30], fillvalue=None)
        ((1, 10), (2, 20), (None, 30))
        
        >>> Pipeline([1, 2, 3]).zip_longest([10, 20], fillvalue=0)
        ((1, 10), (2, 20), (3, 0))
        """
        return Pipeline(itertools.zip_longest(self, other, fillvalue=fillvalue))

    def zip_with(self, fn: Callable[[T_co, U], V], other: Iterable[U], strict: bool = False) -> Pipeline[V]:
        """Zip with *other* and immediately combine pairs using *fn*.
        
        >>> Pipeline([1, 2]).zip_with(lambda a, b: a + b, [10, 20])
        (11, 22)
        """
        return Pipeline(fn(a, b) for a, b in zip(self, other, strict=strict))

    def par_zip_with(self, fn: Callable[[T_co, U], V], 
                     other: Iterable[U],
                     strict: bool = False,
                     processes: int | None = None,
                     maxtasksperchild: int | None = None,
                     chunksize: int | None = None) -> Pipeline[V]:
        """Zip with *other* and immediately combine pairs using *fn* in parallel.
        *fn* must be picklable, so it can't be a lambda function.
        
        >>> from operator import add
        >>> Pipeline([1, 2]).par_zip_with(add, [10, 20], processes=2)
        (11, 22)
        
        Reproducible shuffle example:
        
        >>> seeds = [123, 456, 789]
        >>> Pipeline([1, 2, 3, 4] * 3).batch(4).par_zip_with(shuffle_batch, seeds, processes=2)
        ((1, 2, 4, 3), (4, 2, 3, 1), (4, 3, 1, 2))
        """
        with Pool(processes=processes, maxtasksperchild=maxtasksperchild) as pool:
            return Pipeline(pool.starmap(fn, zip(self, other, strict=strict), chunksize))

    def join_with(self: Pipeline[T], separator: T) -> Pipeline[T]:
        """Join elements with a *separator*.
        
        >>> Pipeline([1, 2, 3]).join_with(0)
        (1, 0, 2, 0, 3)
        """
        if self.is_empty():
            return Pipeline([])
        return Pipeline(itertools.chain.from_iterable(
            (item, separator) for item in self[:-1])).extend([self[-1]])

    def split_at(self, pred: Callable[[T_co], bool], maxsplit: int = -1, 
                 keep_separator: bool = False) -> Pipeline[Pipeline[T_co]]:
        """Split the pipeline at every occurrence of an element for which *pred* returns True.
        
        >>> Pipeline([1, 2, 0, 3, 4, 0, 5]).split_at(lambda x: x == 0)
        ((1, 2), (3, 4), (5,))
        
        >>> Pipeline([1, 2, 0, 3, 4, 0, 5]).split_at(lambda x: x == 0, keep_separator=True)
        ((1, 2), (0,), (3, 4), (0,), (5,))
        """
        return Pipeline(Pipeline(batch) for batch in more_itertools.split_at(
            self, pred, maxsplit=maxsplit, keep_separator=keep_separator))

    def cartesian_product(self, other: Iterable[U]) -> Pipeline[tuple[T_co, U]]:
        """Return the Cartesian product of *self* x *other*.
        
        >>> Pipeline([1, 2]).cartesian_product([10, 20])
        ((1, 10), (1, 20), (2, 10), (2, 20))
        """
        return Pipeline(itertools.product(self, other))

    def outer_product(self, fn: Callable[[T_co, U], V], other: Iterable[U]) -> Pipeline[Pipeline[V]]:
        """Return the outer product of *self* x *other* using *fn* to combine pairs.
        
        >>> Pipeline([1, 2, 3]).outer_product(lambda a, b: a * b, [1, 2, 3])
        ((1, 2, 3), (2, 4, 6), (3, 6, 9))
        """
        return Pipeline(Pipeline(row) for row in more_itertools.outer_product(func=fn, xs=self, ys=other))

    def sort(self, key: Callable[[T_co], Any] | None = None, reverse: bool = False) -> Pipeline[T_co]:
        """Sort the elements.
        
        >>> Pipeline([3, 1, 2]).sort()
        (1, 2, 3)
        
        >>> Pipeline([3, 1, 2]).sort(reverse=True)
        (3, 2, 1)
        """
        return Pipeline(sorted(self, key=key, reverse=reverse)) # type: ignore

    def unique(self) -> Pipeline[T_co]:
        """Remove duplicates while preserving order.
        
        >>> Pipeline([1, 2, 2, 3]).unique()
        (1, 2, 3)
        """
        return Pipeline(dict.fromkeys(self))
    
    def slice(self, start: int = 0, end: int | None = None, step: int = 1) -> Pipeline[T_co]:
        """Return a slice of the pipeline like *self[start:end:step]*.
        
        >>> Pipeline([1, 2, 3, 4, 5]).slice(1, 4)
        (2, 3, 4)
        """
        if end is None:
            end = len(self)
        return Pipeline(self[start:end:step])

    def take(self, n: int) -> Pipeline[T_co]:
        """Return the first *n* items.
        
        >>> Pipeline([1, 2, 3, 4]).take(2)
        (1, 2)

        >>> Pipeline([1, 2, 3, 4]).take(-1)
        (1, 2, 3)
        """
        return Pipeline(self[:n])
    
    def drop(self, n: int) -> Pipeline[T_co]:
        """Drop the first *n* items.

        >>> Pipeline([1, 2, 3, 4]).drop(2)
        (3, 4)

        >>> Pipeline([1, 2, 3, 4]).drop(-3)
        (2, 3, 4)
        """
        return Pipeline(self[n:])

    def enumerate(self, start: int = 0) -> Pipeline[tuple[int, T_co]]:
        """Enumerate the pipeline, yielding (index, item) pairs.
        
        >>> Pipeline(['a', 'b']).enumerate()
        ((0, 'a'), (1, 'b'))
        """
        return Pipeline(enumerate(self, start))

    def batch(self, n: int, strict: bool = False) -> Pipeline[Pipeline[T_co]]:
        """Group the data into fixed-size chunks. Like :func:`more_itertools.chunked`.
        
        >>> Pipeline(range(1, 6)).batch(2)
        ((1, 2), (3, 4), (5,))
        """
        return Pipeline([Pipeline(batch) for batch 
                         in more_itertools.chunked(self, n, strict=strict)])
    
    def batch_fill(self, n: int, 
                   fillvalue: U,
                   incomplete: Literal['fill', 'ignore', 'strict'] = 'fill') -> Pipeline[Pipeline[T_co | U]]:
        """Batch with padding via *fillvalue* (delegate to :func:`more_itertools.grouper`).
        
        >>> Pipeline(range(1, 6)).batch_fill(2, fillvalue=0)
        ((1, 2), (3, 4), (5, 0))
        """
        return Pipeline([Pipeline(row) for row in more_itertools.grouper(
                        self, n, incomplete=incomplete, fillvalue=fillvalue)])

    def flatten(self: Pipeline[Iterable[T]]) -> Pipeline[T]:
        """Flatten one level of nesting.
        
        >>> Pipeline([[1, 2], [3, 4]]).flatten()
        (1, 2, 3, 4)
        """
        if not all(isinstance(item, Iterable) for item in self):
            raise ValueError("flatten requires a Pipeline of Iterables")
        return Pipeline(itertools.chain.from_iterable(self))

    def flat_map(self, fn: Callable[[T_co], Iterable[U]]) -> Pipeline[U]:
        """Map each element to an iterable and flatten the result.
        
        >>> Pipeline([1, 2, 3]).flat_map(lambda x: [x] * 2)
        (1, 1, 2, 2, 3, 3)
        
        >>> Pipeline([1, 2, 3]).flat_map(lambda x: range(x))
        (0, 0, 1, 0, 1, 2)
        """
        return self.map(fn).flatten()

    def for_each(self, fn: Callable[[T_co], None]) -> Pipeline[T_co]:
        """Call a side-effecting function for every element and return self.
        
        >>> Pipeline([1, 2, 3]).for_each(print)
        1
        2
        3
        (1, 2, 3)
        """
        for item in self:
            fn(item)
        return self

    def par_for_each(self, fn: Callable[[T_co], None],
                     processes: int | None = None,
                     maxtasksperchild: int | None = None,
                     chunksize: int | None = None) -> Pipeline[T_co]:
        """Call a side-effecting function for every element in parallel 
        using a pool of processes and return self.
        *fn* must be picklable, so it can't be a lambda function.
        
        >>> Pipeline(range(1, 11)).par_for_each(swallow, processes=2)
        (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        """
        with Pool(processes=processes, maxtasksperchild=maxtasksperchild) as pool:
            pool.map(fn, self, chunksize)
        return self

    def for_self(self, fn: Callable[[Pipeline[T_co]], None]) -> Pipeline[T_co]:
        """Call *fn(self)* for its side-effects and return self.
        
        >>> Pipeline([1, 2, 3]).for_self(lambda p: print(p.len()))
        3
        (1, 2, 3)
        """
        fn(self)
        return self

    def apply(self, fn: Callable[[Iterable[T_co]], Iterable[U]]) -> Pipeline[U]:
        """Apply a custom or external iterable-to-iterable function (e.g. from *itertools* or *more_itertools*).
        To preserve type safety, it's recommended to use a type hint for *fn*.
        
        >>> transpose: Callable[[Iterable[Iterable[int]]], Iterable[tuple[int, ...]]] = more_itertools.transpose
        >>> Pipeline([[1, 2, 3], [4, 5, 6]]).apply(transpose)
        ((1, 4), (2, 5), (3, 6))
        
        >>> pairwise: Callable[[Iterable[int]], Iterable[tuple[int, int]]] = itertools.pairwise
        >>> Pipeline([1, 2, 3]).apply(pairwise)
        ((1, 2), (2, 3))
        """
        return Pipeline(fn(self))

    def transpose(self: Pipeline[Iterable[T]]) -> Pipeline[Pipeline[T]]:
        """Transpose a pipeline of iterables (like :func:`more_itertools.transpose`).
        
        >>> Pipeline([["Roger", "Alice", "Bob"], [24, 35, 60]]).transpose()
        (('Roger', 24), ('Alice', 35), ('Bob', 60))
        
        >>> Pipeline([[1, 2, 3], [4, 5, 6]]).transpose()
        ((1, 4), (2, 5), (3, 6))
        """
        return Pipeline(Pipeline(row) for row in more_itertools.transpose(self))   

    def print(self, label: str = "", 
              label_only: bool = False,
              end: str | None = "\n",
              file: IO[str] | None = None,
              flush: bool = False) -> Pipeline[T_co]:
        """Print the pipeline (optionally with a *label*) and return *self*.
        
        >>> Pipeline([1, 2, 3]).print("Numbers: ", end="\\n\\n")
        Numbers: (1, 2, 3)
        <BLANKLINE>
        (1, 2, 3)
        
        >>> Pipeline([1, 2, 3]).print("Numbers:", label_only=True)
        Numbers:
        (1, 2, 3)
        """
        if label_only:
            print(label, end=end, file=file, flush=flush)
        else:
            print(f"{label}{self}", end=end, file=file, flush=flush)
        return self

    def pprint(self, label: str = "", end: str = "",
               stream: IO[str] | None = None, 
               indent: int = 1, width: int = 80, 
               depth: int | None = None, 
               compact: bool = False, 
               sort_dicts: bool = True, 
               underscore_numbers: bool = False) -> Pipeline[T_co]:
        """Pretty-print the pipeline with :pymeth:`pprint.pprint`.
        
        >>> Pipeline([1, 2, 3]).pprint("Numbers:" , end="---------")
        Numbers:
        (1, 2, 3)
        ---------
        (1, 2, 3)
        """
        if label:
            print(label, file=stream)
        pprint(self, stream=stream, indent=indent, width=width,
               depth=depth, compact=compact, sort_dicts=sort_dicts,
               underscore_numbers=underscore_numbers)
        if end:
            print(end, file=stream)
        return self

    def print_json(self, label: str = "", end: str = "", 
                   stream: IO[str] | None = None, 
                   indent: int | str | None = 2,
                   default: Callable[[Any], Any] = default_json_encoder) -> Pipeline[T_co]:
        """Print the pipeline as JSON (with an optional *label*).
        
        >>> Pipeline([1, 2, 3]).print_json()
        [
          1,
          2,
          3
        ]
        (1, 2, 3)
        
        >>> Pipeline([Vector2(1.0, 2.0)]).print_json()
        [
          {
            "x": 1.0,
            "y": 2.0
          }
        ]
        (Vector2(x=1.0, y=2.0),)
        """
        if label:
            print(label, file=stream)
        print(json.dumps(self, indent=indent, default=default), file=stream)
        if end:
            print(end, file=stream)
        return self

    def print_table(self: Pipeline[T_co], label: str = "", end: str = "",
                    stream: IO[str] | None = None,
                    headers: str | dict[Any, str] | Sequence[str] = "keys",
                    tablefmt: str = "github",
                    floatfmt: str | Iterable[str] = "g",
                    intfmt: str | Iterable[str] = "",
                    numalign: str | None = "default",
                    stralign: str | None = "default",
                    missingval: str | Iterable[str] = "",
                    showindex: str | bool | Iterable[Any] = "default",
                    disable_numparse: bool | Iterable[int] = False,
                    colalign: Iterable[str | None] | None = None,
                    maxcolwidths: int | Iterable[int | None] | None = None,
                    rowalign: str | Iterable[str] | None = None,
                    maxheadercolwidths: int | Iterable[int] | None = None) -> Pipeline[T_co]:
        """Pretty-print a pipeline of "rows" as a table using :func:`tabulate`.
        
        >>> Pipeline([{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}]).print_table()
        | name   |   age |
        |--------|-------|
        | Alice  |    30 |
        | Bob    |    25 |
        ({'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25})
        
        >>> Pipeline([Vector2(1.0, 2.0), Vector2(3.0, 4.0)]).print_table(showindex=True)
        |    |   x |   y |
        |----|-----|-----|
        |  0 |   1 |   2 |
        |  1 |   3 |   4 |
        (Vector2(x=1.0, y=2.0), Vector2(x=3.0, y=4.0))
        """
        if label:
            print(label, file=stream)
        print(tabulate(self, # type: ignore
                       headers=headers, 
                       tablefmt=tablefmt, 
                       floatfmt=floatfmt, 
                       intfmt=intfmt, 
                       numalign=numalign, 
                       stralign=stralign, 
                       missingval=missingval, 
                       showindex=showindex, 
                       disable_numparse=disable_numparse,
                       colalign=colalign,
                       maxcolwidths=maxcolwidths,
                       rowalign=rowalign,
                       maxheadercolwidths=maxheadercolwidths), file=stream)
        if end:
            print(end, file=stream)
        return self

    def extend(self, items: Iterable[T_co]) -> Pipeline[T_co]:
        """Return a new pipeline with *items* appended.
        
        >>> Pipeline([1, 2]).extend([3, 4])
        (1, 2, 3, 4)
        """
        return Pipeline(self + tuple(items))
    
    def insert_at(self, index: int, items: Iterable[T_co]) -> Pipeline[T_co]:
        """Insert *items* at *index*.
        
        >>> Pipeline([1, 2, 5]).insert_at(2, [3, 4])
        (1, 2, 3, 4, 5)
        """
        return Pipeline(self[:index] + tuple(items) + self[index:])
    
    def reverse(self) -> Pipeline[T_co]:
        """Reverse the order of the elements.
        
        >>> Pipeline([1, 2, 3]).reverse()
        (3, 2, 1)
        """
        return Pipeline(reversed(self))

    def group_by(self, key: Callable[[T_co], K]) -> Pipeline[tuple[K, Pipeline[T_co]]]:
        """Group elements by *key* and return (key, subgroup) pairs.
        Use to_dict() to convert the pairs to a dictionary.
        
        >>> names = ['Roger', 'Alice', 'Adam', 'Bob']
        >>> Pipeline(names).group_by(lambda name: name[0])
        (('R', ('Roger',)), ('A', ('Alice', 'Adam')), ('B', ('Bob',)))
        
        >>> people = [{'name': 'Roger', 'age': 25},
        ...           {'name': 'Alice', 'age': 25},
        ...           {'name': 'Bob', 'age': 11}]
        >>> Pipeline(people).group_by(lambda person: person['age'])
        ((25, ({'name': 'Roger', 'age': 25}, {'name': 'Alice', 'age': 25})), (11, ({'name': 'Bob', 'age': 11},)))
        
        >>> Pipeline(range(10)).group_by(lambda x: x % 2 == 0)
        ((True, (0, 2, 4, 6, 8)), (False, (1, 3, 5, 7, 9)))
        """
        grouped: defaultdict[K, list[T_co]] = defaultdict(list)
        for item in self:
            grouped[key(item)].append(item)
        return Pipeline((k, Pipeline(v)) for k, v in grouped.items())

    def sample(self, n: int) -> Pipeline[T_co]:
        """Select *n* random elements from the pipeline. 
        For repeatable results, set the random seed before calling this method.
        
        >>> random.seed(1234)
        >>> Pipeline([1, 2, 3, 4, 5]).sample(3)
        (4, 1, 5)
        """
        return Pipeline(random.sample(self, n))
    
    def shuffle(self) -> Pipeline[T_co]:
        """Shuffle the elements. 
        For repeatable results, set the random seed before calling this method.
        
        >>> random.seed(1234)
        >>> Pipeline([1, 2, 3, 4, 5]).shuffle()
        (4, 1, 5, 3, 2)
        """
        return self.sample(self.len())
    
    # === Terminal methods ===

    def to_list(self) -> list[T_co]:
        """Convert to a list`.
        
        >>> Pipeline([1, 2, 3]).to_list()
        [1, 2, 3]
        """
        return list(self)

    def to_tuple(self) -> tuple[T_co, ...]:
        """Convert to a plain tuple.
        
        >>> Pipeline([1, 2, 3]).to_tuple()
        (1, 2, 3)
        """
        return tuple(self)

    def to_set(self) -> set[T_co]:
        """Convert to a set, removing duplicates.
        
        >>> Pipeline([1, 2, 3, 3]).to_set()
        {1, 2, 3}
        """
        return set(self)

    def to_dict(self: Pipeline[tuple[K, V]]) -> dict[K, V]:
        """Convert a pipeline of (key, value) tuples to a dict.
        
        >>> Pipeline([("a", 1), ("b", 2)]).to_dict()
        {'a': 1, 'b': 2}
        """
        return dict(self)

    def to_str(self, separator: str = '') -> str:
        """Convert each element to a string and join them with the *separator*.
        
        >>> Pipeline([1, 2, 3]).to_str(', ')
        '1, 2, 3'
        """
        return separator.join(self.map(str))
        
    def to_json(self, indent: int | str | None = 2, 
                default: Callable[[Any], Any] = default_json_encoder) -> str:
        """Serialize the pipeline to a JSON string.
        
        >>> Pipeline([1, 2, 3]).to_json()
        '[\\n  1,\\n  2,\\n  3\\n]'
        
        >>> Pipeline([Vector2(1.0, 2.0)]).to_json()
        '[\\n  {\\n    "x": 1.0,\\n    "y": 2.0\\n  }\\n]'
        """
        return json.dumps(self, indent=indent, default=default)

    def to_pformat(self, indent: int = 1, 
                   width: int = 80, 
                   depth: int | None = None, 
                   compact: bool = False, 
                   sort_dicts: bool = True, 
                   underscore_numbers: bool = False) -> str:
        """Return the pretty-formatted string representation of the pipeline.
                
        >>> Pipeline([Vector2(1.0, 2.0), Vector2(3.0, 4.0)]).to_pformat()
        '(Vector2(x=1.0, y=2.0), Vector2(x=3.0, y=4.0))'
        """
        return pformat(self, indent=indent, width=width, depth=depth, compact=compact, 
                       sort_dicts=sort_dicts, underscore_numbers=underscore_numbers)

    def to_table(self: Pipeline[T_co], 
                 headers: str | dict[Any, str] | Sequence[str] = "keys",
                 tablefmt: str = "github",
                 floatfmt: str | Iterable[str] = "g",
                 intfmt: str | Iterable[str] = "",
                 numalign: str | None = "default",
                 stralign: str | None = "default",
                 missingval: str | Iterable[str] = "",
                 showindex: str | bool | Iterable[Any] = "default",
                 disable_numparse: bool | Iterable[int] = False,
                 colalign: Iterable[str | None] | None = None,
                 maxcolwidths: int | Iterable[int | None] | None = None,
                 rowalign: str | Iterable[str] | None = None,
                 maxheadercolwidths: int | Iterable[int] | None = None) -> str:
        """Convert the pipeline to a formatted table string using :func:`tabulate`.
        
        >>> Pipeline([{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}]).to_table()
        '| name   |   age |\\n|--------|-------|\\n| Alice  |    30 |\\n| Bob    |    25 |'
        """
        return tabulate(self, # type: ignore
                        headers=headers, 
                        tablefmt=tablefmt, 
                        floatfmt=floatfmt, 
                        intfmt=intfmt, 
                        numalign=numalign, 
                        stralign=stralign, 
                        missingval=missingval, 
                        showindex=showindex, 
                        disable_numparse=disable_numparse,
                        colalign=colalign,
                        maxcolwidths=maxcolwidths,
                        rowalign=rowalign,
                        maxheadercolwidths=maxheadercolwidths)

    def reduce(self, fn: Callable[[V, T_co], V], initial: V) -> V:
        """Reduce the pipeline to a single value using *fn*.
        
        >>> Pipeline([104, 101, 108, 108, 111]).reduce(lambda acc, x: acc + chr(x), "")     
        'hello'
        """
        return functools.reduce(fn, self, initial)

    def reduce_non_empty(self, fn: Callable[[T_co, T_co], T_co]) -> T_co:
        """Reduce a non-empty pipeline to a single value using *fn*.
        
        >>> Pipeline([1, 2, 3]).reduce_non_empty(lambda acc, x: acc + x)
        6
        """
        if self.is_empty():
            raise ValueError("Pipeline is empty")
        return functools.reduce(fn, self)

    def par_reduce_non_empty(
        self,
        fn: Callable[[T_co, T_co], T_co],
        processes: int | None = None,
        maxtasksperchild: int | None = None,
        chunksize: int | None = None) -> T_co:
        """
        Parallel binary-tree reduction. O(log n)
        *fn* must be picklable (no lambdas).

        >>> from operator import add
        >>> Pipeline("Parallelism!").par_reduce_non_empty(add, processes=2)
        'Parallelism!'
        """
        if self.is_empty():
            raise ValueError("Pipeline is empty")

        values = list(self)
        with Pool(processes=processes, maxtasksperchild=maxtasksperchild) as pool:
            while len(values) > 1:
                # pairwise grouping: (v0,v1), (v2,v3), ...
                pairs = list(zip(values[::2], values[1::2]))
                # reduce each pair in parallel
                reduced = pool.starmap(fn, pairs, chunksize) if pairs else []
                # carry over the last element if the list length was odd
                if len(values) % 2 == 1:
                    reduced.append(values[-1])
                values = reduced
        return values[0]

    def len(self) -> int:
        """Return the length of the pipeline.
        
        >>> Pipeline([1, 2, 3]).len()
        3
        """
        return len(self)
    
    def min(self) -> T_co:
        """Return the minimum element.
        
        >>> Pipeline([3, 1, 2]).min()
        1
        """
        return min(self) # type: ignore 
    
    def max(self) -> T_co:
        """Return the maximum element.
        
        >>> Pipeline([3, 1, 2]).max()
        3
        """
        return max(self) # type: ignore
    
    def sum(self) -> T_co:
        """Return the sum of the elements.
        
        >>> Pipeline([1, 2, 3]).sum()
        6
        """
        return sum(self) # type: ignore
    
    def avg(self) -> float:
        """Return the average of the elements.
        
        >>> Pipeline([1, 2, 3]).avg()
        2.0
        """
        if self.is_empty():
            raise ValueError("Pipeline is empty")
        return sum(self) / len(self) # type: ignore
    
    def any(self) -> bool:
        """Return True if any element is True.
        
        >>> Pipeline([False, False, True]).any()
        True
        
        >>> Pipeline([False, False, False]).any()
        False
        """
        return any(self)
    
    def all(self) -> bool:
        """Return True if all elements are True.
        
        >>> Pipeline([True, True, True]).all()
        True
        
        >>> Pipeline([True, False, True]).all()
        False
        """
        return all(self)
    
    def contains(self, pred: Callable[[T_co], bool]) -> bool:
        """Return True if any element passes the predicate.
        
        >>> Pipeline([1, 2, 3]).contains(lambda x: x == 2)
        True
        
        >>> Pipeline([1, 2, 3]).contains(lambda x: x > 3)
        False
        """
        for item in self:
            if pred(item):
                return True
        return False

    def is_empty(self) -> bool:
        """Return True if the pipeline is empty.
        
        >>> Pipeline([]).is_empty()
        True
        
        >>> Pipeline([1, 2]).is_empty()
        False
        """
        return len(self) == 0

    def unzip(self: Pipeline[tuple[T, U]]) -> tuple[Pipeline[T], Pipeline[U]]:
        """Opposite of zip. Unzip a pipeline of (a, b) pairs into a pair of pipelines.
        Can be used for extracting keys and values from a grouped pipeline.
        
        >>> Pipeline([1, 2, 3]).zip([10, 20, 30]).unzip()
        ((1, 2, 3), (10, 20, 30))
        
        >>> names = ['Alice', 'Bob', 'Charlie']
        >>> keys, values = Pipeline(names).group_by(lambda name: name[0]).unzip()
        >>> keys
        ('A', 'B', 'C')
        >>> values
        (('Alice',), ('Bob',), ('Charlie',))
        """
        return Pipeline(self).map(lambda x: x[0]), Pipeline(self).map(lambda x: x[1])

    # === Dunder methods ===
    
    def __add__(self, other: Iterable[T_co]) -> Pipeline[T_co]: # type: ignore
        """Concatenate with another iterable.
        
        >>> Pipeline([1, 2]) + [3, 4]
        (1, 2, 3, 4)
        """
        return Pipeline(self.to_list() + list(other)) 

    def __radd__(self, other: Iterable[T_co]) -> Pipeline[T_co]: # type: ignore
        """Concatenate with another iterable (right addition).
        
        >>> [1, 2] + Pipeline([3, 4])
        (1, 2, 3, 4)
        """
        return Pipeline(list(other) + self.to_list())

    def __mul__(self, n: int) -> Pipeline[T_co]: # type: ignore
        """Repeat the pipeline *n* times.
        
        >>> Pipeline([1, 2]) * 2
        (1, 2, 1, 2)
        """
        return Pipeline(self.to_list() * n)
 
    def __rmul__(self, n: int) -> Pipeline[T_co]: # type: ignore
        """Repeat the pipeline *n* times (right multiplication).
        
        >>> 2 * Pipeline([1, 2])
        (1, 2, 1, 2)
        """
        return self * n

# === Helpers ===

def square(x: float) -> float:
    """Used for testing."""
    return x * x

def swallow(x: Any) -> None:
    """Used for testing."""
    pass

def shuffle_batch(batch: Pipeline[int], seed: int) -> Pipeline[int]:
    """Used for tesing."""
    random.seed(seed)
    return batch.shuffle()

@dataclass
class Vector2:
    """Used for testing."""
    x: float
    y: float

def unpack(fn: Callable[[T, U], V]) -> Callable[[tuple[T, U]], V]:
    """Returns a function that unpacks a 2-tuple and applies a binary function to its elements.
    Useful for functions that expect two arguments but you have a tuple.
    
    >>> Pipeline([(1, 2), (3, 4)]).map(unpack(lambda a, b: a + b))
    (3, 7)
    """
    def wrapper(pair: tuple[T, U]) -> V:
        a, b = pair
        return fn(a, b)
    return wrapper

if __name__ == "__main__":
    # Interpreter usage: 
    # from importlib import reload; import oa_utils.pipeline; reload(oa_utils.pipeline); from oa_utils.pipeline import Pipeline, unpack
    import doctest
    doctest.testmod()
    