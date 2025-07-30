"""Tests for the dict2css function."""

from pypertext.hypertext import dict2css


def test_dict2css_simple():
    """Test simple CSS generation."""
    style = {"body": {"background-color": "red", "color": "white"}}
    result = dict2css(style)
    assert result == "body{background-color:red;color:white;}"


def test_dict2css_multiple_selectors():
    """Test multiple CSS selectors."""
    style = {
        "body": {"margin": "0", "padding": "0"},
        "h1": {"font-size": "24px", "color": "blue"}
    }
    result = dict2css(style)
    assert "body{margin:0;padding:0;}" in result
    assert "h1{font-size:24px;color:blue;}" in result


def test_dict2css_string_value():
    """Test CSS with string value instead of dict."""
    style = {"body": "background-color: red;"}
    result = dict2css(style)
    assert result == "body{background-color: red;}"


def test_dict2css_nested_media_query():
    """Test nested media query."""
    style = {
        "@media (max-width: 600px)": {
            "body": {"background-color": "red"},
            ".container": {"width": "100%"}
        }
    }
    result = dict2css(style)
    assert "@media (max-width: 600px){" in result
    assert "body{background-color:red;}" in result
    assert ".container{width:100%;}" in result
    assert result.endswith("}")


def test_dict2css_value_ending_with_brace():
    """Test CSS value ending with brace."""
    style = {"body": {"content": "'}'"}}
    result = dict2css(style)
    assert result == "body{content:'}';}"


def test_dict2css_empty():
    """Test empty dict."""
    result = dict2css({})
    assert result == ""


def test_dict2css_single_property():
    """Test single property."""
    style = {"p": {"color": "green"}}
    result = dict2css(style)
    assert result == "p{color:green;}"


def test_dict2css_class_selector():
    """Test class selector."""
    style = {".container": {"width": "100%", "max-width": "1200px"}}
    result = dict2css(style)
    assert result == ".container{width:100%;max-width:1200px;}"


def test_dict2css_id_selector():
    """Test ID selector."""
    style = {"#header": {"height": "60px", "background": "#333"}}
    result = dict2css(style)
    assert result == "#header{height:60px;background:#333;}"


def test_dict2css_pseudo_selector():
    """Test pseudo selector."""
    style = {"a:hover": {"color": "red", "text-decoration": "underline"}}
    result = dict2css(style)
    assert result == "a:hover{color:red;text-decoration:underline;}"


def test_dict2css_complex_selector():
    """Test complex selector."""
    style = {"div.container > p:first-child": {"margin-top": "0"}}
    result = dict2css(style)
    assert result == "div.container > p:first-child{margin-top:0;}"


def test_dict2css_keyframes():
    """Test keyframes."""
    style = {
        "@keyframes slide": {
            "from": "transform: translateX(0);",
            "to": "transform: translateX(100%);"
        }
    }
    result = dict2css(style)
    assert "@keyframes slide{" in result
    assert "from:transform: translateX(0);" in result
    assert "to:transform: translateX(100%);" in result


def test_dict2css_nested_selectors():
    """Test nested selectors."""
    style = {
        ".card": {
            "padding": "10px",
            "background": "white",
            ".title": {
                "font-size": "20px",
                "color": "blue"
            },
            ".content": {
                "margin-top": "5px"
            }
        }
    }
    result = dict2css(style)
    assert ".card{padding:10px;background:white;}" in result
    assert ".card .title{font-size:20px;color:blue;}" in result
    assert ".card .content{margin-top:5px;}" in result


def test_dict2css_parent_reference():
    """Test parent reference with &."""
    style = {
        ".button": {
            "padding": "10px",
            "&:hover": {
                "background": "blue"
            },
            "&.active": {
                "background": "green"
            }
        }
    }
    result = dict2css(style)
    assert ".button{padding:10px;}" in result
    assert ".button:hover{background:blue;}" in result
    assert ".button.active{background:green;}" in result


def test_dict2css_deeply_nested():
    """Test deeply nested selectors."""
    style = {
        ".nav": {
            "display": "flex",
            "ul": {
                "list-style": "none",
                "li": {
                    "padding": "5px",
                    "a": {
                        "color": "black",
                        "&:hover": {
                            "color": "blue"
                        }
                    }
                }
            }
        }
    }
    result = dict2css(style)
    assert ".nav{display:flex;}" in result
    assert ".nav ul{list-style:none;}" in result
    assert ".nav ul li{padding:5px;}" in result
    assert ".nav ul li a{color:black;}" in result
    assert ".nav ul li a:hover{color:blue;}" in result


def test_dict2css_media_query_nested():
    """Test media query with nested content."""
    style = {
        "@media (max-width: 768px)": {
            ".container": {
                "width": "100%",
                ".header": {
                    "font-size": "18px"
                }
            }
        }
    }
    result = dict2css(style)
    assert "@media (max-width: 768px){" in result
    assert ".container{width:100%;}" in result
    assert ".container .header{font-size:18px;}" in result


