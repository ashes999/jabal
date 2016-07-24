from browser import window
from browser import console
from browser import document

global melonjs
melonjs = window.me

def load_script(path):
    el = document.createElement('script')
    el.async = False
    el.src = path
    el.type = 'text/javascript'

    apply_to = document.body #document.getElementsByTagName('HEAD')[0]
    apply_to.appendChild(el)

def init(width, height, resources):
    game = Game(width, height, resources)
    # We have to allow JS to interact with this object for some operations
    # eg. assigning resources automatically from resources.js
    window.game = game

    # Game Scripts. Load after Brython so window.game is defined.
    # Plugins
    load_script("lib/debugPanel.js")
    # Content
    load_script("js/entities/entities.js")    
    load_script("js/entities/HUD.js")
    load_script("js/screens/play.js")
    
    game.onload()

class Game:
    def __init__(self, width, height, resources):
        self.data = { "score" : 0 }        
        
        self.width = width
        self.height = height
        self.resources = resources

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
        console.log(self.width)
        console.log(self.height)
        console.log(self.resources)
        
    def loaded(self): 
        # set the "Play/Ingame" Screen Object
        melonjs.state.set(melonjs.state.PLAY, PlayScreen())

        # set a fade transition effect
        melonjs.state.transition("fade","#000000", 250)

        # start the game
        melonjs.state.change(melonjs.state.PLAY)
        