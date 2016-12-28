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
            if not directory_to_skip == None and (entry == directory_to_skip or entry.endswith("{0}{1}".format(os.path.sep, directory_to_skip))):
                continue
            seen_already = traverse_for_mtime(entry_src, seen_already, directory_to_skip, relative_directory)
        else:
            f = File(entry, entry_src, os.stat(entry_src).st_mtime)
            if relative_directory == None:
                seen_already[entry] = f
            else:
                relative_path = f.relative_path(relative_directory)
                seen_already[relative_path] = f

    return seen_already

# Deletes the contents of a directory (recursively), but leaves the directory itself
def recreate_directory(directory):
    for entry in os.listdir(directory):
        entry_src = os.path.join(directory, entry)
        if os.path.isdir(entry_src):
            shutil.rmtree(entry_src)
        else:
            os.remove(entry_src)

# http://stackoverflow.com/a/18503387/210780
def ensure_exists(path):
    sub_path = os.path.dirname(path)
    if not os.path.exists(sub_path):
        ensure_exists(sub_path)
    if not os.path.exists(path):
        os.mkdir(path)

# Copies file in relative_directory to output_directory.
# Preserves modification time and other metadata
def safe_copy(file, relative_directory, output_directory, message_string = ""):
    source = file.relative_path(relative_directory)
    # Destination, relative eg. copy /game/assets/images/player.png to /game/bin/assets.images/player.png
    # Also handles creating said directory structure if it doesn't exist
    destination = "{0}{1}{2}".format(output_directory, os.path.sep, file.relative_path(relative_directory))
    end_index = destination.rindex(os.path.sep)
    path  = destination[0:end_index]
    ensure_exists(path)
    # copy2: preserve modification time
    shutil.copy2(file.full_path, destination)
    print("Copied {2} file from {0} to {1}".format(source, destination, message_string))
