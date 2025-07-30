from pathlib import Path

import lxml.etree as ET

from excel2moodle.core.dataStructure import QuestionDB
from excel2moodle.core.settings import Settings, Tags

settings = Settings()

katName = "NFM2"
database = QuestionDB(settings)

settings.set(Tags.QUESTIONVARIANT, 1)
database.spreadsheet = Path("test/TestQuestion.ods")
excelFile = settings.get(Tags.SPREADSHEETPATH)
database.readCategoriesMetadata(excelFile)
database.initAllCategories(excelFile)
category = database.categories[katName]
qlist = [database.setupAndParseQuestion(category, 1)]
tree = ET.Element("quiz")
database._appendQElements(category, qlist, tree, includeHeader=False)


def test_resultValueOfNFMQuestion() -> None:
    answer = tree.find("question").find("answer")
    tolerance = answer.find("tolerance")
    result = answer.find("text")
    print(result)
    assert result.text == "127.0"
    assert tolerance.text == "6.35"
