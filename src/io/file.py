class File:
    def __init__(self, filename, full_path, mtime):
        self.filename = filename;
        self.full_path = full_path
        self.mtime = mtime
        
    @property
    def filename(self):
        return self.filename;
        
    @property
    def full_path(self):
        return self.full_path
        
    @property
    def mtime(self):
        return self.mtime
        
    def relative_path(self, root_dir):
        return self.full_path.replace(root_dir, "")
        
    def __repr__(self):
        return "File: {0}".format(self.full_path)