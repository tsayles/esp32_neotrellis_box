# API Reference

*To be completed during network integration phase.*

## MQTT Topics

### Command Topics (publish)

| Topic Pattern | Payload | Description |
|---------------|---------|-------------|
| `neotrellis/<device_id>/button/<n>/press` | — | Button press event |

### Status Topics (subscribe)

| Topic Pattern | Payload | Description |
|---------------|---------|-------------|
| `neotrellis/<device_id>/status` | `online`/`offline` | Device availability |

## HTTP Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET    | `/`  | Web configuration UI |
| GET    | `/api/status` | Device status JSON |
| POST   | `/api/config` | Update configuration |
