from Qt import QtCore
import six

from ..utils import ShotgunFieldWidgetMeta


@six.add_metaclass(ShotgunFieldWidgetMeta)
class WidgetBase(QtCore.QObject):
    _TYPE_ = None
    value_changed = QtCore.Signal(str)

    def __init__(self, entity_type, field_name, shotgun, value=None, field_data=None, parent=None):
        self.shotgun = shotgun
        self._value = value
        self._entity_type = entity_type
        self._field = field_name
        self._field_data = field_data
        self.setup_widget()

    @property
    def field(self):
        return self._field

    def get_value(self):
        return self._get_value()

    def set_value(self, value):
        self._set_value(value)

    def _default_value(self):
        return ""

    def setup_widget(self):
        raise NotImplementedError

    def _get_value(self):
        return self._value

    def _set_value(self, value):
        # Should set the widget
        raise NotImplementedError