def test_dict2css_mixed_properties_and_nested():
    """Test mixing properties and nested selectors."""
    style = {
        ".form": {
            "padding": "20px",
            "background": "#f5f5f5",
            "input": {
                "width": "100%",
                "padding": "5px"
            },
            "button": {
                "margin-top": "10px",
                "&:disabled": {
                    "opacity": "0.5"
                }
            }
        }
    }
    result = dict2css(style)
    assert ".form{padding:20px;background:#f5f5f5;}" in result
    assert ".form input{width:100%;padding:5px;}" in result
    assert ".form button{margin-top:10px;}" in result
    assert ".form button:disabled{opacity:0.5;}" in result


def test_dict2css_pseudo_selectors():
    """Test pseudo-class and pseudo-element selectors."""
    style = {
        ".button": {
            "padding": "10px",
            ":hover": {
                "background": "blue"
            },
            ":focus": {
                "outline": "2px solid red"
            },
            "::before": {
                "content": "'→'"
            },
            "::after": {
                "content": "'←'"
            }
        }
    }
    result = dict2css(style)
    assert ".button{padding:10px;}" in result
    assert ".button:hover{background:blue;}" in result
    assert ".button:focus{outline:2px solid red;}" in result
    assert ".button::before{content:'→';}" in result
    assert ".button::after{content:'←';}" in result


def test_dict2css_attribute_selectors():
    """Test attribute selectors."""
    style = {
        ".input": {
            "border": "1px solid gray",
            "[disabled]": {
                "opacity": "0.5"
            },
            "[type='text']": {
                "padding": "5px"
            },
            "[data-valid='true']": {
                "border-color": "green"
            }
        }
    }
    result = dict2css(style)
    assert ".input{border:1px solid gray;}" in result
    assert ".input[disabled]{opacity:0.5;}" in result
    assert ".input[type='text']{padding:5px;}" in result
    assert ".input[data-valid='true']{border-color:green;}" in result


def test_dict2css_combinator_selectors():
    """Test combinator selectors (>, +, ~)."""
    style = {
        ".parent": {
            "position": "relative",
            "> .child": {
                "margin": "10px"
            },
            "+ .sibling": {
                "border-top": "1px solid"
            },
            "~ .general-sibling": {
                "color": "gray"
            }
        }
    }
    result = dict2css(style)
    assert ".parent{position:relative;}" in result
    assert ".parent > .child{margin:10px;}" in result
    assert ".parent + .sibling{border-top:1px solid;}" in result
    assert ".parent ~ .general-sibling{color:gray;}" in result


def test_dict2css_parent_reference_variations():
    """Test various parent reference (&) patterns."""
    style = {
        ".card": {
            "padding": "20px",
            "&.active": {
                "border": "2px solid blue"
            },
            "&[data-selected]": {
                "background": "yellow"
            },
            "&:not(.disabled)": {
                "cursor": "pointer"
            },
            "& .nested": {
                "margin": "5px"
            }
        }
    }
    result = dict2css(style)
    assert ".card{padding:20px;}" in result
    assert ".card.active{border:2px solid blue;}" in result
    assert ".card[data-selected]{background:yellow;}" in result
    assert ".card:not(.disabled){cursor:pointer;}" in result
    assert ".card .nested{margin:5px;}" in result


def test_dict2css_complex_nested_selectors():
    """Test complex nested selector combinations."""
    style = {
        ".list": {
            "list-style": "none",
            "> li": {
                "padding": "5px",
                ":first-child": {
                    "border-top": "none"
                },
                ":last-child": {
                    "border-bottom": "none"
                },
                "[data-active]": {
                    "background": "lightblue",
                    "::before": {
                        "content": "'*'"
                    }
                }
            }
        }
    }
    result = dict2css(style)
    assert ".list{list-style:none;}" in result
    assert ".list > li{padding:5px;}" in result
    assert ".list > li:first-child{border-top:none;}" in result
    assert ".list > li:last-child{border-bottom:none;}" in result
    assert ".list > li[data-active]{background:lightblue;}" in result
    assert ".list > li[data-active]::before{content:'*';}" in result


def test_dict2css_at_rules_with_nested():
    """Test @media and other at-rules with nested content."""
    style = {
        "@media (max-width: 768px)": {
            ".container": {
                "width": "100%",
                "> .row": {
                    "flex-direction": "column"
                }
            },
            "@supports (display: grid)": {
                ".grid": {
                    "display": "grid"
                }
            }
        }
    }
    result = dict2css(style)
    assert "@media (max-width: 768px){" in result
    assert ".container{width:100%;}" in result
    assert ".container > .row{flex-direction:column;}" in result
    assert "@supports (display: grid){" in result
    assert ".grid{display:grid;}" in result


def test_dict2css_edge_cases():
    """Test edge cases for selector combinations."""
    style = {
        "": {  # Empty selector
            "color": "red"
        },
        " .spaced": {  # Selector with leading space
            "margin": "10px"
        },
        ".parent": {
            "": {  # Empty nested selector
                "padding": "5px"
            },
            " ": {  # Space as selector
                "border": "1px solid"
            }
        }
    }
    result = dict2css(style)
    # These edge cases should still produce valid CSS
    assert "{color:red;}" in result
    assert " .spaced{margin:10px;}" in result