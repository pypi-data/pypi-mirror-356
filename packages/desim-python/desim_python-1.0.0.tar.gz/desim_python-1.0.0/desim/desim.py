"""
File:        desim/desim.py
Author:      Luis Enrique Arias Curbelo <lariasec@gmail.com> <github.com/larias95>
Created:     2025-06-14
Updated:     2025-06-14
Description: This module implements a Discrete Event Simulation (DES) framework
             for modeling systems where state changes occur at discrete points in time.
License:     MIT License (see LICENSE file)
"""

from abc import ABC, abstractmethod
from heapq import heappop, heappush
from typing import Any, Callable


class DiscreteEvent(ABC):
    """Base class for modeling events."""

    def __init__(self, t: float):
        """Initialize a new instance of an event.

        Args:
            t (float): Point in time. The moment the event occurs.
        """
        self.t = t
        self.cancelled = False

    def __lt__(self, other: "DiscreteEvent"):
        """Allow sorting events by time of occurrence."""
        return self.t < other.t

    @abstractmethod
    def _run(self, env) -> list["DiscreteEvent"]:
        """Function to be overriden by derived classes. Implement event logic here.

        Args:
            env (Any): A user-defined object with environment information, system state, etc.

        Returns:
            list[DiscreteEvent]: A list of consequent events to be added to the events queue.
        """
        ...

    def _after(self, dt: float):
        """Helper function used by derived classes to compute a step in time.

        Args:
            dt (float): A deltatime.

        Returns:
            float: A point in time after `dt` elapsed.
        """
        return self.t + dt

    def cancel(self):
        """Prevent an event to be executed. The events queue will discard it."""
        self.cancelled = True


class DiscreteEventQueue:
    """Class that implements a queue of events, sorting them by their times of occurrence."""

    def __init__(self, t0: float = 0):
        """Initialize a new instance of an events queue.

        Args:
            t0 (float, optional): The start point in time of the simulation. Defaults to 0.
        """
        self._events: list[DiscreteEvent] = []
        self.t = t0

    def empty(self):
        """Return whether there are pending events in the queue.

        Returns:
            bool: `True` if no pending events are in the queue. Otherwise, `False`.
        """
        return len(self._events) == 0

    def step(self, env):
        """Perform a time step by executing the earliest event in the queue, if any.

        Args:
            env (Any): A user-defined object with environment information, system state, etc. to be passed to events.

        Returns:
            bool: `True` if an event was executed. Otherwise, `False`.
        """
        self._skip_cancelled()

        if self.empty():
            return False

        e = heappop(self._events)
        self._check_no_time_travel(e)
        self.t = e.t
        self.add_events(e._run(env))

        return True

    def add_events(self, events: list[DiscreteEvent]):
        """Add events to the queue.

        Args:
            events (list[DiscreteEvent]): A list of events to be added.
        """
        for e in events:
            heappush(self._events, e)

    def _skip_cancelled(self):
        """Discard cancelled events."""
        while not self.empty() and self._events[0].cancelled:
            heappop(self._events)

    def _check_no_time_travel(self, e: DiscreteEvent):
        """Throw an exception if the time of occurrence of the event is earlier than the current time of the queue.

        Args:
            e (DiscreteEvent): An event to be tested.

        Raises:
            ValueError: Time travel not allowed.
        """
        if e.t < self.t:
            raise ValueError("Time travel not allowed.")


def run_to(
    t: float,
    queue: DiscreteEventQueue,
    env,
    callback: Callable[[DiscreteEventQueue, Any], None] = None,
):
    """Helper function to run a simulation up to a certain point in time.

    Args:
        t (float): A point in time.
        queue (DiscreteEventQueue): An events queue.
        env (Any): A user-defined object with environment information, system state, etc. to be passed to events.
        callback (Callable[[DiscreteEventQueue, Any], None], optional): A callback function to be invoked after each simulation step. Defaults to None.
    """
    while not queue.empty() and queue.t < t:
        if queue.step(env) and (callback is not None):
            callback(queue, env)


def run_to_end(
    queue: DiscreteEventQueue,
    env,
    callback: Callable[[DiscreteEventQueue, Any], None] = None,
):
    """Helper function to run a simulation until no more events remain in the queue.

    Args:
        queue (DiscreteEventQueue): An events queue.
        env (Any): A user-defined object with environment information, system state, etc. to be passed to events.
        callback (Callable[[DiscreteEventQueue, Any], None], optional): A callback function to be invoked after each simulation step. Defaults to None.
    """
    while not queue.empty():
        if queue.step(env) and (callback is not None):
            callback(queue, env)
