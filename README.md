# Blueblack

Automatically change to light and dark mode depending on your location.

Uses `python-astral` library to calculate sunrise & sunset time.

## Configuration

Location: `$XDG_CONFIG_HOME/blueblack/`

Main configuration file must be written in `YAML`.

Example:

```yaml
"lat": 23.2003
"lng": 31.1233
"offset_sunrise": "1:00:00" # Run 1 hour later
"offset_sunset": "-0.5" # Run 30 minutes earlier
```

`lat`: your latitude.  
`lng`: your longitude.  
`offset_sunrise` and `offset_sunset`: offset for sunrise & sunset. This can be as these 3 formats: `%H`, `%H:%M`, `%H:%M:%S` (float), positive for push, negative for pull.

When it's slightly past sunrise or sunset time (around 5 seconds), executable scripts inside `XDG_CONFIG_HOME/blueblack/{dark,light}_mode` will run automatically.
Some examples are provided in [the source code page](https://github.com/smitropoulos/blueblack/tree/main/configs)
