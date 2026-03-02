def pytest_addoption(parser):
    parser.addoption(
        "--specs",
        action="store",
        default=None,
        help="Target specs from '/docs/spec' directory.",
    )
