# TODO: not set up after cosmic transition

- gdrive script
- mounts / favourites in file manager
- store the config toml files repeatable

https://github.com/cosmic-utils

<!--  -->

flatpak install flathub io.github.cosmic_utils.camera
sudo apt-get install cosmic-store

<!-- install minimon from the cosmic store -->

activate in applets -> configure to thigs you want to be displayed

<!--  -->

cargo install --git https://github.com/estin/cos-cli
cos-cli info

nano ~/.config/cosmic/com.system76.CosmicSettings.WindowRules/v1/tiling_exception_custom

```cmd
[
    (appid: "", title: ".*CopyQ.*", enabled: true),
]
```
