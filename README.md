![logo](mountain.png)
# Jabal

Write Python code. Get desktop, mobile, and web games from one code-base.

Jabal leverages Brython to embed itself and run inside a webpage, and wraps and exposes mature Javascript libraries for game development under Pythonic interfaces.  To create stand-alone desktop executables, Jabal wraps Brythonic code in a self-contained Javascript environment.

# Getting Started

Clone this repository. Then, add the following sample code to `main.py`:

```python
from browser import console, window, document

Jabal.init(800, 600)
Jabal.background("#444")

Jabal.audio.load("blip", "blip.wav")

e = Jabal.Entity('2D, DOM, Color, Fourway, Mouse')
e.size(48, 48).color('red').move(32, 16).move_with_keyboard()

e.on_click(lambda: Jabal.audio.play("blip")) 
```

This creates an `800x600` greyish background with a red square. The red square responds to arrow keys (and WASD). Clicking on it plays `blip.wave` (create one with [BFXR](http://www.bfxr.net/)).

You can write your own code, too 