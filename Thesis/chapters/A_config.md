# config and input

## Operating condition (`config/operation.yaml`)

Table: Operation Conditions
| property | value | unit |
| excess air ratio | 1.1 | dimensionless |

## Air input properties (`config/air.yaml`)

Table: Air Properties
| property | value | unit |
| T | 300.0 | kelvin |
| P | 101325 | Pa |
| composition $\mathrm{O_2}$ | 0.2095 | dimensionless |
| composition $\mathrm{N_2}$ | 0.7808 | dimensionless |
| composition $\mathrm{Ar}$ | 0$.0093 | dimensionless |
| composition $\mathrm{CO_2}$ | 0.0004 | dimensionless |
| composition H2O | 0.0 | dimensionless |

## Fuel properties and composition (`config/fuel.yaml`)

Table: Fuel Properties
| property | value | unit |
| T | 300.0 | kelvin |
| P | 101325 | Pa |
| mass flow | 0.1 | kg/s |
| composition $\mathrm{CH_4}$ | 0.80 | dimensionless |
| composition $\mathrm{C_2H_6}$ | 0.10 | dimensionless |
| composition $\mathrm{C_3H_8}$ | 0.04 | dimensionless |
| composition $\mathrm{C_4H_{10}}$ | 0.01 | dimensionless |
| composition $\mathrm{H_2S}$ | 0.01 | dimensionless |
| composition $\mathrm{N_2}$ | 0.02 | dimensionless |
| composition $\mathrm{CO_2}$ | 0.01 | dimensionless |
| composition $\mathrm{H_2O}$ | 0.01 | dimensionless |

## Water input properties (`config/water.yaml`)

Table: Water Properties
| property | value | unit |
| enthalpy | 300000 | J/kg |
| pressure | 1000000 | Pa |
| composition $\mathrm{H_2O}$ | 1.0 | dimensionless |

## Drum geometry and wall properties (`config/drum.yaml`)

Table: Drum Properties
| property | value | unit |
| inner diameter | 4.5 | m |
| length | 5.0 | m |
| wall inner roughness | 5 | micrometer |
| fouling thickness | 0.0001 | m |
| fouling conductivity | 0.2 | W/m/K |

## Heat exchanger stages (`config/stages.yaml`)

Table: HX 1
| property | value | unit |
| kind | single tube | |
| pool boiling | true | |
| inner diameter | 1.4 | m |
| inner length | 5.276 | m |
| wall thickness | 0.0029 | m |
| wall conductivity | 16 | W/m/K |
| wall inner roughness | 0.5 | micrometer |
| wall inner emissivity | 0.80 | dimensionless |
| wall inner fouling thickness | 0.0001 | m |
| wall inner fouling conductivity | 0.20 | W/m/K |
| wall outer roughness | 0.5 | micrometer |
| wall outer emissivity | 0.80 | dimensionless |
| wall outer fouling thickness | 0.0001 | m |
| wall outer fouling conductivity | 0.20 | W/m/K |

Table: HX 2
| property | value | unit |
| kind | reversal chamber | |
| pool boiling | true | |
| inner diameter | 1.6 | m |
| inner length | 0.8 | m |
| curvature radius | 0.8 | m |
| wall thickness | 0.0029 | m |
| wall conductivity | 16 | W/m/K |
| wall inner roughness | 0.5 | micrometer |
| wall inner emissivity | 0.80 | dimensionless |
| wall inner fouling thickness | 0.0001 | m |
| wall inner fouling conductivity | 0.20 | W/m/K |
| wall outer roughness | 0.5 | micrometer |
| wall outer emissivity | 0.80 | dimensionless |
| wall outer fouling thickness | 0.0001 | m |
| wall outer fouling conductivity | 0.20 | W/m/K |

