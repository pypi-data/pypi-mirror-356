"""Tests for the Bootstrap module."""

import pytest
from pypertext import ht
from pypertext.bootstrap import (
    Container, Row, Col, Stack, Heading, Text, Button, ButtonGroup,
    Form, FormGroup, Input, Select, Textarea, Checkbox, Radio,
    Card, CardGroup, CardDeck, Nav, NavItem, Navbar, Alert, Badge,
    Progress, ListGroup, ListGroupItem, Modal, ModalTrigger, Table,
    Spinner, Accordion, Breadcrumb, Pagination, padding, margin,
    display, flex, cdn_bootstrap_css, cdn_bootstrap_js, BootstrapDocument,
    Breakpoint, Spacing, Dropdown, DropdownItem, DropdownDivider,
    Collapse, CollapseToggle, TabContent, TabPane, Carousel, CarouselItem,
    Offcanvas, OffcanvasTrigger, Toast, ToastContainer, Tooltip, Popover,
    InputGroup, InputGroupText, Figure, CloseButton, Range, Switch,
    FileInput, Ratio, VisuallyHidden, StretchedLink
)


class TestLayoutComponents:
    """Test layout components."""

    def test_container_default(self):
        """Test default container."""
        container = Container("Hello World")
        assert container.tag == "div"
        assert "container" in container.attributes.get("classes", [])
        assert container.children[0] == "Hello World"

    def test_container_fluid(self):
        """Test fluid container."""
        container = Container("Hello", fluid=True)
        assert "container-fluid" in container.attributes.get("classes", [])

    def test_container_fluid_breakpoint(self):
        """Test fluid container with breakpoint."""
        container = Container("Hello", fluid="md")
        assert "container-md" in container.attributes.get("classes", [])

    def test_row_basic(self):
        """Test basic row."""
        row = Row("content")
        assert row.tag == "div"
        assert "row" in row.attributes.get("classes", [])

    def test_row_with_columns(self):
        """Test row with column configuration."""
        row = Row(cols=2, cols_md=3, g=3)
        classes = row.attributes.get("classes", [])
        assert "row" in classes
        assert "row-cols-2" in classes
        assert "row-cols-md-3" in classes
        assert "g-3" in classes

    def test_row_alignment(self):
        """Test row alignment."""
        row = Row(align="center", justify="between")
        classes = row.attributes.get("classes", [])
        assert "align-items-center" in classes
        assert "justify-content-between" in classes

    def test_col_basic(self):
        """Test basic column."""
        col = Col("content")
        assert col.tag == "div"
        assert "col" in col.attributes.get("classes", [])

    def test_col_with_span(self):
        """Test column with span."""
        col = Col("content", span=6)
        assert "col-6" in col.attributes.get("classes", [])

    def test_col_auto_width(self):
        """Test column with auto width."""
        col = Col("content", span=True)
        assert "col" in col.attributes.get("classes", [])

    def test_col_responsive(self):
        """Test responsive column."""
        col = Col("content", sm=12, md=6, lg=4)
        classes = col.attributes.get("classes", [])
        assert "col-sm-12" in classes
        assert "col-md-6" in classes
        assert "col-lg-4" in classes

    def test_col_offset(self):
        """Test column offset."""
        col = Col("content", offset=2, offset_md=3)
        classes = col.attributes.get("classes", [])
        assert "offset-2" in classes
        assert "offset-md-3" in classes

    def test_col_order(self):
        """Test column order."""
        col = Col("content", order="first")
        assert "order-first" in col.attributes.get("classes", [])

    def test_stack_vertical(self):
        """Test vertical stack."""
        stack = Stack("item1", "item2", gap=3)
        classes = stack.attributes.get("classes", [])
        assert "vstack" in classes
        assert "gap-3" in classes

    def test_stack_horizontal(self):
        """Test horizontal stack."""
        stack = Stack("item1", "item2", direction="horizontal", gap=2)
        classes = stack.attributes.get("classes", [])
        assert "hstack" in classes
        assert "gap-2" in classes

    def test_stack_alignment(self):
        """Test stack alignment."""
        stack = Stack(align="center", justify="between", wrap=True)
        classes = stack.attributes.get("classes", [])
        assert "align-items-center" in classes
        assert "justify-content-between" in classes
        assert "flex-wrap" in classes


