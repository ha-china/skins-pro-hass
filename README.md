# Skins Pro

Home Assistant integration for managing [Skins Pro](https://github.com/ha-china/Skins-Pro) Lovelace card themes.

Provides services to download, list, and remove skin themes from the Lovelace card's skin store.

## Services

### `skins_pro.download_skin`

Download and install a skin theme from the CDN.

| Field | Type | Description |
|-------|------|-------------|
| `skin_id` | `string` | Unique identifier of the skin (e.g. `"mario"`, `"sky"`) |

Returns `{"success": true, "base_path": "/local/skins-pro/mario/"}` on success.

### `skins_pro.remove_skin`

Remove a previously installed skin.

| Field | Type | Description |
|-------|------|-------------|
| `skin_id` | `string` | Identifier of the skin to remove |

### `skins_pro.list_skins`

List all installed skins. Returns `{"skins": ["mario", "sky", ...]}`.

## Installation

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=ha-china&repository=skins-pro-hass&category=integration)

1. Click the badge above to add this repository to HACS, or manually add `https://github.com/ha-china/skins-pro-hass` as a custom integration repository in HACS.
2. Search for "Skins Pro" in HACS and install.
3. Restart Home Assistant.
4. Go to **Settings → Devices & Services → Add Integration → Skins Pro**.
5. Confirm to enable.

After installation, the [Skins Pro Lovelace card](https://github.com/ha-china/Skins-Pro) can call its services to download themes from the skin store directly to your Home Assistant server.
