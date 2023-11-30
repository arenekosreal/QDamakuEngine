# QDamakuEngine

## What is this

This is just a Damaku Engine written in PySide6


## How to use

1. Prepare poetry

    See https://python-poetry.org/docs/#installation for more info.

2. Install project

    Run `poetry install` in this repository

3. Build wheel

    Run `poetry build` in this repository, you will find artifacts in `dist` folder

4. Install wheel

    Run `python -m installer dist/*.whl` in this repository to install it.

5. Run the program

    Run `qdamakuengine` in your terminal and everything should be fine.

6. Run from source

    After finishing step 2, run `poetry run qdamakuengine` in this repository instead building, installing and running.


## API

Simply connect to the socket and send json string like this:
```json
{
    "text": "sample-damaku"
}
```
And you should received the response like this:
```json
{
    "result": 0,
    "message": "Success to record damaku"
}
```
When there is something wrong, you need to check result code and message for detailed info.