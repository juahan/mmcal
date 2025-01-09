"""Calendar platform for Magic Mirror Calendar integration."""
from datetime import datetime, timedelta
import logging
from typing import Any

from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, CONF_CALENDAR_NAME
from . import MagicMirrorCalendarDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Magic Mirror Calendar platform."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities(
        [MagicMirrorCalendar(coordinator, config_entry)], True
    )

class MagicMirrorCalendar(CoordinatorEntity, CalendarEntity):
    """Magic Mirror Calendar."""

    def __init__(
        self,
        coordinator: MagicMirrorCalendarDataUpdateCoordinator,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the Magic Mirror Calendar."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._attr_unique_id = f"{DOMAIN}_{config_entry.entry_id}"
        self._attr_name = config_entry.data.get(CONF_CALENDAR_NAME, "Magic Mirror Calendar")

    @property
    def event(self) -> CalendarEvent | None:
        """Return the next upcoming event."""
        if not self.coordinator.data or "events" not in self.coordinator.data:
            return None

        events = self.coordinator.data["events"]
        now = datetime.now()
        
        # Filter future events and sort by start time
        future_events = [
            event for event in events 
            if event["start"] > now
        ]
        if not future_events:
            return None

        future_events.sort(key=lambda x: x["start"])
        next_event = future_events[0]

        return CalendarEvent(
            summary=next_event["summary"],
            start=next_event["start"],
            end=next_event["end"] or (next_event["start"] + timedelta(hours=1)),
            description=next_event.get("description", ""),
            location=next_event.get("location", ""),
        )

    async def async_get_events(
        self, hass: HomeAssistant, start_date: datetime, end_date: datetime
    ) -> list[CalendarEvent]:
        """Get all events in a specific time frame."""
        if not self.coordinator.data or "events" not in self.coordinator.data:
            return []

        events = []
        for event in self.coordinator.data["events"]:
            if start_date <= event["start"] <= end_date:
                events.append(
                    CalendarEvent(
                        summary=event["summary"],
                        start=event["start"],
                        end=event["end"] or (event["start"] + timedelta(hours=1)),
                        description=event.get("description", ""),
                        location=event.get("location", ""),
                    )
                )

        return events