class TestTypographyComponents:
    """Test typography components."""

    def test_heading_basic(self):
        """Test basic heading."""
        heading = Heading("Test Title", level=2)
        assert heading.tag == "h2"
        assert heading.children[0] == "Test Title"

    def test_heading_display(self):
        """Test heading with display size."""
        heading = Heading("Big Title", level=1, display=3)
        assert "display-3" in heading.attributes.get("classes", [])

    def test_text_basic(self):
        """Test basic text."""
        text = Text("Hello World")
        assert text.tag == "p"
        assert text.children[0] == "Hello World"

    def test_text_lead(self):
        """Test lead text."""
        text = Text("Important text", lead=True)
        assert "lead" in text.attributes.get("classes", [])

    def test_text_formatting(self):
        """Test text formatting."""
        text = Text("Formatted", size=4, weight="bold", style="italic")
        classes = text.attributes.get("classes", [])
        assert "fs-4" in classes
        assert "fw-bold" in classes
        assert "fst-italic" in classes

    def test_text_alignment(self):
        """Test text alignment."""
        text = Text("Centered", align="center")
        assert "text-center" in text.attributes.get("classes", [])

    def test_text_color(self):
        """Test text color."""
        text = Text("Colored", color="success", bg="warning")
        classes = text.attributes.get("classes", [])
        assert "text-success" in classes
        assert "bg-warning" in classes


class TestButtonComponents:
    """Test button components."""

    def test_button_basic(self):
        """Test basic button."""
        button = Button("Click me")
        assert button.tag == "button"
        assert button.children[0] == "Click me"
        assert "btn" in button.attributes.get("classes", [])
        assert "btn-primary" in button.attributes.get("classes", [])

    def test_button_variant(self):
        """Test button variant."""
        button = Button("Save", variant="success")
        assert "btn-success" in button.attributes.get("classes", [])

    def test_button_outline(self):
        """Test outline button."""
        button = Button("Cancel", variant="secondary", outline=True)
        assert "btn-outline-secondary" in button.attributes.get("classes", [])

    def test_button_size(self):
        """Test button size."""
        button = Button("Small", size="sm")
        assert "btn-sm" in button.attributes.get("classes", [])

    def test_button_disabled(self):
        """Test disabled button."""
        button = Button("Disabled", disabled=True)
        assert button.attributes.get("disabled") is True

    def test_button_link(self):
        """Test button as link."""
        button = Button("Link", href="/test")
        assert button.tag == "a"
        assert button.attributes.get("href") == "/test"
        assert button.attributes.get("role") == "button"

    def test_button_block(self):
        """Test block button."""
        button = Button("Block", block=True)
        classes = button.attributes.get("classes", [])
        assert "d-block" in classes
        assert "w-100" in classes

    def test_button_group_basic(self):
        """Test basic button group."""
        group = ButtonGroup(Button("One"), Button("Two"))
        assert group.tag == "div"
        assert "btn-group" in group.attributes.get("classes", [])
        assert group.attributes.get("role") == "group"

    def test_button_group_vertical(self):
        """Test vertical button group."""
        group = ButtonGroup(Button("One"), vertical=True)
        assert "btn-group-vertical" in group.attributes.get("classes", [])

    def test_button_group_size(self):
        """Test button group size."""
        group = ButtonGroup(Button("One"), size="lg")
        assert "btn-group-lg" in group.attributes.get("classes", [])


