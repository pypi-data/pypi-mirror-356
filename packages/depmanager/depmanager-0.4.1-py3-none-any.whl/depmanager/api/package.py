"""
Manager for package.
"""

from pathlib import Path
from sys import stderr


class PackageManager:
    """
    Manager fo package.
    """

    def __init__(self, system=None, verbosity: int = 0, fast: bool = False):
        from depmanager.api.internal.system import LocalSystem
        from depmanager.api.local import LocalManager

        self.verbosity = verbosity
        if type(system) is LocalSystem:
            self.__sys = system
        elif type(system) is LocalManager:
            self.__sys = system.get_sys()
        else:
            self.__sys = LocalSystem(verbosity=verbosity)

    def query(self, query, remote_name: str = "", transitive: bool = False):
        """
        Do a query into database.
        :param query: Query's data.
        :param remote_name: Remote's name to search of empty for local.
        :param transitive: Starting from remote_name unroll the lis of source local -> remote
        :return: List of packages matching the query.
        """
        using_name = "local"
        if remote_name in self.__sys.remote_database:
            using_name = remote_name
        elif remote_name == "default":
            using_name = self.__sys.default_remote

        if transitive:
            slist = self.__sys.get_source_list()
        else:
            slist = [using_name]
        started = False
        db = []
        for s in slist:
            if s == using_name:
                started = True
            if not started:
                continue
            if s == "local":
                ldb = self.__sys.local_database.query(query)
            else:
                ldb = self.__sys.remote_database[s].query(query)
            for dep in ldb:
                dep.source = s
            db += ldb
        return db

    def get_default_remote(self):
        """
        Get the default remote name
        :return:
        """
        return self.__sys.default_remote

    def remote_name(self, args):
        """
        Get remote name based of arguments.
        :param args: Arguments.
        :return: Remote name.
        """
        if args.default:
            return self.__sys.default_remote
        if args.name in self.__sys.remote_database:
            return args.name
        return ""

    def add_from_location(self, source: Path):
        """
        Add a package to the local database
        :param source: Path to the package source
        :return:
        """
        if not source.exists():
            print(f"WARNING: Location {source} does not exists.", file=stderr)
            return
        if source.is_dir():
            if not (source / "edp.info").exists():
                print(
                    f"WARNING: Location {source} does not contains edp.info file.",
                    file=stderr,
                )
                return
            self.__sys.import_folder(source)
            return
        elif source.is_file():
            suffixes = []
            if len(source.suffixes) > 0:
                suffixes = [source.suffixes[-1]]
                if suffixes == [".gz"] and len(source.suffixes) > 1:
                    suffixes = [source.suffixes[-2], source.suffixes[-1]]
            if suffixes == ["zip"]:
                from zipfile import ZipFile

                destination_dir = self.__sys.temp_path / "pack"
                destination_dir.mkdir(parents=True)
                if self.verbosity > 2:
                    print(
                        f"PackageManager::add_from_location - Extract ZIP from {source} to {destination_dir}"
                    )
                with ZipFile(source) as archive:
                    archive.extractall(destination_dir)
            elif suffixes in [[".tgz"], [".tar", ".gz"]]:
                import tarfile

                destination_dir = self.__sys.temp_path / "pack"
                destination_dir.mkdir(parents=True)
                if self.verbosity > 2:
                    print(
                        f"PackageManager::add_from_location - Extract TGZ from {source} to {destination_dir}"
                    )
                with tarfile.open(str(source), "r|gz") as archive:
                    archive.extractall(destination_dir)
            else:
                print(f"WARNING: File {source} has unsupported format.", file=stderr)
                return
            if destination_dir is not None:
                if not (destination_dir / "edp.info").exists():
                    print(
                        f"WARNING: Archive does not contains package info.", file=stderr
                    )
                    return
                self.__sys.import_folder(destination_dir)

    def remove_package(self, pack, remote_name: str = ""):
        """
        Suppress package in local database.
        :param pack: The package to remove.
        :param remote_name: The remote server to use.
        """
        if remote_name == "":
            self.__sys.remove_local(pack)
            return
        if remote_name == "default":
            remote_name = self.__sys.default_remote
        if remote_name not in self.__sys.remote_database:
            print(f"ERROR: no remote named {remote_name} found.", file=stderr)
            return
        remote = self.__sys.remote_database[remote_name]
        remote.delete(pack)

    def add_from_remote(self, dep, remote_name):
        """
        Get a package from remote to local.
        :param dep: The dependency to get.
        :param remote_name: The remote server to use.
        """
        if remote_name == "default":
            remote_name = self.__sys.default_remote
        if remote_name not in self.__sys.remote_database:
            print(f"ERROR: no remote named {remote_name} found.", file=stderr)
            return
        remote = self.__sys.remote_database[remote_name]
        finds = remote.query(dep)
        if len(finds) > 1:
            print("WARNING: more than 1 package matches the request:", file=stderr)
            for find in finds:
                print(f"         {find.properties.get_as_str()}")
            print(
                "         Precise your request, only one package per pull allowed.",
                file=stderr,
            )
            return
        if len(finds) == 0:
            print("ERROR: no package matches the request.", file=stderr)
            return
        res = remote.pull(finds[0], self.__sys.temp_path)
        if res is None:
            file = self.__sys.temp_path / f"{finds[0].properties.hash()}.tgz"
        else:
            file = self.__sys.temp_path / f"{res}"
        self.add_from_location(file)

    def add_to_remote(self, dep, remote_name):
        """
        Get a package from local to remote.
        :param dep: The dependency to send.
        :param remote_name: The remote server to use.
        """
        if remote_name == "default":
            remote_name = self.__sys.default_remote
        if remote_name not in self.__sys.remote_database:
            print(f"ERROR: no remote named {remote_name} found.", file=stderr)
            return
        if self.verbosity > 1:
            print(f"Using remote named {remote_name}.")
        remote = self.__sys.remote_database[remote_name]
        finds = self.__sys.local_database.query(dep)
        if len(finds) > 1:
            if self.verbosity == 1:
                print("\n")
            print("WARNING: more than 1 package matches the request:", file=stderr)
            for find in finds:
                print(f"         {find.properties.get_as_str()}")
            print(
                "         Precise your request, only one package per push allowed.",
                file=stderr,
            )
            return
        if len(finds) == 0:
            print("ERROR: no package matches the request.", file=stderr)
            return

        dep_path = self.__sys.temp_path / (Path(dep.get_path()).name + ".tgz")
        if self.verbosity > 1:
            print(f"Compressing library to file {dep_path}.")
        self.__sys.local_database.pack(finds[0], self.__sys.temp_path, "tgz")
        if self.verbosity > 1:
            print(f"Starting upload.")
        remote.push(finds[0], dep_path)
