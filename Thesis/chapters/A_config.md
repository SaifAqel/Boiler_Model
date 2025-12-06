# config and input

## Air properties (`config/air.yaml`)

```yaml
T: { value: 300.0, unit: kelvin }
P: { value: 101325, unit: Pa }
composition:
  O2: { value: 0.2095, unit: dimensionless }
  N2: { value: 0.7808, unit: dimensionless }
  Ar: { value: 0.0093, unit: dimensionless }
  CO2: { value: 0.0004, unit: dimensionless }
  H2O: { value: 0.0, unit: dimensionless }
```

## Drum geometry and wall properties (`config/drum.yaml`)

```yaml
inner_diameter: { value: 4.5, unit: m }
length: { value: 5.0, unit: m } # informational here
wall:
  surfaces:
    inner:
      roughness: { value: 5, unit: micrometer }
      emissivity: { value: 0.80, unit: dimensionless }
      fouling_thickness: { value: 0.0001, unit: m }
      fouling_conductivity: { value: 0.2, unit: W/m/K }
```

## Fuel properties and composition (`config/fuel.yaml`)

```yaml
T: { value: 300.0, unit: kelvin }
P: { value: 101325, unit: Pa }
mass_flow: { value: 0.1, unit: kg/s }
composition:
  CH4: { value: 0.80, unit: dimensionless }
  C2H6: { value: 0.10, unit: dimensionless }
  C3H8: { value: 0.04, unit: dimensionless }
  C4H10: { value: 0.01, unit: dimensionless }
  H2S: { value: 0.01, unit: dimensionless }
  N2: { value: 0.02, unit: dimensionless }
  CO2: { value: 0.01, unit: dimensionless }
  H2O: { value: 0.01, unit: dimensionless }
```

## Operating condition (`config/operation.yaml`)

```yaml
excess_air_ratio: { value: 1.1, unit: dimensionless }
```

## Heat exchanger stages (`config/stages.yaml`)