class TestFormComponents:
    """Test form components."""

    def test_form_basic(self):
        """Test basic form."""
        form = Form()
        assert form.tag == "form"
        assert "vstack" in form.attributes.get("classes", [])
        assert form.attributes.get("method") == "post"

    def test_form_inline(self):
        """Test inline form."""
        form = Form(inline=True, gap=2)
        classes = form.attributes.get("classes", [])
        assert "row" in classes
        assert "row-cols-lg-auto" in classes
        assert "align-items-center" in classes
        assert "g-2" in classes

    def test_form_validated(self):
        """Test validated form."""
        form = Form(validated=True)
        assert "was-validated" in form.attributes.get("classes", [])

    def test_form_group_basic(self):
        """Test basic form group."""
        group = FormGroup()
        assert group.tag == "div"
        assert "mb-3" in group.attributes.get("classes", [])

    def test_form_group_floating(self):
        """Test floating form group."""
        group = FormGroup(floating=True)
        assert "form-floating" in group.attributes.get("classes", [])

    def test_input_basic(self):
        """Test basic input."""
        input_el = Input(name="test", value="hello")
        assert input_el.tag == "input"
        assert "form-control" in input_el.attributes.get("classes", [])
        assert input_el.attributes.get("name") == "test"
        assert input_el.attributes.get("value") == "hello"

    def test_input_with_label(self):
        """Test input with label."""
        input_el = Input(name="email", label="Email Address")
        element = input_el.get_element()
        # Should return a FormGroup with label and input
        assert element.tag == "div"
        assert "mb-3" in element.attributes.get("classes", [])

    def test_input_floating_label(self):
        """Test input with floating label."""
        input_el = Input(name="email", label="Email", floating_label=True)
        element = input_el.get_element()
        # Should return a FormGroup with form-floating class
        assert "form-floating" in element.attributes.get("classes", [])

    def test_select_basic(self):
        """Test basic select."""
        select = Select(name="choice", options=["A", "B", "C"])
        assert select.tag == "select"
        assert "form-select" in select.attributes.get("classes", [])
        assert len(select.children) == 3

    def test_select_with_tuples(self):
        """Test select with value/label tuples."""
        options = [("val1", "Label 1"), ("val2", "Label 2")]
        select = Select(name="choice", options=options)
        assert len(select.children) == 2

    def test_select_with_placeholder(self):
        """Test select with placeholder."""
        select = Select(name="choice", options=["A", "B"], placeholder="Choose...")
        # Should have placeholder + options
        assert len(select.children) == 3

    def test_textarea_basic(self):
        """Test basic textarea."""
        textarea = Textarea(name="message", value="Hello")
        assert textarea.tag == "textarea"
        assert "form-control" in textarea.attributes.get("classes", [])
        assert textarea.attributes.get("rows") == 3

    def test_checkbox_basic(self):
        """Test basic checkbox."""
        checkbox = Checkbox(name="agree", label="I agree", checked=True)
        assert checkbox.tag == "div"
        assert "form-check" in checkbox.attributes.get("classes", [])
        # Should have input and label children
        assert len(checkbox.children) == 2

    def test_checkbox_switch(self):
        """Test checkbox as switch."""
        checkbox = Checkbox(name="toggle", switch=True)
        assert "form-switch" in checkbox.attributes.get("classes", [])

    def test_radio_basic(self):
        """Test basic radio button."""
        radio = Radio(name="option", value="yes", label="Yes")
        assert radio.tag == "div"
        assert "form-check" in radio.attributes.get("classes", [])


class TestCardComponents:
    """Test card components."""

    def test_card_basic(self):
        """Test basic card."""
        card = Card(title="Test Card", body="Card content")
        assert card.tag == "div"
        assert "card" in card.attributes.get("classes", [])

    def test_card_with_image(self):
        """Test card with image."""
        card = Card(img_src="/test.jpg", img_alt="Test")
        assert "card" in card.attributes.get("classes", [])

    def test_card_colors(self):
        """Test card colors."""
        card = Card(color="success")
        assert "text-bg-success" in card.attributes.get("classes", [])

    def test_card_group(self):
        """Test card group."""
        group = CardGroup(Card(title="Card 1"), Card(title="Card 2"))
        assert "card-group" in group.attributes.get("classes", [])

    def test_card_deck(self):
        """Test card deck."""
        deck = CardDeck(Card(title="Card 1"), cols_md=2, gap=4)
        classes = deck.attributes.get("classes", [])
        assert "row" in classes
        assert "g-4" in classes


