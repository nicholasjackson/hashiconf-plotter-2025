## Generating Patterns

The `generate_pattern.py` script handles both JSON pattern generation and SVG creation in a single command.

### Basic Usage

Generate a new random pattern (creates both JSON and SVG files):
```bash
python generate_pattern.py
```

This will create:
- `pattern.json` - The pattern data file
- `pattern_combined.svg` - Combined pattern with both colors
- `pattern_color1.svg` - Purple/first color only
- `pattern_color2.svg` - Cyan/second color only

### Options

**Generate with a specific seed** (for reproducible patterns):
```bash
python generate_pattern.py --seed 123
```

**Skip JSON generation** (regenerate SVGs from existing pattern.json):
```bash
python generate_pattern.py --skip-json
```

**Enable debug mode** (adds grid and ID numbers for debugging):
```bash
python generate_pattern.py --debug
```

**Send to plotter** (automatically plot after generation):
```bash
python generate_pattern.py --plot color1    # Plot purple layer
python generate_pattern.py --plot color2    # Plot cyan layer
python generate_pattern.py --plot combined  # Plot both layers
```

**Combine options**:
```bash
# Generate with seed and debug mode
python generate_pattern.py --seed 42 --debug

# Regenerate SVGs with debug and send to plotter
python generate_pattern.py --skip-json --debug --plot color1

# Generate reproducible pattern and plot combined
python generate_pattern.py --seed 123 --plot combined
```

### Command Line Options

- `-s, --seed SEED` - Random seed for reproducible patterns
- `--debug` - Enable debug mode with grid and ID numbers
- `--skip-json` - Skip JSON generation and use existing pattern.json
- `--json-file JSON_FILE` - Specify JSON file name (default: pattern.json)
- `--plot {color1,color2,combined}` - Send specified SVG to the plotter after generation

### Plotter Support

To use the `--plot` flag, you need to install the AxiDraw module:
```bash
pip install pyaxidraw
```

The plot functionality uses the `plot.py` module to send SVG files directly to the AxiDraw plotter.