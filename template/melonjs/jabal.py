from browser import window
global melonjs
melonjs = window.me

def init():
    global game
    game = Game()
    game.onload()
    

class Game:
    def __init__(self):
        self.data = { "score" : 0 }
        
        # TODO: externalize to user
        # TODO: turn into tuple?
        self.resources = [
            # background
            { "name": "background", "type": "image", "src": "data/img/background/bg_dirt128.png" },
            # upper part of foreground
            { "name": "grass_upper", "type": "image", "src": "data/img/foreground/grass_upper128.png" },
            # lower part of foreground
            { "name": "grass_lower", "type": "image", "src": "data/img/foreground/grass_lower128.png" },
            # more sprites
            { "name": "mole", "type": "image", "src": "data/img/sprites/mole.png" },

            # bitmap font
            { "name": "PressStart2P", "type":"image", "src": "data/fnt/PressStart2P.png" },
            { "name": "PressStart2P", "type":"binary", "src": "data/fnt/PressStart2P.fnt"},

            # main music track
            { "name": "whack", "type": "audio", "src": "data/bgm/" },
            # Laugh audio FX
            # { "name": "laugh", "type": "audio", "src": "data/sfx/" },
            # ow audio FX
            { "name": "ow", "type": "audio", "src": "data/sfx/" }
        ]

    def onload(self):
        # we don't need the default 60fps for a whack-a-mole !
        melonjs.sys.fps = 30;

        # Initialize the video.
        settings = { "wrapper" : "screen", "scale": "auto" }
        if (not melonjs.video.init(1024, 768, settings)):
            window.alert("Your browser does not support HTML5 canvas.")
            return

        # initialize the "sound engine"
        melonjs.audio.init("mp3,ogg")

        # set all ressources to be loaded
        # melonjs.loader.preload(self.resources, self.loaded.bind(self.onload))
        melonjs.loader.preload(self.resources, self.loaded)
        
    def loaded(self):        
        # set the "Play/Ingame" Screen Object
        melonjs.state.set(melonjs.state.PLAY, Game().PlayScreen())

        # set a fade transition effect
        melonjs.state.transition("fade","#000000", 250)

        # start the game
        melonjs.state.change(melonjs.state.PLAY)