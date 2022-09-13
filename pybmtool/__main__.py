import sys
import click
from pybmtool.BMParse import BMParse
from pybmtool.BMTool import BMTool


@click.group()
def cli() -> None:
    """A Python CLI tool for parsing Apple's BuildManifest file."""
    sys.tracebacklimit = 0


@cli.group()
def component() -> None:
    """BuildManifest component parsing commands"""
    pass


@component.command("list")
@click.option(
    "-m",
    "--manifest",
    "manifest_",
    type=str,
    help="Input BuildManifest path",
    required=False,
)
@click.option(
    "-u",
    "--url",
    "url_",
    type=str,
    help="Or input BuildManifest from ipsw url",
    required=False,
)
@click.option(
    "-b",
    "--board",
    "board_",
    type=str,
    help="Input device board config",
    required=True,
)
@click.option(
    "-v",
    "--variant",
    "variant_",
    type=int,
    help="Input restore variant",
    required=False,
)
def listComponents(
    board_: str, manifest_: str = "", url_: str = "", variant_: int = 0
) -> None:
    """List components for board and variant from BuildManifest."""
    if len(board_) < 1:
        raise click.BadParameter("No board specified")
    board_ = board_.lower()
    ap = f"{board_[-2]}{board_[-1]}"
    if not ap.__eq__("ap"):
        raise click.BadParameter("Invalid board config")
    if not manifest_ or len(manifest_) < 1:
        if not url_ or len(url_) < 1:
            raise click.BadParameter("No ipsw url or BuildManifest provided")
    try:
        bm = BMParse(buildManifestPath=manifest_, url=url_)
    except:
        if url_ and len(url_) > 0:
            raise click.BadParameter(f"Failed to initialize BuildManifest: {url_}")
        else:
            raise click.BadParameter(f"Failed to initialize BuildManifest: {manifest_}")
    variant = "Erase"
    if variant_ > 0:
        variant = "Update"
    if url_:
        print(f"Getting list of components for {board_}, {variant} from {bm.url}")
    else:
        print(
            f"Getting list of components for {board_}, {variant} from {bm.buildManifestPath}"
        )
    componentList = bm.getComponentList(board=board_, update=bool(variant_))
    for comp in componentList[:-1]:
        print(f"{comp}")
    print(f"{componentList[-1]}", end="")


@component.command("path")
@click.option(
    "-m",
    "--manifest",
    "manifest_",
    type=str,
    help="Input BuildManifest path",
    required=False,
)
@click.option(
    "-u",
    "--url",
    "url_",
    type=str,
    help="Or input BuildManifest from ipsw url",
    required=False,
)
@click.option(
    "-b",
    "--board",
    "board_",
    type=str,
    help="Input device board config",
    required=True,
)
@click.option(
    "-v",
    "--variant",
    "variant_",
    type=int,
    help="Input restore variant",
    required=False,
)
@click.option(
    "-c",
    "--component",
    "component_",
    type=str,
    help="Input component name",
    required=True,
)
def listComponent(
    board_: str, component_: str, manifest_: str = "", url_: str = "", variant_: int = 0
) -> None:
    """Get path in ipsw for specified component for board and variant from BuildManifest."""
    if not board_ or len(board_) < 1:
        raise click.BadParameter("No board specified")
    if not component_ or len(component_) < 1:
        raise click.BadParameter("No component specified")
    board_ = board_.lower()
    ap = f"{board_[-2]}{board_[-1]}"
    if not ap.__eq__("ap"):
        raise click.BadParameter("Invalid board config")
    if not manifest_ or len(manifest_) < 1:
        if not url_ or len(url_) < 1:
            raise click.BadParameter("No ipsw url or BuildManifest provided")
    try:
        bm = BMParse(buildManifestPath=manifest_, url=url_)
    except:
        if url_ and len(url_) > 0:
            raise click.BadParameter(f"Failed to initialize BuildManifest: {url_}")
        else:
            raise click.BadParameter(f"Failed to initialize BuildManifest: {manifest_}")
    variant = "Erase"
    if variant_ > 0:
        variant = "Update"
    if url_:
        print(
            f"Getting path of component {component_} for {board_}, {variant} from {bm.url}"
        )
    else:
        print(
            f"Getting path of component {component_} for {board_}, {variant} from {bm.buildManifestPath}"
        )
    path = bm.getComponentPath(
        board=board_, component=component_, update=bool(variant_)
    )
    if not path or len(path) < 1:
        raise click.BadParameter(f"Failed to get path for {component_}")
    else:
        print(path)


