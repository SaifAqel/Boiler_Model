# Abstract {-}

This thesis develops a three pass fire tube industrial shell boiler model, implemented in Python, the modelling framework integrates (i) detailed fuel-air combustion, (ii) six sequential gas side heat exchange stages representing furnace, tube banks, reversal chambers, and economizer, and (iii) a water/steam circuit governed by saturated boiling in the pressure parts and single phase heating in the economizer. The gas–water energy balance is solved using a one dimensional marching algorithm, which updates local heat transfer coefficients, wall temperatures, and segmental duties based on a full resistance network.

Combustion calculations provide the adiabatic flame temperature, the fully burnt flue gas composition, and the total heat release the natural gas fuel provides. Hydraulic losses are resolved concurrently using friction factor and minor loss correlations yielding complete gas/water pressure drop profiles. Boiler level performance metrics, obtained under different operation conditions and analyzed,demonstrating that efficiency exhibits a shallow optimum near the design excess air setting; that pressure chiefly affects steam quantity rather than boiler efficiency; and that firing rate scales heat duties approximately linearly within the practical load range. The modelling framework provides a physics based tool suitable for analyzing industrial shell boiler behavior, supporting performance evaluation, operational optimization, and design exploration.

## Latin symbols

| Symbol                   | Name                             | Units                                |
| ------------------------ | -------------------------------- | ------------------------------------ |
| $A$                      | Area                             | m$^2$                                |
| $A_j$                    | Gray-band weight                 | --                                   |
| $A_{\mathrm{bulk}}$      | Bulk cross-flow area             | m$^2$                                |
| $A_{\mathrm{cold,flow}}$ | Cold-side flow area              | m$^2$                                |
| $A_{\mathrm{flow}}$      | Flow area                        | m$^2$                                |
| $\mathrm{AFR}$           | Air–fuel ratio                   | --                                   |
| $A_{\mathrm{hot,flow}}$  | Hot-side flow area               | m$^2$                                |
| $B$                      | Baffle spacing                   | m                                    |
| $C$                      | Correlation coefficient          | --                                   |
| $C_0$                    | Bundle loss constant             | --                                   |
| $D$                      | Characteristic diameter          | m                                    |
| $D_h$                    | Hydraulic diameter               | m                                    |
| $D_i$                    | Inner diameter                   | m                                    |
| $D_o$                    | Outer diameter                   | m                                    |
| $D_{\mathrm{shell}}$     | Shell diameter                   | m                                    |
| $\mathrm{d}x$            | Step length                      | m                                    |
| $f$                      | Friction factor                  | --                                   |
| $F$                      | View/enhancement factor          | --                                   |
| $G$                      | Mass flux                        | kg\,m$^{-2}$\,s$^{-1}$               |
| $Gz$                     | Graetz number                    | --                                   |
| $h$                      | Enthalpy / HTC                   | J\,kg$^{-1}$ / W\,m$^{-2}$\,K$^{-1}$ |
| $h_g$                    | Gas-side HTC                     | W\,m$^{-2}$\,K$^{-1}$                |
| $\mathrm{HHV}$           | Higher heating value             | J\,kg$^{-1}$ (or J\,mol$^{-1}$)      |
| $\dot H$                 | Enthalpy rate                    | W                                    |
| $h_w$                    | Water-side HTC                   | W\,m$^{-2}$\,K$^{-1}$                |
| $K$                      | Loss/absorption coefficient      | --                                   |
| $k$                      | Thermal conductivity             | W\,m$^{-1}$\,K$^{-1}$                |
| $K_j$                    | Gray-band absorption             | --                                   |
| $L$                      | Length                           | m                                    |
| $L_b$                    | Mean beam length                 | m                                    |
| $\mathrm{LHV}$           | Lower heating value              | J\,kg$^{-1}$ (or J\,mol$^{-1}$)      |
| $M$                      | Molar mass                       | kg\,mol$^{-1}$                       |
| $M_{\mathrm{mix}}$       | Mixture molar mass               | kg\,mol$^{-1}$                       |
| $\dot m$                 | Mass flow rate                   | kg\,s$^{-1}$                         |
| $M_{\mathrm{w}}$         | Water molar mass                 | kg\,mol$^{-1}$                       |
| $n$                      | Moles / exponent                 | mol (or --)                          |
| $\dot n$                 | Molar flow rate                  | mol\,s$^{-1}$                        |
| $N$                      | Count                            | --                                   |
| $N_{\mathrm{rows}}$      | Tube rows                        | --                                   |
| $Nu$                     | Nusselt number                   | --                                   |
| $p$                      | Pressure / partial pressure      | Pa                                   |
| $P$                      | Pressure                         | Pa                                   |
| $P_{\mathrm{LHV}}$       | LHV firing rate                  | W                                    |
| $p_r$                    | Reduced pressure                 | --                                   |
| $Pr$                     | Prandtl number                   | --                                   |
| $Q$                      | Heat rate                        | W                                    |
| $q$                      | Dynamic pressure                 | Pa                                   |
| $q'(x)$                  | Linear heat flux                 | W\,m$^{-1}$                          |
| $q''$                    | Heat flux                        | W\,m$^{-2}$                          |
| $Q_{\mathrm{in}}$        | Heat input                       | W                                    |
| $Q_{\mathrm{useful}}$    | Useful heat                      | W                                    |
| $R$                      | Thermal resistance / bend radius | --                                   |
| $Re$                     | Reynolds number                  | --                                   |
| $R_p$                    | Roughness parameter              | \textmu m                            |
| $R'$                     | Resistance per length            | K\,W$^{-1}$\,m$^{-1}$                |
| $S$                      | Suppression/pitch factor         | --                                   |
| $S_L$                    | Longitudinal pitch               | m                                    |
| $S_T$                    | Transverse pitch                 | m                                    |
| $T$                      | Temperature                      | K                                    |
| $T_{\mathrm{ad}}$        | Adiabatic flame temp.            | K                                    |
| $T_{\mathrm{film}}$      | Film temperature                 | K                                    |
| $T_{\mathrm{sat}}$       | Saturation temperature           | K                                    |
| $t$                      | Wall thickness                   | m                                    |
| $\tau_j$                 | Optical thickness                | --                                   |
| $UA$                     | Overall conductance              | W\,K$^{-1}$                          |
| $UA'(x)$                 | Conductance per length           | W\,K$^{-1}$\,m$^{-1}$                |
| $u_{\max}$               | Velocity factor                  | --                                   |
| $V$                      | Velocity                         | m\,s$^{-1}$                          |
| $w_i$                    | Mass fraction                    | --                                   |
| $X$                      | Mole fraction vector             | --                                   |
| $x$                      | Vapor quality / mole fraction    | --                                   |
| $x$                      | Axial coordinate                 | m                                    |
| $x_i$                    | Mole fraction                    | --                                   |
| $X_{tt}$                 | Martinelli parameter             | --                                   |
| $y_i$                    | Molar fraction                   | --                                   |
| $\zeta$                  | Loss coefficient                 | --                                   |

