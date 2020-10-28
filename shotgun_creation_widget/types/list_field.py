from Qt import QtWidgets, QtCore

from .base_field import WidgetBase

# Unsupported


class ListField(QtWidgets.QComboBox, WidgetBase):
    _TYPE_ = "list"

    def __init__(self, entity_type, field_name, shotgun, value=None,
                 field_data=None, parent=None):
        QtWidgets.QComboBox.__init__(self, parent)
        self._set_value(value)
        WidgetBase.__init__(
            self,
            entity_type=entity_type,
            field_name=field_name,
            shotgun=shotgun,
            value=value,
            field_data=field_data,
        )

    def _get_values_for_shotgun_field(self):
        return self._field_data.get("properties", {}).get("value_values", {})

    def setup_widget(self):
        # Cache schema?
        # Background shotgun cacher?
        # Who knows?
        self.addItem("")
        valid_values = self._get_values_for_shotgun_field()
        self.addItems(valid_values)
        self.currentTextChanged.connect(self._handle_text_changed)

    def _set_value(self, value):
        if not value:
            value = self._default_value()
        self._value = value
        index = self.findText(value)
        if index >= 0:
            self.setCurrentIndex(index)

    @QtCore.Slot(str)
    def _handle_text_changed(self, new_text):
        self._value = new_text
        self.value_changed.emit(self._field)