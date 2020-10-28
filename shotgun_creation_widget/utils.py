from Qt import QtWidgets


_DATA_TYPE_WIDGETS = {}
_FIELD_WIDGETS = {}


def _register_datatype_class(data_type, widget_class):
    if data_type in _DATA_TYPE_WIDGETS:
        raise ValueError(
            "Cannot assign two widget classes to the same data type. "
            "If one of these are meant for a specific field, that field "
            "should be defined using the _FIELDS_ list."
        )
    print("Registering {} to {}".format(data_type, widget_class))
    _DATA_TYPE_WIDGETS[data_type] = widget_class


def _register_field_class(entity, field, widget_class):
    if field in _FIELD_WIDGETS:
        raise ValueError(
            "Cannot assign two widget classes to the same field. "
            "If one of these are meant for a specific field, make sure you "
            "are referring to unique fields using the _FIELDS_ list."
        )
    print("Registering {}.{} to {}".format(entity, field, widget_class))
    _FIELD_WIDGETS["{}.{}".format(entity, field)] = widget_class


class ShotgunFieldWidgetMeta(type(QtWidgets.QWidget)):

    def __new__(mcl, name, bases, data):
        if "_TYPE_" not in data:
            raise ValueError(
                "Widget classes must implement the _TYPE_ class attribute to "
                "define what their mapping is. Class {} did not!".format(name)
            )

        if name != "WidgetBase" and "WidgetBase" not in map(lambda b: b.__name__, bases):
            raise ValueError(
                "Classes using the ShotgunFieldWidgetMeta must inherit from "
                "WidgetBase. Class {} did not!".format(name)
            )

        field_class = super(ShotgunFieldWidgetMeta, mcl).__new__(
            mcl, name, bases, data
        )

        if "_FIELDS_" in data:
            for (entity_type, field_name) in data["_FIELDS_"]:
                _register_field_class(
                    entity=entity_type,
                    field=field_name,
                    widget_class=field_class
                )
        else:
            # this widget is to be used for all fields of a certain type
            _register_datatype_class(
                data_type=data["_TYPE_"], widget_class=field_class
            )

        return field_class


def create_widget(entity_type, field_name, data_type=None, value=None, shotgun=None, field_data=None):
    from .types import WidgetBase
    entity_field = "{}.{}".format(entity_type, field_name)
    if entity_field in _FIELD_WIDGETS:
        return _FIELD_WIDGETS[entity_field](
            entity_type=entity_type, field_name=field_name, value=value, shotgun=shotgun, field_data=field_data,
        )
    if data_type is None:
        data_type = shotgun.schema_field_read(
            entity_type=entity_type,
            field_name=field_name
        ).get(field_name, {}).get("data_type", {}).get("value", None)

    if data_type is None:
        raise ValueError(
            "Unable to find specific field widget for {field} and unable "
            "to determine data type for that field.".format(field=field_name)
        )
    if data_type in _DATA_TYPE_WIDGETS:
        return _DATA_TYPE_WIDGETS[data_type](
            entity_type=entity_type, field_name=field_name, value=value, shotgun=shotgun, field_data=field_data,
        )
    raise ValueError(
        "Unable to find specific data type widget for {data_type} or field "
        "widget for {field}.".format(data_type=data_type, field=field_name)
    )
