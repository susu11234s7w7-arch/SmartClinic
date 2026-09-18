import smart_clinic


def test_package_imports_cleanly() -> None:
    assert smart_clinic.__name__ == "smart_clinic"
