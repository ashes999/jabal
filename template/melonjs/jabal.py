from browser import window
from browser import console
import javascript

global melonjs
melonjs = window.me

def init(width, height, resources, starting_screen):
    game = Game(width, height, resources, starting_screen)    
    # We have to allow JS to interact with this object for some operations
    # eg. assigning resources automatically from resources.js
    window.game = game

    # Game Scripts. Load after Brython so window.game is defined.
    # Plugins
    javascript.load("lib/debugPanel.js")
    # Content
    javascript.load("js/entities/entities.js")    
    javascript.load("js/entities/HUD.js")
    javascript.load("js/screens/play.js")
    
    game.onload()

class Game:
    def __init__(self, width, height, resources, starting_screen):
        self.data = { "score" : 0 }        
        
        self.width = width
        self.height = height
        self.resources = resources
        window.copyBrythonMethodsToObjectRoot(starting_screen)
        self.starting_screen = starting_screen

    def onload(self):
        # we don't need the default 60fps for a whack-a-mole !
        melonjs.sys.fps = 30;

        # Initialize the video.
        settings = { "wrapper" : "screen", "scale": "auto" }
        if (not melonjs.video.init(self.width, self.height, settings)):
            window.alert("Your browser does not support HTML5 canvas.")
            return

        # initialize the "sound engine"
        melonjs.audio.init("mp3,ogg")

        # set all ressources to be loaded
        # melonjs.loader.preload(self.resources, self.loaded.bind(self.onload))
        melonjs.loader.preload(self.resources, self.loaded)
        
    def loaded(self): 
        # set the "Play/Ingame" Screen Object
        melonjs.state.set(melonjs.state.PLAY, self.starting_screen)

        # set a fade transition effect
        melonjs.state.transition("fade","#000000", 250)

        # start the game
        melonjs.state.change(melonjs.state.PLAY)