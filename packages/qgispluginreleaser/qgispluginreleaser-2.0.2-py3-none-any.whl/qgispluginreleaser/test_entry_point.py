from unittest import mock

from qgispluginreleaser.entry_point import create_zipfile


def _return_metadata():
    return "metadata.txt"


def _mock_glob(something):
    return ["something.zip"]


def test_makefile_call():
    with mock.patch(
        "qgispluginreleaser.entry_point.find_metadata_file", _return_metadata
    ):
        with mock.patch("subprocess.call") as mocked:
            # ^^^ handles "make zip" call
            create_zipfile({})
            assert mocked.called


def test_ziprename():
    with mock.patch(
        "qgispluginreleaser.entry_point.find_metadata_file", _return_metadata
    ):
        with mock.patch("subprocess.call"):  # "make zip"
            with mock.patch("glob.glob", _mock_glob):
                with mock.patch("shutil.copy") as mocked:
                    create_zipfile({"version": "1.0", "workingdir": "/tmp"})
                    mocked.assert_called_with("something.zip", "/tmp/something.1.0.zip")
