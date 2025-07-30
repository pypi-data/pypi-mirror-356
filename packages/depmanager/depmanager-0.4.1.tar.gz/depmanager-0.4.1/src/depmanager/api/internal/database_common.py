"""
Database Object.
"""

from pathlib import Path
from sys import stderr

from depmanager.api.internal.dependency import Dependency, Props


class __DataBase:
    """
    Abstract class describing database.
    """

    def __init__(self, verbosity: int = 0):
        self.verbosity = verbosity
        self.valid_shape = True
        self.dependencies = []

    def deps_from_strings(self, strings: list, append: bool = False):
        """
        Define or append Deps from string list.
        :param strings: List of deps string.
        :param append: Append to current list or flush the list.
        """
        if not self.valid_shape:
            return
        if not append:
            self.dependencies = []
        for dep in strings:
            self.dependencies.append(Dependency(dep))

    def deps_to_strings(self):
        """
        Create the list of deps strings.
        :return: List of deps string.
        """
        if not self.valid_shape:
            return []
        return [dep.properties.get_as_str() for dep in self.dependencies]

    def query(self, data: any([str, dict, Dependency, Props]) = None):
        """
        Get a list of dependencies matching data.
        :param data: The query data.
        :return: List of Dependencies.
        """
        if not self.valid_shape:
            return []
        if data is None:
            props = Props({}, query=True)
        elif type(data) in [str, dict]:
            props = Props(data, query=True)
        elif type(data) is Dependency:
            props = data.properties
        elif type(data) is Props:
            props = data
        else:
            return []
        return sorted(
            [dep for dep in self.dependencies if dep.match(props)], reverse=True
        )


class __RemoteDatabase(__DataBase):
    """
    Abstract class describing database in a remote destination.
    """

    destination = ""

    def __init__(
        self,
        destination: any([str, Path]),
        default: bool = False,
        user: str = "",
        cred: str = "",
        kind: str = "invalid",
        verbosity: int = 0,
    ):
        super().__init__(verbosity)
        self.destination = destination
        self.default = default
        self.kind = kind
        self.user = user
        self.cred = cred
        self.initiated = False
        self.remote_type = "unknown"
        self.version = "0.0"

    def get_server_type(self):
        """
        Returns the server's type.
        :return: Server type.
        """
        return self.remote_type

    def get_dep_list(self):
        """
        Get a list of string describing dependency from the server.
        """
        if not self.valid_shape:
            return
        from tempfile import mkdtemp
        from shutil import rmtree

        temp_dir = Path(mkdtemp())
        self.get_file("deplist.txt", temp_dir)
        if not self.valid_shape:
            rmtree(temp_dir)
            return
        self.__read_dep_list(temp_dir / "deplist.txt")
        rmtree(temp_dir)

    def send_dep_list(self):
        """
        Push the list of dependencies to the server.
        """
        if not self.valid_shape:
            return
        from tempfile import mkdtemp
        from shutil import rmtree

        temp_dir = Path(mkdtemp())
        self.__write_dep_list(temp_dir / "deplist.txt")
        if not self.valid_shape:
            rmtree(temp_dir)
            return
        self.send_file(temp_dir / "deplist.txt", "deplist.txt")
        rmtree(temp_dir)

    def __read_dep_list(self, file: Path):
        self.dependencies = []
        if not file.exists():
            self.valid_shape = False
            return
        with open(file) as fp:
            lines = fp.readlines()
        self.deps_from_strings(lines)

    def __write_dep_list(self, file: Path):
        lines = self.deps_to_strings()
        file.parent.mkdir(parents=True, exist_ok=True)
        with open(file, "w") as fb:
            for line in lines:
                fb.write(f"{line}\n")

    def __initialize(self):
        self.connect()
        self.get_dep_list()
        self.initiated = True

    def push(self, dep: Dependency, file: Path, force: bool = False):
        """
        Push a dependency to the remote.
        :param dep: Dependency's description.
        :param file: Dependency archive file.
        :param force: If true re-upload a file that already exists.
        """
        if not self.valid_shape:
            return
        if not file.exists():
            return
        result = self.query(dep)
        if len(result) != 0 and not force:
            print(
                f"WARNING: Cannot push dependency {dep.properties.name}: already on server.",
                file=stderr,
            )
            return
        destination = f"{dep.properties.name}/{dep.properties.hash()}.tgz"
        self.send_file(file, destination)
        if not self.valid_shape:
            return
        self.dependencies.append(dep)
        self.send_dep_list()

    def pull(self, dep: Dependency, destination: Path):
        """
        Pull a dependency from remote.
        :param dep: Dependency information.
        :param destination: Destination directory
        """
        if destination.exists() and not destination.is_dir():
            return
        deps = self.query(dep)
        if len(deps) != 1:
            return
        dep = deps[0]
        file = f"{dep.properties.name}/{dep.properties.hash()}.tgz"
        self.get_file(file, destination)

    def delete(self, dep: Dependency):
        """
        Suppress the dependency from the server
        :param dep: Dependency information.
        :return: True if success.
        """
        if not self.valid_shape:
            return
        result = self.query(dep)
        if len(result) == 0:
            print(
                f"WARNING: Cannot suppress dependency {dep.properties.name}: not on server.",
                file=stderr,
            )
            return
        if len(result) > 1:
            print(
                f"WARNING: Cannot suppress dependency {dep.properties.name}: multiple dependencies match on server.",
                file=stderr,
            )
            return
        self.suppress(dep)
        self.dependencies.remove(dep)
        self.send_dep_list()

    def query(self, data: any([str, dict, Dependency, Props]) = None):
        """
        Get a list of dependencies matching data.
        :param data: The query data.
        :return: List of Dependencies.
        """
        if not self.initiated:
            self.__initialize()
        return super().query(data)

    def connect(self):
        """
        Initialize the connection to remote host.
        TO IMPLEMENT IN DERIVED CLASS.
        """
        self.valid_shape = False
        print("WARNING: __RemoteDatabase::__connect() not implemented.", file=stderr)

    def get_file(self, distant_name: str, destination: Path):
        """
        Download a file.
        TO IMPLEMENT IN DERIVED CLASS.
        :param distant_name: Name in the distant location.
        :param destination: Destination path.
        """
        self.valid_shape = False
        print(
            f"WARNING: __RemoteDatabase::get_file({distant_name},{destination}) not implemented.",
            file=stderr,
        )

    def send_file(self, source: Path, distant_name: str):
        """
        Upload a file.
        TO IMPLEMENT IN DERIVED CLASS.
        :param source: File to upload.
        :param distant_name: Name in the distant location.
        """
        self.valid_shape = False
        print(
            f"WARNING: __RemoteDatabase::send_file({source}, {distant_name}) not implemented.",
            file=stderr,
        )

    def get_server_version(self):
        """
        Returns the server's version
        :return: Server version.
        """
        self.valid_shape = False
        print(
            f"WARNING: __RemoteDatabase::get_server_version() not implemented.",
            file=stderr,
        )

    def suppress(self, dep: Dependency) -> bool:
        """
        Suppress the dependency from the server
        TO IMPLEMENT IN DERIVED CLASS.
        :param dep: Dependency information.
        :return: True if success.
        """
        self.valid_shape = False
        print(f"WARNING: __RemoteDatabase::delete({dep}) not implemented.", file=stderr)
        return False

    def get_remote_info(self) -> dict:
        """
        Get information about the remote.
        :return: Dictionary with remote information.
        """
        return {
            "destination": str(self.destination),
            "default": self.default,
            "user": self.user,
            "kind": self.kind,
            "remote_type": self.remote_type,
            "version": self.version,
        }
