from browser import window
global craftyjs
craftyjs = window.Crafty

def init(width, height):
    # Populate properties. TODO: use reflection
    # Set up in jabal.js
    craftyjs.audio = window.craftyProperties["audio"]
    craftyjs.support = window.craftyProperties["support"]
    window.craftyProperties = None

    craftyjs.init(800, 600)
    background("#444")

# Colour (eg. "red") or code (eg. #fff, #FE9828)
def background(color):
    craftyjs.background(color)

def entity(components):
    return Entity(components)

def load_audio(files):
    for file in files:
        dotIndex = file.index('.')
        id = file[0:dotIndex]
        craftyjs.audio.add(id, file)

def play_audio(id):
    craftyjs.audio.play(id)

class Entity:
    def __init__(self):
        self.entity = craftyjs.e('2D, Alpha, Delay, Color, Collision, Canvas')

    def colour(self, code):
        self.entity.color(code)
        return self

    def image(self, filename):
        self.entity.requires('Image').image(filename)
        return self

    # lambda: takes no parameters
    def on_click(self, click_lambda):
        # Click doesn't work on some mobiles with PhoneGap, for some reason.
        # See: https://github.com/craftyjs/Crafty/issues/1043
        # Mouse-up seems to work, so bind to that.
        self.entity.requires('Mouse').bind("MouseUp", lambda: click_lambda())
        return self

    def move(self, x, y):
        self.entity.attr({ "x": x, "y": y })
        return self

    def move_with_keyboard(self, velocity = 100):
        self.entity.requires('Fourway').fourway(velocity)
        return self

    def size(self, width, height):
        self.entity.attr({ "w": width, "h": height })
        return self