```yaml
HX_1:
  kind: "single_tube"
  pool_boiling: true
  inner_diameter: { value: 1.4, unit: m }
  inner_length: { value: 5.276, unit: m }
  wall:
    thickness: { value: 0.0029, unit: m }
    conductivity: { value: 16, unit: W/m/K }
    surfaces:
      inner:
        roughness: { value: 0.5, unit: micrometer }
        emissivity: { value: 0.80, unit: dimensionless }
        fouling_thickness: { value: 0.0001, unit: m }
        fouling_conductivity: { value: 0.20, unit: W/m/K }
      outer:
        roughness: { value: 0.5, unit: micrometer }
        emissivity: { value: 0.80, unit: dimensionless }
        fouling_thickness: { value: 0.0001, unit: m }
        fouling_conductivity: { value: 0.20, unit: W/m/K }

HX_2:
  kind: "reversal_chamber"
  pool_boiling: true
  inner_diameter: { value: 1.6, unit: m }
  inner_length: { value: 0.8, unit: m }
  curvature_radius: { value: 0.8, unit: m }
  nozzles:
    inlet:
      k: { value: 1, unit: dimensionless }
    outlet:
      k: { value: 1, unit: dimensionless }
  wall:
    thickness: { value: 0.0029, unit: m }
    conductivity: { value: 16, unit: W/m/K }
    surfaces:
      inner:
        roughness: { value: 0.5, unit: micrometer }
        emissivity: { value: 0.80, unit: dimensionless }
        fouling_thickness: { value: 0.0001, unit: m }
        fouling_conductivity: { value: 0.20, unit: W/m/K }
      outer:
        roughness: { value: 0.5, unit: micrometer }
        emissivity: { value: 0.80, unit: dimensionless }
        fouling_thickness: { value: 0.0001, unit: m }
        fouling_conductivity: { value: 0.20, unit: W/m/K }

HX_3:
  kind: "tube_bank"
  pool_boiling: true
  inner_diameter: { value: 0.076, unit: m }
  inner_length: { value: 4.975, unit: m }
  tubes_number: { value: 118, unit: dimensionless }
  arrangement: "staggered"
  N_rows: { value: 6, unit: dimensionless }
  ST: { value: 0.11, unit: m }
  SL: { value: 0.11, unit: m }
  baffle_spacing: { value: 0.075, unit: m }
  shell_inner_diameter: { value: 1.80, unit: m } # Ds
  baffle_cut: { value: 0.25, unit: dimensionless } # Bc = L_bch / Ds
  bundle_clearance: { value: 0.010, unit: m }
  wall:
    thickness: { value: 0.0029, unit: m }
    conductivity: { value: 16, unit: W/m/K }
    surfaces:
      inner:
        roughness: { value: 0.5, unit: micrometer }
        emissivity: { value: 0.80, unit: dimensionless }
        fouling_thickness: { value: 0.0001, unit: m }
        fouling_conductivity: { value: 0.20, unit: W/m/K }
      outer:
        roughness: { value: 0.5, unit: micrometer }
        emissivity: { value: 0.80, unit: dimensionless }
        fouling_thickness: { value: 0.0001, unit: m }
        fouling_conductivity: { value: 0.20, unit: W/m/K }

HX_4:
  kind: "reversal_chamber"
  pool_boiling: true
  inner_diameter: { value: 1.6, unit: m }
  inner_length: { value: 0.8, unit: m }
  curvature_radius: { value: 0.8, unit: m }
  nozzles:
    inlet:
      k: { value: 1, unit: dimensionless }
    outlet:
      k: { value: 1, unit: dimensionless }
  wall:
    thickness: { value: 0.0029, unit: m }
    conductivity: { value: 16, unit: W/m/K }
    surfaces:
      inner:
        roughness: { value: 0.5, unit: micrometer }
        emissivity: { value: 0.80, unit: dimensionless }
        fouling_thickness: { value: 0.0001, unit: m }
        fouling_conductivity: { value: 0.20, unit: W/m/K }
      outer:
        roughness: { value: 0.5, unit: micrometer }
        emissivity: { value: 0.80, unit: dimensionless }
        fouling_thickness: { value: 0.0001, unit: m }
        fouling_conductivity: { value: 0.20, unit: W/m/K }

HX_5:
  kind: "tube_bank"
  pool_boiling: true
  inner_diameter: { value: 0.076, unit: m }
  inner_length: { value: 5.620, unit: m }
  tubes_number: { value: 100, unit: dimensionless }
  arrangement: "staggered"
  N_rows: { value: 6, unit: dimensionless }
  ST: { value: 0.11, unit: m }
  SL: { value: 0.11, unit: m }
  baffle_spacing: { value: 0.075, unit: m }
  shell_inner_diameter: { value: 1.80, unit: m } # Ds
  baffle_cut: { value: 0.25, unit: dimensionless } # Bc = L_bch / Ds
  bundle_clearance: { value: 0.010, unit: m }
  wall:
    thickness: { value: 0.0029, unit: m }
    conductivity: { value: 16, unit: W/m/K }
    surfaces:
      inner:
        roughness: { value: 0.5, unit: micrometer }
        emissivity: { value: 0.80, unit: dimensionless }
        fouling_thickness: { value: 0.0001, unit: m }
        fouling_conductivity: { value: 0.20, unit: W/m/K }
      outer:
        roughness: { value: 0.5, unit: micrometer }
        emissivity: { value: 0.80, unit: dimensionless }
        fouling_thickness: { value: 0.0001, unit: m }
        fouling_conductivity: { value: 0.20, unit: W/m/K }

HX_6:
  kind: "economiser"
  pool_boiling: false
  inner_diameter: { value: 0.076, unit: m } # unchanged
  inner_length: { value: 7.5, unit: m } # was 5.620
  tubes_number: { value: 160, unit: dimensionless } # was 100
  layout: "triangular"
  arrangement: "inline"
  N_rows: { value: 4, unit: dimensionless }
  ST: { value: 0.123, unit: m } # keep pitch
  SL: { value: 0.123, unit: m }
  baffle_spacing: { value: 0.085, unit: m } # was 0.105 → higher h
  shell_inner_diameter: { value: 1.80, unit: m }
  baffle_cut: { value: 0.25, unit: dimensionless }
  bundle_clearance: { value: 0.010, unit: m }
  wall:
    thickness: { value: 0.0025, unit: m } # thinner wall
    conductivity: { value: 30, unit: W/m/K }
    surfaces:
      inner:
        roughness: { value: 0.5, unit: micrometer }
        emissivity: { value: 0.80, unit: dimensionless }
        fouling_thickness: { value: 0.0, unit: m } # best case to raise UA
        fouling_conductivity: { value: 0.20, unit: W/m/K }
      outer:
        roughness: { value: 0.5, unit: micrometer }
        emissivity: { value: 0.80, unit: dimensionless }
        fouling_thickness: { value: 0.0, unit: m }
        fouling_conductivity: { value: 0.20, unit: W/m/K }
```

## Water side properties (`config/water.yaml`)

```yaml
enthalpy: { value: 300000, unit: J/kg }
pressure: { value: 1000000, unit: Pa }
composition:
  H2O: { value: 1.0, unit: dimensionless }
drum:
  flow_area: { value: 5, unit: m^2 }
```

\newpage
