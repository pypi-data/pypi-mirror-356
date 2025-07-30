"""Tests for the Document class."""

from pypertext.hypertext import Document, ht, Element


def test_document_creation():
    """Test basic document creation."""
    doc = Document()
    assert isinstance(doc, Element)
    assert doc.page_title is None
    assert doc.headers is None
    assert doc.status_code == 200
    assert isinstance(doc.title, Element)
    assert isinstance(doc.head, Element)
    assert isinstance(doc.body, Element)
    assert isinstance(doc.html, Element)


def test_document_with_page_title():
    """Test document with page title."""
    doc = Document(page_title="My Page")
    assert doc.page_title == "My Page"


def test_document_with_headers():
    """Test document with headers."""
    headers = {"X-Custom-Header": "value"}
    doc = Document(headers=headers)
    assert doc.headers == headers


def test_document_with_status_code():
    """Test document with custom status code."""
    doc = Document(status_code=404)
    assert doc.status_code == 404


def test_document_with_children():
    """Test document with children."""
    doc = Document(
        ht.h1("Welcome"),
        ht.p("This is a paragraph")
    )
    assert len(doc.children) == 2


def test_document_get_element():
    """Test get_element method."""
    doc = Document(page_title="Test Page")
    doc + ht.h1("Hello")
    doc + ht.p("World")
    
    element = doc.get_element()
    assert element == doc.html
    assert doc.title.children == ["Test Page"]
    assert doc.body.children == doc.children
    assert doc.body.attributes == doc.attributes


def test_document_to_string():
    """Test converting document to string."""
    doc = Document(page_title="Test")
    doc + ht.h1("Hello World")
    
    result = doc.to_string()
    assert result.startswith("<!DOCTYPE html>")
    assert "<html>" in result
    assert "<head>" in result
    assert "<title>Test</title>" in result
    assert "<body>" in result
    assert "<h1>Hello World</h1>" in result
    assert "</html>" in result


def test_document_empty():
    """Test empty document."""
    doc = Document()
    result = doc.to_string()
    assert "<!DOCTYPE html>" in result
    assert "<html>" in result
    assert "<head>" in result
    assert "<body></body>" in result


def test_document_head_contains_meta():
    """Test document head contains required meta tags."""
    doc = Document()
    head_str = ht.render_element(doc.head)
    assert 'charset="utf-8"' in head_str
    assert 'name="viewport"' in head_str
    assert 'content="width=device-width, initial-scale=1"' in head_str
    assert 'http-equiv="X-UA-Compatible"' in head_str


def test_document_with_attributes():
    """Test document with attributes on body."""
    doc = Document(classes=["container"], id="main")
    doc + ht.h1("Test")
    
    element = doc.get_element()
    assert doc.body.attributes["classes"] == ["container"]
    assert doc.body.attributes["id"] == "main"


def test_document_add_to_head():
    """Test adding elements to head."""
    doc = Document()
    doc.head + ht.link(rel="stylesheet", href="styles.css")
    doc.head + ht.script(src="script.js")
    
    head_str = ht.render_element(doc.head)
    assert 'rel="stylesheet"' in head_str
    assert 'href="styles.css"' in head_str
    assert 'src="script.js"' in head_str


def test_document_add_to_body():
    """Test adding elements directly to body."""
    doc = Document()
    doc.body + ht.div("Direct to body")
    doc + ht.div("Through document")
    
    # Direct additions to body appear in body.children
    assert len(doc.body.children) == 1
    assert doc.body.children[0].tag == "div"
    
    # Additions to doc appear in doc.children
    assert len(doc.children) == 1
    
    # When rendered, body.children gets replaced with doc.children
    result = doc.to_string()
    # Only the content added through doc appears
    assert "Through document" in result
    assert "Direct to body" not in result


def test_document_modify_html_attributes():
    """Test modifying html element attributes."""
    doc = Document()
    doc.html.set_attrs(lang="en", dir="ltr")
    
    result = doc.to_string()
    assert 'lang="en"' in result
    assert 'dir="ltr"' in result


def test_document_chaining():
    """Test method chaining with document."""
    doc = Document(page_title="Chain Test")
    doc + ht.h1("Title") + ht.p("Paragraph")
    doc.set_attrs(classes=["page"])
    
    assert len(doc.children) == 2
    assert doc.attributes["classes"] == ["page"]


def test_document_render_complex():
    """Test rendering complex document."""
    doc = Document(page_title="Complex Page")
    doc.head + ht.style(
        "body { margin: 0; } .container { max-width: 1200px; }"
    )
    
    doc + ht.header(
        ht.nav(
            ht.a("Home", href="/"),
            ht.a("About", href="/about")
        )
    )
    doc + ht.main(
        ht.h1("Welcome"),
        ht.section(
            ht.p("Content goes here"),
            classes=["content"]
        ),
        classes=["container"]
    )
    doc + ht.footer("© 2024")
    
    result = doc.to_string()
    assert "<header>" in result
    assert "<nav>" in result
    assert '<a href="/">Home</a>' in result
    assert "<main" in result
    assert 'class="container"' in result
    assert "<footer>© 2024</footer>" in result