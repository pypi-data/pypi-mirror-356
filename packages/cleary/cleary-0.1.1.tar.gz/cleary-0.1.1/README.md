# cleary

**Ultimate cross-platform console clearer.**

Cleary instantly clears your terminal or console on any OS. Works with PowerShell, CMD, bash, zsh, and more.

## Features

- Clears input buffer and screen by default
- Delay before clearing (`--delay N`)
- Run any command after clearing (`--`)
- Info about the tool (`info`)

## Install

```sh
pip install cleary
```

## Usage

```sh
cleary
cleary --delay 2
cleary -- pip list
cleary info
``` 