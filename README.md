## Generating datafiles

To generate the datafiles, run the following command:

```bash
python generate_json.py --seed 44 
```

`--seed` is an optional argument to set the random seed for reproducibility. Running the command with the same seed should produce the same output files.

```bash
python generate_pattern.py --data-file=pattern.json --debug
```

`--debug` is an optional argument that prints a grid and the id numbbers for easier debugging. ID corresponds to the ID inside the datafile.