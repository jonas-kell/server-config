# TODO: not set up after cosmic transition

- terminator shortcut
- gdrive script
- mounts / favourites in file manager
- cpu / GPU state
- store the config toml files repeatable

https://github.com/cosmic-utils

<!--  -->

cargo install --git https://github.com/estin/cos-cli
cos-cli info

nano ~/.config/cosmic/com.system76.CosmicSettings.WindowRules/v1/tiling_exception_custom

```cmd
[
    (appid: "", title: ".*CopyQ.*", enabled: true),
]
```
