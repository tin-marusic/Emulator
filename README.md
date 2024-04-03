# Emulator

# Install instructions

```
cmsrel CMSSW_13_3_0
cd CMSSW_13_3_0/src
cmsenv
git clone https://github.com/mkovac/Emulator.git
make
./run
```

Pokretanje
- potrebno je da se svi input fileovi nalaze u mapi 'inputs'
- pretanjem 'output_gen.py' (iz mape 'python code from josip') učitavaju se sve datoteke iz mape 'inputs' te se time generiraju outputi u mapu 'outputs'
- u mapi plot nalaze se dvije python skripte:
    -'sum_outputs.py' automatski sumira sve datoteke iz mape 'outputs',odvojeno za H i E, te generira koordinate za plot
    -'plot_sum' izrađuje grafove iz tih datoteka za ECAL i Hadronic dio