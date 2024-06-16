from __future__ import annotations

import re
from dataclasses import dataclass

from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe


@dataclass
class EventType:
    """
    The event type used

    """

    # Method names must be lowercase and only contain strings, numbers and
    # underscores, but must not start with either a number or underscore.
    # The max length is 50 characters.
    #
    # This is OK: yolo, Hello_World, jerry123. This is not: 1pineappleplease
    name: str
    label: str  # Human readable label
    color: str | None = None  # Foreground CSS color used in the Admin changelist.
    bgcolor: str | None = None  # Background CSS color used in the Admin changelist.

    def __post_init__(self) -> None:
        """Validate the attributes"""
        if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]{0,49}$", self.name):
            msg = (
                f"The name {self.name} must be alphanumeric characters, "
                f"not start with number, and at most 50 characters."
            )
            raise TypeError(msg)

    @property
    @method_decorator(mark_safe)
    def html_label(self) -> str:
        styles = " ".join(
            (
                f"color: {self.color};" if self.color else "",
                f"background-color: {self.bgcolor};" if self.bgcolor else "",
            ),
        )
        return f'<span class="eventType" style="{styles}">{self.label}</span>'


@dataclass
class EventTypeList:
    """
    List that holds all event types and adds some filter features.
    """

    events: list[EventType]

    def __init__(self, *events: EventType) -> None:
        self.events = list(events)

    def by_name(self, name: str) -> EventType | None:
        """
        Get an event type from the list by its name.
        Returns None if the event does not exist.
        """
        return next(
            filter(lambda e: e is not None and e.name == name, self.events), None
        )
