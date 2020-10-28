from Qt import QtWidgets, QtCore

from .base_field import WidgetBase

# Unsupported


class ImageField(QtWidgets.QWidget, WidgetBase):
    _TYPE_ = "image"

    def __init__(self, entity_type, field_name, shotgun, value=None,
                 field_data=None, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self._set_value(value)
        WidgetBase.__init__(
            self,
            entity_type=entity_type,
            field_name=field_name,
            shotgun=shotgun,
            value=value,
            field_data=field_data,
        )

    def setup_widget(self):
        # Cache schema?
        # Background shotgun cacher?
        # Who knows?
        pass

    def _set_value(self, value):
        if not value:
            value = self._default_value()
        self._value = value
        # Do stuff
