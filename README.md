# Skins Pro

Home Assistant integration for managing [Skins Pro](https://github.com/ha-china/Skins-Pro) Lovelace card themes.

Provides services to download, list, and remove skin themes from the Lovelace card's skin store.

## Services

### `skins_pro.download_skin`

Download and install a skin theme from the skin store.

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

## How it works

When the Skins Pro Lovelace card calls `skins_pro.download_skin`, this integration:

1. Fetches the skin package (`.zip`) from the skin store hosted on Cloudflare R2.
2. Extracts it to `<config>/www/skins-pro/<skin_id>/` on your Home Assistant server.
3. The card loads assets (images, CSS) directly from `/local/skins-pro/<skin_id>/` — no browser upload, no YAML config.
4. Downloaded skins appear in the card editor with a "(Downloaded)" suffix; bundled skins continue to load from the card's built-in store.

> All data stays on your server. The remote storage is only used to fetch the initial package. Once installed, the skin runs entirely from local files.

## Installation

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=ha-china&repository=skins-pro-hass&category=integration)

1. Click the badge above to add this repository to HACS, or manually add `https://github.com/ha-china/skins-pro-hass` as a custom integration repository in HACS.
2. Search for "Skins Pro" in HACS and install.
3. Restart Home Assistant.
4. Go to **Settings → Devices & Services → Add Integration → Skins Pro**.
5. Confirm to enable.

After installation, the [Skins Pro Lovelace card](https://github.com/ha-china/Skins-Pro) can call its services to download themes from the skin store directly to your Home Assistant server.

---

# Skins Pro（中文）

用于管理 [Skins Pro](https://github.com/ha-china/Skins-Pro) Lovelace 卡片主题的 Home Assistant 集成。

提供服务，用于从 Lovelace 卡片的皮肤商店中下载、列出和移除皮肤主题。

## 服务

### `skins_pro.download_skin`

从皮肤商店下载并安装皮肤主题。

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `skin_id` | `string` | 皮肤的唯一标识（如 `"mario"`、`"sky"`） |

成功时返回 `{"success": true, "base_path": "/local/skins-pro/mario/"}`。

### `skins_pro.remove_skin`

移除之前已安装的皮肤。

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `skin_id` | `string` | 要移除的皮肤标识 |

### `skins_pro.list_skins`

列出所有已安装的皮肤。返回 `{"skins": ["mario", "sky", ...]}`。

## 工作原理

当 Skins Pro Lovelace 卡片调用 `skins_pro.download_skin` 时，本集成会执行以下操作：

1. 从托管在 Cloudflare R2 上的皮肤商店获取皮肤压缩包（`.zip`）。
2. 将其解压到 Home Assistant 服务器的 `<config>/www/skins-pro/<skin_id>/` 目录。
3. 卡片直接从 `/local/skins-pro/<skin_id>/` 加载资源（图片、CSS）——无需浏览器上传，无需 YAML 配置。
4. 已下载的皮肤会在卡片编辑器中显示"(Downloaded)"（已下载）后缀；内置皮肤继续从卡片的内置商店加载。

> 所有数据都保留在你的服务器上。远程存储仅用于获取初始压缩包。安装完成后，皮肤完全从本地文件运行。

## 安装

[![打开你的 Home Assistant 实例并在 Home Assistant Community Store 中打开一个仓库。](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=ha-china&repository=skins-pro-hass&category=integration)

1. 点击上方徽章将本仓库添加到 HACS，或在 HACS 中手动将 `https://github.com/ha-china/skins-pro-hass` 添加为自定义集成仓库。
2. 在 HACS 中搜索"Skins Pro"并安装。
3. 重启 Home Assistant。
4. 进入 **设置 → 设备与服务 → 添加集成 → Skins Pro**。
5. 确认启用。

安装完成后，[Skins Pro Lovelace 卡片](https://github.com/ha-china/Skins-Pro) 即可调用其服务，将皮肤商店中的主题直接下载到你的 Home Assistant 服务器。
