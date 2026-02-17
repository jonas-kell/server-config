# How to generate templates

## Installed gnome extensions

```cmd
gnome-extensions list --enabled
```

## Gnome extensions settings

Dump them (the template file contains manual template changes!!!)

```cmd
dconf dump /org/gnome/shell/extensions/ > gnome-extensions-settings.dconf.j2
```

Load them (manually) (!! repo stores a format-bearing file, you can not load the un-rendered version !!)

```cmd
dconf load /org/gnome/shell/extensions/ < gnome-extensions-settings.dconf
```

Manual editing (most importantly deletion of old keys)

```cmd
dconf-editor
```
