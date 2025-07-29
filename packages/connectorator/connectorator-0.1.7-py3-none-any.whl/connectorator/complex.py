import types
from functools import lru_cache
from urllib.parse import urlencode

NETBOX_URL = "https://demo.netbox.dev"

STATUS = "status"
ROLE_ID = "role_id"
SITE_ID = "site_id"

EXAMPLE_INPUT = types.MappingProxyType(
    {
        "manufacturer": ["cisco"],
        "role": ["router", "core-switch", "access-switch"],
        "status": ["active", "offline"],
        "site": ["dm-akronsk", "dm-albany", "dm-camden"],
    },
)

EXAMPLE_RESULT = [  # noqa: WPS407
    ("manufacturer_id", 3),
    (ROLE_ID, 1),
    (ROLE_ID, 2),
    (ROLE_ID, 4),
    (STATUS, "active"),
    (STATUS, "offline"),
    (SITE_ID, 2),
    (SITE_ID, 3),
    (SITE_ID, 6),
    ("brief", "true"),
    ("limit", 500),
]


@lru_cache
def _get_site_id(site_slug: str) -> int:
    """Заглушка для получения id сайта по его slug."""
    site_id = {
        "dm-akronsk": 2,
        "dm-albany": 3,
        "dm-binghamton": 4,
        "dm-buffalo": 5,
        "dm-camden": 6,
    }.get(site_slug)
    if site_id is None:
        raise ValueError(f"неизвестный сайт '{site_slug}'")
    return site_id


@lru_cache
def _get_device_role_id(device_role_slug: str) -> int:
    """Заглушка для получения id роли устройства по её slug."""
    device_role_id = {
        "router": 1,
        "core-switch": 2,
        "distribution-switch": 3,
        "access-switch": 4,
    }.get(device_role_slug)
    if device_role_id is None:
        raise ValueError(f"неизвестная роль устройства '{device_role_slug}'")
    return device_role_id


@lru_cache
def _get_manufacturer_id(manufacturer_slug: str) -> int:
    manufacturer_id = {
        "arista": 1,
        "cisco": 3,
        "juniper": 7,
    }.get(manufacturer_slug)
    if manufacturer_id is None:
        raise ValueError(f"неизвестный производитель '{manufacturer_slug}'")
    return manufacturer_id


def craft_nb_query(
    request_params: dict[str, list[str]],
) -> list[tuple[str, str | int]]:
    """Преобразование набора параметров в request params.

    Args:
        request_params (dict[str, str]): параметры запроса.
        ```python
        {
            "manufacturer": ["cisco"],
            "role": ["router"],
            "status": ["active", "offline"],
            "site": ["dm-akronsk", "dm-albany"],
        }
        ```

    Raises:
        ValueError: если переданы неизвестные или пустые параметры

    Returns:
        list[tuple[str, str | int]]: список кортежей из переданных параметров + brief и limit:
        ```python
        [
            ("manufacturer_id", 3),
            ("role", "router"),
            ("status", "active"),
            ("status", "offline"),
            ("site_id", 2),
            ("site_id", 3),
            ("brief", "true"),
            ("limit", 500),
        ]
        ```
    """
    function_map = {
        "site": _get_site_id,
        "name": lambda x: x.lower,
        "role": _get_device_role_id,
        "manufacturer": _get_manufacturer_id,
        STATUS: lambda x: x,
    }
    nb_item_field_map = {
        "site": "site_id",
        "role": "role_id",
        "manufacturer": "manufacturer_id",
        STATUS: STATUS,
        "name": "name__ie",
    }
    if len(request_params) == 0:
        raise ValueError("отсутствуют параметры запроса")

    nb_query = []

    for item_type, items in request_params.items():
        for item_val in items:
            mapped_function = function_map.get(item_type)
            nb_item_field = nb_item_field_map.get(item_type, item_type)
            if not mapped_function or not nb_item_field:
                raise ValueError(f"неизвестный тип параметра '{item_type}'")
            nb_query.append(
                (nb_item_field, mapped_function(item_val)),
            )

    nb_query.append(("brief", "true"))
    nb_query.append(("limit", 500))
    return nb_query


if __name__ == "__main__":
    result = craft_nb_query(EXAMPLE_INPUT)  # type: ignore
    assert result == EXAMPLE_RESULT, "функция 'craft_nb_query' работает некорректно"
    print(f"{NETBOX_URL}/api/dcim/devices/?{urlencode(result)}")
