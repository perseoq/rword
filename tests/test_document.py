
from rword.core.document import Document


def test_new_document_has_no_path(document):
    assert document.file_path is None
    assert document.is_new
    assert document.extension == ""


def test_document_with_path(tmp_path):
    path = tmp_path / "doc.txt"
    document = Document(path)
    assert document.file_path == path
    assert not document.is_new
    assert document.name == "doc.txt"
    assert document.extension == ".txt"


def test_document_name_default():
    assert Document().name == "Sin título"


def test_document_file_path_setter(tmp_path):
    document = Document()
    path = tmp_path / "other.md"
    document.file_path = path
    assert document.file_path == path
    assert document.extension == ".md"
