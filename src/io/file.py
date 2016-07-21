import datetime

class File:
    def __init__(self, filename, full_path, mtime):
        self.filename = filename;
        self.full_path = full_path
        # To prevent incorrectly re-copying when times vary by fractional seconds,
        # since rounding time is not easy, just use a conveniently-precise string
        # representation of the date/time. We use yyyy-MM-dd hh:MM:ss.tttt
        # %f gives us tttttt (which is too precise), so we truncate two digits.
        self.mtime = datetime.datetime.fromtimestamp(mtime)
        self.mtime = self.mtime.strftime('%Y-%m-%d %H:%M:%S.%f')[:-2]
        
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