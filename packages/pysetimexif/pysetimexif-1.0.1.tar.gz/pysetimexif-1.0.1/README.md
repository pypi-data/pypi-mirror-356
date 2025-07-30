# pysetimexif

Tool for setting 'modified timestamp' on files according to their EXIF information.  
Supported formats: Same as ExifRead. Currently TIFF, JPEG, PNG, Webp and HEIC.

## Installation

```
pip install pysetimexif-1.0.0-py3-none-any.whl
```

or

```
pipx install pysetimexif-1.0.0-py3-none-any.whl
```

## Usage

pysetimexif [-h] [-r] paths [paths ...]

Set 'modified timestamp' on files according to their embedded exif information.

positional arguments:
paths - one or more files or directories to process

options:
-h, --help show this help message and exit
-r, --recursive Process paths recursively

## License

[MIT](https://choosealicense.com/licenses/mit/)

## References

[ExifRead](https://pypi.org/project/ExifRead/)
