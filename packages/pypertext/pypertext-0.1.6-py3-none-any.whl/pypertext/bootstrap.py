"""
Bootstrap CSS components for Pypertext.

This module provides a comprehensive set of Bootstrap 5 components with a declarative API
for building responsive web interfaces.

Example:
    ```python
    from pypertext import ht
    from pypertext.bootstrap import Container, Row, Col, Button, Card

    # Create a responsive layout
    page = Container(
        Row(
            Col(
                Card(
                    title="Welcome",
                    body="Hello, Bootstrap!",
                    footer=Button("Click me", variant="primary")
                ),
                md=6
            ),
            Col(
                Card(
                    title="Features",
                    body="Responsive and modern"
                ),
                md=6
            )
        )
    )
    ```

Changes
-------
0.1.6 - Added bootstrap module
"""

import typing as t
from enum import Enum
from pypertext import ht, Element, Document, dict2css, ElementChild


# Type aliases for better readability
Size = t.Literal["sm", "md", "lg", "xl", "xxl"]
Variant = t.Literal["primary", "secondary", "success", "danger", "warning", "info", "light", "dark"]
ButtonVariant = t.Union[
    Variant,
    t.Literal[
        "link",
        "outline-primary",
        "outline-secondary",
        "outline-success",
        "outline-danger",
        "outline-warning",
        "outline-info",
        "outline-light",
        "outline-dark",
    ],
]


class Breakpoint(str, Enum):
    """Bootstrap breakpoints for responsive design."""

    XS = ""  # <576px
    SM = "sm"  # ≥576px
    MD = "md"  # ≥768px
    LG = "lg"  # ≥992px
    XL = "xl"  # ≥1200px
    XXL = "xxl"  # ≥1400px


class Spacing(str, Enum):
    """Bootstrap spacing utilities."""

    AUTO = "auto"
    ZERO = "0"
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"


# Layout Components


class Container(Element):
    """
    Bootstrap container component for responsive layout.

    Args:
        *children: Child elements to include in the container
        fluid: If True, creates a full-width container
        **kwargs: Additional attributes to pass to the container
    """

    def __init__(self, *children: ElementChild, fluid: t.Union[bool, Size] = False, **kwargs) -> None:
        super().__init__(*children, **kwargs)
        self.tag = "div"

        if fluid is True:
            self.add_classes("container-fluid")
        elif isinstance(fluid, str):
            self.add_classes(f"container-{fluid}")
        else:
            self.add_classes("container")


class Row(Element):
    """
    Bootstrap row component for grid layout.

    Args:
        *children: Child elements (typically Col components)
        cols: Number of columns (1-12) or "auto"
        cols_sm: Number of columns for small screens
        cols_md: Number of columns for medium screens
        cols_lg: Number of columns for large screens
        cols_xl: Number of columns for extra large screens
        cols_xxl: Number of columns for extra extra large screens
        g: Gutter spacing (0-5)
        gx: Horizontal gutter spacing (0-5)
        gy: Vertical gutter spacing (0-5)
        align: Vertical alignment (start, center, end)
        justify: Horizontal justification (start, center, end, around, between, evenly)
        **kwargs: Additional attributes
    """

    def __init__(
        self,
        *children: ElementChild,
        cols: t.Optional[t.Union[int, t.Literal["auto"]]] = None,
        cols_sm: t.Optional[t.Union[int, t.Literal["auto"]]] = None,
        cols_md: t.Optional[t.Union[int, t.Literal["auto"]]] = None,
        cols_lg: t.Optional[t.Union[int, t.Literal["auto"]]] = None,
        cols_xl: t.Optional[t.Union[int, t.Literal["auto"]]] = None,
        cols_xxl: t.Optional[t.Union[int, t.Literal["auto"]]] = None,
        g: t.Optional[int] = None,
        gx: t.Optional[int] = None,
        gy: t.Optional[int] = None,
        align: t.Optional[t.Literal["start", "center", "end"]] = None,
        justify: t.Optional[t.Literal["start", "center", "end", "around", "between", "evenly"]] = None,
        **kwargs,
    ) -> None:
        super().__init__(*children, **kwargs)
        self.tag = "div"
        self.add_classes("row")

        # Add column classes
        if cols is not None:
            self.add_classes(f"row-cols-{cols}")
        if cols_sm is not None:
            self.add_classes(f"row-cols-sm-{cols_sm}")
        if cols_md is not None:
            self.add_classes(f"row-cols-md-{cols_md}")
        if cols_lg is not None:
            self.add_classes(f"row-cols-lg-{cols_lg}")
        if cols_xl is not None:
            self.add_classes(f"row-cols-xl-{cols_xl}")
        if cols_xxl is not None:
            self.add_classes(f"row-cols-xxl-{cols_xxl}")

        # Add gutter classes
        if g is not None:
            self.add_classes(f"g-{g}")
        if gx is not None:
            self.add_classes(f"gx-{gx}")
        if gy is not None:
            self.add_classes(f"gy-{gy}")

        # Add alignment classes
        if align:
            self.add_classes(f"align-items-{align}")
        if justify:
            self.add_classes(f"justify-content-{justify}")


class Col(Element):
    """
    Bootstrap column component for grid layout.

    Args:
        *children: Child elements
        span: Column span (1-12, "auto", or True for equal width)
        sm: Column span for small screens
        md: Column span for medium screens
        lg: Column span for large screens
        xl: Column span for extra large screens
        xxl: Column span for extra extra large screens
        offset: Column offset (0-11)
        offset_sm: Column offset for small screens
        offset_md: Column offset for medium screens
        offset_lg: Column offset for large screens
        offset_xl: Column offset for extra large screens
        offset_xxl: Column offset for extra extra large screens
        order: Column order (1-12, "first", "last")
        align: Self alignment (start, center, end, baseline, stretch)
        **kwargs: Additional attributes
    """

    def __init__(
        self,
        *children: ElementChild,
        span: t.Optional[t.Union[bool, int, t.Literal["auto"]]] = None,
        sm: t.Optional[t.Union[int, t.Literal["auto"]]] = None,
        md: t.Optional[t.Union[int, t.Literal["auto"]]] = None,
        lg: t.Optional[t.Union[int, t.Literal["auto"]]] = None,
        xl: t.Optional[t.Union[int, t.Literal["auto"]]] = None,
        xxl: t.Optional[t.Union[int, t.Literal["auto"]]] = None,
        offset: t.Optional[int] = None,
        offset_sm: t.Optional[int] = None,
        offset_md: t.Optional[int] = None,
        offset_lg: t.Optional[int] = None,
        offset_xl: t.Optional[int] = None,
        offset_xxl: t.Optional[int] = None,
        order: t.Optional[t.Union[int, t.Literal["first", "last"]]] = None,
        align: t.Optional[t.Literal["start", "center", "end", "baseline", "stretch"]] = None,
        **kwargs,
    ) -> None:
        super().__init__(*children, **kwargs)
        self.tag = "div"

        # Add column classes
        if span is True:
            self.add_classes("col")
        elif span is not None:
            self.add_classes(f"col-{span}")
        elif not any([sm, md, lg, xl, xxl]):
            # Default to col if no specific breakpoints
            self.add_classes("col")

        # Add responsive column classes
        if sm is not None:
            self.add_classes(f"col-sm-{sm}")
        if md is not None:
            self.add_classes(f"col-md-{md}")
        if lg is not None:
            self.add_classes(f"col-lg-{lg}")
        if xl is not None:
            self.add_classes(f"col-xl-{xl}")
        if xxl is not None:
            self.add_classes(f"col-xxl-{xxl}")

        # Add offset classes
        if offset is not None:
            self.add_classes(f"offset-{offset}")
        if offset_sm is not None:
            self.add_classes(f"offset-sm-{offset_sm}")
        if offset_md is not None:
            self.add_classes(f"offset-md-{offset_md}")
        if offset_lg is not None:
            self.add_classes(f"offset-lg-{offset_lg}")
        if offset_xl is not None:
            self.add_classes(f"offset-xl-{offset_xl}")
        if offset_xxl is not None:
            self.add_classes(f"offset-xxl-{offset_xxl}")

        # Add order class
        if order is not None:
            self.add_classes(f"order-{order}")

        # Add alignment class
        if align:
            self.add_classes(f"align-self-{align}")


# Stack Layout (Flexbox utilities)


