# Pypertext

Create HTML elements the Pythonic way with a chainable, expressive API.

```python
from pypertext import ht

page = ht.div(
    ht.h1("Welcome to Pypertext"),
    ht.p("Build HTML with Python!", style={"color": "blue"}),
    classes=["container", "page"],
    id="main-content"
)
print(page)
# <div class="container page" id="main-content">
#   <h1>Welcome to Pypertext</h1>
#   <p style="color: blue;">Build HTML with Python!</p>
# </div>
```

## Install

```bash
pip install pypertext
```

## Core Features

### 🏗️ Element Creation with `ht`

Create any HTML element using the `ht` factory:

```python
from pypertext import ht

# Basic elements
ht.div("Hello World")
ht.span("Text", id="my-span")
ht.button("Click me", type="submit", classes=["btn", "primary"])

# Self-closing elements
ht.img(src="image.jpg", alt="Description")
ht.input(type="text", placeholder="Enter name")
ht.br()
```

### ⛓️ Chainable Operations

Build complex HTML structures with method chaining and operators:

```python
# Using + operator to add children
container = ht.div(classes=["container"])
container + ht.h1("Title") + ht.p("Content") + ht.button("Action")

# Using += for incremental building
form = ht.form(action="/submit", method="post")
form += ht.input(type="text", name="username", placeholder="Username")
form += ht.input(type="password", name="password", placeholder="Password")
form += ht.button("Login", type="submit")

# Using call syntax for chaining
nav = ht.nav()
nav(
    ht.a("Home", href="/"),
    ht.a("About", href="/about"),
    ht.a("Contact", href="/contact"),
    classes=["navigation"]
)
```

### 🎨 Dynamic Styling with dict2css

Convert Python dictionaries to CSS with support for nested selectors:

```python
from pypertext import dict2css, ht

# Simple CSS
styles = {
    "body": {"margin": "0", "font-family": "Arial, sans-serif"},
    ".container": {"max-width": "1200px", "margin": "0 auto"}
}

# Nested selectors with pseudo-classes
advanced_styles = {
    ".card": {
        "padding": "20px",
        "border": "1px solid #ddd",
        ":hover": {"box-shadow": "0 4px 8px rgba(0,0,0,0.1)"},
        ".title": {"font-size": "1.5rem", "margin-bottom": "10px"},
        "&.featured": {"border-color": "gold"},
        "> .content": {"line-height": "1.6"}
    }
}

css = dict2css(advanced_styles)
ht.style(css)  # <style>{".card": ...}</style>
```

### 📄 Full Document Creation

Create complete HTML documents with the `Document` class:

```python
from pypertext import Document, ht

# Basic document
doc = Document(page_title="My Website")
doc += ht.header(
    ht.nav(
        ht.a("Home", href="/"),
        ht.a("Blog", href="/blog"),
        classes=["main-nav"]
    )
)
doc += ht.main(
    ht.h1("Welcome"),
    ht.p("This is my website built with Pypertext!"),
    classes=["content"]
)
doc += ht.footer("© 2025 My Website")

print(doc)
# Outputs complete HTML document with DOCTYPE, head, and body
```

### 🔧 Flexible Content Types

Add almost any type of content as children:

```python
# Strings and numbers
ht.div("Text content", 42, 3.14)

# Lists and iterables
ht.ul([ht.li(item) for item in ["Apple", "Banana", "Cherry"]])

# Functions for dynamic content
def get_current_time() -> str:
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

ht.div("Current time: ", get_current_time)

# Other elements
header = ht.header(ht.h1("Site Title"))
main = ht.main("Content")
page = ht.div(header, main, classes=["page-layout"])
```

### 🏷️ Modify elements

```python
element = ht.div("Content")

# Add classes
element.add_classes("container", "primary")
element.add_classes(["responsive", "animated"])

# Check for classes
if element.has_classes("container", "primary"):
    print("Has required classes")

# Remove classes
element.remove_classes("animated")

# Merge with existing classes
element.merge_attrs(classes=["new-class"])

# Append children
element.append(ht.div("Child"))

# Extend children
element.extend(ht.div("Hello"), ht.div("World"))

# Insert children at index position
element.insert(0, ht.div("First"))
```

### 📝 Attribute Handling

Flexible attribute management:

```python
# Set attributes
button = ht.button("Submit")
button.set_attrs(type="submit", disabled=True, data_action="form-submit")

# Merge attributes (combines values for duplicate keys)
button.merge_attrs(classes=["btn"], data_extra="value")

# Dictionary-style attribute assignment
form = ht.form() + {"method": "post", "action": "/submit"}

# Style dictionaries
styled_div = ht.div(
    "Styled content",
    style={"background": "blue", "color": "white", "padding": "10px"}
)

# Private attributes starting with an underscore hold state and are not rendered
el = ht.div("Private state", _metadata={"key": "value"})
el.attributes["_metadata"]  # Access private attributes
```

### 🔄 Method Chaining and Pipes

Chain operations for readable code:

