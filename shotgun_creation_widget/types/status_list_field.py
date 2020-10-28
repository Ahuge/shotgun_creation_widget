from Qt import QtWidgets, QtCore

from .base_field import WidgetBase

# Unsupported


class StatusListField(QtWidgets.QComboBox, WidgetBase):
    _TYPE_ = "status_list"

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
        return self._field_data.get("properties", {}).get("valid_values", {}).get("value", [])

    def setup_widget(self):
        # Cache schema?
        # Background shotgun cacher?
        # Who knows?
        self.addItem("")
        self.setMinimumWidth(125)
        valid_values = self._get_values_for_shotgun_field()
        self.addItems(valid_values)
        self.setSizeAdjustPolicy(self.AdjustToContents)
        self.currentIndexChanged.connect(self._handle_text_changed)

    def _default_value(self):
        return self._get_values_for_shotgun_field()[0]

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
