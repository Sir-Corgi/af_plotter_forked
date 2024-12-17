# af_plotter

`af_plotter` processes the AlphaFold3 JSON files it finds using the `--glob` search
in the `target` directories and/or the `target` JSON files listed. Optionally, the
`-R` (`--recursive`) flag allows `af_plotter` to descend through the given directories
applying the `--glob` search pattern.

By default both PAE and pLDDT plots are produced. These can be individually
disabled by passing `--nopae` and `--noplddt`, respectively.
