# SPICE Simulations

ngspice netlists and results for power management
circuit validation.

## Simulations

| ID | Circuit | Status |
|----|---------|--------|
| SIM-01 | LDO regulation (AMS1117-3.3) | Pending |
| SIM-02 | TP4056 charge profile | Pending |
| SIM-03 | Battery discharge / runtime | Pending |
| SIM-04 | USB–battery switchover | Pending |
| SIM-05 | Battery voltage divider / ADC | Pending |
| SIM-06 | I2C pull-up timing | Pending |

## Running Simulations

```bash
# Run a single simulation
ngspice -b -o results/sim-01.log sim-01-ldo-regulation.cir

# Run all simulations
for f in *.cir; do
  ngspice -b -o "results/${f%.cir}.log" "$f"
done
```

## Directory Layout

```
spice/
├── sim-01-ldo-regulation.cir
├── sim-02-tp4056-charge.cir
├── sim-03-battery-discharge.cir
├── sim-04-power-switchover.cir
├── sim-05-voltage-divider.cir
├── sim-06-i2c-pullup.cir
└── results/
    ├── sim-01.log
    └── ...
```
