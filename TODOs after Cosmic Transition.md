# TODO: not set up after cosmic transition

- mounts / favourites in file manager
- store the config toml files repeatable

https://github.com/cosmic-utils

<!--  -->

flatpak install flathub io.github.cosmic_utils.camera
sudo apt-get install cosmic-store

<!-- install minimon from the cosmic store (CPU / etc. performance) -->

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

<!--  -->

Clear gnome online accounts links -> non working cloud integrations

rm -rf ~/.config/goa-1.0

Google drive rclone shortcut just keeps working and can be reused (Applications->right-click->pin)
