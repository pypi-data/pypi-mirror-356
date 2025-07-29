import importlib

from qgispluginreleaser.entry_point import create_zipfile, find_metadata_file


def test_entry_point_available():
    entry_points = importlib.metadata.entry_points(
        group="zest.releaser.releaser.after_checkout"
    )
    assert "qgispluginreleaser.entry_point" in str(entry_points)


def test_metadata_file():
    # Should return false for us.
    assert not find_metadata_file()


def test_stops_if_no_metadata_file():
    # Should return false for us.
    assert not create_zipfile({})
