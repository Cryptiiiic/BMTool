import os
import io
import plistlib
import urllib.request
import remotezip
from pybmtool import file_io


class BMParse:
    def __init__(self, build_manifest_path: str = "", url: str = "", outdir: str = ""):
        self.build_manifest_path = build_manifest_path
        self.url = url
        self.outdir = f"{os.getcwd()}"
        self.remote_zip = ""
        self.manifest = {}
        if outdir and len(outdir) > 0:
            self.outdir = outdir
        if not self.build_manifest_path or len(self.build_manifest_path) < 1:
            if not self.url or len(self.url) < 1:
                raise ValueError(
                    f"{self.__class__.__name__}: {self.__init__.__name__}:"
                    " buildManifestPath and url are both empty, no data to use!"
                )
            else:
                self.remote_zip = remotezip.RemoteZip(url=self.url)
                if not self.remote_zip:
                    raise Exception
                self.build_manifest_path = f"{self.outdir}/BuildManifest.plist"
                if not self.download_manifest():
                    raise ValueError(
                        f"{self.__class__.__name__}: {self.__init__.__name__}: failed"
                        " to download manifest!"
                    )
        self.load_manifest()

    def download_manifest(self) -> bool:
        if os.path.exists(self.build_manifest_path):
            os.remove(self.build_manifest_path)
        manifest_url = f"{self.url.rsplit('/', 1)[0]}/BuildManifest.plist"
        response = None
        try:
            response = urllib.request.urlopen(url=manifest_url)
        except:
            pass
        if response is not None:
            data = response.read(response.length)

            def openManifest(manifestFile):
                manifestFile.write(data)
                return True

            if not file_io(
                path=self.build_manifest_path,
                binary=True,
                write=True,
                callback=openManifest,
            ):
                raise ValueError(
                    f"{self.__class__.__name__}: {self.download_manifest.__name__}:"
                    " failed to open manifest for writing"
                )
        if not response or response.status != 200:
            try:
                if (
                    len(
                        self.remote_zip.extract(
                            member="BuildManifest.plist", path=self.outdir
                        )
                    )
                    < 1
                ):
                    raise ValueError(
                        f"{self.__class__.__name__}: {self.download_manifest.__name__}:"
                        " failed to download BuildManifest!"
                    )
            except:
                pass
        return True

    def load_manifest(self) -> bool:
        def open_manifest(manifest_file):
            manifest_file.seek(0, io.SEEK_SET)
            self.manifest = plistlib.load(manifest_file)
            if len(self.manifest) < 1:
                return False
            else:
                return True

        if not file_io(
            path=self.build_manifest_path,
            binary=True,
            write=False,
            callback=open_manifest,
        ):
            raise ValueError(
                f"{self.__class__.__name__}: {self.load_manifest.__name__}: failed to"
                " open manifest file!"
            )
        else:
            return True

    def get_board_identity(self, board: str, update: bool = False) -> dict:
        if self.manifest.get("BuildIdentities", None):
            for identity in self.manifest["BuildIdentities"]:
                if identity.get("Info", None):
                    if identity["Info"].get("DeviceClass", None):
                        if identity["Info"]["DeviceClass"].__eq__(board):
                            if identity["Info"].get("RestoreBehavior", None):
                                if update:
                                    if identity["Info"]["RestoreBehavior"].__eq__(
                                        "Update"
                                    ):
                                        return identity
                                else:
                                    if identity["Info"]["RestoreBehavior"].__eq__(
                                        "Erase"
                                    ):
                                        return identity
            return {}
        else:
            return {}

    def get_component_path(
        self, board: str, component: str, update: bool = False
    ) -> str:
        identity = self.get_board_identity(board, update)
        if len(identity) < 1:
            raise ValueError(
                f"{self.__class__.__name__}: {self.get_component_path.__name__}: failed"
                " to find matching board identity!"
            )
        if identity.get("Manifest", None):
            if identity["Manifest"].get(component, None):
                if identity["Manifest"][component].get("Info", None):
                    if identity["Manifest"][component]["Info"].get("Path", None):
                        return identity["Manifest"][component]["Info"]["Path"]
        return ""

    def get_component_list(self, board, update: bool = False) -> list:
        identity = self.get_board_identity(board, update)
        if len(identity) < 1:
            raise ValueError(
                f"{self.__class__.__name__}: {self.get_component_list.__name__}: failed"
                " to find matching board identity!"
            )
        if identity.get("Manifest", None):
            return list(identity["Manifest"].keys())

        return []