class TestNavigationComponents:
    """Test navigation components."""

    def test_nav_basic(self):
        """Test basic nav."""
        nav = Nav()
        assert nav.tag == "ul"
        assert "nav" in nav.attributes.get("classes", [])

    def test_nav_tabs(self):
        """Test nav tabs."""
        nav = Nav(style="tabs")
        assert "nav-tabs" in nav.attributes.get("classes", [])

    def test_nav_vertical(self):
        """Test vertical nav."""
        nav = Nav(vertical=True)
        assert "flex-column" in nav.attributes.get("classes", [])

    def test_nav_item(self):
        """Test nav item."""
        item = NavItem("Home", href="/", active=True)
        assert item.tag == "li"
        assert "nav-item" in item.attributes.get("classes", [])

    def test_navbar_basic(self):
        """Test basic navbar."""
        navbar = Navbar(brand="My App")
        assert navbar.tag == "nav"
        assert "navbar" in navbar.attributes.get("classes", [])


class TestAlertComponents:
    """Test alert components."""

    def test_alert_basic(self):
        """Test basic alert."""
        alert = Alert("Test message")
        assert alert.tag == "div"
        classes = alert.attributes.get("classes", [])
        assert "alert" in classes
        assert "alert-primary" in classes
        assert alert.attributes.get("role") == "alert"

    def test_alert_variant(self):
        """Test alert variant."""
        alert = Alert("Warning!", variant="warning")
        assert "alert-warning" in alert.attributes.get("classes", [])

    def test_alert_dismissible(self):
        """Test dismissible alert."""
        alert = Alert("Dismissible", dismissible=True)
        assert "alert-dismissible" in alert.attributes.get("classes", [])

    def test_badge_basic(self):
        """Test basic badge."""
        badge = Badge("New")
        assert badge.tag == "span"
        classes = badge.attributes.get("classes", [])
        assert "badge" in classes
        assert "text-bg-primary" in classes

    def test_badge_pill(self):
        """Test pill badge."""
        badge = Badge("5", pill=True)
        assert "rounded-pill" in badge.attributes.get("classes", [])


class TestProgressComponents:
    """Test progress components."""

    def test_progress_basic(self):
        """Test basic progress."""
        progress = Progress(value=50)
        assert progress.tag == "div"
        assert "progress" in progress.attributes.get("classes", [])
        # Should have progress bar child
        assert len(progress.children) == 1

    def test_progress_striped(self):
        """Test striped progress."""
        progress = Progress(value=75, striped=True, animated=True)
        assert "progress" in progress.attributes.get("classes", [])


class TestListComponents:
    """Test list group components."""

    def test_list_group_basic(self):
        """Test basic list group."""
        list_group = ListGroup()
        assert list_group.tag == "ul"
        assert "list-group" in list_group.attributes.get("classes", [])

    def test_list_group_numbered(self):
        """Test numbered list group."""
        list_group = ListGroup(numbered=True)
        assert list_group.tag == "ol"
        assert "list-group-numbered" in list_group.attributes.get("classes", [])

    def test_list_group_horizontal(self):
        """Test horizontal list group."""
        list_group = ListGroup(horizontal=True)
        assert "list-group-horizontal" in list_group.attributes.get("classes", [])

    def test_list_group_item(self):
        """Test list group item."""
        item = ListGroupItem("Item 1", active=True)
        assert item.tag == "li"
        classes = item.attributes.get("classes", [])
        assert "list-group-item" in classes
        assert "active" in classes

    def test_list_group_item_link(self):
        """Test list group item as link."""
        item = ListGroupItem("Link", href="/test")
        assert item.tag == "a"
        assert item.attributes.get("href") == "/test"


class TestModalComponents:
    """Test modal components."""

    def test_modal_basic(self):
        """Test basic modal."""
        modal = Modal(id="test-modal", title="Test Modal", body="Modal content")
        assert modal.tag == "div"
        classes = modal.attributes.get("classes", [])
        assert "modal" in classes
        assert "fade" in classes
        assert modal.attributes.get("id") == "test-modal"

    def test_modal_size(self):
        """Test modal size."""
        modal = Modal(id="big-modal", size="lg")
        assert modal.tag == "div"

    def test_modal_trigger(self):
        """Test modal trigger."""
        trigger = ModalTrigger("Open Modal", target="test-modal")
        assert trigger.attributes.get("data_bs_toggle") == "modal"
        assert trigger.attributes.get("data_bs_target") == "#test-modal"


