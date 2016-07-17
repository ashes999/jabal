// Store properties. Crafty uses Crafty.extend(...) which calls
// for key in obj { this[key] = obj[key] }.
// As of these versions, Brython doesn't carry those over to the Python,
// it only seems to carry over methods. We can easily get around this by
// storing those properties separately and assigning them later.
window.craftyProperties = {
    "audio": Crafty.audio,
    "support": Crafty.support
};