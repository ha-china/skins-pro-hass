"""Skins Pro - Download and manage Skins Pro Lovelace card skin themes."""
from __future__ import annotations

import logging
import os
import shutil
import zipfile
from io import BytesIO
from pathlib import Path

import aiohttp
import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.typing import ConfigType

DOMAIN = "skins_pro"
LOGGER = logging.getLogger(__name__)

CDN_BASE = "https://cdn.jsdelivr.net/gh/ha-china/Skins-Pro@store"
SKINS_DIR = "skins-pro"
SKIN_ID_PATTERN = r"^[a-zA-Z0-9][a-zA-Z0-9_-]*$"

SERVICE_DOWNLOAD = "download_skin"
SERVICE_REMOVE = "remove_skin"
SERVICE_LIST = "list_skins"

DOWNLOAD_SCHEMA = vol.Schema({
    vol.Required("skin_id"): cv.matches_regex(SKIN_ID_PATTERN),
}, extra=vol.ALLOW_EXTRA)

REMOVE_SCHEMA = vol.Schema({
    vol.Required("skin_id"): cv.matches_regex(SKIN_ID_PATTERN),
}, extra=vol.ALLOW_EXTRA)

LIST_SCHEMA = vol.Schema({}, extra=vol.ALLOW_EXTRA)


def _register_service(hass, service, handler, schema):
    kwargs = {"schema": schema}
    try:
        from homeassistant.const import ServiceResponseMode
        kwargs["supports_response"] = ServiceResponseMode.OPTIONAL
    except (ImportError, AttributeError):
        pass
    hass.services.async_register(DOMAIN, service, handler, **kwargs)


async def _setup_services(hass: HomeAssistant) -> None:
    """Register all services."""
    session = async_get_clientsession(hass)

    async def _download(call: ServiceCall) -> dict | None:
        skin_id = call.data["skin_id"]
        www_skins = hass.config.path("www", SKINS_DIR)
        target = hass.config.path("www", SKINS_DIR, skin_id)

        os.makedirs(www_skins, exist_ok=True)
        if os.path.exists(target):
            shutil.rmtree(target)

        url = f"{CDN_BASE}/store/{skin_id}.zip"
        LOGGER.debug("Downloading skin '%s' from %s", skin_id, url)

        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=60)) as resp:
                if resp.status != 200:
                    msg = f"CDN returned HTTP {resp.status} for skin '{skin_id}'"
                    LOGGER.error(msg)
                    return {"success": False, "error": msg}
                data = await resp.read()
        except Exception as err:
            LOGGER.error("Download failed for '%s': %s", skin_id, err)
            return {"success": False, "error": str(err)}

        try:
            with zipfile.ZipFile(BytesIO(data)) as zf:
                for member in zf.namelist():
                    parts = member.split("/", 1)
                    if len(parts) < 2 or not parts[1]:
                        continue
                    dest = os.path.join(target, parts[1])
                    if member.endswith("/"):
                        os.makedirs(dest, exist_ok=True)
                    else:
                        os.makedirs(os.path.dirname(dest), exist_ok=True)
                        with zf.open(member) as src, open(dest, "wb") as dst:
                            shutil.copyfileobj(src, dst)
        except Exception as err:
            LOGGER.error("Extraction failed for '%s': %s", skin_id, err)
            if os.path.exists(target):
                shutil.rmtree(target)
            return {"success": False, "error": f"Extraction failed: {err}"}

        LOGGER.info("Skin '%s' installed successfully", skin_id)
        return {
            "success": True,
            "base_path": f"/local/{SKINS_DIR}/{skin_id}/",
        }

    async def _remove(call: ServiceCall) -> dict:
        skin_id = call.data["skin_id"]
        target = hass.config.path("www", SKINS_DIR, skin_id)
        if os.path.exists(target):
            shutil.rmtree(target)
            LOGGER.info("Skin '%s' removed", skin_id)
        return {"success": True}

    async def _list(_call: ServiceCall) -> dict:
        www_skins = hass.config.path("www", SKINS_DIR)
        if not os.path.isdir(www_skins):
            return {"skins": []}
        skins = sorted(
            d.name for d in Path(www_skins).iterdir()
            if d.is_dir() and not d.name.startswith(".")
        )
        return {"skins": skins}

    _register_service(hass, SERVICE_DOWNLOAD, _download, DOWNLOAD_SCHEMA)
    _register_service(hass, SERVICE_REMOVE, _remove, REMOVE_SCHEMA)
    _register_service(hass, SERVICE_LIST, _list, LIST_SCHEMA)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up integration via YAML (not used)."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up integration from config entry."""
    await _setup_services(hass)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload integration."""
    for service in (SERVICE_DOWNLOAD, SERVICE_REMOVE, SERVICE_LIST):
        hass.services.async_remove(DOMAIN, service)
    return True