## Greek symbols

| Symbol                 | Name                               | Units                        |
| ---------------------- | ---------------------------------- | ---------------------------- |
| $\alpha$               | Exponent/constant                  | --                           |
| $\Delta P$             | Pressure drop                      | Pa                           |
| $\Delta T$             | Temperature difference             | K                            |
| $\delta$               | Thickness                          | m                            |
| $\varepsilon$          | Emissivity / roughness             | --                           |
| $\eta$                 | Efficiency                         | --                           |
| $\kappa$               | Thermal conductivity               | W\,m$^{-1}$\,K$^{-1}$        |
| $\lambda$              | Excess air ratio                   | --                           |
| $\mu$                  | Dynamic viscosity                  | Pa\,s                        |
| $\nu$                  | Stoichiometric/kinematic viscosity | mol/mol (or m$^2$\,s$^{-1}$) |
| $\Phi_{\mathrm{geom}}$ | Geometry factor                    | --                           |
| $\phi$                 | Correction/geometry factor         | --                           |
| $\pi$                  | Pi                                 | --                           |
| $\rho$                 | Density                            | kg\,m$^{-3}$                 |
| $\sigma$               | Stefan–Boltzmann constant          | W\,m$^{-2}$\,K$^{-4}$        |

## Subscripts / indices / conventions

| Index    | Meaning          | Units |
| -------- | ---------------- | ----- |
| ad       | Adiabatic        | --    |
| air      | Air              | --    |
| b        | Bulk             | --    |
| bend     | Bend             | --    |
| boiler   | Boiler           | --    |
| c / cold | Cold side        | --    |
| conv     | Convective       | --    |
| crit     | Critical         | --    |
| drum     | Drum             | --    |
| eq       | Equilibrium      | --    |
| f        | Saturated liquid | --    |
| fg       | Gas fouling      | --    |
| fo       | Water fouling    | --    |
| fw       | Feedwater        | --    |
| g        | Gas side         | --    |
| gw       | Gas wall         | --    |
| HX$_j$   | HX stage         | --    |
| in       | Inlet            | --    |
| indirect | Indirect         | --    |
| l        | Liquid           | --    |
| lo       | Liquid-only      | --    |
| minor    | Minor loss       | --    |
| nb       | Nucleate boiling | --    |
| out      | Outlet           | --    |
| prod     | Products         | --    |
| rad      | Radiative        | --    |
| react    | Reactants        | --    |
| ref      | Reference        | --    |
| sens     | Sensible         | --    |
| stage    | Stage            | --    |
| steam    | Steam            | --    |
| tot      | Total            | --    |
| w        | Water side       | --    |
| wall     | Wall             | --    |
| ww       | Water wall       | --    |

## Abbreviations

| Abbrev.    | Meaning                          | Units |
| ---------- | -------------------------------- | ----- |
| AFR        | Air–fuel ratio                   | --    |
| API        | Active pharmaceutical ingredient | --    |
| CIP        | Clean-in-place                   | --    |
| HHV        | Higher heating value             | --    |
| HP         | Enthalpy–pressure mode           | --    |
| HTC        | Heat-transfer coefficient        | --    |
| IAPWS-IF97 | Water/steam properties standard  | --    |
| LHV        | Lower heating value              | --    |
| NASA       | Thermo data source               | --    |

\newpage