```python
# Method chaining
result = (
    ht.div("Base content")
    .add_classes("container", "main")
    .set_attrs(id="content-area")
    .append(ht.p("Additional paragraph"))
)

# Pipe pattern for custom transformations
def add_bootstrap_classes(element):
    element.add_classes("d-flex", "justify-content-center")
    return element

def add_data_attributes(element, **data):
    for key, value in data.items():
        element.set_attrs(**{f"data_{key}": value})
    return element

card = (
    ht.div("Card content")
    .pipe(add_bootstrap_classes)
    .pipe(add_data_attributes, toggle="modal", target="#myModal")
)
```

### 🌐 ASGI Integration

Use Document as an ASGI application with Starlette/FastAPI:

```python
from starlette.applications import Starlette
from starlette.routing import Route
from pypertext import Document, ht

async def homepage(request):
    doc = Document(page_title="My App")
    doc += ht.h1("Hello from Pypertext!")
    doc += ht.p("This page was generated with Python")
    return doc

async def user_profile(request):
    username = request.path_params['username']
    doc = Document(page_title=f"Profile - {username}")
    doc += ht.h1(f"Welcome, {username}!")
    doc += ht.p("Your profile page")
    return doc

app = Starlette(routes=[
    Route("/", homepage),
    Route("/user/{username}", user_profile),
])
```

### 🧩 Custom Components

Create reusable components:

```python
def card(title, content, **attrs):
    return ht.div(
        ht.div(title, classes=["card-title"]),
        ht.div(content, classes=["card-content"]),
        classes=["card"],
        **attrs
    )

def alert(message, type="info"):
    return ht.div(
        message,
        classes=["alert", f"alert-{type}"],
        role="alert"
    )

# Usage
page = ht.div(
    card("Welcome", "This is a reusable card component"),
    alert("Success! Your data was saved.", type="success"),
    classes=["page"]
)
```

Any class with `get_element` method can be used as an Element:

```python
class Book:
    def __init__(self, title: str, author: str):
        self.title = title
        self.author = author

    def get_element(self):
        return ht.div(
            ht.h2(self.title, classes=["book-title"]),
            ht.p(f"by {self.author}", classes=["book-author"]),
            classes=["book"]
        )

book = Book("1984", "George Orwell")
page = ht.div(
    book,
    classes=["book-page"]
)
```

### CSS-in-Python Styling

```python
app_styles = {
    ":root": {
        "--primary-color": "#007bff",
        "--secondary-color": "#6c757d",
        "--font-family": "system-ui, sans-serif"
    },
    "body": {
        "font-family": "var(--font-family)",
        "line-height": "1.6",
        "margin": "0"
    },
    ".container": {
        "max-width": "1200px",
        "margin": "0 auto",
        "padding": "0 20px"
    },
    ".btn": {
        "display": "inline-block",
        "padding": "0.5rem 1rem",
        "border": "none",
        "border-radius": "0.25rem",
        "cursor": "pointer",
        "text-decoration": "none",
        "&:hover": {
            "opacity": "0.8"
        },
        "&.btn-primary": {
            "background-color": "var(--primary-color)",
            "color": "white"
        }
    },
    "@media (max-width: 768px)": {
        ".container": {
            "padding": "0 10px"
        },
        ".btn": {
            "width": "100%",
            "text-align": "center"
        }
    }
}

# Create complete styled page
doc = Document(page_title="Styled App")
doc.head += ht.style(dict2css(app_styles))
doc += ht.div(
    ht.h1("Styled with Pypertext"),
    ht.p("This page uses CSS-in-Python styling"),
    ht.button("Click me", classes=["btn", "btn-primary"]),
    classes=["container"]
)
```

## API Reference

### Core Classes

- **`ht`**: Factory for creating HTML elements
- **`Element`**: Base class for all HTML elements with chainable methods
- **`Document`**: Specialized element for complete HTML documents with ASGI support
- **`dict2css`**: Function to convert Python dictionaries to CSS strings

### Element Methods

- **`.add_classes(*classes)`**: Add CSS classes
- **`.remove_classes(*classes)`**: Remove CSS classes  
- **`.has_classes(*classes)`**: Check if element has classes
- **`.set_attrs(**attrs)`**: Set attributes (replaces existing)
- **`.merge_attrs(**attrs)`**: Merge attributes (combines existing)
- **`.append(*children)`**: Add children to element
- **`.extend(*children)`**: Extend children elements
- **`.insert(index, *children)`**: Insert children at specific position
- **`.pipe(function, *args, **kwargs)`**: Apply custom function to element

### Document attributes

- **`.head`**: `<head>` Element, contains `<title>`, `<style>`, etc.
- **`.body`**: `<body>` Element, contains main children of the document
- **`.title`**: `<title>` Element, holds the document title
- **`.html`**: `<html>` Element, root of the document
- **`.page_title`**: String, title of the document for `<title>` tag
- **`.headers`**: A dictionary of response headers used in ASGI responses
- **`.status_code`**: Integer, HTTP status code for ASGI responses

## Changes

- **0.1.5** - Element attributes starting with underscores are now ignored and treated as private attributes to hold state.
- **0.1.4** - Improved rendering efficiency, dict2css can handle nested selectors and various types of CSS values. Added ElementChild type for better type hinting.
- **0.1.3** - Added the setup_logging function to configure logging.
- **0.1.2** - Replaced dict-based elements to class-based elements with the Element class.