# config and input

## Air Properties ($config/air.yaml$) {- .unlisted}

Table: Air parameters.

|       Quantity / Species        |       Symbol        |  Value   |     Units     |
| :-----------------------------: | :-----------------: | :------: | :-----------: |
|           Temperature           |         $T$         |  300.0   | $\mathrm{K}$  |
|            Pressure             |         $P$         |  101325  | $\mathrm{Pa}$ |
|     Oxygen (molar fraction)     | $x_{\mathrm{O_2}}$  | 0.23067  |     $(-)$     |
|    Nitrogen (molar fraction)    | $x_{\mathrm{N_2}}$  | 0.755866 |     $(-)$     |
|     Argon (molar fraction)      |  $x_{\mathrm{Ar}}$  | 0.01287  |     $(-)$     |
| Carbon dioxide (molar fraction) | $x_{\mathrm{CO_2}}$ | 0.000594 |     $(-)$     |
|  Water vapour (molar fraction)  | $x_{\mathrm{H_2O}}$ |   0.0    |     $(-)$     |

## Drum Geometry and Wall Properties ($config/drum.yaml$) {- .unlisted}

Table: Drum parameters.

|         Quantity          |          Symbol          |       Value        |            Units             |
| :-----------------------: | :----------------------: | :----------------: | :--------------------------: |
|      Inner diameter       |   $D_{\mathrm{drum}}$    |        4.5         |         $\mathrm{m}$         |
|          Length           |   $L_{\mathrm{drum}}$    |        5.0         |         $\mathrm{m}$         |
|      Wall thickness       | $\delta_{\mathrm{wall}}$ |        0.05        |         $\mathrm{m}$         |
| Wall thermal conductivity |   $k_{\mathrm{wall}}$    |         40         | $\mathrm{W\,m^{-1}\,K^{-1}}$ |
|  Inner surface roughness  |      $\varepsilon$       |         5          |       $\mu\mathrm{m}$        |
| Inner surface emissivity  |     $\varepsilon_r$      |        0.80        |            $(-)$             |
|     Fouling thickness     |        $\delta_f$        | $1.0\times10^{-4}$ |         $\mathrm{m}$         |
|   Fouling conductivity    |          $k_f$           |        0.2         | $\mathrm{W\,m^{-1}\,K^{-1}}$ |

## Fuel Properties ($config/fuel.yaml$) {- .unlisted}

Table: Fuel parameters.

|        Quantity / Species         |          Symbol           |  Value   |         Units         |
| :-------------------------------: | :-----------------------: | :------: | :-------------------: |
|            Temperature            |            $T$            |  300.0   |     $\mathrm{K}$      |
|             Pressure              |            $P$            |  101325  |     $\mathrm{Pa}$     |
|          Mass flow rate           | $\dot{m}_{\mathrm{fuel}}$ |   0.1    | $\mathrm{kg\,s^{-1}}$ |
|     Methane (molar fraction)      |      $\mathrm{CH_4}$      | 0.849546 |         $(-)$         |
|      Ethane (molar fraction)      |     $\mathrm{C_2H_6}$     | 0.061889 |         $(-)$         |
|     Propane (molar fraction)      |     $\mathrm{C_3H_8}$     | 0.020597 |         $(-)$         |
|      Butane (molar fraction)      |   $\mathrm{C_4H_{10}}$    | 0.005154 |         $(-)$         |
| Hydrogen sulfide (molar fraction) |      $\mathrm{H_2S}$      | 0.000103 |         $(-)$         |
|     Nitrogen (molar fraction)     |      $\mathrm{N_2}$       | 0.041293 |         $(-)$         |
|  Carbon dioxide (molar fraction)  |      $\mathrm{CO_2}$      | 0.016418 |         $(-)$         |
|      Water (molar fraction)       |      $\mathrm{H_2O}$      |  0.005   |         $(-)$         |
|      Argon (molar fraction)       |       $\mathrm{Ar}$       |   0.0    |         $(-)$         |

## Operating Conditions ($config/operation.yaml$) {- .unlisted}

Table: Operation parameters.

