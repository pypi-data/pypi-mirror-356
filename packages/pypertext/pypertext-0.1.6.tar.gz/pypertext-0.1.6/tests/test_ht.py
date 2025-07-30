"""Tests for the ht class."""

from pypertext.hypertext import ht, Element, SELF_CLOSING_TAGS


def test_ht_tag_creation():
    """Test creating elements with ht."""
    div = ht.div()
    assert isinstance(div, Element)
    assert div.tag == "div"
    
    span = ht.span()
    assert isinstance(span, Element)
    assert span.tag == "span"


def test_ht_with_children():
    """Test creating elements with children."""
    div = ht.div("Hello", "World")
    assert len(div.children) == 2
    assert div.children[0] == "Hello"
    assert div.children[1] == "World"


def test_ht_with_attributes():
    """Test creating elements with attributes."""
    button = ht.button(type="submit", classes=["btn", "btn-primary"])
    assert button.attributes["type"] == "submit"
    assert set(button.attributes["classes"]) == {"btn", "btn-primary"}


def test_ht_render_simple():
    """Test rendering simple element."""
    result = ht.render_element(ht.div("Hello"))
    assert result == "<div>Hello</div>"


def test_ht_render_with_attributes():
    """Test rendering element with attributes."""
    result = ht.render_element(ht.div("Hello", id="test", data_value="123"))
    assert result == '<div id="test" data-value="123">Hello</div>'


def test_ht_render_with_classes():
    """Test rendering element with classes."""
    result = ht.render_element(ht.div("Hello", classes=["foo", "bar"]))
    assert 'class="foo bar"' in result or 'class="bar foo"' in result


def test_ht_render_nested():
    """Test rendering nested elements."""
    result = ht.render_element(
        ht.div(
            ht.h1("Title"),
            ht.p("Paragraph")
        )
    )
    assert result == "<div><h1>Title</h1><p>Paragraph</p></div>"


def test_ht_render_self_closing():
    """Test rendering self-closing tags."""
    result = ht.render_element(ht.br())
    assert result == "<br/>"
    
    result = ht.render_element(ht.img(src="test.jpg", alt="Test"))
    assert result == '<img src="test.jpg" alt="Test"/>'


def test_ht_render_boolean_attributes():
    """Test rendering boolean attributes."""
    result = ht.render_element(ht.input(type="checkbox", checked=True))
    assert 'checked' in result
    assert 'checked=' not in result
    
    result = ht.render_element(ht.input(type="checkbox", checked=False))
    assert 'checked' not in result


def test_ht_render_none_value():
    """Test rendering with None values."""
    result = ht.render_element(None)
    assert result == ""
    
    result = ht.render_element(ht.div(None, "Hello", None))
    assert result == "<div>Hello</div>"


def test_ht_render_numbers():
    """Test rendering numbers."""
    result = ht.render_element(123)
    assert result == "123"
    
    result = ht.render_element(ht.div(123, 45.67))
    assert result == "<div>12345.67</div>"


def test_ht_render_function_child():
    """Test rendering function as child."""
    def content():
        return "Dynamic content"
    
    result = ht.render_element(ht.div(content))
    assert result == "<div>Dynamic content</div>"


def test_ht_render_function_attribute():
    """Test rendering function as attribute."""
    def get_id():
        return "dynamic-id"
    
    result = ht.render_element(ht.div("Test", id=get_id))
    assert result == '<div id="dynamic-id">Test</div>'


def test_ht_render_style_dict():
    """Test rendering style as dict."""
    result = ht.render_element(ht.div("Test", style={"color": "red", "font-size": "16px"}))
    assert 'style="' in result
    assert "color: red" in result
    assert "font-size: 16px" in result


def test_ht_render_list_attribute():
    """Test rendering list as attribute."""
    result = ht.render_element(ht.div("Test", data_values=["a", "b", "c"]))
    assert 'data-values="a b c"' in result


def test_ht_render_underscore_to_dash():
    """Test underscore to dash conversion."""
    result = ht.render_element(ht.div("Test", data_my_value="123"))
    assert 'data-my-value="123"' in result


def test_ht_render_for_attribute():
    """Test for_ attribute conversion."""
    result = ht.render_element(ht.label("Name", for_="name-input"))
    assert 'for="name-input"' in result


def test_ht_render_quote_handling():
    """Test handling quotes in attribute values."""
    result = ht.render_element(ht.div("Test", title='Say "Hello"'))
    assert "title='Say \"Hello\"'" in result


def test_ht_call():
    """Test calling ht directly."""
    # ht is a class with metaclass, not callable directly
    # Create instance first
    h = ht()
    el = h("custom-tag", "Content", id="test")
    assert el.tag == "custom-tag"
    assert el.children == ["Content"]
    assert el.attributes["id"] == "test"


def test_ht_custom_tags():
    """Test custom/unconventional tags."""
    result = ht.render_element(ht.my_custom_tag("Hello"))
    assert result == "<my-custom-tag>Hello</my-custom-tag>"


def test_ht_render_empty_element():
    """Test rendering empty element."""
    result = ht.render_element(ht.div())
    assert result == "<div></div>"


def test_ht_render_element_with_get_element():
    """Test rendering object with get_element method."""
    class CustomElement:
        def get_element(self):
            return ht.span("Custom")
    
    result = ht.render_element(ht.div(CustomElement()))
    assert result == "<div><span>Custom</span></div>"


def test_ht_render_recursive_function():
    """Test recursive function evaluation."""
    def outer():
        def inner():
            return "Nested"
        return inner
    
    result = ht.render_element(outer)
    assert result == "Nested"


def test_ht_all_self_closing_tags():
    """Test all self-closing tags are handled properly."""
    for tag in ["br", "hr", "img", "input", "meta", "link"]:
        assert tag in SELF_CLOSING_TAGS
        el = getattr(ht, tag)()
        result = ht.render_element(el)
        assert result.endswith("/>")
        assert not result.endswith(f"></{tag}>")


def test_ht_render_document():
    """Test render_document method."""
    body = ht.div("Hello World")
    result = ht.render_document(body, title="Test Page")
    
    assert "<!DOCTYPE html>" in result
    assert "<html>" in result
    assert "</html>" in result
    assert "<head>" in result
    assert "<title>Test Page</title>" in result
    assert "<body>" in result
    assert "<div>Hello World</div>" in result
    assert 'charset="utf-8"' in result