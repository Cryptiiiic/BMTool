import os
import remotezip

from pybmtool.BMParse import BMParse


class BMTool:
    def __init__(self, bm: BMParse, outDir: str = ""):
        self.bm = bm
        self.outDir = f"{os.getcwd()}"
        if outDir and len(outDir) > 0:
            self.outDir = outDir
        if not self.bm.buildManifestPath or len(self.bm.buildManifestPath) < 1:
            if not self.bm.url or len(self.bm.url) < 1:
                raise ValueError(
                    f"{self.__class__.__name__}: {self.__init__.__name__}: buildManifestPath and url "
                    f"are both empty, no data to use!"
                )
        self.remoteZip = remotezip.RemoteZip(url=self.bm.url)

    def downloadComponent(
        self, board: str, component: str, update: bool = False
    ) -> str:
        if not component or len(component) < 1:
            raise ValueError(
                f"{self.__class__.__name__}: {self.downloadComponent.__name__}: no component name "
                f"provided!"
            )
        path = self.bm.getComponentPath(board=board, component=component, update=update)
        if not path or len(path) < 1:
            raise ValueError(
                f"{self.__class__.__name__}: {self.downloadComponent.__name__}: failed to get "
                f"component path for {component}!"
            )
        result = self.remoteZip.extract(member=path, path=self.outDir)
        if not result or len(result) < 1:
            raise ValueError(
                f"{self.__class__.__name__}: {self.downloadComponent.__name__}: failed to download "
                f"component {component}!"
            )
        return result

    def downloadComponents(
        self,
        board: str,
        componentList: list,
        update: bool = False,
        ignoreFailure: bool = False,
    ) -> list:
        if not componentList or len(componentList) < 1:
            raise ValueError(
                f"{self.__class__.__name__}: {self.downloadComponent.__name__}: no component names "
                f"provided!"
            )
        resultList = []
        for component in componentList:
            result = self.downloadComponent(
                board=board, component=component, update=update
            )
            if not result or len(result) < 1:
                if ignoreFailure:
                    print(
                        f"{self.__class__.__name__}: {self.downloadComponent.__name__}: failed to get "
                        f"component path for {component}!"
                    )
                else:
                    raise ValueError(
                        f"{self.__class__.__name__}: {self.downloadComponent.__name__}: failed to get "
                        f"component path for {component}!"
                    )
            if not result or len(result) < 1:
                if ignoreFailure:
                    print(
                        f"{self.__class__.__name__}: {self.downloadComponent.__name__}: failed to download "
                        f"component {component}!"
                    )
                else:
                    raise ValueError(
                        f"{self.__class__.__name__}: {self.downloadComponent.__name__}: failed to download "
                        f"component {component}!"
                    )
            resultList.append(result)
        return resultList
