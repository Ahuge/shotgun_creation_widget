from Qt import QtWidgets, QtCore

from .base_field import WidgetBase


class CurrencyField(QtWidgets.QDoubleSpinBox, WidgetBase):
    _TYPE_ = "currency"

    def __init__(self, entity_type, field_name, shotgun, value=None,
                 field_data=None, parent=None):
        QtWidgets.QDoubleSpinBox.__init__(self, parent)
        self._set_value(value)
        WidgetBase.__init__(
            self,
            entity_type=entity_type,
            field_name=field_name,
            shotgun=shotgun,
            value=value,
            field_data=field_data,
        )
        self._timer = QtCore.QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.setInterval(300)
        self._timer.timeout.connect(self._handle_timeout)

    def setup_widget(self):
        self.setMaximum(float("inf"))
        self.setMinimum(float("-inf"))
        self.setDecimals(2)
        self.setPrefix("$")
        self.setMinimumWidth(100)
        self.valueChanged.connect(self._handle_value_changed)

    def _default_value(self):
        return 0.0

    def _set_value(self, value):
        if not value:
            value = self._default_value()
        self.setValue(value)
        self._value = value

    @QtCore.Slot()
    def _handle_timeout(self):
        self.value_changed.emit(self._field)

    @QtCore.Slot()
    def _handle_value_changed(self, value):
        if self._timer.isActive():
            self._timer.stop()
            self._type_timer.start()

        self._value = value
