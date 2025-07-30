"""
Local instance of manager.
"""

from pathlib import Path


class LocalManager:
    """
    Local manager.
    """

    version = "0.4.1"

    def __init__(self, system=None, verbosity: int = 0):
        from depmanager.api.internal.system import LocalSystem

        self.verbosity = verbosity
        if type(system) is LocalSystem:
            self.__sys = system
        else:
            self.__sys = LocalSystem(verbosity=verbosity)
        self.root_path = Path(__file__).resolve().parent.parent

    def get_sys(self):
        """
        Access to internal system.
        :return: Internal system.
        """
        return self.__sys

    def get_base_path(self):
        """
        Get the base folder of local data.
        :return: The base path.
        """
        return self.__sys.base_path

    def get_cmake_dir(self):
        """
        Get the path to cmake additional functions.
        :return: Path to cmake functions.
        """
        return self.root_path / "cmake"

    def get_version(self):
        """
        Version of the package manager.
        :return: Version.
        """
        return self.version

    def clean_tmp(self):
        """
        Clean the Temp Folder.
        """
        self.__sys.clear_tmp()
        self.__sys.release()