class Stack(Element):
    """
    Bootstrap stack component for vertical or horizontal layouts.

    Args:
        *children: Child elements
        direction: Stack direction ("vertical" or "horizontal")
        gap: Gap between items (0-5)
        align: Alignment (start, center, end, baseline, stretch)
        justify: Justification (start, center, end, around, between, evenly)
        wrap: Whether items should wrap
        **kwargs: Additional attributes
    """

    def __init__(
        self,
        *children: ElementChild,
        direction: t.Literal["vertical", "horizontal"] = "vertical",
        gap: t.Optional[int] = None,
        align: t.Optional[t.Literal["start", "center", "end", "baseline", "stretch"]] = None,
        justify: t.Optional[t.Literal["start", "center", "end", "around", "between", "evenly"]] = None,
        wrap: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(*children, **kwargs)
        self.tag = "div"

        if direction == "vertical":
            self.add_classes("vstack")
        else:
            self.add_classes("hstack")

        if gap is not None:
            self.add_classes(f"gap-{gap}")

        if align:
            self.add_classes(f"align-items-{align}")

        if justify:
            self.add_classes(f"justify-content-{justify}")

        if wrap:
            self.add_classes("flex-wrap")


# Typography Components


class Heading(Element):
    """
    Bootstrap heading component with display options.

    Args:
        text: Heading text
        level: Heading level (1-6)
        display: Display size (1-6) for larger headings
        **kwargs: Additional attributes
    """

    def __init__(self, text: str, level: int = 1, display: t.Optional[int] = None, **kwargs) -> None:
        super().__init__(text, **kwargs)
        self.tag = f"h{level}"

        if display is not None:
            self.add_classes(f"display-{display}")


class Text(Element):
    """
    Bootstrap text component with typography utilities.

    Args:
        *children: Text content
        tag: HTML tag (p, span, div, etc.)
        lead: Make text stand out
        size: Text size (1-6)
        weight: Font weight (light, lighter, normal, bold, bolder)
        style: Font style (italic, normal)
        decoration: Text decoration (none, underline, line-through)
        transform: Text transform (lowercase, uppercase, capitalize)
        align: Text alignment (start, center, end, justify)
        wrap: Text wrapping (wrap, nowrap)
        truncate: Truncate text with ellipsis
        color: Text color variant
        bg: Background color variant
        **kwargs: Additional attributes
    """

    def __init__(
        self,
        *children: ElementChild,
        tag: str = "p",
        lead: bool = False,
        size: t.Optional[int] = None,
        weight: t.Optional[t.Literal["light", "lighter", "normal", "bold", "bolder"]] = None,
        style: t.Optional[t.Literal["italic", "normal"]] = None,
        decoration: t.Optional[t.Literal["none", "underline", "line-through"]] = None,
        transform: t.Optional[t.Literal["lowercase", "uppercase", "capitalize"]] = None,
        align: t.Optional[t.Literal["start", "center", "end", "justify"]] = None,
        wrap: t.Optional[t.Literal["wrap", "nowrap"]] = None,
        truncate: bool = False,
        color: t.Optional[Variant] = None,
        bg: t.Optional[Variant] = None,
        **kwargs,
    ) -> None:
        super().__init__(*children, **kwargs)
        self.tag = tag

        if lead:
            self.add_classes("lead")

        if size is not None:
            self.add_classes(f"fs-{size}")

        if weight:
            self.add_classes(f"fw-{weight}")

        if style:
            self.add_classes(f"fst-{style}")

        if decoration:
            self.add_classes(f"text-decoration-{decoration}")

        if transform:
            self.add_classes(f"text-{transform}")

        if align:
            self.add_classes(f"text-{align}")

        if wrap:
            self.add_classes(f"text-{wrap}")

        if truncate:
            self.add_classes("text-truncate")

        if color:
            self.add_classes(f"text-{color}")

        if bg:
            self.add_classes(f"bg-{bg}")


# Button Components


class Button(Element):
    """
    Bootstrap button component.

    Args:
        text: Button text
        variant: Button variant (primary, secondary, etc.)
        size: Button size (sm, lg)
        outline: Use outline style
        disabled: Disable the button
        active: Active state
        type: Button type attribute
        href: If provided, renders as an anchor tag
        block: Full width button
        **kwargs: Additional attributes
    """

    def __init__(
        self,
        text: str,
        variant: ButtonVariant = "primary",
        size: t.Optional[t.Literal["sm", "lg"]] = None,
        outline: bool = False,
        disabled: bool = False,
        active: bool = False,
        type: t.Literal["button", "submit", "reset"] = "button",
        href: t.Optional[str] = None,
        block: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(text, **kwargs)

        if href:
            self.tag = "a"
            self.set_attrs(href=href, role="button")
        else:
            self.tag = "button"
            self.set_attrs(type=type)

        self.add_classes("btn")

        # Handle variant
        if outline and variant in ["primary", "secondary", "success", "danger", "warning", "info", "light", "dark"]:
            self.add_classes(f"btn-outline-{variant}")
        else:
            self.add_classes(f"btn-{variant}")

        if size:
            self.add_classes(f"btn-{size}")

        if disabled:
            if self.tag == "button":
                self.set_attrs(disabled=True)
            else:
                self.add_classes("disabled")

        if active:
            self.add_classes("active")

        if block:
            self.add_classes("d-block", "w-100")


class ButtonGroup(Element):
    """
    Bootstrap button group component.

    Args:
        *children: Button elements
        vertical: Vertical button group
        size: Button group size (sm, lg)
        role: ARIA role
        label: ARIA label
        **kwargs: Additional attributes
    """

    def __init__(
        self,
        *children: ElementChild,
        vertical: bool = False,
        size: t.Optional[t.Literal["sm", "lg"]] = None,
        role: str = "group",
        label: t.Optional[str] = None,
        **kwargs,
    ) -> None:
        super().__init__(*children, **kwargs)
        self.tag = "div"

        if vertical:
            self.add_classes("btn-group-vertical")
        else:
            self.add_classes("btn-group")

        if size:
            self.add_classes(f"btn-group-{size}")

        self.set_attrs(role=role)

        if label:
            self.set_attrs(aria_label=label)


# Form Components


class Form(Element):
    """
    Bootstrap form component.

    Args:
        *children: Form elements
        validated: Add validation styling
        inline: Inline form layout
        gap: Gap between form controls (0-5)
        method: Form submission method (get, post)
        action: Form action URL
        multipart_form_data: Use multipart/form-data encoding (for file uploads)
        **kwargs: Additional attributes
    """

    def __init__(
        self,
        *children: ElementChild,
        validated: bool = False,
        inline: bool = False,
        gap: t.Optional[int] = None,
        method: t.Literal["get", "post"] = "post",
        action: t.Optional[str] = None,
        multipart_form_data: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(*children, **kwargs)
        self.tag = "form"

        if validated:
            self.add_classes("was-validated")

        if inline:
            self.add_classes("row", "row-cols-lg-auto", "align-items-center")
            if gap is not None:
                self.add_classes(f"g-{gap}")
        else:
            # For vertical forms, use vstack with gap for proper spacing
            self.add_classes("vstack")
            if gap is not None:
                self.add_classes(f"gap-{gap}")

        if method:
            self.set_attrs(method=method)

        if action:
            self.set_attrs(action=action)

        if multipart_form_data:
            self.set_attrs(enctype="multipart/form-data")


class FormGroup(Element):
    """
    Bootstrap form group for organizing form controls.

    Args:
        *children: Form elements (label, input, help text, etc.)
        mb: Margin bottom spacing (0-5)
        floating: Use floating label layout
        **kwargs: Additional attributes
    """

    def __init__(self, *children: ElementChild, mb: int = 3, floating: bool = False, **kwargs) -> None:
        super().__init__(*children, **kwargs)
        self.tag = "div"

        if floating:
            self.add_classes("form-floating")
        else:
            self.add_classes(f"mb-{mb}")


class Input(Element):
    """
    Bootstrap form input component.

    Args:
        type: Input type
        name: Input name
        value: Input value
        placeholder: Placeholder text
        label: Label text (creates a label element)
        size: Input size (sm, lg)
        readonly: Read-only input
        disabled: Disabled input
        required: Required input
        invalid_feedback: Invalid feedback message
        valid_feedback: Valid feedback message
        help_text: Help text
        floating_label: Use floating label (label must be provided)
        **kwargs: Additional attributes
    """

    def __init__(
        self,
        type: str = "text",
        name: t.Optional[str] = None,
        value: t.Optional[str] = None,
        placeholder: t.Optional[str] = None,
        label: t.Optional[str] = None,
        size: t.Optional[t.Literal["sm", "lg"]] = None,
        readonly: bool = False,
        disabled: bool = False,
        required: bool = False,
        invalid_feedback: t.Optional[str] = None,
        valid_feedback: t.Optional[str] = None,
        help_text: t.Optional[str] = None,
        floating_label: bool = False,
        **kwargs,
    ) -> None:
        # Remove non-input attributes
        self._label = label
        self._invalid_feedback = invalid_feedback
        self._valid_feedback = valid_feedback
        self._help_text = help_text
        self._floating_label = floating_label

        super().__init__(**kwargs)
        self.tag = "input"
        self.add_classes("form-control")

        # Set input attributes
        self.set_attrs(type=type)

        if name:
            self.set_attrs(name=name, id=name)

        if value is not None:
            self.set_attrs(value=value)

        if placeholder:
            self.set_attrs(placeholder=placeholder)

        if size:
            self.add_classes(f"form-control-{size}")

        if readonly:
            self.set_attrs(readonly=True)

        if disabled:
            self.set_attrs(disabled=True)

        if required:
            self.set_attrs(required=True)

    def get_element(self) -> Element:
        """Return the input with label and feedback as a form group."""
        if self._label or self._invalid_feedback or self._valid_feedback or self._help_text:
            group = FormGroup(floating=self._floating_label)

            # Add label before input for normal layout
            if self._label and not self._floating_label:
                label_el = ht.label(self._label, for_=self.attributes.get("id", ""))
                label_el.add_classes("form-label")
                group.append(label_el)

            # Add the input (create a new input element to avoid circular reference)
            input_el = ht.input(**self.attributes)
            group.append(input_el)

            # Add label after input for floating layout
            if self._label and self._floating_label:
                label_el = ht.label(self._label, for_=self.attributes.get("id", ""))
                group.append(label_el)

            # Add feedback messages
            if self._invalid_feedback:
                group.append(ht.div(self._invalid_feedback, classes="invalid-feedback"))

            if self._valid_feedback:
                group.append(ht.div(self._valid_feedback, classes="valid-feedback"))

            # Add help text
            if self._help_text:
                help_el = ht.small(self._help_text, classes="form-text")
                group.append(help_el)

            return group

        return self


class Select(Element):
    """
    Bootstrap select component.

    Args:
        name: Select name
        options: List of options (strings or tuples of (value, label))
        value: Selected value
        label: Label text
        placeholder: Placeholder text (appears as disabled, non-selectable first option)
        size: Select size (sm, lg)
        multiple: Allow multiple selections
        disabled: Disabled select
        required: Required select
        help_text: Help text
        floating_label: Use floating label (label must be provided)
        **kwargs: Additional attributes
    """

    def __init__(
        self,
        name: t.Optional[str] = None,
        options: t.Optional[t.List[t.Union[str, t.Tuple[str, str]]]] = None,
        value: t.Optional[str] = None,
        label: t.Optional[str] = None,
        placeholder: t.Optional[str] = None,
        size: t.Optional[t.Literal["sm", "lg"]] = None,
        multiple: bool = False,
        disabled: bool = False,
        required: bool = False,
        help_text: t.Optional[str] = None,
        floating_label: bool = False,
        **kwargs,
    ) -> None:
        self._label = label
        self._help_text = help_text
        self._floating_label = floating_label

        super().__init__(**kwargs)
        self.tag = "select"
        self.add_classes("form-select")

        if name:
            self.set_attrs(name=name, id=name)

        if size:
            self.add_classes(f"form-select-{size}")

        if multiple:
            self.set_attrs(multiple=True)

        if disabled:
            self.set_attrs(disabled=True)

        if required:
            self.set_attrs(required=True)

        # Add placeholder option if provided
        placeholder_added = False
        if placeholder:
            placeholder_opt = ht.option(placeholder, value="", selected=not bool(value), disabled=True)
            self.append(placeholder_opt)
            placeholder_added = True
        elif floating_label and label:
            # Add a blank placeholder option for floating labels if no explicit placeholder
            placeholder_opt = ht.option("", value="", selected=not bool(value), disabled=True, hidden=True)
            self.append(placeholder_opt)
            placeholder_added = True

        # Add options
        if options:
            for option in options:
                if isinstance(option, tuple):
                    opt_value, opt_label = option
                    opt_el = ht.option(opt_label, value=opt_value)
                    if opt_value == value:
                        opt_el.set_attrs(selected=True)
                        # Remove selected from placeholder if a real option is selected
                        if placeholder_added and hasattr(self, "children") and self.children:
                            self.children[0].attributes.pop("selected", None)
                else:
                    opt_el = ht.option(option, value=option)
                    if option == value:
                        opt_el.set_attrs(selected=True)
                        # Remove selected from placeholder if a real option is selected
                        if placeholder_added and hasattr(self, "children") and self.children:
                            self.children[0].attributes.pop("selected", None)
                self.append(opt_el)

    def get_element(self) -> Element:
        """Return the select with label and help text as a form group."""
        if self._label or self._help_text:
            group = FormGroup(floating=self._floating_label)

            # Add label before select for normal layout
            if self._label and not self._floating_label:
                label_el = ht.label(self._label, for_=self.attributes.get("id", ""))
                label_el.add_classes("form-label")
                group.append(label_el)

            # Create a new select element to avoid circular reference
            select_el = ht.select(**self.attributes)
            # Copy the option children
            for child in self.children:
                select_el.append(child)
            group.append(select_el)

            # Add label after select for floating layout
            if self._label and self._floating_label:
                label_el = ht.label(self._label, for_=self.attributes.get("id", ""))
                group.append(label_el)

            if self._help_text:
                help_el = ht.small(self._help_text, classes="form-text")
                group.append(help_el)

            return group

        return self


class Textarea(Element):
    """
    Bootstrap textarea component.

    Args:
        name: Textarea name
        value: Textarea value
        rows: Number of rows
        placeholder: Placeholder text
        label: Label text
        readonly: Read-only textarea
        disabled: Disabled textarea
        required: Required textarea
        help_text: Help text
        floating_label: Use floating label (label must be provided)
        **kwargs: Additional attributes
    """

    def __init__(
        self,
        name: t.Optional[str] = None,
        value: t.Optional[str] = None,
        rows: int = 3,
        placeholder: t.Optional[str] = None,
        label: t.Optional[str] = None,
        readonly: bool = False,
        disabled: bool = False,
        required: bool = False,
        help_text: t.Optional[str] = None,
        floating_label: bool = False,
        **kwargs,
    ) -> None:
        self._label = label
        self._help_text = help_text
        self._floating_label = floating_label

        super().__init__(value or "", **kwargs)
        self.tag = "textarea"
        self.add_classes("form-control")

        if name:
            self.set_attrs(name=name, id=name)

        self.set_attrs(rows=rows)

        if placeholder:
            self.set_attrs(placeholder=placeholder)

        if readonly:
            self.set_attrs(readonly=True)

        if disabled:
            self.set_attrs(disabled=True)

        if required:
            self.set_attrs(required=True)

    def get_element(self) -> Element:
        """Return the textarea with label and help text as a form group."""
        if self._label or self._help_text:
            group = FormGroup(floating=self._floating_label)

            # Add label before textarea for normal layout
            if self._label and not self._floating_label:
                label_el = ht.label(self._label, for_=self.attributes.get("id", ""))
                label_el.add_classes("form-label")
                group.append(label_el)

            # Create a new textarea element to avoid circular reference
            textarea_el = ht.textarea(**self.attributes)
            textarea_el.add_classes("form-control")

            # For floating labels, we need to set explicit height since Bootstrap's form-floating overrides rows
            if self._floating_label and "rows" in self.attributes:
                rows = int(self.attributes["rows"])
                # Approximate height calculation: each row is about 1.5em, plus padding
                height = f"{1.5 * rows + 1}em"
                existing_style = textarea_el.attributes.get("style", "")
                new_style = f"height: {height};" + (f" {existing_style}" if existing_style else "")
                textarea_el.set_attrs(style=new_style)

            # Copy any text content
            for child in self.children:
                textarea_el.append(child)
            group.append(textarea_el)

            # Add label after textarea for floating layout
            if self._label and self._floating_label:
                label_el = ht.label(self._label, for_=self.attributes.get("id", ""))
                group.append(label_el)

            if self._help_text:
                help_el = ht.small(self._help_text, classes="form-text")
                group.append(help_el)

            return group

        return self


class Checkbox(Element):
    """
    Bootstrap checkbox component.

    Args:
        name: Checkbox name
        label: Checkbox label
        checked: Whether checkbox is checked
        value: Checkbox value
        disabled: Disabled checkbox
        inline: Inline checkbox
        switch: Render as switch
        **kwargs: Additional attributes
    """

    def __init__(
        self,
        name: t.Optional[str] = None,
        label: t.Optional[str] = None,
        checked: bool = False,
        value: str = "on",
        disabled: bool = False,
        inline: bool = False,
        switch: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.tag = "div"

        if inline:
            self.add_classes("form-check", "form-check-inline")
        else:
            self.add_classes("form-check")

        if switch:
            self.add_classes("form-switch")

        # Create checkbox input
        input_attrs = {
            "type": "checkbox",
            "classes": "form-check-input",
            "value": value,
            "checked": False,
            "disabled": False,
        }

        if name:
            input_attrs["name"] = name
            input_attrs["id"] = f"{name}-{value}"

        if checked:
            input_attrs["checked"] = True

        if disabled:
            input_attrs["disabled"] = True

        checkbox = ht.input(**input_attrs)
        self.append(checkbox)

        # Add label
        if label:
            label_el = ht.label(label, classes="form-check-label")
            if name:
                label_el.set_attrs(for_=f"{name}-{value}")
            self.append(label_el)


class Radio(Element):
    """
    Bootstrap radio button component.

    Args:
        name: Radio button name
        label: Radio button label
        value: Radio button value
        checked: Whether radio is checked
        disabled: Disabled radio
        inline: Inline radio
        **kwargs: Additional attributes
    """

    def __init__(
        self,
        name: str,
        label: t.Optional[str] = None,
        value: str = "on",
        checked: bool = False,
        disabled: bool = False,
        inline: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.tag = "div"

        if inline:
            self.add_classes("form-check", "form-check-inline")
        else:
            self.add_classes("form-check")

        # Create radio input
        input_attrs = {
            "type": "radio",
            "name": name,
            "id": f"{name}-{value}",
            "classes": "form-check-input",
            "value": value,
            "checked": False,
            "disabled": False,
        }

        if checked:
            input_attrs["checked"] = True

        if disabled:
            input_attrs["disabled"] = True

        radio = ht.input(**input_attrs)
        self.append(radio)

        # Add label
        if label:
            label_el = ht.label(label, classes="form-check-label", for_=f"{name}-{value}")
            self.append(label_el)


# Card Components


class Card(Element):
    """
    Bootstrap card component.

    Args:
        *children: Card content (if not using title/body/footer)
        title: Card title
        subtitle: Card subtitle
        body: Card body content
        footer: Card footer content
        header: Card header content
        img_src: Card image source
        img_alt: Card image alt text
        img_position: Image position (top, bottom)
        color: Card color variant
        bg: Card background variant
        text_color: Text color variant
        border: Border color variant
        **kwargs: Additional attributes
    """

    def __init__(
        self,
        *children: ElementChild,
        title: t.Optional[str] = None,
        subtitle: t.Optional[str] = None,
        body: t.Optional[ElementChild] = None,
        footer: t.Optional[ElementChild] = None,
        header: t.Optional[ElementChild] = None,
        img_src: t.Optional[str] = None,
        img_alt: str = "",
        img_position: t.Literal["top", "bottom"] = "top",
        color: t.Optional[Variant] = None,
        bg: t.Optional[Variant] = None,
        text_color: t.Optional[Variant] = None,
        border: t.Optional[Variant] = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.tag = "div"
        self.add_classes("card")

        # Apply color classes
        if color:
            self.add_classes(f"text-bg-{color}")
        else:
            if bg:
                self.add_classes(f"bg-{bg}")
            if text_color:
                self.add_classes(f"text-{text_color}")

        if border:
            self.add_classes(f"border-{border}")

        # Add header
        if header:
            self.append(ht.div(header, classes="card-header"))

        # Add image (top position)
        if img_src and img_position == "top":
            self.append(ht.img(src=img_src, alt=img_alt, classes="card-img-top"))

        # Add body
        if body or title or subtitle:
            body_el = ht.div(classes="card-body")

            if title:
                body_el.append(ht.h5(title, classes="card-title"))

            if subtitle:
                body_el.append(ht.h6(subtitle, classes="card-subtitle mb-2 text-muted"))

            if body:
                if isinstance(body, str):
                    body_el.append(ht.p(body, classes="card-text"))
                else:
                    body_el.append(body)

            self.append(body_el)

        # Add custom children
        if children:
            for child in children:
                self.append(child)

        # Add image (bottom position)
        if img_src and img_position == "bottom":
            self.append(ht.img(src=img_src, alt=img_alt, classes="card-img-bottom"))

        # Add footer
        if footer:
            self.append(ht.div(footer, classes="card-footer"))


class CardGroup(Element):
    """
    Bootstrap card group for displaying cards together.

    Args:
        *children: Card elements
        **kwargs: Additional attributes
    """

    def __init__(self, *children: ElementChild, **kwargs) -> None:
        super().__init__(*children, **kwargs)
        self.tag = "div"
        self.add_classes("card-group")


class CardDeck(Element):
    """
    Bootstrap card deck using grid system.

    Args:
        *children: Card elements
        cols_sm: Columns on small screens
        cols_md: Columns on medium screens
        cols_lg: Columns on large screens
        cols_xl: Columns on extra large screens
        gap: Gap between cards (0-5)
        **kwargs: Additional attributes
    """

    def __init__(
        self,
        *children: ElementChild,
        cols_sm: t.Optional[int] = None,
        cols_md: t.Optional[int] = None,
        cols_lg: t.Optional[int] = None,
        cols_xl: t.Optional[int] = None,
        gap: int = 3,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.tag = "div"
        self.add_classes("row", f"g-{gap}")

        # Determine column classes
        col_classes = []
        if cols_sm:
            col_classes.append(f"col-sm-{12 // cols_sm}")
        if cols_md:
            col_classes.append(f"col-md-{12 // cols_md}")
        if cols_lg:
            col_classes.append(f"col-lg-{12 // cols_lg}")
        if cols_xl:
            col_classes.append(f"col-xl-{12 // cols_xl}")

        if not col_classes:
            col_classes = ["col"]

        # Wrap each card in a column
        for child in children:
            col = ht.div(child, classes=" ".join(col_classes))
            self.append(col)


# Navigation Components


class Nav(Element):
    """
    Bootstrap navigation component.

    Args:
        *children: Navigation items
        style: Navigation style (tabs, pills, underline)
        vertical: Vertical navigation
        fill: Fill available space
        justified: Equal-width elements
        **kwargs: Additional attributes
    """

    def __init__(
        self,
        *children: ElementChild,
        style: t.Optional[t.Literal["tabs", "pills", "underline"]] = None,
        vertical: bool = False,
        fill: bool = False,
        justified: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(*children, **kwargs)
        self.tag = "ul"
        self.add_classes("nav")

        if style:
            self.add_classes(f"nav-{style}")

        if vertical:
            self.add_classes("flex-column")

        if fill:
            self.add_classes("nav-fill")

        if justified:
            self.add_classes("nav-justified")


class NavItem(Element):
    """
    Bootstrap navigation item.

    Args:
        text: Link text
        href: Link URL
        active: Active state
        disabled: Disabled state
        **kwargs: Additional attributes
    """

    def __init__(self, text: str, href: str = "#", active: bool = False, disabled: bool = False, **kwargs) -> None:
        super().__init__(**kwargs)
        self.tag = "li"
        self.add_classes("nav-item")

        link = ht.a(text, href=href, classes="nav-link")

        if active:
            link.add_classes("active")
            link.set_attrs(aria_current="page")

        if disabled:
            link.add_classes("disabled")

        self.append(link)


class Navbar(Element):
    """
    Bootstrap navbar component.

    Args:
        brand: Brand text or element
        brand_href: Brand link URL
        items: List of navigation items
        expand: Breakpoint for expansion (sm, md, lg, xl, xxl)
        dark: Dark navbar
        bg: Background color variant
        fixed: Fixed position (top, bottom)
        sticky: Sticky position (top)
        container: Container type (True, False, or breakpoint)
        **kwargs: Additional attributes
    """

    def __init__(
        self,
        brand: t.Optional[ElementChild] = None,
        brand_href: str = "#",
        items: t.Optional[t.List[ElementChild]] = None,
        expand: t.Optional[Size] = "lg",
        dark: bool = False,
        bg: t.Optional[Variant] = None,
        fixed: t.Optional[t.Literal["top", "bottom"]] = None,
        sticky: t.Optional[t.Literal["top"]] = None,
        container: t.Union[bool, Size] = True,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.tag = "nav"
        self.add_classes("navbar")

        if expand:
            self.add_classes(f"navbar-expand-{expand}")
        else:
            self.add_classes("navbar-expand")

        if dark:
            self.add_classes("navbar-dark")
        else:
            self.add_classes("navbar-light")

        if bg:
            self.add_classes(f"bg-{bg}")

        if fixed:
            self.add_classes(f"fixed-{fixed}")

        if sticky:
            self.add_classes(f"sticky-{sticky}")

        # Create container
        if container is True:
            content = ht.div(classes="container")
        elif isinstance(container, str):
            content = ht.div(classes=f"container-{container}")
        else:
            content = self

        # Add brand
        if brand:
            brand_el = ht.a(brand, href=brand_href, classes="navbar-brand")
            content.append(brand_el)

        # Add toggler button
        toggler_id = f"navbar-{id(self)}"
        toggler = ht.button(
            ht.span(classes="navbar-toggler-icon"),
            classes="navbar-toggler",
            type="button",
            data_bs_toggle="collapse",
            data_bs_target=f"#{toggler_id}",
            aria_controls=toggler_id,
            aria_expanded="false",
            aria_label="Toggle navigation",
        )
        content.append(toggler)

        # Add collapse container
        collapse = ht.div(classes="collapse navbar-collapse", id=toggler_id)

        if items:
            nav = ht.ul(classes="navbar-nav")
            for item in items:
                if isinstance(item, str):
                    nav.append(NavItem(item))
                else:
                    nav.append(item)
            collapse.append(nav)

        content.append(collapse)

        if container is not False:
            self.append(content)


# Alert Components


class Alert(Element):
    """
    Bootstrap alert component.

    Args:
        *children: Alert content
        variant: Alert variant (primary, secondary, etc.)
        dismissible: Show dismiss button
        fade: Enable fade animation
        show: Show the alert (for fade animation)
        **kwargs: Additional attributes
    """

    def __init__(
        self,
        *children: ElementChild,
        variant: Variant = "primary",
        dismissible: bool = False,
        fade: bool = True,
        show: bool = True,
        **kwargs,
    ) -> None:
        super().__init__(*children, **kwargs)
        self.tag = "div"
        self.add_classes("alert", f"alert-{variant}")
        self.set_attrs(role="alert")

        if dismissible:
            self.add_classes("alert-dismissible")

        if fade:
            self.add_classes("fade")

        if show:
            self.add_classes("show")

        if dismissible:
            close_btn = ht.button(type="button", classes="btn-close", data_bs_dismiss="alert", aria_label="Close")
            self.append(close_btn)


# Badge Components


class Badge(Element):
    """
    Bootstrap badge component.

    Args:
        text: Badge text
        variant: Badge variant
        pill: Rounded pill style
        **kwargs: Additional attributes
    """

    def __init__(self, text: str, variant: Variant = "primary", pill: bool = False, **kwargs) -> None:
        super().__init__(text, **kwargs)
        self.tag = "span"
        self.add_classes("badge", f"text-bg-{variant}")

        if pill:
            self.add_classes("rounded-pill")


# Progress Components


class Progress(Element):
    """
    Bootstrap progress component.

    Args:
        value: Progress value (0-100)
        min: Minimum value
        max: Maximum value
        label: Progress label
        variant: Progress bar variant
        striped: Striped progress bar
        animated: Animated stripes
        height: Progress bar height in pixels
        **kwargs: Additional attributes
    """

    def __init__(
        self,
        value: float = 0,
        min: float = 0,
        max: float = 100,
        label: t.Optional[str] = None,
        variant: t.Optional[Variant] = None,
        striped: bool = False,
        animated: bool = False,
        height: t.Optional[int] = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.tag = "div"
        self.add_classes("progress")

        if height:
            self.set_attrs(style=f"height: {height}px")

        # Calculate percentage
        percentage = ((value - min) / (max - min)) * 100

        # Create progress bar
        bar = ht.div(
            label or "",
            classes="progress-bar",
            role="progressbar",
            style=f"width: {percentage}%",
            aria_valuenow=str(value),
            aria_valuemin=str(min),
            aria_valuemax=str(max),
        )

        if variant:
            bar.add_classes(f"bg-{variant}")

        if striped:
            bar.add_classes("progress-bar-striped")

        if animated:
            bar.add_classes("progress-bar-animated")

        self.append(bar)


# List Group Components


class ListGroup(Element):
    """
    Bootstrap list group component.

    Args:
        *children: List group items
        flush: Remove borders and rounded corners
        numbered: Numbered list
        horizontal: Horizontal list group
        **kwargs: Additional attributes
    """

    def __init__(
        self,
        *children: ElementChild,
        flush: bool = False,
        numbered: bool = False,
        horizontal: t.Union[bool, Size] = False,
        **kwargs,
    ) -> None:
        super().__init__(*children, **kwargs)

        if numbered:
            self.tag = "ol"
        else:
            self.tag = "ul"

        self.add_classes("list-group")

        if flush:
            self.add_classes("list-group-flush")

        if numbered:
            self.add_classes("list-group-numbered")

        if horizontal is True:
            self.add_classes("list-group-horizontal")
        elif horizontal:
            self.add_classes(f"list-group-horizontal-{horizontal}")


class ListGroupItem(Element):
    """
    Bootstrap list group item.

    Args:
        *children: Item content
        active: Active state
        disabled: Disabled state
        action: Action item (hover effect)
        variant: Color variant
        href: Link URL (makes it an anchor)
        **kwargs: Additional attributes
    """

    def __init__(
        self,
        *children: ElementChild,
        active: bool = False,
        disabled: bool = False,
        action: bool = False,
        variant: t.Optional[Variant] = None,
        href: t.Optional[str] = None,
        **kwargs,
    ) -> None:
        super().__init__(*children, **kwargs)

        if href:
            self.tag = "a"
            self.set_attrs(href=href)
        else:
            self.tag = "li"

        self.add_classes("list-group-item")

        if active:
            self.add_classes("active")

        if disabled:
            self.add_classes("disabled")

        if action:
            self.add_classes("list-group-item-action")

        if variant:
            self.add_classes(f"list-group-item-{variant}")


# Modal Components


class Modal(Element):
    """
    Bootstrap modal component.

    Args:
        id: Modal ID
        title: Modal title
        body: Modal body content
        footer: Modal footer content
        size: Modal size (sm, lg, xl)
        centered: Vertically center modal
        scrollable: Scrollable modal body
        static: Static backdrop
        fullscreen: Fullscreen modal
        **kwargs: Additional attributes
    """

    def __init__(
        self,
        id: str,
        title: t.Optional[str] = None,
        body: t.Optional[ElementChild] = None,
        footer: t.Optional[ElementChild] = None,
        size: t.Optional[t.Literal["sm", "lg", "xl"]] = None,
        centered: bool = False,
        scrollable: bool = False,
        static: bool = False,
        fullscreen: t.Union[bool, t.Literal["sm", "md", "lg", "xl", "xxl"]] = False,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.tag = "div"
        self.add_classes("modal", "fade")
        self.set_attrs(id=id, tabindex="-1")

        if static:
            self.set_attrs(data_bs_backdrop="static", data_bs_keyboard="false")

        # Create modal dialog
        dialog = ht.div(classes="modal-dialog")

        if size:
            dialog.add_classes(f"modal-{size}")

        if centered:
            dialog.add_classes("modal-dialog-centered")

        if scrollable:
            dialog.add_classes("modal-dialog-scrollable")

        if fullscreen is True:
            dialog.add_classes("modal-fullscreen")
        elif fullscreen:
            dialog.add_classes(f"modal-fullscreen-{fullscreen}-down")

        # Create modal content
        content = ht.div(classes="modal-content")

        # Add header
        if title:
            header = ht.div(
                ht.h5(title, classes="modal-title"),
                ht.button(type="button", classes="btn-close", data_bs_dismiss="modal", aria_label="Close"),
                classes="modal-header",
            )
            content.append(header)

        # Add body
        if body:
            content.append(ht.div(body, classes="modal-body"))

        # Add footer
        if footer:
            content.append(ht.div(footer, classes="modal-footer"))

        dialog.append(content)
        self.append(dialog)


class ModalTrigger(Button):
    """
    Bootstrap modal trigger button.

    Args:
        text: Button text
        target: Target modal ID
        **kwargs: Additional button attributes
    """

    def __init__(self, text: str, target: str, **kwargs) -> None:
        super().__init__(text, **kwargs)
        self.set_attrs(data_bs_toggle="modal", data_bs_target=f"#{target}")


# Table Components


class Table(Element):
    """
    Bootstrap table component with advanced formatting.

    Args:
        *children: Table content (thead, tbody, etc.)
        headers: List of header strings
        rows: List of dicts representing table rows
        striped: Striped rows
        hover: Hover effect
        bordered: Bordered table
        borderless: Borderless table
        small: Compact table
        responsive: Responsive table (True or breakpoint)
        variant: Table variant
        caption: Table caption
        **kwargs: Additional attributes

    Examples:
        >>> data = [
        ...     {"name": "Product A", "value": 1234.56, "percent": 0.25, "bytes": 123456789},
        ...     {"name": "Product B", "value": 7890.12, "percent": 0.75, "bytes": 987654321},
        ... ]
        >>> table = (Table(headers=["name", "value", "percent", "bytes"], rows=data)
        ...    .fmt_currency("value")
        ...    .fmt_percent("percent")
        ...    .fmt_bytes("bytes")
        ...    .cols_align(["value", "percent", "bytes"], "right")
        ...    .table_header("Sales Report", "Q4 2024")
        ...    .table_source_note("Source: Internal Sales Database")
        ...    .get_element())
        >>> print(str(table))
    """

    def __init__(
        self,
        *children: ElementChild,
        headers: t.Optional[t.List[str]] = None,
        rows: t.Optional[t.List[t.Dict[str, t.Any]]] = None,
        striped: bool = False,
        hover: bool = False,
        bordered: bool = False,
        borderless: bool = False,
        small: bool = False,
        responsive: t.Union[bool, Size] = False,
        variant: t.Optional[Variant] = None,
        caption: t.Optional[str] = None,
        **kwargs,
    ) -> None:
        super().__init__(*children, **kwargs)
        self._headers = headers
        self._rows = rows
        self._striped = striped
        self._hover = hover
        self._bordered = bordered
        self._borderless = borderless
        self._small = small
        self._responsive = responsive
        self._variant = variant
        self._caption = caption

        # Formatting configurations
        self._formatters: t.Dict[str, t.Callable] = {}
        self._column_alignments: t.Dict[str, str] = {}
        self._column_widths: t.Dict[str, str] = {}
        self._column_labels: t.Dict[str, str] = {}
        self._column_rotations: t.Dict[str, int] = {}
        self._hidden_columns: t.Set[str] = set()
        self._column_order: t.Optional[t.List[str]] = None
        self._header_content: t.Optional[ElementChild] = None
        self._spanners: t.List[t.Tuple[t.List[str], str]] = []
        self._stub_columns: t.Set[str] = set()
        self._stubhead_label: t.Optional[str] = None
        self._source_notes: t.List[str] = []
        self._cell_styles: t.List[t.Tuple[t.Callable, t.Dict[str, str]]] = []
        self._table_options: t.Dict[str, t.Any] = {}
        self._data_colors: t.List[t.Tuple[t.Callable, str, t.Optional[t.Tuple[float, float]]]] = []
        self._missing_substitution: t.Optional[str] = None
        self._zero_substitution: t.Optional[str] = None

    def fmt_number(self, columns: t.Union[str, t.List[str]], decimals: int = 2, use_seps: bool = True) -> "Table":
        """Format numeric values with specified decimal places and separators."""
        cols = [columns] if isinstance(columns, str) else columns
        for col in cols:
            self._formatters[col] = lambda x: f"{x:,.{decimals}f}" if use_seps else f"{x:.{decimals}f}"
        return self

    def fmt_integer(self, columns: t.Union[str, t.List[str]], use_seps: bool = True) -> "Table":
        """Format values as integers."""
        cols = [columns] if isinstance(columns, str) else columns
        for col in cols:
            self._formatters[col] = lambda x: f"{int(x):,}" if use_seps else str(int(x))
        return self

    def fmt_percent(self, columns: t.Union[str, t.List[str]], decimals: int = 1) -> "Table":
        """Format values as percentages."""
        cols = [columns] if isinstance(columns, str) else columns
        for col in cols:
            self._formatters[col] = lambda x: f"{x:.{decimals}%}"
        return self

    def fmt_scientific(self, columns: t.Union[str, t.List[str]], decimals: int = 2) -> "Table":
        """Format values in scientific notation."""
        cols = [columns] if isinstance(columns, str) else columns
        for col in cols:
            self._formatters[col] = lambda x: f"{x:.{decimals}e}"
        return self

    def fmt_currency(self, columns: t.Union[str, t.List[str]], currency: str = "$", decimals: int = 2) -> "Table":
        """Format values as currency."""
        cols = [columns] if isinstance(columns, str) else columns
        for col in cols:
            self._formatters[col] = lambda x: f"{currency}{x:,.{decimals}f}"
        return self

    def fmt_bytes(self, columns: t.Union[str, t.List[str]], binary: bool = True) -> "Table":
        """Format values as bytes with appropriate units."""
        cols = [columns] if isinstance(columns, str) else columns
        for col in cols:

            def format_bytes(x):
                units = ["B", "KiB", "MiB", "GiB", "TiB"] if binary else ["B", "KB", "MB", "GB", "TB"]
                factor = 1024 if binary else 1000
                for unit in units:
                    if abs(x) < factor:
                        return f"{x:.1f} {unit}"
                    x /= factor
                return f"{x:.1f} {units[-1]}"

            self._formatters[col] = format_bytes
        return self

    def fmt_roman(self, columns: t.Union[str, t.List[str]]) -> "Table":
        """Format values as Roman numerals."""
        cols = [columns] if isinstance(columns, str) else columns
        for col in cols:

            def to_roman(n):
                vals = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
                syms = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
                result = ""
                for v, s in zip(vals, syms):
                    count = int(n / v)
                    if count:
                        result += s * count
                        n -= v * count
                return result

            self._formatters[col] = to_roman
        return self

    def fmt_date(self, columns: t.Union[str, t.List[str]], date_style: str = "%Y-%m-%d") -> "Table":
        """Format values as dates."""
        cols = [columns] if isinstance(columns, str) else columns
        for col in cols:
            self._formatters[col] = lambda x: x.strftime(date_style) if hasattr(x, "strftime") else str(x)
        return self

    def fmt_time(self, columns: t.Union[str, t.List[str]], time_style: str = "%H:%M:%S") -> "Table":
        """Format values as times."""
        cols = [columns] if isinstance(columns, str) else columns
        for col in cols:
            self._formatters[col] = lambda x: x.strftime(time_style) if hasattr(x, "strftime") else str(x)
        return self

    def fmt_bool(self, columns: t.Union[str, t.List[str]], true_val: str = "True", false_val: str = "False") -> "Table":
        """Format True and False values."""
        cols = [columns] if isinstance(columns, str) else columns
        for col in cols:
            self._formatters[col] = lambda x: true_val if x else false_val
        return self

    def fmt_datetime(self, columns: t.Union[str, t.List[str]], date_style: str = "%Y-%m-%d %H:%M:%S") -> "Table":
        """Format values as datetimes."""
        cols = [columns] if isinstance(columns, str) else columns
        for col in cols:
            self._formatters[col] = lambda x: x.strftime(date_style) if hasattr(x, "strftime") else str(x)
        return self

    def fmt_units(self, columns: t.Union[str, t.List[str]], unit: str) -> "Table":
        """Format measurement units."""
        cols = [columns] if isinstance(columns, str) else columns
        for col in cols:
            self._formatters[col] = lambda x: f"{x} {unit}"
        return self

    def fmt_image(
        self, columns: t.Union[str, t.List[str]], width: t.Optional[str] = None, height: t.Optional[str] = None
    ) -> "Table":
        """Format image paths to generate images in cells."""
        cols = [columns] if isinstance(columns, str) else columns
        for col in cols:

            def create_img(path):
                img = ht.img(src=str(path), classes="img-fluid")
                if width:
                    img.set_attrs(width=width)
                if height:
                    img.set_attrs(height=height)
                return img

            self._formatters[col] = create_img
        return self

    def fmt_icon(self, columns: t.Union[str, t.List[str]], icon_set: str = "bi") -> "Table":
        """Use icons within table cells."""
        cols = [columns] if isinstance(columns, str) else columns
        for col in cols:
            self._formatters[col] = lambda x: ht.i(classes=f"{icon_set} {icon_set}-{x}")
        return self

    def fmt_nanoplot(self, columns: t.Union[str, t.List[str]]) -> "Table":
        """Format data for nanoplot visualizations (inline sparklines)."""
        cols = [columns] if isinstance(columns, str) else columns
        for col in cols:

            def create_sparkline(data):
                if not isinstance(data, (list, tuple)):
                    return str(data)
                # Create simple SVG sparkline
                if not data:
                    return ""
                min_val = min(data)
                max_val = max(data)
                range_val = max_val - min_val or 1
                width = 100
                height = 20
                points = []
                for i, val in enumerate(data):
                    x = (i / (len(data) - 1)) * width if len(data) > 1 else width / 2
                    y = height - ((val - min_val) / range_val) * height
                    points.append(f"{x},{y}")
                path = " ".join(points)
                return ht.svg(
                    ht.polyline(points=path, fill="none", stroke="currentColor", stroke_width="2"),
                    width=str(width),
                    height=str(height),
                    viewBox=f"0 0 {width} {height}",
                    style="vertical-align: middle;",
                )

            self._formatters[col] = create_sparkline
        return self

    def fmt(self, columns: t.Union[str, t.List[str]], fn: t.Callable) -> "Table":
        """Set a column format with a formatter function."""
        cols = [columns] if isinstance(columns, str) else columns
        for col in cols:
            self._formatters[col] = fn
        return self

    def data_color(
        self,
        columns: t.Union[str, t.List[str]],
        palette: str = "blue",
        domain: t.Optional[t.Tuple[float, float]] = None,
    ) -> "Table":
        """Perform data cell colorization."""
        cols = [columns] if isinstance(columns, str) else columns
        for col in cols:

            def predicate(row, c=col):
                return c in row

            self._data_colors.append((predicate, palette, domain))
        return self

    def sub_missing(self, missing_text: str = "—") -> "Table":
        """Substitute missing values in the table body."""
        self._missing_substitution = missing_text
        return self

    def sub_zero(self, zero_text: str = "—") -> "Table":
        """Substitute zero values in the table body."""
        self._zero_substitution = zero_text
        return self

    def cols_align(
        self, columns: t.Union[str, t.List[str]], align: t.Literal["start", "center", "end", "justify"] = "start"
    ) -> "Table":
        """Set the alignment of one or more columns."""
        cols = [columns] if isinstance(columns, str) else columns
        for col in cols:
            self._column_alignments[col] = align
        return self

    def cols_width(self, columns: t.Union[str, t.List[str]], width: str) -> "Table":
        """Set the widths of columns."""
        cols = [columns] if isinstance(columns, str) else columns
        for col in cols:
            self._column_widths[col] = width
        return self

    def cols_label(self, **labels: str) -> "Table":
        """Relabel one or more columns."""
        self._column_labels.update(labels)
        return self

    def cols_label_rotate(self, columns: t.Union[str, t.List[str]], rotation: int = 45) -> "Table":
        """Rotate the column label for one or more columns."""
        cols = [columns] if isinstance(columns, str) else columns
        for col in cols:
            self._column_rotations[col] = rotation
        return self

    def cols_move(self, columns: t.Union[str, t.List[str]], after: t.Optional[str] = None) -> "Table":
        """Move one or more columns."""
        if self._headers:
            cols = [columns] if isinstance(columns, str) else columns
            new_order = [h for h in self._headers if h not in cols]
            if after:
                idx = new_order.index(after) + 1
                new_order[idx:idx] = cols
            else:
                new_order = cols + new_order
            self._column_order = new_order
        return self

    def cols_move_to_start(self, columns: t.Union[str, t.List[str]]) -> "Table":
        """Move one or more columns to the start."""
        return self.cols_move(columns, after=None)

    def cols_move_to_end(self, columns: t.Union[str, t.List[str]]) -> "Table":
        """Move one or more columns to the end."""
        if self._headers:
            cols = [columns] if isinstance(columns, str) else columns
            new_order = [h for h in self._headers if h not in cols] + cols
            self._column_order = new_order
        return self

    def cols_hide(self, columns: t.Union[str, t.List[str]]) -> "Table":
        """Hide one or more columns."""
        cols = [columns] if isinstance(columns, str) else columns
        self._hidden_columns.update(cols)
        return self

    def cols_unhide(self, columns: t.Union[str, t.List[str]]) -> "Table":
        """Unhide one or more columns."""
        cols = [columns] if isinstance(columns, str) else columns
        self._hidden_columns.difference_update(cols)
        return self

    def table_header(self, title: ElementChild, subtitle: t.Optional[ElementChild] = None) -> "Table":
        """Add a table header."""
        header = ht.div(classes="table-header mb-3")
        if isinstance(title, str):
            header.append(ht.h3(title))
        else:
            header.append(title)
        if subtitle:
            if isinstance(subtitle, str):
                header.append(ht.p(subtitle, classes="text-muted"))
            else:
                header.append(subtitle)
        self._header_content = header
        return self

    def table_spanner(self, label: str, columns: t.List[str]) -> "Table":
        """Insert a spanner above a selection of column headings."""
        self._spanners.append((columns, label))
        return self

    def table_spanner_delim(self, delim: str = "_") -> "Table":
        """Insert spanners by splitting column names with a delimiter."""
        if self._headers:
            groups = {}
            for header in self._headers:
                parts = header.split(delim, 1)
                if len(parts) == 2:
                    group, col = parts
                    if group not in groups:
                        groups[group] = []
                    groups[group].append(header)
            for group, cols in groups.items():
                self._spanners.append((cols, group))
        return self

    def table_stub(self, columns: t.Union[str, t.List[str]]) -> "Table":
        """Add a table stub to emphasize row information."""
        cols = [columns] if isinstance(columns, str) else columns
        self._stub_columns.update(cols)
        return self

    def table_stubhead(self, label: str) -> "Table":
        """Add label text to the stubhead."""
        self._stubhead_label = label
        return self

    def table_source_note(self, source_note: str) -> "Table":
        """Add a source note citation."""
        self._source_notes.append(source_note)
        return self

    def table_style(self, style: t.Dict[str, str], locations: t.Callable[[t.Dict[str, t.Any]], bool]) -> "Table":
        """Add custom style to one or more cells."""
        self._cell_styles.append((locations, style))
        return self

    def table_options(self, **options) -> "Table":
        """Modify the table output options."""
        self._table_options.update(options)
        return self

    def _apply_formatter(self, value: t.Any, column: str) -> t.Any:
        """Apply formatter to a value."""
        if value is None or (isinstance(value, str) and not value):
            if self._missing_substitution is not None:
                return self._missing_substitution
        elif value == 0 and self._zero_substitution is not None:
            return self._zero_substitution

        if column in self._formatters:
            try:
                return self._formatters[column](value)
            except Exception:
                return str(value)
        return value

    def get_element(self) -> Element:
        """Render the table with all formatting applied."""
        container = ht.div()

        # Add header if specified
        if self._header_content:
            container.append(self._header_content)

        table = ht.table(classes="table")
        if self._striped:
            table.add_classes("table-striped")
        if self._hover:
            table.add_classes("table-hover")
        if self._bordered:
            table.add_classes("table-bordered")
        if self._borderless:
            table.add_classes("table-borderless")
        if self._small:
            table.add_classes("table-sm")
        if self._variant:
            table.add_classes(f"table-{self._variant}")

        if self._caption:
            table.append(ht.caption(self._caption))

        if self._headers and self._rows is not None:
            # Determine column order
            headers = self._column_order if self._column_order else self._headers
            headers = [h for h in headers if h not in self._hidden_columns]

            # Create thead with spanners if any
            thead = ht.thead()

            # Add spanner row if there are spanners
            if self._spanners:
                spanner_row = ht.tr()
                processed_cols = set()

                for header in headers:
                    # Check if this column is under a spanner
                    under_spanner = False
                    for cols, label in self._spanners:
                        if header in cols and header not in processed_cols:
                            # Count consecutive columns under this spanner
                            span_count = sum(1 for h in headers if h in cols)
                            spanner_row.append(
                                ht.th(label, colspan=str(span_count), scope="colgroup", classes="text-center")
                            )
                            processed_cols.update(cols)
                            under_spanner = True
                            break

                    if not under_spanner and header not in processed_cols:
                        spanner_row.append(ht.th("", rowspan="2"))
                        processed_cols.add(header)

                thead.append(spanner_row)

            # Main header row
            tr_head = ht.tr()
            for h in headers:
                label = self._column_labels.get(h, h)
                th = ht.th(label, scope="col")

                # Apply column alignment
                if h in self._column_alignments:
                    align = self._column_alignments[h]
                    th.add_classes(f"text-{align}" if align != "justify" else align)

                # Apply column rotation
                if h in self._column_rotations:
                    rotation = self._column_rotations[h]
                    th.set_attrs(style=f"transform: rotate({rotation}deg);")

                # Apply column width
                if h in self._column_widths:
                    th.set_attrs(style=f"width: {self._column_widths[h]};")

                tr_head.append(th)
            thead.append(tr_head)
            table.append(thead)

            # Create tbody
            tbody = ht.tbody()
            for row_idx, row in enumerate(self._rows):
                tr = ht.tr()
                for col_idx, h in enumerate(headers):
                    value = row.get(h, "")
                    formatted_value = self._apply_formatter(value, h)

                    # Create cell
                    if h in self._stub_columns:
                        cell = ht.th(formatted_value, scope="row")
                    else:
                        cell = ht.td(formatted_value)

                    # Apply column alignment
                    if h in self._column_alignments:
                        align = self._column_alignments[h]
                        cell.add_classes(f"text-{align}" if align != "justify" else align)

                    # Apply cell styles
                    cell_style = {}
                    for predicate, style in self._cell_styles:
                        if predicate({"row": row, "column": h, "value": value, "row_idx": row_idx, "col_idx": col_idx}):
                            cell_style.update(style)

                    # Apply data colors
                    for predicate, palette, domain in self._data_colors:
                        if predicate(row):
                            # Simple color gradient based on value
                            if isinstance(value, (int, float)):
                                # Normalize value to 0-1 range
                                if domain:
                                    min_val, max_val = domain
                                else:
                                    # Calculate min/max from all values in this column
                                    col_values = [r.get(h, 0) for r in self._rows if isinstance(r.get(h), (int, float))]
                                    min_val = min(col_values) if col_values else 0
                                    max_val = max(col_values) if col_values else 1

                                if max_val > min_val:
                                    normalized = (value - min_val) / (max_val - min_val)
                                    # Simple blue gradient
                                    if palette == "blue":
                                        intensity = int(255 * (1 - normalized))
                                        cell_style["background-color"] = f"rgb({intensity}, {intensity}, 255)"
                                        cell_style["color"] = "white" if normalized > 0.5 else "black"

                    if cell_style:
                        style_str = "; ".join(f"{k}: {v}" for k, v in cell_style.items())
                        cell.set_attrs(style=style_str)

                    tr.append(cell)
                tbody.append(tr)
            table.append(tbody)
        else:
            for child in self.children:
                table.append(child)

        # Wrap in responsive container if needed
        if self._responsive:
            if self._responsive is True:
                table_wrapper = ht.div(table, classes="table-responsive")
            else:
                table_wrapper = ht.div(table, classes=f"table-responsive-{self._responsive}")
        else:
            table_wrapper = table

        container.append(table_wrapper)

        # Add source notes
        if self._source_notes:
            notes_container = ht.div(classes="table-notes mt-2")
            for note in self._source_notes:
                notes_container.append(ht.small(note, classes="text-muted d-block"))
            container.append(notes_container)

        return container


# Utility Components


class Spinner(Element):
    """
    Bootstrap spinner component.

    Args:
        style: Spinner style (border, grow)
        size: Spinner size (sm)
        variant: Color variant
        label: Screen reader label
        **kwargs: Additional attributes
    """

    def __init__(
        self,
        style: t.Literal["border", "grow"] = "border",
        size: t.Optional[t.Literal["sm"]] = None,
        variant: t.Optional[Variant] = None,
        label: str = "Loading...",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.tag = "div"
        self.add_classes(f"spinner-{style}")
        self.set_attrs(role="status")

        if size:
            self.add_classes(f"spinner-{style}-{size}")

        if variant:
            self.add_classes(f"text-{variant}")

        # Add screen reader text
        self.append(ht.span(label, classes="visually-hidden"))


class Accordion(Element):
    """
    Bootstrap accordion component.

    Args:
        id: Accordion ID
        items: List of accordion items (title, content) tuples
        flush: Flush style
        always_open: Keep other items open
        first_open: If True, first item is open; if False, first item is collapsed
        **kwargs: Additional attributes
    """

    def __init__(
        self,
        id: str,
        items: t.List[t.Tuple[str, ElementChild]],
        flush: bool = False,
        always_open: bool = False,
        first_open: bool = True,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.tag = "div"
        self.add_classes("accordion")
        self.set_attrs(id=id)

        if flush:
            self.add_classes("accordion-flush")

        # Create accordion items
        for i, (title, content) in enumerate(items):
            item_id = f"{id}-item-{i}"
            collapse_id = f"{id}-collapse-{i}"

            item = ht.div(classes="accordion-item")

            # Header
            header = ht.h2(classes="accordion-header", id=item_id)
            button = ht.button(
                title,
                classes="accordion-button",
                type="button",
                data_bs_toggle="collapse",
                data_bs_target=f"#{collapse_id}",
                aria_expanded="true" if (i == 0 and first_open) else "false",
                aria_controls=collapse_id,
            )

            # Collapse all except first if first_open, or collapse all if not first_open
            if (i > 0) or (i == 0 and not first_open):
                button.add_classes("collapsed")

            header.append(button)
            item.append(header)

            # Body
            collapse = ht.div(
                ht.div(content, classes="accordion-body"),
                id=collapse_id,
                classes="accordion-collapse collapse",
                aria_labelledby=item_id,
            )

            if i == 0 and first_open:
                collapse.add_classes("show")

            if not always_open:
                collapse.set_attrs(data_bs_parent=f"#{id}")

            item.append(collapse)
            self.append(item)


class Breadcrumb(Element):
    """
    Bootstrap breadcrumb navigation.

    Args:
        items: List of breadcrumb items (text, href) tuples
        divider: Custom divider
        **kwargs: Additional attributes
    """

    def __init__(self, items: t.List[t.Tuple[str, t.Optional[str]]], divider: t.Optional[str] = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.tag = "nav"
        self.set_attrs(aria_label="breadcrumb")

        if divider:
            self.set_attrs(style=f'--bs-breadcrumb-divider: "{divider}";')

        ol = ht.ol(classes="breadcrumb")

        for i, (text, href) in enumerate(items):
            item = ht.li(classes="breadcrumb-item")

            if i == len(items) - 1:  # Last item
                item.add_classes("active")
                item.set_attrs(aria_current="page")
                item.append(text)
            else:
                item.append(ht.a(text, href=href or "#"))

            ol.append(item)

        self.append(ol)


class Pagination(Element):
    """
    Bootstrap pagination component.

    Args:
        current: Current page number
        total: Total number of pages
        size: Pagination size (sm, lg)
        align: Alignment (start, center, end)
        prev_text: Previous button text
        next_text: Next button text
        **kwargs: Additional attributes
    """

    def __init__(
        self,
        current: int = 1,
        total: int = 1,
        size: t.Optional[t.Literal["sm", "lg"]] = None,
        align: t.Optional[t.Literal["start", "center", "end"]] = None,
        prev_text: str = "Previous",
        next_text: str = "Next",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.tag = "nav"
        self.set_attrs(aria_label="Pagination")

        ul = ht.ul(classes="pagination")

        if size:
            ul.add_classes(f"pagination-{size}")

        if align:
            ul.add_classes(f"justify-content-{align}")

        # Previous button
        prev_item = ht.li(classes="page-item")
        if current == 1:
            prev_item.add_classes("disabled")
        prev_item.append(ht.a(prev_text, href="#", classes="page-link", tabindex="-1" if current == 1 else None))
        ul.append(prev_item)

        # Page numbers
        for page in range(1, total + 1):
            item = ht.li(classes="page-item")
            if page == current:
                item.add_classes("active")
                item.set_attrs(aria_current="page")
            item.append(ht.a(str(page), href="#", classes="page-link"))
            ul.append(item)

        # Next button
        next_item = ht.li(classes="page-item")
        if current == total:
            next_item.add_classes("disabled")
        next_item.append(ht.a(next_text, href="#", classes="page-link", tabindex="-1" if current == total else None))
        ul.append(next_item)

        self.append(ul)


# Dropdown Components


class Dropdown(Element):
    """
    Bootstrap dropdown component.

    Args:
        trigger: Trigger element (button, link, etc.)
        items: List of dropdown items
        direction: Dropdown direction (down, up, start, end)
        split: Split button dropdown
        auto_close: Auto close behavior (true, false, inside, outside)
        **kwargs: Additional attributes
    """

    def __init__(
        self,
        trigger: Element,
        items: t.List[ElementChild],
        direction: t.Literal["down", "up", "start", "end"] = "down",
        split: bool = False,
        auto_close: t.Literal["true", "false", "inside", "outside"] = "true",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.tag = "div"

        if direction == "down":
            self.add_classes("dropdown")
        else:
            self.add_classes(f"drop{direction}")

        # Set up trigger
        if isinstance(trigger, Button):
            trigger.add_classes("dropdown-toggle")
            trigger.set_attrs(data_bs_toggle="dropdown", aria_expanded="false")
        elif hasattr(trigger, "add_classes"):
            trigger.add_classes("dropdown-toggle")
            trigger.set_attrs(data_bs_toggle="dropdown", aria_expanded="false")

        if split:
            # For split dropdowns, the trigger should be a button group
            self.append(trigger)
        else:
            self.append(trigger)

        # Create dropdown menu
        menu = ht.ul(classes="dropdown-menu")
        if auto_close != "true":
            menu.set_attrs(data_bs_auto_close=auto_close)

        for item in items:
            if isinstance(item, str):
                menu.append(DropdownItem(item))
            else:
                menu.append(item)

        self.append(menu)


class DropdownItem(Element):
    """
    Bootstrap dropdown item.

    Args:
        text: Item text
        href: Link URL (makes it a link)
        active: Active state
        disabled: Disabled state
        header: Render as header
        **kwargs: Additional attributes
    """

    def __init__(
        self,
        text: str = "",
        href: t.Optional[str] = None,
        active: bool = False,
        disabled: bool = False,
        header: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.tag = "li"

        if header:
            self.append(ht.h6(text, classes="dropdown-header"))
        else:
            if href:
                link = ht.a(text, href=href, classes="dropdown-item")
            else:
                link = ht.button(text, type="button", classes="dropdown-item")

            if active:
                link.add_classes("active")
            if disabled:
                link.add_classes("disabled")

            self.append(link)


class DropdownDivider(Element):
    """Bootstrap dropdown divider."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.tag = "li"
        self.append(ht.hr(classes="dropdown-divider"))


# Collapse Components


class Collapse(Element):
    """
    Bootstrap collapse component.

    Args:
        id: Collapse ID
        content: Collapsible content
        show: Initially shown
        horizontal: Horizontal collapse
        **kwargs: Additional attributes
    """

    def __init__(
        self,
        id: str,
        content: ElementChild,
        show: bool = False,
        horizontal: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(content, **kwargs)
        self.tag = "div"
        self.set_attrs(id=id)

        classes = ["collapse"]
        if horizontal:
            classes.append("collapse-horizontal")
        if show:
            classes.append("show")

        self.add_classes(*classes)


class CollapseToggle(Button):
    """
    Bootstrap collapse toggle button.

    Args:
        text: Button text
        target: Target collapse ID
        **kwargs: Additional button attributes
    """

    def __init__(self, text: str, target: str, **kwargs) -> None:
        super().__init__(text, **kwargs)
        self.set_attrs(
            data_bs_toggle="collapse", data_bs_target=f"#{target}", aria_expanded="false", aria_controls=target
        )


# Tab Components


class TabContent(Element):
    """
    Bootstrap tab content container.

    Args:
        *children: Tab panes
        **kwargs: Additional attributes
    """

    def __init__(self, *children: ElementChild, **kwargs) -> None:
        super().__init__(*children, **kwargs)
        self.tag = "div"
        self.add_classes("tab-content")


class TabPane(Element):
    """
    Bootstrap tab pane.

    Args:
        id: Pane ID
        content: Pane content
        active: Active pane
        fade: Enable fade animation
        **kwargs: Additional attributes
    """

    def __init__(
        self,
        id: str,
        content: ElementChild,
        active: bool = False,
        fade: bool = True,
        **kwargs,
    ) -> None:
        super().__init__(content, **kwargs)
        self.tag = "div"
        self.set_attrs(id=id, role="tabpanel")

        classes = ["tab-pane"]
        if fade:
            classes.append("fade")
        if active:
            classes.extend(["show", "active"])

        self.add_classes(*classes)


# Carousel Components


class Carousel(Element):
    """
    Bootstrap carousel component.

    Args:
        id: Carousel ID
        items: List of carousel items
        indicators: Show indicators
        controls: Show controls
        fade: Fade transition
        touch: Enable touch swiping
        interval: Auto-cycle interval (milliseconds, False to disable)
        keyboard: Enable keyboard navigation
        pause: Pause on hover behavior
        ride: Auto-start behavior
        wrap: Whether to cycle continuously
        **kwargs: Additional attributes
    """

    def __init__(
        self,
        id: str,
        items: t.List["CarouselItem"],
        indicators: bool = True,
        controls: bool = True,
        fade: bool = False,
        touch: bool = True,
        interval: t.Union[int, bool] = 5000,
        keyboard: bool = True,
        pause: t.Literal["hover", "false"] = "hover",
        ride: t.Literal["carousel", "false"] = "false",
        wrap: bool = True,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.tag = "div"
        self.set_attrs(id=id, data_bs_ride=ride)

        classes = ["carousel", "slide"]
        if fade:
            classes.append("carousel-fade")

        self.add_classes(*classes)

        # Set data attributes
        if interval is not False:
            self.set_attrs(data_bs_interval=str(interval))
        else:
            self.set_attrs(data_bs_interval="false")

        if not touch:
            self.set_attrs(data_bs_touch="false")
        if not keyboard:
            self.set_attrs(data_bs_keyboard="false")
        if pause != "hover":
            self.set_attrs(data_bs_pause=pause)
        if not wrap:
            self.set_attrs(data_bs_wrap="false")

        # Add indicators
        if indicators and items:
            indicators_el = ht.div(classes="carousel-indicators")
            for i in range(len(items)):
                button = ht.button(
                    type="button", data_bs_target=f"#{id}", data_bs_slide_to=str(i), aria_label=f"Slide {i + 1}"
                )
                if i == 0:
                    button.add_classes("active")
                    button.set_attrs(aria_current="true")
                indicators_el.append(button)
            self.append(indicators_el)

        # Add carousel inner
        inner = ht.div(classes="carousel-inner")
        for i, item in enumerate(items):
            if i == 0 and not item.attributes.get("classes", []):
                item.add_classes("active")
            inner.append(item)
        self.append(inner)

        # Add controls
        if controls:
            prev_btn = ht.button(
                ht.span(classes="carousel-control-prev-icon", aria_hidden="true"),
                ht.span("Previous", classes="visually-hidden"),
                classes="carousel-control-prev",
                type="button",
                data_bs_target=f"#{id}",
                data_bs_slide="prev",
            )
            next_btn = ht.button(
                ht.span(classes="carousel-control-next-icon", aria_hidden="true"),
                ht.span("Next", classes="visually-hidden"),
                classes="carousel-control-next",
                type="button",
                data_bs_target=f"#{id}",
                data_bs_slide="next",
            )
            self.append(prev_btn, next_btn)


class CarouselItem(Element):
    """
    Bootstrap carousel item.

    Args:
        content: Item content
        active: Active item
        interval: Custom interval for this item
        **kwargs: Additional attributes
    """

    def __init__(
        self,
        content: ElementChild,
        active: bool = False,
        interval: t.Optional[int] = None,
        **kwargs,
    ) -> None:
        super().__init__(content, **kwargs)
        self.tag = "div"

        classes = ["carousel-item"]
        if active:
            classes.append("active")

        self.add_classes(*classes)

        if interval is not None:
            self.set_attrs(data_bs_interval=str(interval))


# Offcanvas Components


class Offcanvas(Element):
    """
    Bootstrap offcanvas component.

    Args:
        id: Offcanvas ID
        title: Offcanvas title
        body: Offcanvas body content
        placement: Placement (start, end, top, bottom)
        backdrop: Backdrop behavior (true, false, static)
        keyboard: Close with Esc key
        scroll: Allow body scrolling
        **kwargs: Additional attributes
    """

    def __init__(
        self,
        id: str,
        title: t.Optional[str] = None,
        body: t.Optional[ElementChild] = None,
        placement: t.Literal["start", "end", "top", "bottom"] = "start",
        backdrop: t.Literal["true", "false", "static"] = "true",
        keyboard: bool = True,
        scroll: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.tag = "div"
        self.set_attrs(id=id, tabindex="-1")
        self.add_classes("offcanvas", f"offcanvas-{placement}")

        if backdrop != "true":
            self.set_attrs(data_bs_backdrop=backdrop)
        if not keyboard:
            self.set_attrs(data_bs_keyboard="false")
        if scroll:
            self.set_attrs(data_bs_scroll="true")

        # Add header
        if title:
            header = ht.div(
                ht.h5(title, classes="offcanvas-title"),
                ht.button(type="button", classes="btn-close", data_bs_dismiss="offcanvas", aria_label="Close"),
                classes="offcanvas-header",
            )
            self.append(header)

        # Add body
        if body:
            self.append(ht.div(body, classes="offcanvas-body"))


class OffcanvasTrigger(Button):
    """
    Bootstrap offcanvas trigger button.

    Args:
        text: Button text
        target: Target offcanvas ID
        **kwargs: Additional button attributes
    """

    def __init__(self, text: str, target: str, **kwargs) -> None:
        super().__init__(text, **kwargs)
        self.set_attrs(data_bs_toggle="offcanvas", data_bs_target=f"#{target}")


# Toast Components


class Toast(Element):
    """
    Bootstrap toast component.

    Args:
        id: Toast ID
        title: Toast title
        body: Toast body content
        time: Timestamp text
        autohide: Auto hide toast
        delay: Delay before hiding (milliseconds)
        animation: Enable animation
        **kwargs: Additional attributes
    """

    def __init__(
        self,
        id: t.Optional[str] = None,
        title: t.Optional[str] = None,
        body: t.Optional[ElementChild] = None,
        time: t.Optional[str] = None,
        autohide: bool = True,
        delay: int = 5000,
        animation: bool = True,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.tag = "div"
        self.add_classes("toast")
        self.set_attrs(role="alert", aria_live="assertive", aria_atomic="true")

        if id:
            self.set_attrs(id=id)
        if not autohide:
            self.set_attrs(data_bs_autohide="false")
        if delay != 5000:
            self.set_attrs(data_bs_delay=str(delay))
        if not animation:
            self.set_attrs(data_bs_animation="false")

        # Add header
        if title or time:
            header = ht.div(classes="toast-header")
            if title:
                header.append(ht.strong(title, classes="me-auto"))
            if time:
                header.append(ht.small(time, classes="text-muted"))
            header.append(ht.button(type="button", classes="btn-close", data_bs_dismiss="toast", aria_label="Close"))
            self.append(header)

        # Add body
        if body:
            self.append(ht.div(body, classes="toast-body"))


class ToastContainer(Element):
    """
    Bootstrap toast container.

    Args:
        *children: Toast elements
        position: Container position
        **kwargs: Additional attributes
    """

    def __init__(
        self,
        *children: ElementChild,
        position: t.Literal[
            "top-start",
            "top-center",
            "top-end",
            "middle-start",
            "middle-center",
            "middle-end",
            "bottom-start",
            "bottom-center",
            "bottom-end",
        ] = "top-end",
        **kwargs,
    ) -> None:
        super().__init__(*children, **kwargs)
        self.tag = "div"
        self.add_classes("toast-container")

        # Add position classes
        position_classes = {
            "top-start": ["position-fixed", "top-0", "start-0"],
            "top-center": ["position-fixed", "top-0", "start-50", "translate-middle-x"],
            "top-end": ["position-fixed", "top-0", "end-0"],
            "middle-start": ["position-fixed", "top-50", "start-0", "translate-middle-y"],
            "middle-center": ["position-fixed", "top-50", "start-50", "translate-middle"],
            "middle-end": ["position-fixed", "top-50", "end-0", "translate-middle-y"],
            "bottom-start": ["position-fixed", "bottom-0", "start-0"],
            "bottom-center": ["position-fixed", "bottom-0", "start-50", "translate-middle-x"],
            "bottom-end": ["position-fixed", "bottom-0", "end-0"],
        }

        self.add_classes(*position_classes.get(position, []))


# Tooltip and Popover Components


class Tooltip(Element):
    """
    Bootstrap tooltip component.

    Args:
        trigger: Trigger element
        text: Tooltip text
        placement: Tooltip placement
        trigger_event: Trigger event (hover, focus, click)
        **kwargs: Additional attributes
    """

    def __init__(
        self,
        trigger: Element,
        text: str,
        placement: t.Literal["top", "bottom", "start", "end"] = "top",
        trigger_event: t.Literal["hover", "focus", "click"] = "hover",
        **kwargs,
    ) -> None:
        super().__init__(trigger, **kwargs)
        self.tag = "span"

        if hasattr(trigger, "set_attrs"):
            trigger.set_attrs(data_bs_toggle="tooltip", data_bs_placement=placement, title=text)
            if trigger_event != "hover":
                trigger.set_attrs(data_bs_trigger=trigger_event)


class Popover(Element):
    """
    Bootstrap popover component.

    Args:
        trigger: Trigger element
        title: Popover title
        content: Popover content
        placement: Popover placement
        trigger_event: Trigger event
        dismissible: Dismissible popover
        **kwargs: Additional attributes
    """

    def __init__(
        self,
        trigger: Element,
        title: t.Optional[str] = None,
        content: t.Optional[str] = None,
        placement: t.Literal["top", "bottom", "start", "end"] = "top",
        trigger_event: t.Literal["click", "hover", "focus"] = "click",
        dismissible: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(trigger, **kwargs)
        self.tag = "span"

        if hasattr(trigger, "set_attrs"):
            attrs = {"data_bs_toggle": "popover", "data_bs_placement": placement, "data_bs_trigger": trigger_event}

            if title:
                attrs["data_bs_title"] = title
            if content:
                attrs["data_bs_content"] = content
            if dismissible:
                attrs["data_bs_trigger"] = "focus"
                attrs["tabindex"] = "0"

            trigger.set_attrs(**attrs)


# Input Group Components


class InputGroup(Element):
    """
    Bootstrap input group component.

    Args:
        *children: Input group elements
        size: Input group size (sm, lg)
        **kwargs: Additional attributes
    """

    def __init__(self, *children: ElementChild, size: t.Optional[t.Literal["sm", "lg"]] = None, **kwargs) -> None:
        super().__init__(*children, **kwargs)
        self.tag = "div"
        self.add_classes("input-group")

        if size:
            self.add_classes(f"input-group-{size}")


class InputGroupText(Element):
    """
    Bootstrap input group text addon.

    Args:
        text: Addon text
        **kwargs: Additional attributes
    """

    def __init__(self, text: str, **kwargs) -> None:
        super().__init__(text, **kwargs)
        self.tag = "span"
        self.add_classes("input-group-text")


# Utility Components


class Figure(Element):
    """
    Bootstrap figure component.

    Args:
        img_src: Image source
        img_alt: Image alt text
        caption: Figure caption
        **kwargs: Additional attributes
    """

    def __init__(self, img_src: str, img_alt: str = "", caption: t.Optional[str] = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.tag = "figure"
        self.add_classes("figure")

        img = ht.img(src=img_src, alt=img_alt, classes="figure-img img-fluid rounded")
        self.append(img)

        if caption:
            self.append(ht.figcaption(caption, classes="figure-caption"))


class CloseButton(Element):
    """
    Bootstrap close button component.

    Args:
        white: White variant for dark backgrounds
        disabled: Disabled state
        **kwargs: Additional attributes
    """

    def __init__(self, white: bool = False, disabled: bool = False, **kwargs) -> None:
        super().__init__(**kwargs)
        self.tag = "button"
        self.set_attrs(type="button", aria_label="Close")

        classes = ["btn-close"]
        if white:
            classes.append("btn-close-white")

        self.add_classes(*classes)

        if disabled:
            self.set_attrs(disabled=True)


class Range(Element):
    """
    Bootstrap range input component.

    Args:
        name: Input name
        min_val: Minimum value
        max_val: Maximum value
        value: Current value
        step: Step increment
        label: Label text
        disabled: Disabled state
        **kwargs: Additional attributes
    """

    def __init__(
        self,
        name: t.Optional[str] = None,
        min_val: float = 0,
        max_val: float = 100,
        value: t.Optional[float] = None,
        step: float = 1,
        label: t.Optional[str] = None,
        disabled: bool = False,
        **kwargs,
    ) -> None:
        self._label = label

        super().__init__(**kwargs)
        self.tag = "input"
        self.add_classes("form-range")
        self.set_attrs(type="range", min=str(min_val), max=str(max_val), step=str(step))

        if name:
            self.set_attrs(name=name, id=name)
        if value is not None:
            self.set_attrs(value=str(value))
        if disabled:
            self.set_attrs(disabled=True)

    def get_element(self) -> Element:
        """Return the range with label as a form group."""
        if self._label:
            group = FormGroup()

            label_el = ht.label(self._label, for_=self.attributes.get("id", ""))
            label_el.add_classes("form-label")
            group.append(label_el)

            # Create a new range element to avoid circular reference
            range_el = ht.input(**self.attributes)
            group.append(range_el)

            return group

        return self


class Switch(Element):
    """
    Bootstrap switch component (enhanced checkbox).

    Args:
        name: Switch name
        label: Switch label
        checked: Whether switch is checked
        value: Switch value
        disabled: Disabled switch
        **kwargs: Additional attributes
    """

    def __init__(
        self,
        name: t.Optional[str] = None,
        label: t.Optional[str] = None,
        checked: bool = False,
        value: str = "on",
        disabled: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.tag = "div"
        self.add_classes("form-check", "form-switch")

        # Create switch input
        input_attrs: t.Mapping[str, t.Any] = {
            "type": "checkbox",
            "classes": "form-check-input",
            "value": value,
            "role": "switch",
        }

        if name:
            input_attrs["name"] = name
            input_attrs["id"] = f"{name}-switch"

        if checked:
            input_attrs["checked"] = True

        if disabled:
            input_attrs["disabled"] = True

        switch = ht.input(**input_attrs)
        self.append(switch)

        # Add label
        if label:
            label_el = ht.label(label, classes="form-check-label")
            if name:
                label_el.set_attrs(for_=f"{name}-switch")
            self.append(label_el)


class FileInput(Element):
    """
    Bootstrap file input component.

    Args:
        name: Input name
        label: Label text
        multiple: Allow multiple files
        accept: Accepted file types
        disabled: Disabled state
        **kwargs: Additional attributes
    """

    def __init__(
        self,
        name: t.Optional[str] = None,
        label: t.Optional[str] = None,
        multiple: bool = False,
        accept: t.Optional[str] = None,
        disabled: bool = False,
        **kwargs,
    ) -> None:
        self._label = label

        super().__init__(**kwargs)
        self.tag = "input"
        self.add_classes("form-control")
        self.set_attrs(type="file")

        if name:
            self.set_attrs(name=name, id=name)
        if multiple:
            self.set_attrs(multiple=True)
        if accept:
            self.set_attrs(accept=accept)
        if disabled:
            self.set_attrs(disabled=True)

    def get_element(self) -> Element:
        """Return the file input with label as a form group."""
        if self._label:
            group = FormGroup()

            label_el = ht.label(self._label, for_=self.attributes.get("id", ""))
            label_el.add_classes("form-label")
            group.append(label_el)

            # Create a new file input element to avoid circular reference
            file_el = ht.input(**self.attributes)
            group.append(file_el)

            return group

        return self


class Ratio(Element):
    """
    Bootstrap ratio component for responsive embeds.

    Args:
        content: Embedded content
        ratio: Aspect ratio (1x1, 4x3, 16x9, 21x9)
        **kwargs: Additional attributes
    """

    def __init__(
        self,
        content: ElementChild,
        ratio: t.Literal["1x1", "4x3", "16x9", "21x9"] = "16x9",
        **kwargs,
    ) -> None:
        super().__init__(content, **kwargs)
        self.tag = "div"
        self.add_classes("ratio", f"ratio-{ratio}")


class VisuallyHidden(Element):
    """
    Bootstrap visually hidden component for screen readers.

    Args:
        *children: Content for screen readers only
        focusable: Make focusable (visually hidden until focused)
        **kwargs: Additional attributes
    """

    def __init__(self, *children: ElementChild, focusable: bool = False, **kwargs) -> None:
        super().__init__(*children, **kwargs)
        self.tag = "span"

        if focusable:
            self.add_classes("visually-hidden-focusable")
        else:
            self.add_classes("visually-hidden")


class StretchedLink(Element):
    """
    Bootstrap stretched link component.

    Args:
        href: Link URL
        text: Link text
        **kwargs: Additional attributes
    """

    def __init__(self, href: str, text: str = "", **kwargs) -> None:
        super().__init__(text, **kwargs)
        self.tag = "a"
        self.set_attrs(href=href)
        self.add_classes("stretched-link")


# Spacing Utilities


def padding(
    element: Element,
    all: t.Optional[t.Union[int, str]] = None,
    top: t.Optional[t.Union[int, str]] = None,
    bottom: t.Optional[t.Union[int, str]] = None,
    start: t.Optional[t.Union[int, str]] = None,
    end: t.Optional[t.Union[int, str]] = None,
    x: t.Optional[t.Union[int, str]] = None,
    y: t.Optional[t.Union[int, str]] = None,
) -> Element:
    """
    Add Bootstrap padding utilities to an element.

    Args:
        element: Element to add padding to
        all: Padding on all sides (0-5 or "auto")
        top: Top padding
        bottom: Bottom padding
        start: Start padding (left in LTR)
        end: End padding (right in LTR)
        x: Horizontal padding
        y: Vertical padding

    Returns:
        The element with padding classes added
    """
    if all is not None:
        element.add_classes(f"p-{all}")
    if top is not None:
        element.add_classes(f"pt-{top}")
    if bottom is not None:
        element.add_classes(f"pb-{bottom}")
    if start is not None:
        element.add_classes(f"ps-{start}")
    if end is not None:
        element.add_classes(f"pe-{end}")
    if x is not None:
        element.add_classes(f"px-{x}")
    if y is not None:
        element.add_classes(f"py-{y}")
    return element


def margin(
    element: Element,
    all: t.Optional[t.Union[int, str]] = None,
    top: t.Optional[t.Union[int, str]] = None,
    bottom: t.Optional[t.Union[int, str]] = None,
    start: t.Optional[t.Union[int, str]] = None,
    end: t.Optional[t.Union[int, str]] = None,
    x: t.Optional[t.Union[int, str]] = None,
    y: t.Optional[t.Union[int, str]] = None,
) -> Element:
    """
    Add Bootstrap margin utilities to an element.

    Args:
        element: Element to add margin to
        all: Margin on all sides (0-5 or "auto")
        top: Top margin
        bottom: Bottom margin
        start: Start margin (left in LTR)
        end: End margin (right in LTR)
        x: Horizontal margin
        y: Vertical margin

    Returns:
        The element with margin classes added
    """
    if all is not None:
        element.add_classes(f"m-{all}")
    if top is not None:
        element.add_classes(f"mt-{top}")
    if bottom is not None:
        element.add_classes(f"mb-{bottom}")
    if start is not None:
        element.add_classes(f"ms-{start}")
    if end is not None:
        element.add_classes(f"me-{end}")
    if x is not None:
        element.add_classes(f"mx-{x}")
    if y is not None:
        element.add_classes(f"my-{y}")
    return element


# Display Utilities


def display(
    element: Element,
    value: t.Literal[
        "none", "inline", "inline-block", "block", "table", "table-cell", "table-row", "flex", "inline-flex", "grid"
    ],
    breakpoint: t.Optional[Size] = None,
) -> Element:
    """
    Add Bootstrap display utilities to an element.

    Args:
        element: Element to modify
        value: Display value
        breakpoint: Optional breakpoint

    Returns:
        The element with display classes added
    """
    if breakpoint:
        element.add_classes(f"d-{breakpoint}-{value}")
    else:
        element.add_classes(f"d-{value}")
    return element


def flex(
    element: Element,
    direction: t.Optional[t.Literal["row", "row-reverse", "column", "column-reverse"]] = None,
    justify: t.Optional[t.Literal["start", "end", "center", "between", "around", "evenly"]] = None,
    align: t.Optional[t.Literal["start", "end", "center", "baseline", "stretch"]] = None,
    wrap: t.Optional[t.Literal["wrap", "nowrap", "wrap-reverse"]] = None,
    grow: t.Optional[t.Literal[0, 1]] = None,
    shrink: t.Optional[t.Literal[0, 1]] = None,
) -> Element:
    """
    Add Bootstrap flex utilities to an element.

    Args:
        element: Element to modify
        direction: Flex direction
        justify: Justify content
        align: Align items
        wrap: Flex wrap
        grow: Flex grow
        shrink: Flex shrink

    Returns:
        The element with flex classes added
    """
    element.add_classes("d-flex")

    if direction:
        element.add_classes(f"flex-{direction}")
    if justify:
        element.add_classes(f"justify-content-{justify}")
    if align:
        element.add_classes(f"align-items-{align}")
    if wrap:
        element.add_classes(f"flex-{wrap}")
    if grow is not None:
        element.add_classes(f"flex-grow-{grow}")
    if shrink is not None:
        element.add_classes(f"flex-shrink-{shrink}")

    return element


# Helper function to include Bootstrap CSS


def cdn_bootstrap_css(version: str = "5.3.6", theme: t.Optional[str] = None) -> Element:
    """
    Generate Bootstrap CSS link element.

    Args:
        version: Bootstrap version
        theme: Optional Bootswatch theme name

    Returns:
        Link element for Bootstrap CSS
    """
    if theme:
        href = f"https://cdn.jsdelivr.net/npm/bootswatch@{version}/dist/{theme}/bootstrap.min.css"
    else:
        href = f"https://cdn.jsdelivr.net/npm/bootstrap@{version}/dist/css/bootstrap.min.css"

    return ht.link(rel="stylesheet", href=href, crossorigin="anonymous")


def cdn_bootstrap_js(version: str = "5.3.6") -> Element:
    """
    Generate Bootstrap JavaScript bundle script element.

    Args:
        version: Bootstrap version

    Returns:
        Script element for Bootstrap JS
    """
    return ht.script(
        src=f"https://cdn.jsdelivr.net/npm/bootstrap@{version}/dist/js/bootstrap.bundle.min.js", crossorigin="anonymous"
    )


def cdn_bootstrap_icons_css(version: str = "1.13.1") -> Element:
    """
    Generate Bootstrap Icons CSS link element.

    Args:
        version: Bootstrap Icons version

    Returns:
        Link element for Bootstrap Icons CSS
    """
    return ht.link(
        rel="stylesheet",
        href=f"https://cdn.jsdelivr.net/npm/bootstrap-icons@{version}/font/bootstrap-icons.min.css",
    )


def cdn_plotly_js(version: str = "3.0.1") -> Element:
    """
    Generate Plotly JavaScript script element.

    Args:
        version: Plotly version

    Returns:
        Script element for Plotly JS
    """
    return ht.script(src=f"https://cdn.plot.ly/plotly-{version}.min.js", charset="utf-8", type="text/javascript")


class BootstrapDocument(Document):
    def __init__(self, *args, page_title=None, headers=None, status_code=200, **kwargs):
        super().__init__(*args, page_title=page_title, headers=headers, status_code=status_code, **kwargs)
        self.html.set_attrs(data_bs_theme="dark")
        self.head += cdn_bootstrap_css()
        self.head += cdn_bootstrap_js()
        self.head += cdn_plotly_js()
        self.head += ht.style(
            dict2css(
                {
                    ":root,[data-bs-theme=dark]": {
                        "--bs-body-bg": "#000",
                        "--bs-body-color": "#FFF",
                        "--bs-secondary-bg": "#343a40",
                        "--bs-secondary-color": "#adb5bd",
                    },
                    ".plotly-chart-container": {"margin": "0 auto", "width": "100%"},
                    ".plotly-chart": {"margin": "0 auto"},
                    ".plotly .svg-container": {
                        "margin": "0 auto",
                    },
                    ".plot-container.plotly": {
                        "margin": "0 auto",
                        "width": "auto !important",
                        "height": "100%",
                    },
                }
            )
        )


def icon(name: str, classes: t.Optional[t.List[str]] = None, **kwargs) -> Element:
    """
    Generate a Bootstrap icon element.

    Args:
        name: Icon name (e.g., "bi-alarm")
        classes: Additional CSS classes
        **kwargs: Additional attributes

    Returns:
        Icon element
    """
    if classes is None:
        classes = []
    classes.extend(["bi", f"bi-{name}"])

    return ht.i(classes=classes, **kwargs)


__all__ = [
    # Layout Components
    "Container",
    "Row",
    "Col",
    "Stack",
    # Typography Components
    "Heading",
    "Text",
    # Button Components
    "Button",
    "ButtonGroup",
    # Form Components
    "Form",
    "FormGroup",
    "Input",
    "Select",
    "Textarea",
    "Checkbox",
    "Radio",
    # Card Components
    "Card",
    "CardGroup",
    "CardDeck",
    # Navigation Components
    "Nav",
    "NavItem",
    "Navbar",
    # Alert Components
    "Alert",
    "Badge",
    # Progress Components
    "Progress",
    # List Components
    "ListGroup",
    "ListGroupItem",
    # Modal Components
    "Modal",
    "ModalTrigger",
    # Table Components
    "Table",
    # Utility Components
    "Spinner",
    "Accordion",
    "Breadcrumb",
    "Pagination",
    # Dropdown Components
    "Dropdown",
    "DropdownItem",
    "DropdownDivider",
    # Collapse Components
    "Collapse",
    "CollapseToggle",
    # Tab Components
    "TabContent",
    "TabPane",
    # Carousel Components
    "Carousel",
    "CarouselItem",
    # Offcanvas Components
    "Offcanvas",
    "OffcanvasTrigger",
    # Toast Components
    "Toast",
    "ToastContainer",
    # Tooltip and Popover Components
    "Tooltip",
    "Popover",
    # Input Group Components
    "InputGroup",
    "InputGroupText",
    # Additional Utility Components
    "Figure",
    "CloseButton",
    "Range",
    "Switch",
    "FileInput",
    "Ratio",
    "VisuallyHidden",
    "StretchedLink",
    # Utility Functions
    "padding",
    "margin",
    "display",
    "flex",
    "icon",
    # CDN Helpers
    "cdn_bootstrap_css",
    "cdn_bootstrap_js",
    "cdn_bootstrap_icons_css",
    "cdn_plotly_js",
    # Document
    "BootstrapDocument",
    # Enums
    "Breakpoint",
    "Spacing",
]
