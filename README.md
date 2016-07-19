![logo](mountain.png)
# Jabal

Write Python code. Get desktop, mobile, and web games from one code-base.

Jabal leverages Brython to embed itself and run inside a webpage, and wraps and exposes mature Javascript libraries for game development under Pythonic interfaces.  To create stand-alone desktop executables, Jabal wraps Brythonic code in a self-contained Javascript environment.

# Getting Started

Clone this repository somewhere.

In a separate directory, add the following sample code to `main.py`:

```python
Jabal.init(800, 600)
Jabal.load_audio(["blip.wav"])

e = Entity().size(48, 48).colour('red')
e.move(32, 16).move_with_keyboard().on_click(lambda: Jabal.play_audio("blip"))
```

This creates an `800x600` greyish background with a red square. The red square responds to arrow keys (and WASD). Clicking on it plays `blip.wave` (create one with [BFXR](http://www.bfxr.net/)).

Compile (to Javascript) and run by running `python /path/to/jabal/watch.py`. The resulting Javascript (including assets, etc.) appears in `bin`.

# Create Classes, Not Modules

Jabal embeds your Python code into a single (minified and obfuscated) script. When you use classes, Jabal embeds and inlines them, along with your `main.py` code, into a single, continuous script. They work.

Modules depend fundamentally on being in separate files. They don't work in an embedded environment. 

Sample:

- Create a directory called `utils` with a file called `my_random.py`
- Add a class or module called `MyRandom` into `my_random.py`
- Add `from utils.my_random import MyRandom` in `main.py`

Build your game. The generated `index.html` file in `bin` contains the contents of `my_random.py` before the contents of `main.py`.