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

Run `python -m SimpleHTTPServer` from bin, then open your browser to `localhost:8000`. You should see your game.

# Modules, Classes, and Embedding

By default, Jabal uses AJAX requests to fetch files when you `import` them (eg. `import awesome_random` will make a call to `http://localhost/awesome._random.py`). This is why you need a local web server.

Jabal can optionally combine, obfuscate, and embed your Python code inside the HTML instead. You may want to do this if:

- You don't want to use an HTTP server
- You want your code to be minified/obfuscated
- You didn't create any modules

To use this mode, pass the `--embed-imports` command-line argument to Jabal. The generated `index.html` contains all imports and your `main.py` code, minified and obfuscated.

## Importing Modules

Importing modules currently works like this:

- If the module file is `foo.py`, write `import foo`
- If the module file is `foo/bar.py`, write `from foo import bar`. Note that you'll see a Javascript console error complaining that `foo.py` doesn't exist, even though the import succeeds (see [this issue](https://github.com/brython-dev/brython/issues/458) for some more information).

## Static Classes

Modules aren't minified/obfuscated and are still loaded with AJAX. If this bothers you, you can convert them into classes with static methods (like C#'s static classes). A subset sample of `math` is below:


```
# math.py (module)

def max(a, b)
  pass # ...
  
def pow(a, b)
  pass # ...
  
# math.py (static class)
class Math:
  def __init__(self):
    raise(Exception("Static classes can't be instantiated."))
  
  @staticmethod
  def max(a, b):
    pass # ...
    
  @staticmethod
  def pow(a, b):
    pass # ...
```

# Using your Favourite Javascript Libraries with Jabal

Since Jabal uses Brython and wraps Javascript, you can add your favourite Javascript libraries to Jabal. Simply:

- Clone Jabal from git
- Download the library (regular or minified) and drop it into Jabal's `template/craftyjs/lib` directory
- Add a reference to it (and/or any CSS files, fonts, etc.) in `template/craftyjs/index.html`

If you're actually doing this, please open an issue on GitHub so we can provide a method of doing this that doesn't rely on cloning Jabal from source. 

# Acknowledgements

We are extremely thankful to and grateful for authors of various open-source projects that power Jabal. An incomplete list includes:

- [Brython](https://github.com/brython-dev/brython)
- [CraftyJS](https://github.com/craftyjs/Crafty/) 