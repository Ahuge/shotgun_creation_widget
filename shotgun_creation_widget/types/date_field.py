import datetime

from Qt import QtWidgets, QtCore

from .base_field import WidgetBase


class DateField(QtWidgets.QDateEdit, WidgetBase):
    _TYPE_ = "date"

    def __init__(self, entity_type, field_name, shotgun, value=None,
                 field_data=None, parent=None):
        QtWidgets.QDateEdit.__init__(self, parent)
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
        self.setCalendarPopup(True)
        self.setMinimumWidth(100)
        self.dateChanged.connect(self._handle_date_changed)

    def _default_value(self):
        return datetime.date.today()

    def _set_value(self, value):
        if not value:
            value = self._default_value()
        if not isinstance(value, datetime.date):
            value = datetime.date.fromtimestamp(value)
        self._value = value
        self.setDate(value)

    @QtCore.Slot(datetime.date)
    def _handle_date_changed(self, date):
        self._value = date
        self.value_changed.emit(self._field)
