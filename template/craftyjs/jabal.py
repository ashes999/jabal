from browser import window
global craftyjs
craftyjs = window.Crafty

# This should really be a module, but we lose the filename when we dynamically
# aggregate it into our final Python code, so it's a "static class" (C# semantics).
class Jabal:
    @staticmethod
    def init(width, height):
        # Populate properties. TODO: use reflection
        # Set up in jabal.js
        craftyjs.audio = window.craftyProperties["audio"]
        craftyjs.support = window.craftyProperties["support"]
        window.craftyProperties = None

        craftyjs.init(800, 600)        
        Jabal.background("#444")

    # Colour (eg. "red") or code (eg. #fff, #FE9828)
    @staticmethod    
    def background(color):
        craftyjs.background(color)

    @staticmethod
    def entity(components):
        return Entity(components)

    @staticmethod
    def load_audio(files):
        for file in files:
            dotIndex = file.index('.')
            id = file[0:dotIndex]
            craftyjs.audio.add(id, file)
            
    @staticmethod
    def play_audio(id):
        craftyjs.audio.play(id)

class Entity:    
    def __init__(self):
        self.entity = craftyjs.e('2D, Alpha, Delay, Color, Collision, WebGL, Canvas')

    def colour(self, code):
        self.entity.color(code)
        return self

    def image(self, filename):
        self.entity.requires('Image').image(filename)
        return self

    # lambda: takes no parameters
    def on_click(self, click_lambda):
        self.entity.bind("Click", lambda: click_lambda())
        return self
        
    def move(self, x, y):
        self.entity.attr({ "x": x, "y": y })
        return self
        
    def move_with_keyboard(self, velocity = 20):
        self.entity.fourway(velocity)
        return self
        
    def size(self, width, height):
        self.entity.attr({ "w": 48, "h": 48 })
        return self