// Note: doesn't copy parent method objects. Eg. if your Brython
// object has a "foo" method, but inherits a "bar" method, this
// method currently only copies "foo", not "bar" over.
function copyBrythonMethodsToObjectRoot(bryObj)
{
    // Be 100% sure it's a brython object
    var properties = [];
    
    for (var p in bryObj) {
        properties.push(p);
    }
    
    if (properties.length == 1 && properties[0] == "__class__")
    {
        // Store it in a place where we can easily tweak it: window.temp
        window.temp = bryObj;
              
        for (var m in bryObj.__class__) {
            // Don't try this at home, kids ...
            // window.target.__class__.foo => window.target.foo
            // Exclude things like __mro__ and $slots
            if (m.indexOf('__') == -1 && m.indexOf("$") == -1) {
                eval("window.temp." + m + " = window.temp.__class__." + m);
                console.log("window.temp." + m + " => window.temp.__class__." + m);
            }
        }
        
        window.temp = null;
        
        return bryObj;          
    }
    else
    {
        throw bryObj + " doesn't seem to be a Brython object.";
    }  
}