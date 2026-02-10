def validate_comma_separated_int(
    setting,
    value: str | None = None,
    option_parser=None,
    config_parser=None,
    config_section=None,
) -> list[int]:
    if value is None:
        value = setting
    try:
        return [int(item) for item in value.split(",")]
    except ValueError:
        raise ValueError("Invalid comma-separated list")
