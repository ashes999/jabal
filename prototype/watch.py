import datetime, os.path, sys, time

content_placeholder = '<jabal-main />'

if len(sys.argv) > 2:
    print("Usage: python main.py <main file to watch>")
else:    
    last_updated = None
    
    if len(sys.argv) == 2:
        watch = sys.argv[1]
    else:
        watch = "main.py"
    
    if not os.path.exists('bin'):
        os.makedirs('bin')
    
    while True:
        now = os.path.getmtime(watch)
        if now != last_updated:
            print("{0} changed at {1}. Rebuilding.".format(watch, datetime.datetime.now()))
            last_updated = now
            
            with open(watch) as source_file:
                data = source_file.read()
                
            with open('index.html') as template_file:
                original = template_file.read()
            
            with open('bin/index.html', 'w+') as out_file:
                substituted = original.replace(content_placeholder, data)
                out_file.write(substituted)
                    
        time.sleep(1)