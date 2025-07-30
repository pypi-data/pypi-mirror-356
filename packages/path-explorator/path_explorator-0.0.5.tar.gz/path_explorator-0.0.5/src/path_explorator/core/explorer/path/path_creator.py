from pathlib import Path


class PathCreator:
    def __init__(self):
        pass

    def join_paths(self, path1, path2):
        new_path = Path(Path(path1) / Path(path2))
        return new_path.__str__()
