import datetime, os.path, re, shutil, sys, time
import io.directory

class AppBuilder:
    
    CONTENT_PLACEHOLDER = '<jabal-code />' # string in the template HTML to replace with amalgamated code
    DEFAULT_MAIN_FILE = 'main.py' # entry point file in the user's source code
    OUTPUT_DIRECTORY = 'bin' # subdirectory in the source directory where we output generated code
    TEMPLATE_DIRECTORY = 'template' # directory with all our template files
    MAIN_HTML_FILE = 'index.html' # name of the generated (and template) HTML file
    JABAL_BACKEND = 'craftyjs' # back-end to use in generation
    JABAL_MAIN_PY = 'jabal.py' # file containing jabal's python module, to include first
    JABAL_MAIN_CODE = 'import main' # contents if not embedding everything
    
    # not guaranteed to be a package name and doesn't include multiple imports on one line
    IMPORT_REGEX = '(from ([a-z\._]+) import [a-z]+)'
    IGNORE_IMPORTS = ['browser', 'console', 'document', 'window'] # Brython/JS interop
    
    VALID_COMMAND_LINE_ARGUMENTS = { "embed code": '--embed-code' }
        
    def watch(self):

        data = self.validate_args(sys.argv[1:])
        watch_path = data["watch path"]
        cmdline_arguments = data["command-line arguments"]
        
        main_file = "{0}/{1}".format(watch_path, AppBuilder.DEFAULT_MAIN_FILE)
        output_directory = "{0}/{1}".format(watch_path, AppBuilder.OUTPUT_DIRECTORY)
        
        io.directory.ensure_exists(output_directory)
        
        # Copy backend template. Index.html gets overridden, so it's not excluded.
        relative_template_directory = "{0}/{1}".format(AppBuilder.TEMPLATE_DIRECTORY, AppBuilder.JABAL_BACKEND)
        io.directory.copy_directory_tree(relative_template_directory, output_directory, AppBuilder.OUTPUT_DIRECTORY)
        
        source_relative_directory = "{0}/".format(os.path.realpath(watch_path))
        output_relative_directory = "{0}/".format(os.path.realpath(output_directory))
        
        while True:
            # hash of filename => File instance
            source_files = io.directory.traverse_for_mtime(watch_path, {}, 'bin', source_relative_directory)
            destination_files = io.directory.traverse_for_mtime(output_directory, {}, None, output_relative_directory)
            added_files = [f for f in source_files if not f in destination_files]
            changed_files = [f for f in source_files if destination_files.has_key(f) and source_files[f].mtime != destination_files[f].mtime]
            
            print("CHANGED: {0}".format(changed_files))
            sys.exit(0)
            
            if len(added_files) > 0:
                print "ADDED: {0}".format(added_files)
                
                print("{0} changed at {1}. Rebuilding.".format(main_file, datetime.datetime.now()))
                
                with open("{0}/{1}/{2}".format(AppBuilder.TEMPLATE_DIRECTORY, AppBuilder.JABAL_BACKEND, AppBuilder.MAIN_HTML_FILE)) as template_file:
                    original = template_file.read()
                    
                if AppBuilder.VALID_COMMAND_LINE_ARGUMENTS["embed code"] in cmdline_arguments:
                    with open(main_file) as source_file:
                       main_code = source_file.read()
                       
                    jabal_module_file = "{0}/{1}".format(relative_template_directory, AppBuilder.JABAL_MAIN_PY)
                    with open(jabal_module_file) as jabal_module:
                       jabal_code = jabal_module.read()
                       main_code = "{0}\r\n\r\n\r\n{1}".format(jabal_code, main_code)
                       
                    main_code = self.inline_imports(watch_path, main_code)         
                else:
                    main_code = original.replace(AppBuilder.CONTENT_PLACEHOLDER, AppBuilder.JABAL_MAIN_CODE)
                
                with open("{0}/{1}".format(output_directory, AppBuilder.MAIN_HTML_FILE), 'w+') as out_file:
                    substituted = original.replace(AppBuilder.CONTENT_PLACEHOLDER, main_code)
                    out_file.write(substituted)

            print "src={0} dest={1}".format(len(source_files), len(destination_files))

            sys.exit(0)
            time.sleep(0.5)
                
    def validate_args(self, args):
        if len(args) == 0:
            raise(Exception("Usage: python watch.py /path/to/yourgame"))
        else:
            watch_path = args[0]
                    
        cmdline_args = args[1:]
        for argument in cmdline_args:
            if not argument in AppBuilder.VALID_COMMAND_LINE_ARGUMENTS.values():
                raise(Exception("Invalid command-line argument: {0}".format(argument)))
        
        main_file = "{0}/{1}".format(args[0], AppBuilder.DEFAULT_MAIN_FILE)
        if not os.path.exists(main_file):
            raise(Exception("Can't find {0}".format(main_file)))
            
        return { "watch path": watch_path, "command-line arguments": cmdline_args }
                
    def inline_imports(self, watch_path, python_code):
        # Replace "from a.b import C" with the contents of a/b.py
        # With our current regex, a.b is not guaranteed to be valid
        # TODO: make this recursive
        
        regex = re.compile(AppBuilder.IMPORT_REGEX, re.IGNORECASE)
        matches = regex.findall(python_code) # matching strings
        
        for match in matches:
            import_statement = match[0]
            module_name = match[1]
            
            path_name = "{0}/{1}".format(watch_path, module_name.replace('.', '/'))
            path_name += ".py" 
            
            if module_name in AppBuilder.IGNORE_IMPORTS:
                continue
            
            if not os.path.exists(path_name):
                print("WARNING: imported {0} but {1} doesn't exist".format(module_name, path_name))
            else:
                with open(path_name) as imported_file:
                    imported_code = imported_file.read()
            
                python_code = python_code.replace(import_statement, imported_code)
            
        return python_code