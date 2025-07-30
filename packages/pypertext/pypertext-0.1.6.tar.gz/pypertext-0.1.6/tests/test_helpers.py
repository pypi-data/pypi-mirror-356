"""Tests for helper functions in hypertext module."""

from pypertext.hypertext import (
    _flatten, _listify, _stringify, _merge_dicts, _classes_ensure_list, 
    _is_function, _get_selector_type, _combine_selectors
)


def test_flatten_none():
    """Test _flatten with None input."""
    assert _flatten(None) == []


def test_flatten_string():
    """Test _flatten with string input."""
    assert _flatten("hello") == ["hello"]
    assert _flatten("") == [""]


def test_flatten_simple_list():
    """Test _flatten with simple list."""
    assert _flatten([1, 2, 3]) == [1, 2, 3]
    assert _flatten(["a", "b", "c"]) == ["a", "b", "c"]


def test_flatten_nested_list():
    """Test _flatten with nested lists."""
    assert _flatten([1, [2, 3], 4]) == [1, 2, 3, 4]
    assert _flatten([["a"], ["b", "c"], "d"]) == ["a", "b", "c", "d"]


def test_flatten_deeply_nested():
    """Test _flatten with deeply nested lists."""
    assert _flatten([1, [2, [3, [4, 5]], 6]]) == [1, 2, 3, 4, 5, 6]


def test_flatten_mixed_types():
    """Test _flatten with mixed types."""
    assert _flatten([1, "hello", 3.14, True, [2, "world"]]) == [1, "hello", 3.14, True, 2, "world"]


def test_flatten_with_none_items():
    """Test _flatten with None items in list."""
    assert _flatten([1, None, 2, [3, None, 4]]) == [1, 2, 3, 4]
    assert _flatten([None, None, None]) == []


def test_flatten_empty_lists():
    """Test _flatten with empty lists."""
    assert _flatten([]) == []
    assert _flatten([[], [[]], []]) == []
    assert _flatten([1, [], 2, [[], 3]]) == [1, 2, 3]


def test_flatten_non_list_iterable():
    """Test _flatten with non-list iterables (should treat as non-list)."""
    # Since _flatten only checks for list type specifically
    assert _flatten([1, (2, 3), 4]) == [1, (2, 3), 4]
    assert _flatten([{1, 2}, 3]) == [{1, 2}, 3]


def test_listify_none():
    """Test _listify with None."""
    assert _listify(None) == []


def test_listify_collections():
    """Test _listify with various collections."""
    assert _listify([1, 2, 3]) == [1, 2, 3]
    assert _listify((1, 2, 3)) == [1, 2, 3]
    assert _listify({1, 2, 3}) == [1, 2, 3]
    assert _listify({"a": 1, "b": 2}) == [1, 2]


def test_listify_single_value():
    """Test _listify with single values."""
    assert _listify("hello") == ["hello"]
    assert _listify(123) == [123]
    assert _listify(3.14) == [3.14]
    assert _listify(True) == [True]


def test_stringify_single_values():
    """Test _stringify with single values."""
    assert _stringify("hello") == "hello"
    assert _stringify(123) == "123"
    assert _stringify(3.14) == "3.14"
    assert _stringify(True) == "True"


def test_stringify_list():
    """Test _stringify with list values."""
    assert _stringify([1, 2, 3]) == "1 2 3"
    assert _stringify(["hello", "world"]) == "hello world"
    assert _stringify([1, [2, 3], 4]) == "1 2 3 4"  # Uses _flatten


def test_stringify_with_separator():
    """Test _stringify with custom separator."""
    assert _stringify([1, 2, 3], sep=",") == "1,2,3"
    assert _stringify(["a", "b", "c"], sep=" - ") == "a - b - c"


def test_merge_dicts_simple():
    """Test _merge_dicts with simple dicts."""
    assert _merge_dicts({"a": 1}, {"b": 2}) == {"a": 1, "b": 2}
    # When same key exists, values are converted to list
    assert _merge_dicts({"a": 1}, {"a": 2}) == {"a": [1, 2]}


def test_merge_dicts_nested():
    """Test _merge_dicts with nested dicts."""
    d1 = {"a": {"x": 1, "y": 2}}
    d2 = {"a": {"y": 3, "z": 4}}
    result = _merge_dicts(d1, d2)
    # Nested dicts are merged recursively, duplicate keys become lists
    assert result == {"a": {"x": 1, "y": [2, 3], "z": 4}}


def test_merge_dicts_list_values():
    """Test _merge_dicts with list values."""
    d1 = {"tags": ["a", "b"]}
    d2 = {"tags": ["c", "d"]}
    result = _merge_dicts(d1, d2)
    assert result == {"tags": ["a", "b", "c", "d"]}


def test_merge_dicts_mixed_values():
    """Test _merge_dicts converting non-list to list when merging."""
    d1 = {"key": "value1"}
    d2 = {"key": "value2"}
    result = _merge_dicts(d1, d2)
    assert result == {"key": ["value1", "value2"]}


def test_merge_dicts_multiple():
    """Test _merge_dicts with multiple dicts."""
    result = _merge_dicts({"a": 1}, {"b": 2}, {"c": 3}, {"a": 4})
    # Duplicate keys are merged into lists
    assert result == {"a": [1, 4], "b": 2, "c": 3}


def test_merge_dicts_empty():
    """Test _merge_dicts with empty dicts."""
    assert _merge_dicts() == {}
    assert _merge_dicts({}, {}) == {}
    assert _merge_dicts({"a": 1}, {}) == {"a": 1}


