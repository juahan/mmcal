"""The Magic Mirror Calendar integration."""
from __future__ import annotations

from datetime import datetime, timedelta
import logging
from typing import Any

import aiohttp
from icalendar import Calendar
import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, CONF_URL, Platform
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    CONF_CALENDAR_NAME,
    CONF_MAX_EVENTS,
    DEFAULT_MAX_EVENTS,
    DOMAIN,
    STARTUP_MESSAGE,
)

PLATFORMS: list[Platform] = [Platform.CALENDAR]

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_URL): cv.string,
                vol.Optional(CONF_MAX_EVENTS, default=DEFAULT_MAX_EVENTS): cv.positive_int,
                vol.Optional(CONF_CALENDAR_NAME): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Magic Mirror Calendar component."""
    hass.data.setdefault(DOMAIN, {})

    if DOMAIN in config:
        return True

    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Magic Mirror Calendar from a config entry."""
    coordinator = MagicMirrorCalendarDataUpdateCoordinator(
        hass,
        config_entry=entry,
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok

class MagicMirrorCalendarDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Magic Mirror Calendar data."""

    def __init__(
        self, hass: HomeAssistant, config_entry: ConfigEntry
    ) -> None:
        """Initialize global Magic Mirror Calendar data updater."""
        self.config_entry = config_entry

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=15),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from Magic Mirror Calendar."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.config_entry.data[CONF_URL]) as resp:
                    if resp.status != 200:
                        raise UpdateFailed(
                            f"Error fetching calendar data: {resp.status}"
                        )
                    data = await resp.text()

                calendar = Calendar.from_ical(data)
                events = []

                for component in calendar.walk():
                    if component.name == "VEVENT":
                        event = {
                            "summary": str(component.get("summary", "No Title")),
                            "description": str(component.get("description", "")),
                            "location": str(component.get("location", "")),
                            "start": component.get("dtstart").dt,
                            "end": component.get("dtend").dt if component.get("dtend") else None,
                            "all_day": isinstance(component.get("dtstart").dt, datetime),
                        }
                        events.append(event)

                return {"events": events}

        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")
