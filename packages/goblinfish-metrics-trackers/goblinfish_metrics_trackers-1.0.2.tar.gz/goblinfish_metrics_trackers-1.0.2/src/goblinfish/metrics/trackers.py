#!/usr/bin/env python3
"""
Provides a collection of context manager types that can be used to
track process execution times (latencies), and store other values,
with named associations, before printing or logging them for
collection as metrics.

Usage Example:
--------------
This code:

>>> from goblinfish.metrics.trackers import ProcessTracker
>>> tracker = ProcessTracker()
>>> @tracker
>>> def some_function():
>>>     with tracker.timer('some_process_name'):
>>>         ... # Some process executes here
>>      some_other_function()
>>> @tracker.track
>>> def some_other_function():
>>>     ... # Some process executes here
>>> some_function()

will *print* something like this (pretty-printed here):
{
    "latencies": {
        "some_other_function": 0.005,
        "some_process_name": 0.038,
        "some_function": 0.056
    },
    "metrics": {}
}

See also the examples in the examples directory
"""

from __future__ import annotations

# Built-In Imports
import json
import time
import warnings

from contextlib import AbstractContextManager
from types import BuiltinFunctionType, BuiltinMethodType, \
    FunctionType, MethodType
from typing import Callable


# Concrete Module Classes
class ProcessTracker(AbstractContextManager):
    """
    Defines a context-manager type that can be used to wrap a single
    target callable to capture its total run-time, as well as timers
    within that same context to capture run-times for sub-processes,
    identified by name.
    """

    class _Timer(AbstractContextManager):
        """
        Defines a context-manager type, associated with a ProcessTracker
        instance, that handles the capture of elapsed time for the
        process(es) in the context, with an associated name.
        """
        def __init__(self, main_timer: ProcessTracker, name: str):
            """
            Object initialization.

            Parameters:
            -----------
            main_timer : ProcessTracker
                The ProcessTracker instance that this instance will log
                the elapsed time for the context to execute.
            name : str
                The name that the elapsed-time entry will be associated
                with in the parent ProcessTracker instance.

            Warnings:
            ---------
            If a timer name has already been used in the parent ProcessTracker
            instance
            """
            self._main_timer = main_timer
            self._name = name
            if self._main_timer._timers.get(self._name, None) is not None:
                warnings.warn(
                    f'A duplicate "{name}" timer has been started. This '
                    'may lead to undesirable/inaccurate timing results!'
                )
            self._start_time = None

        def __enter__(self):
            """
            The processes to execute when the context is started.
            See https://docs.python.org/3.11/reference/datamodel.html#object.__enter__
            """  # noqa E501
            self._start_time = time.time()
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            """
            The processes to execute when the context is ended.
            See https://docs.python.org/3.11/reference/datamodel.html#object.__enter__
            """  # noqa E501
            # Assuming that no exceptions were raised, all we need to
            # do is set the elapsed time value
            elapsed_time = int(
                (time.time() - self._start_time) * 1_000_000
            ) / 1_000
            self._main_timer.set_timer(self._name, elapsed_time)

        def __repr__(self) -> str:
            return f'<{self.__class__.__name__} ' \
                f'at {hex(id(self))} name={self._name} ' \
                f'main_timer={self._main_timer}>'

    def __init__(self, output: Callable[str] = print):  # type: ignore
        """
        Object initialization

        Parameters:
        -----------
        output : callable
            The callable (not its name, the actual function) that will
            be used to generate output when the context is exited.
            When called, the output callable will be passed a single
            string value.
        """
        self._timers = {}
        self._metrics = {}
        try:
            assert isinstance(
                output, (
                    BuiltinFunctionType, BuiltinMethodType,
                    FunctionType, MethodType
                )
            ), f'{output} is not a function or method, built-in or otherwise.'
        except AssertionError as error:
            raise TypeError(f'{error}') from error
        self._output = output

    def set_timer(self, name: str, value: float | int):
        """
        Sets the specified value as a timer value mapped to the supplied
        name.

        Parameters:
        -----------
        name : string
            The name of the timer whose value will be set.
        value : float | int (>=0)
            The value to be set for the timer name.
        """
        try:
            assert isinstance(name, str)
            assert name.strip()
            assert isinstance(value, (float, int))
            assert value >= 0
        except AssertionError as error:
            raise ValueError(
                f'The name "{name}" ({type(name).__name__}) or the '
                f'value "{value}" ({type(value).__name__}) will not '
                'convert to JSON'
            ) from error
        else:
            self._timers[name] = value

    def __enter__(self):
        """
        The processes to execute when the context is started.
        See https://docs.python.org/3.11/reference/datamodel.html#object.__enter__
        """  # noqa E501
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        """
        The processes to execute when the context is ended.
        See https://docs.python.org/3.11/reference/datamodel.html#object.__exit__
        """  # noqa E501
        collected = {
            'latencies': self._timers,
            'metrics': self._metrics
        }
        self._output(json.dumps(collected))
        self._timers = {}
        self._metrics = {}

    def set_metric(self, name: str, value: bool | float | int | str):
        """
        Sets the provided value as a metric in the instance using
        the provided name.
        """
        if not isinstance(name, str):
            raise TypeError(
                f'{self.__class__.__name__}.set_metric expects a non-'
                f'empty string name, but was passed "{name}" '
                f'({type(name).__name__}).'
            )
        if not name:
            raise ValueError(
                f'{self.__class__.__name__}.set_metric expects a non-'
                f'empty string name, but was passed "{name}" '
                f'({type(name).__name__}).'
            )
        if not isinstance(value, (bool, float, int, str)):
            raise TypeError(
                f'{self.__class__.__name__}.set_metric expects a value '
                'that is JSON-serializable to a JSON primitive, but was '
                f'passed "{value}" ({type(value).__name__}).'
            )
        self._metrics[name] = value

    def timer(self, name: str):
        """
        Creates and returns a timer context object that keeps track of
        a name to store its value under.
        """
        if self._timers.get(name, None) is not None:
            warnings.warn(
                f'A duplicate "{name}" timer has been started. This '
                'may lead to undesirable/inaccurate timing results!'
            )
        return self._Timer(self, name)

    def track(
        self,
        name_or_target: str | Callable | None = None
    ):
        """
        A method that decorates a target callable, capturing the
        elapsed time the callable takes to run to completion.

        Parameters:
        -----------
        name_or_target : str | callable (optional, defaults to None)
            - If a str, the name of the timer to associate with the
              decorated callable target.
            - If not supplied (None), the name of the decorated callable
              target will be used as the timer name.
        """
        if isinstance(name_or_target, FunctionType):
            def _wrapper(*args, **kwargs):
                with self.timer(name_or_target.__name__):
                    result = name_or_target(*args, **kwargs)
                return result
            return _wrapper
        elif isinstance(name_or_target, str):
            def _capture_name(target):
                def _wrapper(*args, **kwargs):
                    with self.timer(name_or_target):
                        result = target(*args, **kwargs)
                    return result
                return _wrapper
            return _capture_name

    def __call__(self, name_or_target: str | Callable | None = None):
        """
        A method that decorates a target callable, capturing the
        elapsed time the callable takes to run to completion.

        Parameters:
        -----------
        name_or_target : str | callable (optional, defaults to None)
            - If a str, the name of the timer to associate with the
              decorated callable target.
            - If not supplied (None), the name of the decorated callable
              target will be used as the timer name.
        """
        if self._timers != {} or self._metrics != {}:
            warnings.warn(
                f'{self.__class__.__name__} already has timers '
                f'({self._timers}) or metrics ({self._metrics}) '
                'defined; applying it again will destroy those values!'
            )
        if isinstance(name_or_target, FunctionType):
            def _wrapper(*args, **kwargs):
                with self:
                    with self.timer(name_or_target.__name__):
                        result = name_or_target(*args, **kwargs)
                    return result
            return _wrapper
        elif isinstance(name_or_target, str):
            def _capture_name(target):
                def _wrapper(*args, **kwargs):
                    with self:
                        with self.timer(name_or_target):
                            result = target(*args, **kwargs)
                        return result
                return _wrapper
            return _capture_name

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} ' \
            f'at {hex(id(self))} timers={self._timers} ' \
            f'metrics={self._metrics}>'


if __name__ == '__main__':

    pass
