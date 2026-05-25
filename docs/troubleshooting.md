# Troubleshooting

*To be expanded as issues are discovered.*

## Common Issues

### Device does not appear on WiFi

- Verify the ESP32 is powered (check USB LED).
- Hold the BOOT button during power-up to force AP mode.

### Buttons not responding

- Check I2C connections (SDA → GPIO0, SCL → GPIO10).
- Verify I2C pull-up resistors are installed (4.7 kΩ).
- Run an I2C scanner sketch to confirm the NeoTrellis
  address (default `0x2E`).

### MQTT not connecting

- Verify broker address and port in configuration.
- Check WiFi connectivity.
- Confirm broker allows the configured credentials.
