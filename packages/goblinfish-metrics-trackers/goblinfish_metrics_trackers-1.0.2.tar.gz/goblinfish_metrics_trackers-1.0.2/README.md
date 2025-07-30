# The goblinfish.metrics.trackers Package

> Provides context-manager classes to name, track and report elapsed-time and other, user-defined metrics for top-level process entry-points (like AWS Lambda Function handlers, which is what it was originally conceived for) and sub-processes within them.

## Quick Start

Install in your project:

```shell
# Install with pip
pip install goblinfish-metrics-trackers
```

```shell
# Install with pipenv
pipenv install goblinfish-metrics-trackers
```

Import in your code:

```python
from goblinfish.metrics.trackers import ProcessTracker
```

Create the timing-tracker instance:

```python
tracker = ProcessTracker()
```

Decorate your top-level/entry-point function:

```python
@tracker
def some_function():
    ...
```

Add any sub-process timers:

```python
@tracker
def some_function():
    ...

    with tracker.timer('some_process_name'):
        # Do stuff here
        ...
```

Decorate any child process functions with the instance's `.track` method:

```python
@tracker
def some_function():
    ...

    with tracker.timer('some_process_name'):
        some_other_function()
        # Do stuff here
        ...

@tracker.track
def some_other_function():
    ...
```

Set any explicit metrics needed:

```python
@tracker
def some_function():
    ...

    with tracker.timer('some_process_name'):
        try:
            some_other_function()
            # Do stuff here
            ...
        except Exception as error:
            # Count of errors to be aggregated
            tracker.set_metric('some_function_errors', 1)
            # Name of error; simple string values are OK too!
            tracker.set_metric(
                'some_function_error_name', error.__class__.__name__
            )
            # Do stuff here
            ...

@tracker.track
def some_other_function():
    ...
```

When this code is executed, after the context created by the `@tracker` decorator is complete, it will `print` something that looks like this:

```json
{
    "some_function": 0.000,
    "some_other_function": 0.000,
    "some_process_name": 0.000
}
```

More detailed examples can be found in [the `examples` directory](https://bitbucket.org/stonefish-software-studio/goblinfish-metrics-trackers-package/src/main/examples/) in the repository.

### A top-level `ProcessTracker` instance is *required*

This package was designed around the idea of there being a top-level entry-point function and zero-to-many child functions. Applying a `@tracker.track` decorator to a function that isn't called by the entry-point function decorated with `@tracker` will yield unexpected result, or no results at all.

### Behavior in an `asyncio` context

This version will *work* with processes running under `asyncio`, for example:

```python
with tracker.timer('some_async_process'):
    async.run(some_function())
```

…**but** it may only capture the time needed for the async tasks/coroutines to be *created* rather than how long it takes for any of them to *execute*, depending on the implementation pattern used.

A more useful approach, shown in the `li-article-async-example.py` module in [the `examples` directory](https://bitbucket.org/stonefish-software-studio/goblinfish-metrics-trackers-package/src/main/examples/) is to encapsulate the async processes in an async *function*, then wrap all of that function's processes that need to be timed in the context manager. Stripping that function in the example down to a bare minimum simulation, it would look like this:

```python
async def get_person_data():
    sleep_for = random.randrange(2_000, 3_000) / 1000
    with tracker.timer('get_person_data'):
        await asyncio.sleep(sleep_for)
    return {'person_data': ('Professor Plum', dict())}
```

…which will contribute to the logged/printed output in a more meaningful fashion:

```json
{
    "get_person_data": 2215.262,
    "main": 8465.233
}
```

## Contribution guidelines

At this point, contributions are not accepted — I need to finish configuring the repository, deciding on whether I want to set up automated builds for pull-requests, and probably several other items. That said, if you have an idea that you want to propose as an addition, a bug that you want to call out, etc., please feel free to contact the maintainer(s) (see below).

## Who do I talk to?

The current maintainer(s) will always be listed in the `[maintainers]` section of [the `pyproject.toml` file](https://bitbucket.org/stonefish-software-studio/goblinfish-metrics-trackers-package/src/main/pyproject.toml) in the repository.

## Future plans (To-Dos) and BYOLF

While this package should work nicely for anything that can use a generic JSON log-message format, there are any number of products that are designed to read log-messages and ship them to some other service, usually with their own particular format requirements, in order to provide their own dashboards and alarms. If I have time in the future to start looking into those and writing [extras](https://stackoverflow.com/a/52475030) to accommodate, but I'm not confident that I'll have that time.

In the meantime, if there is a need for a specific log-message format, it's possible to BYOLF (**B**ring **Y**our **O**wn **L**og **F**ormat). Just write your own output function, and provide it as an argument to the `ProcessTracker` instance that is being created to track process items. What that would entail is:

- Writing a function that accepts a single `str` parameter.
- Deserializing that parameter from the JSON value that it will be passed.
- Creating the custom log-message output using whatever data is relevant.
- Writing that log-message in whatever manner is appropriate.

A *very* bare-bones example:

```python
def my_log_formatter(output: str) -> None:
    ...  # Handle the "output" log-line here as needed.

tracker = ProcessTracker(my_log_formatter)

# ...
```

Though this package was designed to issue log-messages in a reasonably standard output (`print` or some [`logging` package](https://docs.python.org/3.11/library/logging.html) functionality), there's no *functional* reason that it couldn't, for example, write data straight to some database, call some third-party API, or whatever else.