Table: HX 3
| property | value | unit |
| kind | tube bank | |
| pool boiling | true | |
| inner diameter | 0.076 | m |
| inner length | 4.975 | m |
| tubes number | 118 | dimensionless |
| arrangement | staggered | |
| rows number| 6 | dimensionless |
| ST | 0.11 | m |
| SL | 0.11 | m |
| baffle spacing | 0.075 | m |
| shell inner diameter | 1.80 | m |
| baffle cut | 0.25 | dimensionless |
| bundle clearance | 0.010 | m |
| wall thickness | 0.0029 | m |
| wall conductivity | 16 | W/m/K |
| wall inner roughness | 0.5 | micrometer |
| wall inner emissivity | 0.80 | dimensionless |
| wall inner fouling thickness | 0.0001 | m |
| wall inner fouling conductivity | 0.20 | W/m/K |
| wall outer roughness | 0.5 | micrometer |
| wall outer emissivity | 0.80 | dimensionless |
| wall outer fouling thickness | 0.0001 | m |
| wall outer fouling conductivity | 0.20 | W/m/K |

Table: HX 4
| property | value | unit |
| kind | reversal chamber | |
| pool boiling | true | |
| inner diameter | 1.6 | m |
| inner length | 0.8 | m |
| curvature radius | 0.8 | m |
| wall thickness | 0.0029 | m |
| wall conductivity | 16 | W/m/K |
| wall inner roughness | 0.5 | micrometer |
| wall inner emissivity | 0.80 | dimensionless |
| wall inner fouling thickness | 0.0001 | m |
| wall inner fouling conductivity | 0.20 | W/m/K |
| wall outer roughness | 0.5 | micrometer |
| wall outer emissivity | 0.80 | dimensionless |
| wall outer fouling thickness | 0.0001 | m |
| wall outer fouling conductivity | 0.20 | W/m/K |

Table: HX 5
| property | value | unit |
| kind | tube bank | |
| pool boiling | true | |
| inner diameter | 0.076 | m |
| inner length | 5.620 | m |
| tubes number | 100 | dimensionless |
| arrangement | staggered | |
| rows number | 6 | dimensionless |
| ST | 0.11 | m |
| SL | 0.11 | m |
| baffle spacing | 0.075 | m |
| shell inner diameter | 1.80 | m |
| baffle cut | 0.25 | dimensionless |
| bundle clearance | 0.010 | m |
| wall thickness | 0.0029 | m |
| wall conductivity | 16 | W/m/K |
| wall inner roughness | 0.5 | micrometer |
| wall inner emissivity | 0.80 | dimensionless |
| wall inner fouling thickness | 0.0001 | m |
| wall inner fouling conductivity | 0.20 | W/m/K |
| wall outer roughness | 0.5 | micrometer |
| wall outer emissivity | 0.80 | dimensionless |
| wall outer fouling thickness | 0.0001 | m |
| wall outer fouling conductivity | 0.20 | W/m/K |

Table: HX 6
| property | value | unit |
| kind | economizer | |
| pool boiling | false | |
| inner diameter | 0.076 | m |
| inner length | 7.5 | m |
| tubes number | 160 | dimensionless |
| layout | triangular | |
| arrangement | inline | |
| rows number | 4 | dimensionless |
| ST | 0.123 | m |
| SL | 0.123 | m |
| baffle spacing | 0.085 | m |
| shell inner diameter | 1.80 | m |
| baffle cut | 0.25 | dimensionless |
| bundle clearance | 0.010 | m |
| wall thickness | 0.0025 | m |
| wall conductivity | 30 | W/m/K |
| wall inner roughness | 0.5 | micrometer |
| wall inner emissivity | 0.80 | dimensionless |
| wall inner fouling thickness | 0.0 | m |
| wall inner fouling conductivity | 0.20 | W/m/K |
| wall outer roughness | 0.5 | micrometer |
| wall outer emissivity | 0.80 | dimensionless |
| wall outer fouling thickness | 0.0 | m |
| wall outer fouling conductivity | 0.20 | W/m/K |

\newpage
