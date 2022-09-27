import os
import remotezip

from pybmtool import BMParse


class BMTool:
    def __init__(self, bm: BMParse, outdir: str = ""):
        self.bm = bm
        self.outdir = f"{os.getcwd()}"
        if outdir and len(outdir) > 0:
            self.outdir = outdir
        if not self.bm.build_manifest_path or len(self.bm.build_manifest_path) < 1:
            if not self.bm.url or len(self.bm.url) < 1:
                raise ValueError(
                    f"{self.__class__.__name__}: {self.__init__.__name__}: buildManifestPath and url "
                    f"are both empty, no data to use!"
                )
        self.remote_zip = remotezip.RemoteZip(url=self.bm.url)

    def download_component(
        self, board: str, component: str, update: bool = False
    ) -> str:
        if not component or len(component) < 1:
            raise ValueError(
                f"{self.__class__.__name__}: {self.download_component.__name__}: no component name "
                f"provided!"
            )
        path = self.bm.get_component_path(
            board=board, component=component, update=update
        )
        if not path or len(path) < 1:
            raise ValueError(
                f"{self.__class__.__name__}: {self.download_component.__name__}: failed to get "
                f"component path for {component}!"
            )
        result = self.remote_zip.extract(member=path, path=self.outdir)
        if not result or len(result) < 1:
            raise ValueError(
                f"{self.__class__.__name__}: {self.download_component.__name__}: failed to download "
                f"component {component}!"
            )
        return result

    def download_components(
        self,
        board: str,
        component_list: list,
        update: bool = False,
        ignore_failure: bool = False,
    ) -> list:
        if not component_list or len(component_list) < 1:
            raise ValueError(
                f"{self.__class__.__name__}: {self.download_component.__name__}: no component names "
                f"provided!"
            )
        resultList = []
        for component in component_list:
            result = self.download_component(
                board=board, component=component, update=update
            )
            if not result or len(result) < 1:
                if ignore_failure:
                    print(
                        f"{self.__class__.__name__}: {self.download_component.__name__}: failed to get "
                        f"component path for {component}!"
                    )
                else:
                    raise ValueError(
                        f"{self.__class__.__name__}: {self.download_component.__name__}: failed to get "
                        f"component path for {component}!"
                    )
            if not result or len(result) < 1:
                if ignore_failure:
                    print(
                        f"{self.__class__.__name__}: {self.download_component.__name__}: failed to download "
                        f"component {component}!"
                    )
                else:
                    raise ValueError(
                        f"{self.__class__.__name__}: {self.download_component.__name__}: failed to download "
                        f"component {component}!"
                    )
            resultList.append(result)
        return resultList
