from Qt import QtWidgets, QtGui, QtCore


class ClickableFieldWidget(QtWidgets.QCheckBox):
    """
    This is a single item in the FieldsDropdownWidget.
    If you click it, it will trigger `state_changed` and pass one of the
        following: [CHECKED, UNCHECKED]
    """
    state_changed = QtCore.Signal(str, bool)
    UNCHECKED = 0
    CHECKED = 1

    def __init__(self, name, is_checked, parent=None):
        super(ClickableFieldWidget, self).__init__(name, parent)
        self._name = name
        self._state = self.CHECKED if is_checked else self.UNCHECKED
        self._build_ui()
        self.setCheckState(QtCore.Qt.Checked if is_checked else QtCore.Qt.Unchecked)
        self.stateChanged.connect(self._handle_state_changed)

    @QtCore.Slot(bool)
    def _handle_state_changed(self, new_state):
        self.state_changed.emit(self._name, new_state)

    def _build_ui(self):
        # self.setLayout(QtWidgets.QHBoxLayout())
        self.setText(self._name)
        # https://stackoverflow.com/questions/5962503/qt-checkbox-toolbutton-with-custom-distinct-check-unchecked-icons


class FieldsDropdownWidget(QtWidgets.QToolButton):
    """
    This is a class that will group strings by the groupings dict:
    {
        <name>: [<field_names>...]
    }
    `in_use_fields` and `additional_fields` denote initial state.

    When one of the fields get clicked, we will emit either
        `field_unchecked[str]` or `field_checked[str]` for that field.

    """
    field_unchecked = QtCore.Signal(str)
    field_checked = QtCore.Signal(str)

    def __init__(self, groupings, in_use_fields, additional_fields=(), parent=None):
        super(FieldsDropdownWidget, self).__init__(parent)
        self._groupings = groupings
        self._clicked_fields = in_use_fields
        self._unclicked_fields = additional_fields

        self._widgets = {}
        # Build basic dropdown UI
        # Build groups
        #   Build items in each group
        self.clicked.connect(self._show_fields)

        self.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self._menu = QtWidgets.QMenu()
        # self._menu.setMaximumHeight(300)

        icon = QtGui.QIcon.fromTheme("preferences-system")
        self.setIcon(icon)

        self.rebuild_ui()

        self.setMenu(self._menu)

    def rebuild_ui(self):
        for group in self._groupings:
            label = QtWidgets.QLabel("<b>{}</b>".format(group), self)
            label.setAlignment(QtCore.Qt.AlignCenter)
            _action = QtWidgets.QWidgetAction(self._menu)
            _action.setDefaultWidget(label)
            self._menu.addAction(_action)

            self._menu.addSeparator()
            for field_name in self._groupings[group]:
                if field_name in self._clicked_fields:
                    is_checked = True
                else:
                    is_checked = False
                widget = ClickableFieldWidget(field_name, is_checked=is_checked, parent=self)
                widget.state_changed.connect(self._recieve_clicked_field)
                _action = QtWidgets.QWidgetAction(self._menu)
                _action.setDefaultWidget(widget)
                self._menu.addAction(_action)

    @QtCore.Slot()
    def _show_fields(self):
        pass

    @QtCore.Slot(str, bool)
    def _recieve_clicked_field(self, name, new_state):
        if new_state == ClickableFieldWidget.UNCHECKED:
            print("{} is unchecked".format(name))
            self.field_unchecked.emit(name)
        else:
            print("{} is checked".format(name))
            self.field_checked.emit(name)
