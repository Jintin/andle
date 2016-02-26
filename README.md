# andle
[![PyPI version](https://badge.fury.io/py/andle.svg)](https://badge.fury.io/py/andle)
[![Build Status](https://travis-ci.org/Jintin/andle.svg?branch=master)](https://travis-ci.org/Jintin/andle)
[![Code Climate](https://codeclimate.com/github/Jintin/andle/badges/gpa.svg)](https://codeclimate.com/github/Jintin/andle)
[![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://github.com/JStumpp/awesome-android)

andle is an Android tool to help you sync dependencies, SDK or build tool version.

## Installation
Simple install by [pip](http://pip.readthedocs.org/en/stable/installing):

```bash
$ sudo pip install andle
```

## Usage
The most commonly used command:

```bash
$ andle setsdk -p <path>                    # set android sdk path
$ andle update -p <path> [-d] [-r] [-g]     # sync project gradle config

-h, --help            show this help message and exit
-p PATH, --path PATH  root path
-d, --dryrun          dryrun
-g, --gradle          check gradle version
-r, --remote          check jcenter repository
```

See `andle --help` or `andle <command> --help` for more information.

## Contributing
Bug reports and pull requests are welcome on GitHub at [https://github.com/Jintin/andle](https://github.com/Jintin/andle).

## License
The package is available as open source under the terms of the [MIT License](http://opensource.org/licenses/MIT).
