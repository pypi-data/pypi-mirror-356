from uhura.composition import async_unit


def test_async_unit_is_idempotent():
    async_value = async_unit("test")
    assert async_unit(async_value) is async_value
