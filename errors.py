class ReplacementError(Exception):
    def __init__(self, file_path):
        self.file_path = file_path
