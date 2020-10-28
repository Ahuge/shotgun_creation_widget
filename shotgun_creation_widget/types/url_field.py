from Qt import QtWidgets, QtCore

from .base_field import WidgetBase


class UrlField(QtWidgets.QWidget, WidgetBase):
    # https://github.com/shotgunsoftware/tk-framework-qtwidgets/blob/master/python/shotgun_fields/file_link_widget.py
    _TYPE_ = "url"

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

    def _set_value(self, value):
        if not value:
            value = self._default_value()
        # Build UI
        # Test URL value?
        # Background shotgun cacher?
        # Who knows?
        pass
