import datetime, os.path, sys, time

class AppBuilder:
    
    CONTENT_PLACEHOLDER = '<jabal-main />'
    DEFAULT_MAIN_FILE = 'main.py'
    OUTPUT_DIRECTORY = 'bin'
    TEMPLATE_DIRECTORY = 'template'
    MAIN_HTML_FILE = 'index.html'
        
    def watch(self):

        watch = self.validate_args()
        self.ensure_exists(AppBuilder.OUTPUT_DIRECTORY)
        last_updated = None
        
        while True:
            now = os.path.getmtime(watch)
            if now != last_updated:
                print("{0} changed at {1}. Rebuilding.".format(watch, datetime.datetime.now()))
                last_updated = now
                
                with open(watch) as source_file:
                    data = source_file.read()
                    
                with open("{0}/{1}".format(AppBuilder.TEMPLATE_DIRECTORY, AppBuilder.MAIN_HTML_FILE)) as template_file:
                    original = template_file.read()
                
                with open("{0}/{1}".format(AppBuilder.OUTPUT_DIRECTORY, AppBuilder.MAIN_HTML_FILE), 'w+') as out_file:
                    substituted = original.replace(AppBuilder.CONTENT_PLACEHOLDER, data)
                    out_file.write(substituted)
                        
            time.sleep(0.5)
                
    def validate_args(self):
        if len(sys.argv) > 2:
            print("Usage: python main.py <main file to watch>")
            sys.exit(1)
        else:    
            if len(sys.argv) == 2:
                watch = sys.argv[1]
            else:
                watch = AppBuilder.DEFAULT_MAIN_FILE
            
            return watch
    
    def ensure_exists(self, dir):
        if not os.path.exists(dir):
            os.makedirs(dir)
                
AppBuilder().watch()