"""Config flow for Magic Mirror Calendar integration."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME, CONF_URL
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN, CONF_CALENDAR_NAME, CONF_MAX_EVENTS, DEFAULT_MAX_EVENTS

_LOGGER = logging.getLogger(__name__)

async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    async with aiohttp.ClientSession() as session:
        async with session.get(data[CONF_URL]) as resp:
            if resp.status != 200:
                raise InvalidAuth

    return {"title": data[CONF_CALENDAR_NAME]}

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Magic Mirror Calendar."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
                return self.async_create_entry(title=info["title"], data=user_input)
            except aiohttp.ClientError:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_URL): str,
                    vol.Required(
                        CONF_CALENDAR_NAME, default="Magic Mirror Calendar"
                    ): str,
                    vol.Optional(
                        CONF_MAX_EVENTS, default=DEFAULT_MAX_EVENTS
                    ): int,
                }
            ),
            errors=errors,
        )


class InvalidAuth(Exception):
    """Error to indicate there is invalid auth."""
