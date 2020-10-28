from Qt import QtWidgets, QtCore

from .base_field import WidgetBase


class CheckboxField(QtWidgets.QCheckBox, WidgetBase):
    _TYPE_ = "checkbox"

    def __init__(self, entity_type, field_name, shotgun, value=None,
                 field_data=None, parent=None):
        QtWidgets.QCheckBox.__init__(self, parent)
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
        self.stateChanged.connect(self._handle_state_changed)

    def _default_value(self):
        return QtCore.Qt.Unchecked

    def _set_value(self, value):
        if not value:
            value = self._default_value()
        self.setCheckState(QtCore.Qt.Checked if value else QtCore.Qt.Unchecked)
        self._value = value

    @QtCore.Slot(bool)
    def _handle_state_changed(self, value):
        self._value = value
        self.value_changed.emit(self._field)