def test_classes_ensure_list_string():
    """Test _classes_ensure_list with string input."""
    assert _classes_ensure_list("foo bar baz") == ["foo", "bar", "baz"]
    assert _classes_ensure_list("single") == ["single"]
    # Empty string split returns empty list
    assert _classes_ensure_list("") == []


def test_classes_ensure_list_list():
    """Test _classes_ensure_list with list input."""
    assert _classes_ensure_list(["foo", "bar"]) == ["foo", "bar"]
    assert _classes_ensure_list([]) == []


def test_classes_ensure_list_function():
    """Test _classes_ensure_list with function input."""
    def get_classes():
        return ["dynamic", "classes"]
    
    assert _classes_ensure_list(get_classes) == ["dynamic", "classes"]
    
    def get_string_classes():
        return "foo bar"
    
    assert _classes_ensure_list(get_string_classes) == ["foo", "bar"]


def test_is_function():
    """Test _is_function helper."""
    def regular_func():
        pass
    
    assert _is_function(regular_func)
    assert _is_function(lambda x: x)
    # str.upper is a method_descriptor, not covered by _is_function
    # assert _is_function(str.upper)  # method_descriptor
    assert _is_function(len)  # builtin
    
    # Test bound methods
    s = "test"
    assert _is_function(s.upper)  # bound method
    
    assert not _is_function("string")
    assert not _is_function(123)
    assert not _is_function([1, 2, 3])
    assert not _is_function(None)


def test_flatten_edge_cases():
    """Test _flatten with edge cases."""
    # Test with various non-list types that should be preserved
    class CustomObject:
        pass
    
    obj = CustomObject()
    assert _flatten([1, obj, 3]) == [1, obj, 3]
    
    # Test with dict (should not be flattened)
    assert _flatten([{"a": 1}, {"b": 2}]) == [{"a": 1}, {"b": 2}]
    
    # Test with mixed nesting including None
    assert _flatten([1, [None, [2, None], 3], None, 4]) == [1, 2, 3, 4]


def test_get_selector_type():
    """Test _get_selector_type function."""
    # At-rules
    assert _get_selector_type("@media (max-width: 600px)") == "at-rule"
    assert _get_selector_type("@keyframes spin") == "at-rule"
    assert _get_selector_type("@supports (display: grid)") == "at-rule"
    
    # Parent references
    assert _get_selector_type("&:hover") == "parent-ref"
    assert _get_selector_type("&.active") == "parent-ref"
    assert _get_selector_type("& .child") == "parent-ref"
    
    # Pseudo selectors
    assert _get_selector_type(":hover") == "pseudo"
    assert _get_selector_type(":focus") == "pseudo"
    assert _get_selector_type("::before") == "pseudo"
    assert _get_selector_type("::after") == "pseudo"
    assert _get_selector_type(":first-child") == "pseudo"
    
    # Attribute selectors
    assert _get_selector_type("[disabled]") == "attribute"
    assert _get_selector_type("[type='text']") == "attribute"
    assert _get_selector_type("[data-active]") == "attribute"
    assert _get_selector_type("[data-valid='true']") == "attribute"
    
    # Combinators
    assert _get_selector_type("> .child") == "combinator"
    assert _get_selector_type("+ .sibling") == "combinator"
    assert _get_selector_type("~ .general") == "combinator"
    
    # Regular selectors
    assert _get_selector_type(".class") == "regular"
    assert _get_selector_type("#id") == "regular"
    assert _get_selector_type("div") == "regular"
    assert _get_selector_type(".parent .child") == "regular"


def test_combine_selectors():
    """Test _combine_selectors function."""
    # At-rules (don't combine)
    assert _combine_selectors(".parent", "@media (max-width: 600px)") == "@media (max-width: 600px)"
    
    # Parent references
    assert _combine_selectors(".card", "&:hover") == ".card:hover"
    assert _combine_selectors(".btn", "&.active") == ".btn.active"
    assert _combine_selectors(".list", "& > li") == ".list > li"
    
    # Pseudo selectors
    assert _combine_selectors(".button", ":hover") == ".button:hover"
    assert _combine_selectors(".input", ":focus") == ".input:focus"
    assert _combine_selectors(".element", "::before") == ".element::before"
    
    # Attribute selectors
    assert _combine_selectors(".input", "[disabled]") == ".input[disabled]"
    assert _combine_selectors(".field", "[type='text']") == ".field[type='text']"
    assert _combine_selectors(".item", "[data-active]") == ".item[data-active]"
    
    # Combinators
    assert _combine_selectors(".parent", "> .child") == ".parent > .child"
    assert _combine_selectors(".element", "+ .sibling") == ".element + .sibling"
    assert _combine_selectors(".item", "~ .general") == ".item ~ .general"
    
    # Regular selectors
    assert _combine_selectors(".parent", ".child") == ".parent .child"
    assert _combine_selectors("#container", "div") == "#container div"
    assert _combine_selectors(".nav", "ul li") == ".nav ul li"


def test_combine_selectors_edge_cases():
    """Test _combine_selectors with edge cases."""
    # Empty parent
    assert _combine_selectors("", ".child") == " .child"
    assert _combine_selectors("", ":hover") == ":hover"
    assert _combine_selectors("", "&.active") == ".active"
    
    # Empty child
    assert _combine_selectors(".parent", "") == ".parent "
    
    # Complex selectors
    assert _combine_selectors(".card", "&:not(.disabled)") == ".card:not(.disabled)"
    assert _combine_selectors(".list", "> li:first-child") == ".list > li:first-child"