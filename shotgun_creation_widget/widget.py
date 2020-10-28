from Qt import QtWidgets, QtGui, QtCore

from .utils import create_widget
from .dropdown import FieldsDropdownWidget


class ShotgunEntityCreationWidget(QtWidgets.QWidget):
    def __init__(self, shotgun_connection, project_entity, entity_type, data={}, additional_fields=[], parent=None):
        """
        :param shotgun_api3.Shotgun shotgun_connection:
        :param dict project_entity:
        :param str entity_type:
        :param dict data:
        :param list additional_fields:
        :param None|QtWidgets.QWidget parent:
        """
        super(ShotgunEntityCreationWidget, self).__init__(parent)
        self._shotgun = shotgun_connection
        self._entity_type = entity_type
        self._data = data
        self._additional_fields = additional_fields

        self._project = project_entity

        self._required_fields = {}
        self._optional_fields = {}
        self._hidden_fields = {}

        self._field_widgets = {}
        self.fields_form = None

        self._get_schema_data()
        self._build_ui()

    @staticmethod
    def __bold(text):
        return "<b>{}</b>".format(text)

    def _get_schema_data(self):
        schema_data = self._shotgun.schema_field_read(
            self._entity_type, project_entity=self._project
        )
        for field in schema_data:
            field_data = schema_data.get(field, {})
            required = field_data.get("mandatory", {}).get("value", False)
            if required:
                self._required_fields[field] = field_data
            elif field in self._additional_fields or field in self._data:
                self._optional_fields[field] = field_data
            else:
                self._hidden_fields[field] = schema_data.get(field)

    def _build_header_widget(self):
        project_name = self._project.get("name", None)
        if project_name is None:
            filters = [
                ["id", "is", self._project["id"]]
            ]
            fields = [
                "code", "name", "tank_name"
            ]
            self._project = self._shotgun.find_one(
                "Project",
                filters=filters,
                fields=fields
            )
        text = "<b>Create a new {}</b><sub> -{}</sub".format(
            self._entity_type.capitalize(),
            self._project.get("name")
        )
        header_widget = QtWidgets.QWidget(self)
        header_widget.setLayout(QtWidgets.QHBoxLayout())

        label = QtWidgets.QLabel()
        label.setText(text)

        in_use_fields = {}
        for field_name in self._required_fields:
            in_use_fields[field_name] = self._required_fields[field_name]
        for field_name in self._optional_fields:
            in_use_fields[field_name] = self._optional_fields[field_name]
        fields_dropdown = FieldsDropdownWidget(
            groupings={
                "Required": sorted(self._required_fields.keys()),
                "Other": sorted(
                    [k for k in self._optional_fields] +
                    [k for k in self._hidden_fields]
                )
            },
            in_use_fields=(
                [k for k in self._required_fields] +
                [k for k in self._optional_fields]
            ),
            additional_fields=list(self._hidden_fields.keys()),
        )
        fields_dropdown.field_unchecked.connect(self._handle_unchecked_field)
        fields_dropdown.field_checked.connect(self._handle_checked_field)

        header_widget.layout().addWidget(label)
        header_widget.layout().addWidget(fields_dropdown)
        return header_widget

    def _add_entity_field_widget(self, field, field_data):
        if field not in self._field_widgets:
            data_type = field_data.get("data_type", {}).get("value", None)
            value = field_data.get(
                "properties", {}).get("default_value", {}).get("value", None)

            if field in self._data:
                value = self._data[field]

            widget = create_widget(
                entity_type=self._entity_type,
                field_name=field,
                data_type=data_type,
                value=value,
                shotgun=self._shotgun,
                field_data=field_data,
            )
            widget.value_changed.connect(self._update_value_for_field)
            self._field_widgets[field] = widget
        self.fields_form.layout().addRow(
            self.__bold(field),
            self._field_widgets[field]
        )

    def _build_entity_fields_widget(self, fields=None):
        if fields is None:
            fields = {}
            for field_dict in (self._required_fields, self._optional_fields):
                for field in field_dict:
                    fields[field] = field_dict[field]

        self.fields_form = QtWidgets.QWidget(self)
        self.fields_form.setLayout(QtWidgets.QFormLayout())
        for field in fields:
            field_data = fields[field]
            self._add_entity_field_widget(field, field_data)
        return self.fields_form

    def _build_ui(self):
        self.setLayout(QtWidgets.QVBoxLayout())
        print("Building header_widget")
        header_widget = self._build_header_widget()
        print("Building fields_form_widget")
        fields_form_widget = self._build_entity_fields_widget()
        self.layout().addWidget(header_widget)
        self.layout().addWidget(fields_form_widget)
        print("Finished building")

    @QtCore.Slot(str)
    def _update_value_for_field(self, field_name):
        if field_name not in self._field_widgets:
            raise ValueError("Unknown field {}".format(field_name))
        widget = self._field_widgets.get(field_name)
        value = widget.get_value()
        self._data[field_name] = value

    @QtCore.Slot(str)
    def _handle_unchecked_field(self, field_name):
        widget = self._field_widgets.get(field_name)
        self.fields_form.layout().removeRow(widget)
        widget.hide()

    @QtCore.Slot(str)
    def _handle_checked_field(self, field_name):
        if field_name in self._required_fields:
            field_data = self._required_fields[field_name]
        elif field_name in self._optional_fields:
            field_data = self._optional_fields[field_name]
        elif field_name in self._hidden_fields:
            field_data = self._hidden_fields[field_name]
        else:
            print("could not find field {}".format(field_name))
            return
        self._add_entity_field_widget(field=field_name, field_data=field_data)