from Qt import QtWidgets, QtCore

from .base_field import WidgetBase


class TimecodeField(QtWidgets.QLabel, WidgetBase):
    _TYPE_ = "timecode"

    def __init__(self, entity_type, field_name, shotgun, value=None,
                 field_data=None, parent=None):
        QtWidgets.QLabel.__init__(self, parent)
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
        self.setOpenExternalLinks(True)

    def _set_value(self, value):
        if not value:
            value = self._default_value()
        self._value = value
        self.setText(value)
        self.value_changed.emit(self._field)
