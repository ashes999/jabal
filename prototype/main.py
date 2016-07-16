from browser import console, window, document

# Get the main Crafty instance
Crafty = window.Crafty
# Populate properties. TODO: use reflection
Crafty.audio = window.craftyProperties["audio"]
Crafty.support = window.craftyProperties["support"]

Crafty.init(800, 600)
Crafty.background("#444")

Crafty.audio.add("blip", "blip.wav")

e = Crafty.e('2D, DOM, Color, Fourway, Mouse')
e.attr({ "x": 32, "y": 32, "w": 48, "h": 48 }).color('red').fourway(20)

e.bind("Click", lambda: Crafty.audio.play("blip")); 