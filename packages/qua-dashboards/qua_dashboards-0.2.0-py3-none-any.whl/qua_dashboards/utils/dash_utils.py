from typing import Tuple, Optional, Any, Union
from dash import dcc, html
import dash_bootstrap_components as dbc
from plotly import graph_objects as go

__all__ = [
    "convert_to_dash_component",
    "create_input_field",
    "print_component_structure",
    "get_axis_limits",
]


def convert_to_dash_component(elem: Union[dict, list]) -> Any:
    """
    Recursively converts a serialized Dash component (represented as a dict or list)
    into an actual Dash component instance.

    This function supports components from three namespaces:
      - dash_html_components (accessed via `html`)
      - dash_bootstrap_components (accessed via `dbc`)
      - dash_core_components (accessed via `dcc`)

    For Graph components, if the 'figure' property is provided as a dict,
    it is converted into a plotly.graph_objects.Figure instance.

    Args:
        elem: A dictionary or list representing a serialized Dash component.

    Returns:
        An actual Dash component instance.

    Raises:
        ValueError: If an element has an unknown namespace.
    """
    if isinstance(elem, list):
        # Recursively convert each element in the list.
        return [convert_to_dash_component(e) for e in elem]
    elif isinstance(elem, dict):
        # If the element doesn't have a "namespace" key, it's not a serialized component.
        if "namespace" not in elem:
            return {
                key: convert_to_dash_component(value) for key, value in elem.items()
            }

        # Helper to process the 'children' key recursively.
        def process_children(props: dict) -> dict:
            if "children" in props:
                props["children"] = convert_to_dash_component(props["children"])
            return props

        # Copy properties to avoid modifying the original dictionary.
        props = process_children(elem["props"].copy())
        namespace = elem["namespace"]
        comp_type = elem["type"]

        # Convert based on the namespace.
        if namespace == "dash_html_components":
            cls = getattr(html, comp_type)
            return cls(**props)
        elif namespace == "dash_bootstrap_components":
            cls = getattr(dbc, comp_type)
            return cls(**props)
        elif namespace == "dash_core_components":
            cls = getattr(dcc, comp_type)
            # Special handling for Graph: convert a dict figure into a Figure object.
            if comp_type == "Graph" and isinstance(props.get("figure"), dict):
                props["figure"] = go.Figure(**props["figure"])
            return cls(**props)
        else:
            raise ValueError(f"Unknown element: {elem}")
    else:
        # If the element is not a dict or list, return it unchanged.
        return elem


def create_input_field(
    id,
    label,
    value,
    debounce: bool = True,
    input_style: dict = None,
    div_style: dict = None,
    units: str = None,
    type: str = "number",
    **kwargs,
) -> Any:
    """
    Creates a responsive numeric input field wrapped in a Bootstrap Row.

    The function constructs a labeled input using Dash Bootstrap Components.
    An optional units label can be added after the input.

    Args:
        id: The unique identifier for the input component.
        label: The text label for the input.
        value: The initial numeric value for the input.
        debounce: Whether input events should be debounced (default True).
        input_style: A dictionary of CSS styles for the input element (default width of 80px).
        div_style: A dictionary of CSS styles for the container row.
        units: An optional string representing measurement units.
        **kwargs: Additional keyword arguments passed to dbc.Input.

    Returns:
        A dbc.Row containing the label, input field, and optional units.
    """
    if input_style is None:
        input_style = {"width": "80px"}

    elements = [
        dbc.Col(
            dbc.Label(
                f"{label}:",
                html_for=id,
                className="mr-2",
                style={"white-space": "nowrap"},
            ),
            width="auto",
        ),
        dbc.Col(
            dbc.Input(
                id=id,
                type=type,
                value=value,
                debounce=debounce,
                style=input_style,
                **kwargs,
            ),
            width="auto",
        ),
    ]
    if units is not None:
        elements.append(dbc.Col(dbc.Label(units, className="ml-2"), width="auto"))

    return dbc.Row(
        elements,
        className="align-items-center mb-2",
        style=div_style,
    )


def print_component_structure(comp, indent=0):
    """
    Recursively prints the structure of a Dash component.

    Args:
        comp: The component to print.
        indent: The indentation level (default 0).
    """
    space = " " * indent
    comp_id = getattr(comp, "id", None)
    comp_children = getattr(comp, "children", None)
    print(f"{space}{type(comp).__name__} (id={comp_id})")
    if comp_children is None:
        print(f"{space}  No children")
    elif isinstance(comp_children, list):
        for child in comp_children:
            print_component_structure(child, indent + 2)
    else:
        print_component_structure(comp_children, indent + 2)


def get_axis_limits(
    fig: go.Figure,
) -> Tuple[Optional[Tuple[float, float]], Optional[Tuple[float, float]]]:
    """Returns the min and max limits of x and y axes from a Plotly figure.

    This function scans all traces in the figure and calculates the overall
    min and max of their x and y values. It does not rely on explicitly set
    axis ranges, and instead computes them directly from the data.

    Args:
        fig: A Plotly figure containing one or more traces.

    Returns:
        A tuple containing two tuples:
        - x-axis limits as (x_min, x_max), or (None, None) if no x values.
        - y-axis limits as (y_min, y_max), or (None, None) if no y values.

    Raises:
        TypeError: If the provided input is not a Plotly Figure.
    """
    if not isinstance(fig, go.Figure):
        raise TypeError("Input must be a plotly.graph_objects.Figure")

    x_vals, y_vals = [], []

    for trace in fig.data:
        x = getattr(trace, "x", None)
        y = getattr(trace, "y", None)

        if x is not None:
            x_vals.extend(x)
        if y is not None:
            y_vals.extend(y)

    x_limits = (min(x_vals), max(x_vals)) if x_vals else None
    y_limits = (min(y_vals), max(y_vals)) if y_vals else None

    return x_limits, y_limits
