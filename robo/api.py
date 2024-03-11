import asyncio
import concurrent.futures
from dataclasses import dataclass
from typing import Optional

import robo.extractors as extractors
from robo.types import Result, ResultSummary

# The default amount of parallelism.
#
# This is kinda arbitrary -- we want to be good citizens, but the "correct"
# value depends on the particular client machine and extractor.
#
# Should be "big enough" without hammering too hard on whatever sits at the
# other end (which is more often than not a website). This should be
# override-able by the user, so not a deal-breaker either way.
DEFAULT_MAX_WORKERS = 10


def extract_one(extractor_name: str, key: str, local_testing: bool) -> list[Result]:
    """Fetch the given `Extractor` by name and use it to extract data for the
    given search key. If `local_testing` is `True`, attempt to use local test
    data instead of hitting a remote source."""
    extract = extractors.get_extractor(extractor_name)
    return extract(key.strip(), local_testing)


@dataclass
class RoboOpts:
    # Set to `True` to test using local data rather than hitting remote sources.
    local_testing: bool

    # Maximum number of `extract` operations to run in parallel. If `None`, we
    # allow Python to pick a reasonable max based on your CPU.
    max_parallel: Optional[int] = DEFAULT_MAX_WORKERS

    # Run at most `limit` `extract` operations, regardless of the size of the
    # incoming list. If `None`, we impose no limit.
    # TODO: WARNING: Not actually implemented yet!
    limit: Optional[int] = None


def extract_list(
    extractor_name: str,
    keys: list[str],
    opts: RoboOpts,
) -> ResultSummary:
    """Fetch the given `Extractor` by name and use it to extract data for the
    given list of search keys. Use `opts` to alter extractor behavior."""
    return asyncio.run(
        extract_list_parallel(
            extractor_name, keys, opts.local_testing, opts.max_parallel
        )
    )


# I have chosen here to treat each `Extractor` as a black box bit of (probably)
# blocking IO. (As opposed to making the signature of an `Extractor` `async`,
# for example, and making the whole application more "purely" use `asyncio`.)
#
# This almost certainly makes things a bit less efficient, but has the MAJOR
# upside of encapsulating all the complexity/annoyance of concurrency in this
# one module. And, importantly, it ensures that `Extractor` authors don't have
# to think about it at all, nor do they have to worry about using only
# libraries which support `asyncio` out of the box.
async def extract_list_parallel(
    extractor_name: str,
    keys: list[str],
    local_testing: bool,
    num_parallel: Optional[int],
) -> ResultSummary:
    """Execute the given extractor against the list of search keys, running up
    to `num_parallel` threads in parallel. Passing `None` for `num_parallel`
    will use Python's default maximum value, which depends on your CPU."""
    extract = extractors.get_extractor(extractor_name)

    # Simple wrapper to pair an `extract` result with its key. Useful for gathering
    # the final results summary in a functional, concurrency-friendly way.
    def extract_key_and_result(k: str) -> tuple[str, list[Result]]:
        return (k, extract(k, local_testing))

    # Note that we could just use `to_thread()` for an easier time, but that wasn't
    # added till Python 3.9 and I'm trying to keep support for Python >= 3.8.
    # Also note the custom `ThreadPoolExecutor`, which allows setting the
    # maximum number of workers -- we need a lever to control the parallelism.
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_parallel) as pool:
        # Yet another wrapper, which sends an extractor off to a new thread:
        async def async_extract(k: str):
            return await loop.run_in_executor(pool, extract_key_and_result, k)

        async_results = map(async_extract, keys)
        results: list[tuple[str, list[Result]]] = await asyncio.gather(*async_results)

    results_summary = empty_summary()
    for k, r in results:
        results_summary.append(k, r)
    return results_summary


def empty_summary() -> ResultSummary:
    return ResultSummary(results=[], results_success=set(), results_not_found=set())
