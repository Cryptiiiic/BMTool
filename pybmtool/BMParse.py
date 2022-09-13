import http.client
import os
import io
import plistlib
import urllib.request
import remotezip
from pybmtool.utils import fileIO


class BMParse:
    def __init__(self, buildManifestPath: str = "", url: str = "", outDir: str = ""):
        self.buildManifestPath = buildManifestPath
        self.url = url
        self.outDir = f"{os.getcwd()}"
        self.remoteZip = ""
        self.manifest = {}
        if outDir and len(outDir) > 0:
            self.outDir = outDir
        if not self.buildManifestPath or len(self.buildManifestPath) < 1:
            if not self.url or len(self.url) < 1:
                raise ValueError(
                    f"{self.__class__.__name__}: {self.__init__.__name__}: buildManifestPath and url "
                    f"are both empty, no data to use!"
                )
            else:
                self.remoteZip = remotezip.RemoteZip(url=self.url)
                if not self.remoteZip:
                    raise Exception
                self.buildManifestPath = f"{self.outDir}/BuildManifest.plist"
                if not self.downloadManifest():
                    raise ValueError(
                        f"{self.__class__.__name__}: {self.__init__.__name__}: failed to download "
                        f"manifest!"
                    )
        self.loadManifest()

    def downloadManifest(self) -> bool:
        if os.path.exists(self.buildManifestPath):
            os.remove(self.buildManifestPath)
        manifestURL = f"{self.url.rsplit('/', 1)[0]}/BuildManifest.plist"
        response = None
        try:
            response = urllib.request.urlopen(url=manifestURL)
        except:
            pass
        if response is not None:
            data = response.read(response.length)

            def openManifest(manifestFile):
                manifestFile.write(data)
                return True

            if not fileIO(
                path=self.buildManifestPath,
                binary=True,
                write=True,
                callback=openManifest,
            ):
                raise ValueError(
                    f"{self.__class__.__name__}: {self.downloadManifest.__name__}: failed to open manifest"
                    f" for writing"
                )
        if not response or response.status != 200:
            try:
                if (
                    len(
                        self.remoteZip.extract(
                            member="BuildManifest.plist", path=self.outDir
                        )
                    )
                    < 1
                ):
                    raise ValueError(
                        f"{self.__class__.__name__}: {self.downloadManifest.__name__}: failed to download "
                        f"BuildManifest!"
                    )
            except:
                pass
        return True

    def loadManifest(self) -> bool:
        def openManifest(manifestFile):
            manifestFile.seek(0, io.SEEK_SET)
            self.manifest = plistlib.load(manifestFile)
            if len(self.manifest) < 1:
                return False
            else:
                return True

        if not fileIO(
            path=self.buildManifestPath, binary=True, write=False, callback=openManifest
        ):
            raise ValueError(
                f"{self.__class__.__name__}: {self.loadManifest.__name__}: failed to open manifest "
                f"file!"
            )
        else:
            return True

    def getBoardIdentity(self, board: str, update: bool = False) -> dict:
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

    def getComponentPath(self, board: str, component: str, update: bool = False) -> str:
        identity = self.getBoardIdentity(board, update)
        if len(identity) < 1:
            raise ValueError(
                f"{self.__class__.__name__}: {self.getComponentPath.__name__}: failed to find matching"
                f" board identity!"
            )
        if identity.get("Manifest", None):
            if identity["Manifest"].get(component, None):
                if identity["Manifest"][component].get("Info", None):
                    if identity["Manifest"][component]["Info"].get("Path", None):
                        return identity["Manifest"][component]["Info"]["Path"]
        return ""

    def getComponentList(self, board, update: bool = False) -> list:
        identity = self.getBoardIdentity(board, update)
        if len(identity) < 1:
            raise ValueError(
                f"{self.__class__.__name__}: {self.getComponentList.__name__}: failed to find matching"
                f" board identity!"
            )
        if identity.get("Manifest", None):
            return list(identity["Manifest"].keys())

        return []