|     Quantity     |       Symbol        | Value |     Units      |
| :--------------: | :-----------------: | :---: | :------------: |
| Excess air ratio |      $\lambda$      |  1.1  |     $(-)$      |
|  Drum pressure   | $P_{\mathrm{drum}}$ |  10   | $\mathrm{bar}$ |

## Heat Exchange Stages ($config/stages.yaml$) {- .unlisted}

Table: Stages parameters.

|       Quantity       |         Symbol         | HX-1  | HX-2 | HX-3  | HX-4 | HX-5  |  HX-6  |            Units             |
| :------------------: | :--------------------: | :---: | :--: | :---: | :--: | :---: | :----: | :--------------------------: |
|    Inner diameter    |         $D_i$          |  1.4  | 1.6  | 0.076 | 1.6  | 0.076 | 0.0337 |         $\mathrm{m}$         |
| Inner / tube length  |       $L_i,\,L$        | 5.276 | 0.8  | 4.975 | 0.8  | 5.620 |   80   |         $\mathrm{m}$         |
|    Wall thickness    |        $\delta$        | 0.02  |  —   |   —   |  —   |   —   |   —    |         $\mathrm{m}$         |
| Thermal conductivity |          $k$           |  50   |  —   |   —   |  —   |   —   |   —    | $\mathrm{W\,m^{-1}\,K^{-1}}$ |
|   Curvature radius   |          $R$           |   —   | 0.8  |   —   | 0.8  |   —   |   —    |         $\mathrm{m}$         |
|   Number of tubes    |          $N$           |   —   |  —   |  118  |  —   |  100  |   60   |            $(-)$             |
|    Number of rows    |  $N_{\mathrm{rows}}$   |   —   |  —   |   6   |  —   |   6   |   20   |            $(-)$             |
|  Number of circuits  |         $n_c$          |   —   |  —   |   —   |  —   |   —   |   4    |            $(-)$             |
|   Transverse pitch   |         $S_T$          |   —   |  —   | 0.11  |  —   | 0.11  |  0.09  |         $\mathrm{m}$         |
|  Longitudinal pitch  |         $S_L$          |   —   |  —   | 0.11  |  —   | 0.11  |  0.10  |         $\mathrm{m}$         |
|    Baffle spacing    |          $B$           |   —   |  —   | 0.45  |  —   | 0.45  |  0.25  |         $\mathrm{m}$         |
|      Baffle cut      |          $c$           |   —   |  —   | 0.25  |  —   | 0.25  |  0.25  |            $(-)$             |
|   Bundle clearance   |           —            |   —   |  —   | 0.010 |  —   | 0.010 | 0.010  |         $\mathrm{m}$         |
| Shell inner diameter |  $D_{\mathrm{shell}}$  |   —   |  —   |   —   |  —   |   —   |  0.95  |         $\mathrm{m}$         |
|    Hot inlet loss    |  $K_{\text{hot,in}}$   |  0.5  |  —   |  0.5  |  —   |  0.5  |  0.5   |            $(-)$             |
|   Hot outlet loss    |  $K_{\text{hot,out}}$  |  0.0  |  —   |  1.0  |  —   |  1.0  |  1.0   |            $(-)$             |
|    Hot bend loss     | $K_{\text{hot,bend}}$  |  0.0  | 0.3  |   —   | 0.3  |   —   |   —    |            $(-)$             |
|   Cold inlet loss    |  $K_{\text{cold,in}}$  |  0.0  |  —   |   —   |  —   |   —   |  0.5   |            $(-)$             |
|   Cold outlet loss   | $K_{\text{cold,out}}$  |  0.0  |  —   |   —   |  —   |   —   |  1.0   |            $(-)$             |
|    Cold bend loss    | $K_{\text{cold,bend}}$ |  0.0  |  —   |   —   |  —   |   —   |  0.3   |            $(-)$             |

## Water Properties ($config/water.yaml$) {- .unlisted}

Table: Water parameters.

|     Quantity      |       Symbol        |       Value        |         Units         |
| :---------------: | :-----------------: | :----------------: | :-------------------: |
| Specific enthalpy |         $h$         | $4.40\times10^{5}$ | $\mathrm{J\,kg^{-1}}$ |
|    Composition    | $x_{\mathrm{H_2O}}$ |        1.0         |         $(-)$         |

\newpage
