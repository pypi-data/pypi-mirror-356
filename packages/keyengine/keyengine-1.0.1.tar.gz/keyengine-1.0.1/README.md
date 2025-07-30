# keyengine
## Introduction
Keyengine is a small package made for simple Console interfaces. Keyengine can be used for:
* Interactive menus
* Printing and waiting for input simultaneously
* Checking what letter is currently pressed, for easier creation of your own systems
## Installation
### Python >=3.13
If you have Python 3.13 or newer, please just run `pip install -U keyengine`
### Python >=3.10
If you have Python 3.10 or newer, please just run `pip install -U deprecated keyengine`
## Usage
### menus
`menu(choices: list[str], index: bool = True)`
<br>Takes a list of possible choices and lets the user pick one using the arrow and ENTER keys. Returns the index of the chosen item in the list.
<br>│
<br>├─ choices: A list of possible choices
<br>├─ index: Whether to display an index (i + 1)
### console
`Console()`
<br>A good way to display text while also waiting for input simultaneously. Methods are self-explanatory.