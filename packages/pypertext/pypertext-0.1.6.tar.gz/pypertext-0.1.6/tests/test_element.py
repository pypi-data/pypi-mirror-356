"""Tests for the Element class."""

from pypertext.hypertext import Element


def test_element_creation():
    """Test basic element creation."""
    el = Element()
    assert el.tag == "div"
    assert el.children == []
    assert el.attributes == {}


def test_element_with_args():
    """Test element creation with children."""
    el = Element("Hello", "World")
    assert len(el.children) == 2
    assert el.children[0] == "Hello"
    assert el.children[1] == "World"


def test_element_with_kwargs():
    """Test element creation with attributes."""
    el = Element(id="test", classes=["foo", "bar"])
    assert el.attributes["id"] == "test"
    assert el.attributes["classes"] == ["foo", "bar"]


def test_element_add_string():
    """Test adding strings to element."""
    el = Element()
    el + "Hello"
    assert len(el.children) == 1
    assert el.children[0] == "Hello"


def test_element_add_multiple():
    """Test adding multiple children at once."""
    el = Element()
    el + ["Hello", "World", 123]
    assert len(el.children) == 3
    assert el.children[0] == "Hello"
    assert el.children[1] == "World"
    assert el.children[2] == "123"


def test_element_add_element():
    """Test adding element to element."""
    parent = Element()
    child = Element()
    child.tag = "span"
    parent + child
    assert len(parent.children) == 1
    assert parent.children[0] == child


def test_element_add_dict():
    """Test adding dict as attributes."""
    el = Element()
    el + {"id": "test", "data_value": "123"}
    assert el.attributes["id"] == "test"
    assert el.attributes["data_value"] == "123"


def test_element_iadd():
    """Test += operator."""
    el = Element()
    el += "Hello"
    el += "World"
    assert len(el.children) == 2
    assert el.children[0] == "Hello"
    assert el.children[1] == "World"


def test_element_call():
    """Test calling element to add children and attributes."""
    el = Element()
    result = el("Hello", "World", id="test")
    assert result == el
    assert len(el.children) == 2
    assert el.attributes["id"] == "test"


def test_set_attrs():
    """Test setting attributes."""
    el = Element()
    el.set_attrs(id="test", data_value="123")
    assert el.attributes["id"] == "test"
    assert el.attributes["data_value"] == "123"


def test_set_attrs_with_classes():
    """Test setting attributes with classes."""
    el = Element(classes=["foo"])
    el.set_attrs(classes=["bar", "baz"])
    assert set(el.attributes["classes"]) == {"foo", "bar", "baz"}


def test_merge_attrs():
    """Test merging attributes."""
    el = Element(id="test", data_values=["a"])
    el.merge_attrs(data_values=["b", "c"])
    assert el.attributes["id"] == "test"
    assert el.attributes["data_values"] == ["a", "b", "c"]


def test_add_classes():
    """Test adding classes."""
    el = Element()
    el.add_classes("foo", "bar")
    assert set(el.attributes["classes"]) == {"foo", "bar"}

    el.add_classes("baz")
    assert set(el.attributes["classes"]) == {"foo", "bar", "baz"}


def test_add_classes_with_list():
    """Test adding classes from list."""
    el = Element()
    el.add_classes(["foo", "bar"], "baz")
    assert set(el.attributes["classes"]) == {"foo", "bar", "baz"}


def test_remove_classes():
    """Test removing classes."""
    el = Element(classes=["foo", "bar", "baz"])
    el.remove_classes("bar")
    assert set(el.attributes["classes"]) == {"foo", "baz"}

    el.remove_classes("nonexistent")
    assert set(el.attributes["classes"]) == {"foo", "baz"}


def test_has_classes():
    """Test checking for classes."""
    el = Element(classes=["foo", "bar"])
    assert el.has_classes("foo")
    assert el.has_classes("bar")
    assert el.has_classes("foo", "bar")
    assert not el.has_classes("baz")
    assert not el.has_classes("foo", "baz")
    
    # Empty element
    el2 = Element()
    assert not el2.has_classes("anything")
    assert el2.has_classes()  # all() on empty is True


def test_append():
    """Test append method."""
    el = Element()
    el.append("Hello")
    el.append("World")
    assert len(el.children) == 2
    assert el.children[0] == "Hello"
    assert el.children[1] == "World"


def test_extend():
    """Test extend method."""
    el = Element()
    el.extend("Hello", "World", 123)
    assert len(el.children) == 3
    assert el.children[0] == "Hello"
    assert el.children[1] == "World"
    assert el.children[2] == "123"


def test_insert():
    """Test insert method."""
    el = Element("World")
    el.insert(0, "Hello")
    assert len(el.children) == 2
    assert el.children[0] == "Hello"
    assert el.children[1] == "World"


def test_to_string():
    """Test converting element to string."""
    el = Element("Hello World")
    el.tag = "div"
    assert el.to_string() == "<div>Hello World</div>"


def test_str():
    """Test __str__ method."""
    el = Element("Hello")
    el.tag = "span"
    assert str(el) == "<span>Hello</span>"


def test_repr_html():
    """Test _repr_html_ method for Jupyter."""
    el = Element("Test")
    el.tag = "p"
    assert el._repr_html_() == "<p>Test</p>"


def test_pipe():
    """Test pipe method."""

    def add_id(element: Element, id_value: str) -> Element:
        element.set_attrs(id=id_value)
        return element

    el = Element()
    result = el.pipe(add_id, "test-id")
    assert result == el
    assert el.attributes["id"] == "test-id"


def test_element_with_none():
    """Test adding None values."""
    el = Element()
    el + None
    el + [None, "Hello", None]
    assert len(el.children) == 1
    assert el.children[0] == "Hello"


def test_element_with_bytes():
    """Test adding bytes."""
    el = Element()
    el + b"Hello"
    assert len(el.children) == 1
    assert el.children[0] == "Hello"


def test_element_with_numbers():
    """Test adding numbers."""
    el = Element()
    el + 123
    el + 45.67
    assert len(el.children) == 2
    assert el.children[0] == "123"
    assert el.children[1] == "45.67"


def test_element_with_function():
    """Test adding functions as children."""

    def content():
        return "Dynamic content"

    el = Element()
    el + content
    assert len(el.children) == 1
    assert callable(el.children[0])


def test_element_with_iterable():
    """Test adding iterables."""
    el = Element()
    el + range(3)
    assert len(el.children) == 3
    assert el.children[0] == "0"
    assert el.children[1] == "1"
    assert el.children[2] == "2"


def test_element_classes_as_string():
    """Test classes as space-separated string."""
    el = Element(classes="foo bar baz")
    assert set(el.attributes["classes"]) == {"foo", "bar", "baz"}


def test_element_classes_as_function():
    """Test classes as function."""

    def get_classes():
        return ["dynamic", "classes"]

    el = Element(classes=get_classes)
    # When passing a function, it gets evaluated and stored as the result
    assert el.attributes["classes"] == ["dynamic", "classes"]