class TestTableComponents:
    """Test table components."""

    def test_table_basic(self):
        """Test basic table."""
        headers = ["Name", "Age"]
        rows = [{"Name": "John", "Age": 30}, {"Name": "Jane", "Age": 25}]
        table = Table(headers=headers, rows=rows)
        
        # Test internal properties
        assert table._headers == headers
        assert table._rows == rows

    def test_table_formatting(self):
        """Test table formatting methods."""
        headers = ["Name", "Price"]
        rows = [{"Name": "Product A", "Price": 19.99}]
        table = Table(headers=headers, rows=rows)
        
        # Test method chaining
        formatted_table = table.fmt_currency("Price").cols_align("Price", "end")
        assert "Price" in formatted_table._formatters
        assert formatted_table._column_alignments["Price"] == "end"

    def test_table_striped(self):
        """Test striped table."""
        table = Table(striped=True, hover=True)
        assert table._striped is True
        assert table._hover is True

    def test_table_responsive(self):
        """Test responsive table."""
        table = Table(responsive=True)
        assert table._responsive is True


class TestUtilityComponents:
    """Test utility components."""

    def test_spinner_basic(self):
        """Test basic spinner."""
        spinner = Spinner()
        assert spinner.tag == "div"
        assert "spinner-border" in spinner.attributes.get("classes", [])
        assert spinner.attributes.get("role") == "status"

    def test_spinner_grow(self):
        """Test growing spinner."""
        spinner = Spinner(style="grow", size="sm")
        assert "spinner-grow" in spinner.attributes.get("classes", [])
        assert "spinner-grow-sm" in spinner.attributes.get("classes", [])

    def test_accordion_basic(self):
        """Test basic accordion."""
        items = [("Item 1", "Content 1"), ("Item 2", "Content 2")]
        accordion = Accordion(id="test-accordion", items=items)
        assert accordion.tag == "div"
        assert "accordion" in accordion.attributes.get("classes", [])
        assert accordion.attributes.get("id") == "test-accordion"

    def test_breadcrumb_basic(self):
        """Test basic breadcrumb."""
        items = [("Home", "/"), ("Products", "/products"), ("Item", None)]
        breadcrumb = Breadcrumb(items=items)
        assert breadcrumb.tag == "nav"
        assert breadcrumb.attributes.get("aria_label") == "breadcrumb"

    def test_pagination_basic(self):
        """Test basic pagination."""
        pagination = Pagination(current=2, total=5)
        assert pagination.tag == "nav"
        assert pagination.attributes.get("aria_label") == "Pagination"


class TestUtilityFunctions:
    """Test utility functions."""

    def test_padding_utility(self):
        """Test padding utility function."""
        element = ht.div("content")
        padded = padding(element, all=3, top=2)
        classes = padded.attributes.get("classes", [])
        assert "p-3" in classes
        assert "pt-2" in classes

    def test_margin_utility(self):
        """Test margin utility function."""
        element = ht.div("content")
        margined = margin(element, x=2, bottom="auto")
        classes = margined.attributes.get("classes", [])
        assert "mx-2" in classes
        assert "mb-auto" in classes

    def test_display_utility(self):
        """Test display utility function."""
        element = ht.div("content")
        displayed = display(element, "none", breakpoint="md")
        assert "d-md-none" in element.attributes.get("classes", [])

    def test_flex_utility(self):
        """Test flex utility function."""
        element = ht.div("content")
        flexed = flex(element, direction="column", justify="center", align="center")
        classes = flexed.attributes.get("classes", [])
        assert "d-flex" in classes
        assert "flex-column" in classes
        assert "justify-content-center" in classes
        assert "align-items-center" in classes


class TestCDNHelpers:
    """Test CDN helper functions."""

    def test_cdn_bootstrap_css(self):
        """Test Bootstrap CSS CDN helper."""
        css_link = cdn_bootstrap_css()
        assert css_link.tag == "link"
        assert css_link.attributes.get("rel") == "stylesheet"
        assert "bootstrap" in css_link.attributes.get("href", "")

    def test_cdn_bootstrap_css_with_theme(self):
        """Test Bootstrap CSS with theme."""
        css_link = cdn_bootstrap_css(theme="darkly")
        assert "bootswatch" in css_link.attributes.get("href", "")
        assert "darkly" in css_link.attributes.get("href", "")

    def test_cdn_bootstrap_js(self):
        """Test Bootstrap JS CDN helper."""
        js_script = cdn_bootstrap_js()
        assert js_script.tag == "script"
        assert "bootstrap" in js_script.attributes.get("src", "")


