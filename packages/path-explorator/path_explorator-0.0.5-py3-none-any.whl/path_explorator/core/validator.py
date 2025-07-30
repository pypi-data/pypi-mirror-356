from pathlib import Path


class PathValidator:

    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)

    def does_contain_uplinks(self, path:str | Path):
        path = Path(path)
        if ('..', '.', './') in path.parts:
            return True
        return False

    def does_contain_symlinks_and_uplinks(self, path:str):
        path = Path(path)
        if path.is_symlink() and self.does_contain_uplinks(path):
            return True
        return False


    def is_goes_beyond_limits(self, requesting_path: str):
        if not isinstance(requesting_path, str):
            raise TypeError(f'requesting path arg must be str, not {type(requesting_path)}')
        requesting_path = Path(requesting_path).resolve()
        if not requesting_path.is_relative_to(self.root_dir):
            return True
        return False

    @property
    def root(self):
        return self.root_dir.__str__()

    def is_exists(self, path: str) -> bool:
        """
        Checks if specified path exists
        :param path: path to the entity checking
        :return: exists or not True or False
        """
        if not isinstance(path, str):
            raise TypeError(f'path arg must be str, not {type(path)}')
        entity = Path(self.root_dir, path)
        return entity.exists()


    def is_file(self, path: str) -> bool:
        """
        Checks if specified entity is FILE
        :param path: path to entity
        :return: file or not
        """
        if not isinstance(path, str):
            raise TypeError(f'path arg must be str, not {type(path)}')
        entity = Path(self.root_dir, path)
        return entity.is_file()


    def is_dir(self, path: str) -> bool:
        """
        Checks if specified entity is DIRECTORY/FOLDER
        :param path: path to entity
        :return: dir or not
        """
        if not isinstance(path, str):
            raise TypeError(f'path arg must be str, not {type(path)}')
        entity = Path(self.root_dir, path)
        return entity.is_dir()
