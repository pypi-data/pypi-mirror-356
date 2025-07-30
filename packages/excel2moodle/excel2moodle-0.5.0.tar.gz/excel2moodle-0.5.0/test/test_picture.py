from pathlib import Path

import pytest

from excel2moodle.core.question import Picture
from excel2moodle.core.settings import Settings

settings = Settings()


imgFolder = Path("./test/Abbildungen")


qID = "0103"
katName = "MC1"


@pytest.mark.parametrize(
    ("imgKey", "expected"),
    [
        ("1", "0101.png"),
        ("true", "0103.svg"),
        ("1_a", "0101_a.png"),
        ("0101", "0101.png"),
        ("03", "0103.svg"),
        ("101_a", "0101_a.png"),
    ],
)
def test_PictureFindImgFile(imgKey, expected) -> None:
    imgF = (imgFolder / katName).resolve()
    picture = Picture(imgKey, imgF, qID, width=300)
    print(picture.path)
    p = str(picture.path.stem + picture.path.suffix)
    assert p == expected


@pytest.mark.parametrize(
    ("imgKey", "expected"),
    [
        ("2_b", "0102_b"),
        ("01_a", "0101_a"),
        ("0101", "0101"),
        ("05-c", "0105-c"),
        ("201", "0201"),
        ("101_a", "0101_a"),
        ("3802_c", "3802_c"),
        ("0902_c", "0902_c"),
        pytest.param("13802_c", "3802_c", marks=pytest.mark.xfail),
        pytest.param("false", None, marks=pytest.mark.xfail),
    ],
)
def test_Picture_EvaluateCorrectPicID(imgKey, expected) -> None:
    imgF = (imgFolder / katName).resolve(strict=True)
    picture = Picture(imgKey, imgF, qID, width=300)
    assert picture.picID == expected
