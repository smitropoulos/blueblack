# Blueblack

Automatically change to light and dark mode depending on your location.

~~Internally, Blueblack will use [the Sunrise-sunset API](https://sunrise-sunset.org/api) which is currently free. Please use this responsibly, so we can have free things.~~

This fork uses `python-astral` library to calculate sunrise & sunset time. No need for Internet connection.

## Configuration

Location: `$XDG_CONFIG_HOME/blueblack/`

Main configuration file must be written in `YAML`.

Example:
```yaml
"lat": 23.2003
"lng": 31.1233
"update_days": 1
"offset_sunrise": "1:00:00" # Run 1 hour later
"offset_sunset": "-0.5" # Run 30 minutes earlier
```

`lat`: your latitude.  
`lng`: your longitude.  
`update_days`: update sunrise & sunset time every this (This is from the original project. Since this fork uses `astral`, I don't think this is necessary, but you have to fill this with a number)
`offset_sunrise` and `offset_sunset`: offset for sunrise & sunset. This can be as these 3 formats: `%H`, `%H:%M`, `%H:%M:%S` (float), positive for push, negative for pull.

When it's slightly past sunrise or sunset time (around 5 seconds), executable scripts inside `XDG_CONFIG_HOME/blueblack/{dark,light}_mode` will run automatically.
Some examples are provided in [the source code page(Original author)](https://github.com/smitropoulos/blueblack/tree/main/configs)