class TestBootstrapDocument:
    """Test Bootstrap document."""

    def test_bootstrap_document_basic(self):
        """Test basic Bootstrap document."""
        doc = BootstrapDocument("Hello World")
        assert doc.html.attributes.get("data_bs_theme") == "dark"
        # Should have Bootstrap CSS and JS included
        assert len(doc.head.children) > 0


class TestEnums:
    """Test enum classes."""

    def test_breakpoint_enum(self):
        """Test Breakpoint enum."""
        assert Breakpoint.SM == "sm"
        assert Breakpoint.MD == "md"
        assert Breakpoint.XS == ""

    def test_spacing_enum(self):
        """Test Spacing enum."""
        assert Spacing.AUTO == "auto"
        assert Spacing.ZERO == "0"
        assert Spacing.THREE == "3"


class TestComplexExamples:
    """Test complex component combinations."""

    def test_card_with_form(self):
        """Test card containing a form."""
        form = Form(
            Input(name="email", label="Email", type="email"),
            Button("Submit", type="submit")
        )
        card = Card(title="Login", body=form)
        
        assert card.tag == "div"
        assert "card" in card.attributes.get("classes", [])

    def test_navbar_with_items(self):
        """Test navbar with navigation items."""
        nav_items = [
            NavItem("Home", href="/", active=True),
            NavItem("About", href="/about"),
            NavItem("Contact", href="/contact")
        ]
        navbar = Navbar(brand="My Site", items=nav_items)
        
        assert navbar.tag == "nav"
        assert "navbar" in navbar.attributes.get("classes", [])

    def test_responsive_layout(self):
        """Test responsive layout with grid."""
        layout = Container(
            Row(
                Col("Content 1", md=6),
                Col("Content 2", md=6),
                g=3
            )
        )
        
        assert layout.tag == "div"
        assert "container" in layout.attributes.get("classes", [])


class TestDropdownComponents:
    """Test dropdown components."""

    def test_dropdown_basic(self):
        """Test basic dropdown."""
        trigger = Button("Dropdown")
        items = ["Action", "Another action"]
        dropdown = Dropdown(trigger, items)
        
        assert dropdown.tag == "div"
        assert "dropdown" in dropdown.attributes.get("classes", [])

    def test_dropdown_direction(self):
        """Test dropdown direction."""
        trigger = Button("Drop up")
        dropdown = Dropdown(trigger, [], direction="up")
        assert "dropup" in dropdown.attributes.get("classes", [])

    def test_dropdown_item_basic(self):
        """Test basic dropdown item."""
        item = DropdownItem("Action")
        assert item.tag == "li"

    def test_dropdown_item_link(self):
        """Test dropdown item as link."""
        item = DropdownItem("Link", href="/test")
        assert item.tag == "li"

    def test_dropdown_item_header(self):
        """Test dropdown item as header."""
        item = DropdownItem("Header", header=True)
        assert item.tag == "li"

    def test_dropdown_divider(self):
        """Test dropdown divider."""
        divider = DropdownDivider()
        assert divider.tag == "li"


class TestCollapseComponents:
    """Test collapse components."""

    def test_collapse_basic(self):
        """Test basic collapse."""
        collapse = Collapse(id="test-collapse", content="Collapsible content")
        assert collapse.tag == "div"
        assert "collapse" in collapse.attributes.get("classes", [])
        assert collapse.attributes.get("id") == "test-collapse"

    def test_collapse_show(self):
        """Test collapse initially shown."""
        collapse = Collapse(id="test", content="Content", show=True)
        assert "show" in collapse.attributes.get("classes", [])

    def test_collapse_horizontal(self):
        """Test horizontal collapse."""
        collapse = Collapse(id="test", content="Content", horizontal=True)
        assert "collapse-horizontal" in collapse.attributes.get("classes", [])

    def test_collapse_toggle(self):
        """Test collapse toggle button."""
        toggle = CollapseToggle("Toggle", target="test-collapse")
        assert toggle.attributes.get("data_bs_toggle") == "collapse"
        assert toggle.attributes.get("data_bs_target") == "#test-collapse"


