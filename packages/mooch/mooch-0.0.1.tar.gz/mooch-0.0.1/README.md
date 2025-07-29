# Python Mooch

![PyPI](https://img.shields.io/pypi/v/mooch?label=mooch)
![PyPI - Downloads](https://img.shields.io/pypi/dm/mooch)
<img alt="GitHub Issues or Pull Requests" src="https://img.shields.io/github/issues/nickstuer/mooch">

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)
[![license](https://img.shields.io/github/license/nickstuer/mooch.svg)](LICENSE)

This Python package is a collection of useful Python code that is commonly used on all types of Python projects.

## Table of Contents

- [Features](https://github.com/nickstuer/mooch?tab=readme-ov-file#-features)
- [Install](https://github.com/nickstuer/mooch?tab=readme-ov-file#-install)
- [Usage](https://github.com/nickstuer/mooch?tab=readme-ov-file#-usage)
- [Contributing](https://github.com/nickstuer/mooch?tab=readme-ov-file#-contributing)
- [License](https://github.com/nickstuer/mooch?tab=readme-ov-file#-license)

## 📖 Features


### Config File
Uses a TOML config file. Easily get/set configuration values. Automatically sets values to defaults if they're not currently saved in the configuration file.

### Requires
Throw an exception if the installed python version isn't new enough.
Throw an exception if the desired operating system is incorrect.

### Logging
Add automatic logging to methods that are run by using a decorator. Useful for logging function arguments, start of function and end of function.


## 🛠 Install

```
# PyPI
pip install mooch
```
or
```
uv add mooch
```

##  📌 Dependencies
Python 3.9 or greater

## 🎮 Usage

### Config File
```python
from mooch import Config
default_settings = {
    "settings": {
        "name": "MyName,
        "mood": "happy",
    },
}

config = Config("settings.toml", default_settings)

print(config["settings.mood"])
config["settings.mood"] = "angry"
print(config["settings.mood"])
```

### Requires
Throws an Exception if the requirement isn't satisified.
```python
from mooch.require.require import python_version, operating_system

python_version("3.13")
operating_system("Windows")
```

### Logging Decorator
For adding 'BEGIN' and 'END' to log files whenever the decorated function runs.
Also logs the values of the args passed in.

```python
from mooch.logging.decorators import log_begin_and_end

@log_begin_and_end
def random_function(arg1, arg2){
    print(arg1)
    print(arg2)
}
```

## 🏆 Contributing

PRs accepted.

If editing the Readme, please conform to the [standard-readme](https://github.com/RichardLitt/standard-readme) specification.

#### Bug Reports and Feature Requests
Please use the [issue tracker](https://github.com/nickstuer/mooch/issues) to report any bugs or request new features.

#### Contributors

<a href = "https://github.com/nickstuer/mooch/graphs/contributors">
  <img src = "https://contrib.rocks/image?repo=nickstuer/mooch"/>
</a>

## 📃 License

[MIT © Nick Stuer](LICENSE)