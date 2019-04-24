# Pre War Login - Python fan game mimicking fallout terminal hacking

## Table of Contents

1. [Description](#description)
2. [Parameters](#parameters)
3. [Examples](#examples)
4. [Exit-Status](#exit-status)
5. [Requirements](#requirements)
6. [Installation](#installation)
7. [Authors](#authors)

## Description

Curses based terminal game written in python to work like Fallout's Terminal Hacking mini-Game

_Disclaimer:_ Not made or endorsed by Bethesda, this is fan-made game

## Parameters

  ```shell
  app_curses.py [-h] [-t {3,4,5,6,7,8,9,10}] [-s] {easy,advanced,expert,master}

  positional arguments:
    {easy,advanced,expert,master}
    Set Game Difficulty
      easy - word size between 3 and 5
      advance - word size between 6 and 8
      expert - word size between 9 and 10
      master - word size between 11 and 12

  optional arguments:
    -h, --help            show this help message and exit
    -t {3,4,5,6,7,8,9,10}, --tries {3,4,5,6,7,8,9,10}
                          Number of tries
    -s, --secret          increases difficulty by disabling secret chars.
  ```

## Examples

`app_curses.py easy`

`app_curses.py advanced -t 5`

`app_curses.py --secret master --tries 3`

## Exit-Status

    0  Success
    1  General Failure (varied message)
    2  Incorrect or missing arguments
    3  The terminal is too narrow (min 54) or short (min 21)
    4  Terminal does not support Color

## Requirements

- Python 3.6 and Above
  - Tested on 3.6 and 3.7
- Virtual Env/Pip

## Installation

1. Create a Virtual Env
2. Source the VirtualEnv
3. Install `requirement.txt` with pip

```shell
virtualenv venv --python=python3.7
source venv/bin/activate
pip install -r requirements.txt
```

## Authors

- Anthony Tilelli