class TestTabComponents:
    """Test tab components."""

    def test_tab_content_basic(self):
        """Test basic tab content."""
        content = TabContent()
        assert content.tag == "div"
        assert "tab-content" in content.attributes.get("classes", [])

    def test_tab_pane_basic(self):
        """Test basic tab pane."""
        pane = TabPane(id="test-pane", content="Pane content")
        assert pane.tag == "div"
        assert "tab-pane" in pane.attributes.get("classes", [])
        assert pane.attributes.get("id") == "test-pane"

    def test_tab_pane_active(self):
        """Test active tab pane."""
        pane = TabPane(id="test", content="Content", active=True)
        classes = pane.attributes.get("classes", [])
        assert "active" in classes
        assert "show" in classes

    def test_tab_pane_fade(self):
        """Test tab pane with fade."""
        pane = TabPane(id="test", content="Content", fade=True)
        assert "fade" in pane.attributes.get("classes", [])


class TestCarouselComponents:
    """Test carousel components."""

    def test_carousel_item_basic(self):
        """Test basic carousel item."""
        item = CarouselItem("Item content")
        assert item.tag == "div"
        assert "carousel-item" in item.attributes.get("classes", [])

    def test_carousel_item_active(self):
        """Test active carousel item."""
        item = CarouselItem("Content", active=True)
        assert "active" in item.attributes.get("classes", [])

    def test_carousel_basic(self):
        """Test basic carousel."""
        items = [CarouselItem("Slide 1"), CarouselItem("Slide 2")]
        carousel = Carousel(id="test-carousel", items=items)
        
        assert carousel.tag == "div"
        assert "carousel" in carousel.attributes.get("classes", [])
        assert carousel.attributes.get("id") == "test-carousel"

    def test_carousel_fade(self):
        """Test carousel with fade."""
        items = [CarouselItem("Slide 1")]
        carousel = Carousel(id="test", items=items, fade=True)
        assert "carousel-fade" in carousel.attributes.get("classes", [])

    def test_carousel_no_controls(self):
        """Test carousel without controls."""
        items = [CarouselItem("Slide 1")]
        carousel = Carousel(id="test", items=items, controls=False, indicators=False)
        assert carousel.tag == "div"


class TestOffcanvasComponents:
    """Test offcanvas components."""

    def test_offcanvas_basic(self):
        """Test basic offcanvas."""
        offcanvas = Offcanvas(id="test-offcanvas", title="Title", body="Content")
        assert offcanvas.tag == "div"
        assert "offcanvas" in offcanvas.attributes.get("classes", [])
        assert "offcanvas-start" in offcanvas.attributes.get("classes", [])

    def test_offcanvas_placement(self):
        """Test offcanvas placement."""
        offcanvas = Offcanvas(id="test", placement="end")
        assert "offcanvas-end" in offcanvas.attributes.get("classes", [])

    def test_offcanvas_trigger(self):
        """Test offcanvas trigger."""
        trigger = OffcanvasTrigger("Open", target="test-offcanvas")
        assert trigger.attributes.get("data_bs_toggle") == "offcanvas"
        assert trigger.attributes.get("data_bs_target") == "#test-offcanvas"


class TestToastComponents:
    """Test toast components."""

    def test_toast_basic(self):
        """Test basic toast."""
        toast = Toast(title="Notification", body="Message")
        assert toast.tag == "div"
        assert "toast" in toast.attributes.get("classes", [])
        assert toast.attributes.get("role") == "alert"

    def test_toast_no_autohide(self):
        """Test toast without autohide."""
        toast = Toast(body="Message", autohide=False)
        assert toast.attributes.get("data_bs_autohide") == "false"

    def test_toast_container_basic(self):
        """Test basic toast container."""
        container = ToastContainer()
        assert container.tag == "div"
        assert "toast-container" in container.attributes.get("classes", [])

    def test_toast_container_position(self):
        """Test toast container position."""
        container = ToastContainer(position="bottom-end")
        classes = container.attributes.get("classes", [])
        assert "position-fixed" in classes
        assert "bottom-0" in classes
        assert "end-0" in classes


