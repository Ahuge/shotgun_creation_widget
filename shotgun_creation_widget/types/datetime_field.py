import datetime

from Qt import QtWidgets, QtCore

from .base_field import WidgetBase


class DateTimeField(QtWidgets.QDateTimeEdit, WidgetBase):
    _TYPE_ = "date_time"

    def __init__(self, entity_type, field_name, shotgun, value=None,
                 field_data=None, parent=None):
        QtWidgets.QDateTimeEdit.__init__(self, parent)
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
        self.dateTimeChanged.connect(self._handle_date_time_changed)

    def _default_value(self):
        return datetime.datetime.now()

    def _set_value(self, value):
        if not value:
            value = self._default_value()
        if not isinstance(value, datetime.datetime):
            value = datetime.datetime.fromtimestamp(value)
        self._value = value
        self.setDateTime(value)

    @QtCore.Slot(datetime.datetime)
    def _handle_date_time_changed(self, datetime):
        self._value = datetime
        self.value_changed.emit(self._field)
