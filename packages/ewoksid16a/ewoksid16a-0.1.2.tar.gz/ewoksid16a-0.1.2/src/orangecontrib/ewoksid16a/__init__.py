import sysconfig

NAME = "ewoksid16a"

DESCRIPTION = "Data processing workflows for ID16A"

LONG_DESCRIPTION = "Data processing workflows for ID16A"

ICON = "icons/category.svg"

BACKGROUND = "light-blue"

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
