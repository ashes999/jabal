import os, shutil

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
            
def recreate_directory(directory):
    for entry in os.listdir(directory):
        entry_src = os.path.join(directory, entry)
        if os.path.isdir(entry_src):
            shutil.rmtree(entry_src)
        else:
            os.remove(entry_src)    