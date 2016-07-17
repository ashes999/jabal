import datetime, os.path, re, sys, time

class AppBuilder:
    
    CONTENT_PLACEHOLDER = '<jabal-code />'
    DEFAULT_MAIN_FILE = 'main.py'
    OUTPUT_DIRECTORY = 'bin'
    TEMPLATE_DIRECTORY = 'template'
    MAIN_HTML_FILE = 'index.html'
    
    # not guaranteed to be a package name and doesn't include multiple imports on one line
    IMPORT_REGEX = '(from ([a-z\.]+) import [a-z]+)'
    IGNORE_IMPORTS = ['browser', 'console', 'document', 'window'] # Brython libraries
        
    def watch(self):

        watch_path = self.validate_args()
        main_file = "{0}/{1}".format(watch_path, AppBuilder.DEFAULT_MAIN_FILE)
        output_directory = "{0}/{1}".format(watch_path, AppBuilder.OUTPUT_DIRECTORY)
        self.ensure_exists(output_directory)
        last_updated = None
        
        while True:
            now = os.path.getmtime(main_file)
            if now != last_updated:
                print("{0} changed at {1}. Rebuilding.".format(main_file, datetime.datetime.now()))
                last_updated = now
                
                with open(main_file) as source_file:
                    main_code = source_file.read()
                    
                with_imports = self.inline_imports(main_code)                
                    
                with open("{0}/{1}".format(AppBuilder.TEMPLATE_DIRECTORY, AppBuilder.MAIN_HTML_FILE)) as template_file:
                    original = template_file.read()
                    
                with open("{0}/{1}".format(output_directory, AppBuilder.MAIN_HTML_FILE), 'w+') as out_file:
                    substituted = original.replace(AppBuilder.CONTENT_PLACEHOLDER, with_imports)
                    out_file.write(substituted)
                        
            time.sleep(0.5)
                
    def validate_args(self):
        if len(sys.argv) != 2:
            print("Usage: python watch.py /path/to/yourgame")
            sys.exit(1)
        else:
            watch_path = sys.argv[1]
            
        main_file = "{0}/{1}".format(sys.argv[1], AppBuilder.DEFAULT_MAIN_FILE)
        if not os.path.exists(main_file):
            raise(Exception("Can't find {0}".format(main_file)))
            
        return watch_path
    
    def ensure_exists(self, dir):
        if not os.path.exists(dir):
            os.makedirs(dir)
                
    def inline_imports(self, python_code):
        # Replace "from a.b import C" with the contents of a/b.py
        # With our current regex, a.b is not guaranteed to be valid
        # TODO: make this recursive
        
        regex = re.compile(AppBuilder.IMPORT_REGEX, re.IGNORECASE)
        matches = regex.findall(python_code) # matching strings
        
        for match in matches:
            import_statement = match[0]
            module_name = match[1]
            
            path_name = module_name.replace('.', '/')
            path_name += ".py" 
            
            if AppBuilder.IGNORE_IMPORTS.__contains__(module_name):
                continue
            
            if not os.path.exists(path_name):
                print "WARNING: imported {0} but {1} doesn't exist".format(module_name, path_name)
            
            with open(path_name) as imported_file:
                imported_code = imported_file.read()
            
            python_code = python_code.replace(import_statement, imported_code)
            
        return python_code
            
AppBuilder().watch()