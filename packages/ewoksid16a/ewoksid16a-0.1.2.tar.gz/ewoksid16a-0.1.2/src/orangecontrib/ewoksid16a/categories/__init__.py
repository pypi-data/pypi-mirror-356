import sysconfig

WIDGET_HELP_PATH = (
    # Development documentation (make htmlhelp in ./doc)
    ("{DEVELOP_ROOT}/doc/_build/htmlhelp/index.html", None),
    # Documentation included in wheel
    (
        "{}/help/ewoksid16a/index.html".format(sysconfig.get_path("data")),
        None,
    ),
    # Online documentation url
    ("https://ewoksid16a.readthedocs.io", ""),
)


# Entry point for main Orange categories/widgets discovery
def widget_discovery(discovery):
    from ewoksorange.pkg_meta import get_distribution

    dist = get_distribution("ewoksid16a")
    pkgs = [
        "orangecontrib.ewoksid16a.categories.examples1",
        "orangecontrib.ewoksid16a.categories.examples2",
    ]
    for pkg in pkgs:
        discovery.process_category_package(pkg, distribution=dist)
