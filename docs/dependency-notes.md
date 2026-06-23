# Dependency Notes

Expected Linux Mint / Ubuntu-style packages:

```zsh
sudo apt install python3-gi gir1.2-gtk-4.0 gir1.2-vte-3.91 desktop-file-utils
```

These should be verified before implementation.

Do not install dependencies automatically from this project.

The GTK/VTE modules are imported lazily. CLI parsing and unit tests do not
require a display server or installed GTK/VTE bindings.

## Local Probe Result

The Phase 3 local package check reported:

```text
desktop-file-utils 0.27-2build1
gir1.2-gtk-4.0 4.14.5+ds-0ubuntu0.10
gir1.2-vte-3.91 0.76.0-1ubuntu0.1
python3-gi 3.48.2-1
```

Additional local command checks reported:

```text
Python 3.12.3
desktop-file-validate: /usr/bin/desktop-file-validate
gtk-launch: /usr/bin/gtk-launch
nvim: /home/blndsft/.local/bin/nvim
/home/blndsft/.local/bin/nvim: /home/blndsft/.local/bin/nvim
```

No required package was missing from the `dpkg-query` result.
