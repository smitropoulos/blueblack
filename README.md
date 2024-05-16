# Blueblack

Automatically change to light and dark mode depending on your location.

Set up a simple `config.yaml` under your `$XDG_CONFIG_HOME/blueblack` file with

```
# Get your lattitude and longtitude through e.g. gmaps (https://support.google.com/maps/answer/18539?hl=en&co=GENIE.Platform%3DDesktop)
"lat": 23.2003
"lng": 31.1233
"update_days": 1
```

and change the update_days to something appropriate (e.g. 10 days).

When it's slightly past sunrise or sunset time (around 5 seconds), executable scripts inside `XDG_CONFIG_HOME/blueblack/{dark,light}_mode` will run automatically.
Some examples are provided in [the source code page](https://github.com/smitropoulos/blueblack/tree/main/configs)

Internally, Blueblack will use [the Sunrise-sunset API](https://sunrise-sunset.org/api) which is currently free. Please use this responsibly so we can have free things.
