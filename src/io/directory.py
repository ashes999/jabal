import os, shutil
from file import File

# Copies all the files and folders in "directory" to "destination"
# ignore_if_lambda(file_name) returns True if the file should be ignored
def copy_directory_tree(directory, destination, directory_to_skip = None, exclude_if_lambda = None):
    for entry in os.listdir(directory):
        if not directory_to_skip == None and entry == directory_to_skip:
            continue
        if entry.startswith('.'):
            continue
        if exclude_if_lambda == None or exclude_if_lambda(entry) == False: 
            entry_src = os.path.join(directory, entry)
            if os.path.isdir(entry_src):
                entrydest = os.path.join(destination, entry)
                shutil.copytree(entry_src, entrydest)
            else:
                shutil.copy(os.path.realpath(entry_src), destination)

# Returns a hash of filename => file(filename, relative path, mtime)
def traverse_for_mtime(directory, seen_already, directory_to_skip = None, relative_directory = None):
    directory = os.path.realpath(directory)
    
    for entry in os.listdir(directory):
        
        if entry.startswith('.'):
            continue
            
        entry_src = os.path.join(directory, entry)                
        if os.path.isdir(entry_src):
            if not directory_to_skip == None and (entry == directory_to_skip or entry.endswith("/{0}".format(directory_to_skip))):
                continue
            seen_already = traverse_for_mtime(entry_src, seen_already, directory_to_skip, relative_directory)
        else:
            f = File(entry, entry_src, os.path.getmtime(entry_src))
            if relative_directory == None:
                seen_already[entry] = f
                raise(Exception("!"))
            else:
                relative_path = f.relative_path(relative_directory)
                print "{0} for {1}".format(relative_path, relative_directory)
                seen_already[relative_path] = f
            
    return seen_already

def ensure_exists(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)

# Deletes the contents of a directory (recursively), but leaves the directory itself            
def recreate_directory(directory):
    for entry in os.listdir(directory):
        entry_src = os.path.join(directory, entry)
        if os.path.isdir(entry_src):
            shutil.rmtree(entry_src)
        else:
            os.remove(entry_src)    