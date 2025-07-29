# Ecdysys

Little CLI tool to print and update system
Currently supported package managers are:
- `pacman`
- `yay` and `paru` (aur support)
- `flatpak`
## Installation
```shell
# With pip
pip install ecdysys
# for Arch Linux users
paru -S python-ecdysys
```
2. Create a `config.toml` file, these are the following entry available

| Entry                 | Usage                                    | Example                   |
|-----------------------|------------------------------------------|---------------------------|
| `pkg_managers`*       | package manager to use                   | `[ "pacman", "flatpak" ]` |
| `aur_helper`          | aur helper to use                        | `"paru"`                  |
| `post_install_script` | path to script ot run after installation | `path/to/script`          |
*Must be set

## Usage
```shell
usage: ecdysys [-h] [-l] [-u]

Python CLI to update your system packages

options:
  -h, --help    show this help message and exit
  -l, --list    List available updates
  -u, --update  Update package
```