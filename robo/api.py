import asyncio
import concurrent.futures

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


def extract_list(
    extractor_name: str,
    keys: list[str],
    local_testing: bool,
    num_parallel=DEFAULT_MAX_WORKERS,
) -> ResultSummary:
    """Fetch the given `Extractor` by name and use it to extract data for the
    given list of search keys, running up to `num_parallel` threads in
    parallel. If `local_testing` is `True`, attempt to use local test data
    instead of hitting a remote source."""
    return asyncio.run(
        extract_list_parallel(extractor_name, keys, local_testing, num_parallel)
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
    extractor_name: str, keys: list[str], local_testing: bool, num_parallel: int
) -> ResultSummary:
    """Execute the given extractor against the list of search keys, running up
    to `num_parallel` threads in parallel."""
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
        results = await asyncio.gather(*async_results)

    results_summary = empty_summary()
    for k, r in results:
        results_summary.append(k, r)
    return results_summary


def empty_summary() -> ResultSummary:
    return ResultSummary(results=[], results_success=set(), results_not_found=set())
