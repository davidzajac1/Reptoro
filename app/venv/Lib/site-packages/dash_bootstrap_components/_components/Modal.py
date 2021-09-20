# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Modal(Component):
    """A Modal component.
Create a toggleable dialog using the Modal component. Toggle the visibility
with the `is_open` prop.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The children of this component.

- id (string; optional):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app.

- autoFocus (boolean; optional):
    Puts the focus on the modal when initialized.

- backdrop (boolean | a value equal to: 'static'; optional):
    Includes a modal-backdrop element. Alternatively, specify 'static'
    for a backdrop which doesn't close the modal on click.

- backdropClassName (string; optional):
    CSS class to apply to the backdrop.

- centered (boolean; optional):
    If True, vertically center modal on page.

- className (string; optional):
    Often used with CSS to style elements with common properties.

- contentClassName (string; optional):
    CSS class to apply to the modal content.

- fade (boolean; optional):
    Set to False for a modal that simply appears rather than fades
    into view.

- is_open (boolean; optional):
    Whether modal is currently open.

- keyboard (boolean; optional):
    Close the modal when escape key is pressed.

- labelledBy (string; optional):
    The ARIA labelledby attribute.

- modalClassName (string; optional):
    CSS class to apply to the modal.

- role (string; optional):
    The ARIA role attribute.

- scrollable (boolean; optional):
    It True, scroll the modal body rather than the entire modal when
    it is too long to all fit on the screen.

- size (string; optional):
    Set the size of the modal. Options sm, lg, xl for small, large or
    extra large sized modals, or leave undefined for default size.

- style (dict; optional):
    Defines CSS styles which will override styles previously set.

- tag (string; optional):
    HTML tag to use for the Modal, default: div.

- zIndex (number | string; optional):
    Set the z-index of the modal. Default 1050."""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, style=Component.UNDEFINED, className=Component.UNDEFINED, tag=Component.UNDEFINED, is_open=Component.UNDEFINED, centered=Component.UNDEFINED, scrollable=Component.UNDEFINED, autoFocus=Component.UNDEFINED, size=Component.UNDEFINED, role=Component.UNDEFINED, labelledBy=Component.UNDEFINED, keyboard=Component.UNDEFINED, backdrop=Component.UNDEFINED, modalClassName=Component.UNDEFINED, backdropClassName=Component.UNDEFINED, contentClassName=Component.UNDEFINED, fade=Component.UNDEFINED, zIndex=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'autoFocus', 'backdrop', 'backdropClassName', 'centered', 'className', 'contentClassName', 'fade', 'is_open', 'keyboard', 'labelledBy', 'modalClassName', 'role', 'scrollable', 'size', 'style', 'tag', 'zIndex']
        self._type = 'Modal'
        self._namespace = 'dash_bootstrap_components'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'autoFocus', 'backdrop', 'backdropClassName', 'centered', 'className', 'contentClassName', 'fade', 'is_open', 'keyboard', 'labelledBy', 'modalClassName', 'role', 'scrollable', 'size', 'style', 'tag', 'zIndex']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Modal, self).__init__(children=children, **args)
