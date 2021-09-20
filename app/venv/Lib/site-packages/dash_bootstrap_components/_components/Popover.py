# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Popover(Component):
    """A Popover component.
Popover creates a toggleable overlay that can be used to provide additional
information or content to users without having to load a new page or open a
new window.

Use the `PopoverHeader` and `PopoverBody` components to control the layout
of the children.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The children of this component.

- id (string; optional):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app.

- className (string; optional):
    Often used with CSS to style elements with common properties.

- container (string; optional):
    Where to inject the popper DOM node, default body.

- delay (dict; optional):
    Optionally override show/hide delays - default {show: 0, hide:
    250}.

    `delay` is a dict with keys:

    - hide (number; optional)

    - show (number; optional) | number

- flip (boolean; optional):
    Whether to flip the direction of the popover if too close to the
    container edge, default True.

- hide_arrow (boolean; optional):
    Hide popover arrow.

- innerClassName (string; optional):
    CSS class to apply to the popover.

- is_open (boolean; optional):
    Whether the Popover is open or not.

- key (string; optional):
    A unique identifier for the component, used to improve performance
    by React.js while rendering components See
    https://reactjs.org/docs/lists-and-keys.html for more info.

- loading_state (dict; optional):
    Object that holds the loading state object coming from
    dash-renderer.

    `loading_state` is a dict with keys:

    - component_name (string; optional):
        Holds the name of the component that is loading.

    - is_loading (boolean; optional):
        Determines if the component is loading or not.

    - prop_name (string; optional):
        Holds which property is loading.

- offset (string | number; optional):
    Popover offset.

- placement (a value equal to: 'auto', 'auto-start', 'auto-end', 'top', 'top-start', 'top-end', 'right', 'right-start', 'right-end', 'bottom', 'bottom-start', 'bottom-end', 'left', 'left-start', 'left-end'; optional):
    Specify popover placement.

- style (dict; optional):
    Defines CSS styles which will override styles previously set.

- target (string; optional):
    ID of the component to attach the popover to.

- trigger (string; optional):
    Space separated list of triggers (e.g. \"click hover focus
    legacy\"). These specify ways in which the target component can
    toggle the popover. If not specified you must toggle the popover
    yourself using callbacks. Options are: - \"click\": toggles the
    popover when the target is clicked. - \"hover\": toggles the
    popover when the target is hovered over with the cursor. -
    \"focus\": toggles the popover when the target receives focus -
    \"legacy\": toggles the popover when the target is clicked, but
    will also dismiss the popover when the user clicks outside of the
    popover."""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, style=Component.UNDEFINED, className=Component.UNDEFINED, key=Component.UNDEFINED, placement=Component.UNDEFINED, target=Component.UNDEFINED, container=Component.UNDEFINED, trigger=Component.UNDEFINED, is_open=Component.UNDEFINED, hide_arrow=Component.UNDEFINED, innerClassName=Component.UNDEFINED, delay=Component.UNDEFINED, offset=Component.UNDEFINED, flip=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'className', 'container', 'delay', 'flip', 'hide_arrow', 'innerClassName', 'is_open', 'key', 'loading_state', 'offset', 'placement', 'style', 'target', 'trigger']
        self._type = 'Popover'
        self._namespace = 'dash_bootstrap_components'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'className', 'container', 'delay', 'flip', 'hide_arrow', 'innerClassName', 'is_open', 'key', 'loading_state', 'offset', 'placement', 'style', 'target', 'trigger']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Popover, self).__init__(children=children, **args)
