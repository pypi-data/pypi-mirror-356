"""Test that attributes starting with underscore are not rendered."""

from pypertext import ht


def test_basic_underscore_attribute():
    """Test that a single underscore attribute is not rendered."""
    element = ht.div(id="test", _internal="should-not-render", data_value="should-render")
    html = element.to_string()
    
    # Should contain normal attributes
    assert 'id="test"' in html
    assert 'data-value="should-render"' in html
    
    # Should NOT contain underscore attributes
    assert '_internal' not in html
    assert '-internal' not in html  # Should not be converted to dash either


def test_multiple_underscore_attributes():
    """Test that multiple underscore attributes are not rendered."""
    element = ht.span(
        classes="my-class",  # This should render as class="my-class"
        _meta="internal",
        _data="private",
        title="Hello"
    )
    html = element.to_string()
    
    # Should contain normal attributes
    assert 'class="my-class"' in html
    assert 'title="Hello"' in html
    
    # Should NOT contain underscore attributes
    assert '_meta' not in html
    assert '-meta' not in html
    assert '_data' not in html
    assert '-data' not in html


def test_edge_cases_underscore_attributes():
    """Test edge cases like single underscore and double underscore attributes."""
    element = ht.p(_="should-not-render", __private="also-should-not-render", content="visible")
    html = element.to_string()
    
    # Should contain normal attributes
    assert 'content="visible"' in html
    
    # Should NOT contain underscore attributes
    assert '_=' not in html
    assert '-=' not in html
    assert '__private' not in html
    assert '--private' not in html


def test_underscore_attributes_with_functions():
    """Test that underscore attributes with function values are not rendered."""
    def get_value():
        return "function-value"
    
    element = ht.div(
        id="test",
        _func=get_value,
        data_func=get_value
    )
    html = element.to_string()
    
    # Should contain normal attributes with evaluated functions
    assert 'id="test"' in html
    assert 'data-func="function-value"' in html
    
    # Should NOT contain underscore attributes (check for attribute format, not just substring)
    assert '_func=' not in html
    assert '_func"' not in html


def test_underscore_attributes_preserved_in_element():
    """Test that underscore attributes are still stored in the element's attributes dict."""
    element = ht.div(id="test", _internal="value")
    
    # The underscore attribute should be in the attributes dict
    assert "_internal" in element.attributes
    assert element.attributes["_internal"] == "value"
    
    # But not in the rendered HTML
    html = element.to_string()
    assert "_internal" not in html


def test_special_attribute_for_():
    """Test that the special 'for_' attribute still works (converts to 'for')."""
    element = ht.label(for_="input-id", _private="hidden")
    html = element.to_string()
    
    # Should contain the 'for' attribute
    assert 'for="input-id"' in html
    
    # Should NOT contain underscore attributes
    assert '_private' not in html