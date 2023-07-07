def field_attr(field, attr, attr_value):
    previous_value = field.widget.attrs.get(attr, '')
    field.widget.attrs[attr] = f'{previous_value} {attr_value}'.strip()