class TestTooltipPopoverComponents:
    """Test tooltip and popover components."""

    def test_tooltip_basic(self):
        """Test basic tooltip."""
        button = Button("Hover me")
        tooltip = Tooltip(button, "Tooltip text")
        assert tooltip.tag == "span"

    def test_popover_basic(self):
        """Test basic popover."""
        button = Button("Click me")
        popover = Popover(button, title="Title", content="Content")
        assert popover.tag == "span"


class TestInputGroupComponents:
    """Test input group components."""

    def test_input_group_basic(self):
        """Test basic input group."""
        group = InputGroup()
        assert group.tag == "div"
        assert "input-group" in group.attributes.get("classes", [])

    def test_input_group_size(self):
        """Test input group size."""
        group = InputGroup(size="lg")
        assert "input-group-lg" in group.attributes.get("classes", [])

    def test_input_group_text(self):
        """Test input group text addon."""
        text = InputGroupText("@")
        assert text.tag == "span"
        assert "input-group-text" in text.attributes.get("classes", [])


class TestUtilityComponentsExtended:
    """Test additional utility components."""

    def test_figure_basic(self):
        """Test basic figure."""
        figure = Figure(img_src="/test.jpg", img_alt="Test", caption="Caption")
        assert figure.tag == "figure"
        assert "figure" in figure.attributes.get("classes", [])

    def test_close_button_basic(self):
        """Test basic close button."""
        close = CloseButton()
        assert close.tag == "button"
        assert "btn-close" in close.attributes.get("classes", [])

    def test_close_button_white(self):
        """Test white close button."""
        close = CloseButton(white=True)
        assert "btn-close-white" in close.attributes.get("classes", [])

    def test_range_basic(self):
        """Test basic range input."""
        range_input = Range(name="volume", min_val=0, max_val=100, value=50)
        assert range_input.tag == "input"
        assert "form-range" in range_input.attributes.get("classes", [])

    def test_range_with_label(self):
        """Test range with label."""
        range_input = Range(name="volume", label="Volume")
        element = range_input.get_element()
        assert element.tag == "div"

    def test_switch_basic(self):
        """Test basic switch."""
        switch = Switch(name="toggle", label="Enable notifications")
        assert switch.tag == "div"
        classes = switch.attributes.get("classes", [])
        assert "form-check" in classes
        assert "form-switch" in classes

    def test_file_input_basic(self):
        """Test basic file input."""
        file_input = FileInput(name="upload", label="Choose file")
        assert file_input.tag == "input"
        assert file_input.attributes.get("type") == "file"

    def test_file_input_multiple(self):
        """Test file input with multiple."""
        file_input = FileInput(multiple=True, accept=".jpg,.png")
        assert file_input.attributes.get("multiple") is True
        assert file_input.attributes.get("accept") == ".jpg,.png"

    def test_ratio_basic(self):
        """Test basic ratio component."""
        content = ht.iframe(src="/video")
        ratio = Ratio(content, ratio="16x9")
        assert ratio.tag == "div"
        classes = ratio.attributes.get("classes", [])
        assert "ratio" in classes
        assert "ratio-16x9" in classes

    def test_visually_hidden_basic(self):
        """Test basic visually hidden."""
        hidden = VisuallyHidden("Screen reader only")
        assert hidden.tag == "span"
        assert "visually-hidden" in hidden.attributes.get("classes", [])

    def test_visually_hidden_focusable(self):
        """Test focusable visually hidden."""
        hidden = VisuallyHidden("Skip to content", focusable=True)
        assert "visually-hidden-focusable" in hidden.attributes.get("classes", [])

    def test_stretched_link_basic(self):
        """Test basic stretched link."""
        link = StretchedLink(href="/test", text="Read more")
        assert link.tag == "a"
        assert link.attributes.get("href") == "/test"
        assert "stretched-link" in link.attributes.get("classes", [])