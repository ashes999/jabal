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
    IMPORT_REGEX = r'(from ([a-z\._]+) import [a-z]+)'
    CLASS_REGEX = r'^class'
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
        
        class_regex = re.compile(AppBuilder.CLASS_REGEX, re.IGNORECASE)
        
        print("Monitoring {0} to build to {1}".format(os.path.realpath(watch_path), output_directory))
        
        while True:
            # hash of relative filename => File instance
            source_files = io.directory.traverse_for_mtime(watch_path, {}, 'bin', source_relative_directory)
            destination_files = io.directory.traverse_for_mtime(output_directory, {}, None, output_relative_directory)
            template_files = io.directory.traverse_for_mtime(relative_template_directory, {}, None, "{0}/".format(os.path.realpath(relative_template_directory)))
            
            # Collections of File instances
            added_files = [source_files[f] for f in source_files if not f in destination_files]
            changed_files = [source_files[f] for f in source_files if destination_files.has_key(f) and source_files[f].mtime != destination_files[f].mtime]
            deleted_files = [destination_files[f] for f in destination_files if not f in source_files and not f in template_files]
            
            with open("{0}/{1}/{2}".format(AppBuilder.TEMPLATE_DIRECTORY, AppBuilder.JABAL_BACKEND, AppBuilder.MAIN_HTML_FILE)) as template_file:
                original = template_file.read()
        
            rebuild = False
                
            if len(added_files) > 0:
                rebuild = True
                for file in added_files:
                    io.directory.safe_copy(file, source_relative_directory, output_directory, "new")

            if len(changed_files) > 0:
                rebuild = True            
                for file in changed_files:
                    io.directory.safe_copy(file, source_relative_directory, output_directory, "changed")
                    
            if len(deleted_files) > 0:
                rebuild = True            
                for file in deleted_files:
                    os.remove(file.full_path)
                    print("Deleted bin-only file {0}".format(file.relative_path(output_relative_directory)))                    
                
            if AppBuilder.VALID_COMMAND_LINE_ARGUMENTS["embed code"] in cmdline_arguments and rebuild == True:
                # We may have copied over python files that are not modules. These
                # shouldn't be copied over. Nuke them if that's the case.
                for file in added_files.values():
                    if file.filename.endswith('.py'):
                        with open(file) as python_file:
                            contents = python_file.read()
                        if class_regex.match(contents):
                            # It's not a module. Nuke it!
                            os.remove(file.fullpath)
                            print("Deleted {0} because it was copied over but isn't a module".format(file.filename))                                                      
                
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