@component.command("download")
@click.option(
    "-m",
    "--manifest",
    "manifest_",
    type=str,
    help="Input BuildManifest path",
    required=False,
)
@click.option(
    "-u",
    "--url",
    "url_",
    type=str,
    help="Or input BuildManifest from ipsw url",
    required=True,
)
@click.option(
    "-b",
    "--board",
    "board_",
    type=str,
    help="Input device board config",
    required=True,
)
@click.option(
    "-v",
    "--variant",
    "variant_",
    type=int,
    help="Input restore variant",
    required=False,
)
@click.option(
    "-c",
    "--component",
    "component_",
    type=str,
    help="Input component name",
    required=True,
)
@click.option(
    "-o",
    "--outdir",
    "outdir_",
    type=str,
    help="Input output directory path",
    required=False,
)
def downloadComponent(
    board_: str,
    component_: str,
    manifest_: str = "",
    outdir_: str = "",
    url_: str = "",
    variant_: int = 0,
) -> None:
    """Download specified component from ipsw for board and variant from BuildManifest."""
    if not board_ or len(board_) < 1:
        raise click.BadParameter("No board specified")
    if not component_ or len(component_) < 1:
        raise click.BadParameter("No component specified")
    board_ = board_.lower()
    ap = f"{board_[-2]}{board_[-1]}"
    if not ap.__eq__("ap"):
        raise click.BadParameter("Invalid board config")
    if not manifest_ or len(manifest_) < 1:
        if not url_ or len(url_) < 1:
            raise click.BadParameter("No ipsw url or BuildManifest provided")
    try:
        bm = BMParse(buildManifestPath=manifest_, url=url_)
    except:
        if url_ and len(url_) > 0:
            raise click.BadParameter(f"Failed to initialize BuildManifest: {url_}")
        else:
            raise click.BadParameter(f"Failed to initialize BuildManifest: {manifest_}")
    try:
        if outdir_ and len(outdir_) > 0:
            bmt = BMTool(bm=bm, outDir=outdir_)
        else:
            bmt = BMTool(bm=bm)
    except:
        if url_ and len(url_) > 0:
            raise click.BadParameter(f"Failed to initialize BuildManifest tool: {url_}")
        else:
            raise click.BadParameter(
                f"Failed to initialize BuildManifest tool: {manifest_}"
            )
    variant = "Erase"
    if variant_ > 0:
        variant = "Update"
    if url_:
        print(
            f"Downloading component {component_} for {board_}, {variant} from {bm.url}"
        )
    else:
        print(
            f"Downloading component {component_} for {board_}, {variant} from {bm.buildManifestPath}"
        )
    path = bmt.downloadComponent(
        board=board_, component=component_, update=bool(variant_)
    )
    if not path or len(path) < 1:
        raise click.BadParameter(f"Failed to download {component_}")
    else:
        print(path)


# def main():
#     bm = BMParse(url="https://updates.cdn-apple.com/2022SummerFCS/fullrestores/"
#                      "012-52552/90DDC844-B111-4CBF-8C86-E2A8B604B3D2/iPhone_4.7_15.6.1_19G82_Restore.ipsw")
#     # print(bm.getComponentPath(board="n71ap", component="iBSS", update=False))
#     # for comp in bm.getComponentList(board="n71ap", update=False):
#     #     print(comp)
#     del bm


if __name__ == "__main__":
    cli()
    # main()
