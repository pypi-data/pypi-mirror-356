"""This module contains the view for the pulse programmer module. It is responsible for displaying the pulse sequence and the pulse parameter options."""

import logging
import functools
from PyQt6.QtGui import QValidator
from PyQt6.QtWidgets import (
    QFormLayout,
    QTableWidget,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QLabel,
    QDialog,
    QLineEdit,
    QDialogButtonBox,
    QWidget,
    QToolButton,
    QSizePolicy,
)
from PyQt6.QtCore import pyqtSlot, pyqtSignal
from nqrduck.module.module_view import ModuleView
from nqrduck.assets.icons import Logos
from nqrduck.helpers.duckwidgets import DuckFloatEdit, DuckEdit

from quackseq.pulseparameters import (
    BooleanOption,
    NumericOption,
    FunctionOption,
    TableOption,
)
from nqrduck.helpers.formbuilder import (
    DuckFormBuilder,
    DuckFormFunctionSelectionField,
    DuckFormCheckboxField,
    DuckFormFloatField,
    DuckTableField,
)

from .visual_parameter import VisualParameter

logger = logging.getLogger(__name__)


class PulseProgrammerView(ModuleView):
    """View for the pulse programmer module."""

    def __init__(self, module):
        """Initializes the pulse programmer view.

        Args:
            module (Module): The module to which this view belongs.
        """
        super().__init__(module)

        self.setup_pulsetable()

        self.setup_variabletables()

    def setup_variabletables(self) -> None:
        """Setup the table for the variables."""
        pass

    def setup_pulsetable(self) -> None:
        """Setup the table for the pulse sequence. Also add buttons for saving and loading pulse sequences and editing and creation of events."""
        # Create pulse table
        self.title = QLabel(f"Pulse Sequence: {self.module.model.pulse_sequence.name}")
        # Make title bold
        font = self.title.font()
        font.setBold(True)
        self.title.setFont(font)

        # Table setup
        self.pulse_table = QTableWidget(self)
        self.pulse_table.setSizeAdjustPolicy(
            QTableWidget.SizeAdjustPolicy.AdjustToContents
        )
        self.pulse_table.setAlternatingRowColors(True)
        layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        table_layout = QHBoxLayout()
        table_layout.addWidget(self.pulse_table)
        table_layout.addStretch(1)
        # Add button for new event
        self.new_event_button = QPushButton("New event")
        # Add the New Icon to the button
        icon = Logos.New16x16()
        self.new_event_button.setIconSize(icon.availableSizes()[0])
        self.new_event_button.setIcon(icon)
        self.new_event_button.clicked.connect(self.on_new_event_button_clicked)
        button_layout.addWidget(self.new_event_button)

        # Add button for save pulse sequence
        self.save_pulse_sequence_button = QPushButton("Save pulse sequence")
        self.save_pulse_sequence_button.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        # Add the Save Icon to the button
        icon = Logos.Save16x16()
        self.save_pulse_sequence_button.setIconSize(icon.availableSizes()[0])
        self.save_pulse_sequence_button.setIcon(icon)
        self.save_pulse_sequence_button.clicked.connect(self.on_save_button_clicked)
        button_layout.addWidget(self.save_pulse_sequence_button)

        # Add button for load pulse sequence
        self.load_pulse_sequence_button = QPushButton("Load pulse sequence")
        # Add the Load Icon to the button
        icon = Logos.Load16x16()
        self.load_pulse_sequence_button.setIconSize(icon.availableSizes()[0])
        self.load_pulse_sequence_button.setIcon(icon)
        self.load_pulse_sequence_button.clicked.connect(self.on_load_button_clicked)
        button_layout.addWidget(self.load_pulse_sequence_button)

        # Connect signals
        self.module.model.events_changed.connect(self.on_events_changed)
        self.module.model.pulse_sequence_changed.connect(self.on_pulse_sequence_changed)

        button_layout.addStretch(1)
        layout.addWidget(self.title)
        layout.addLayout(button_layout)
        layout.addLayout(table_layout)
        layout.addStretch(1)

        self.setLayout(layout)

        # Add layout for the event lengths
        self.event_widget = QWidget()
        self.layout().addWidget(self.event_widget)

        self.on_events_changed()

    @pyqtSlot()
    def on_pulse_sequence_changed(self) -> None:
        """This method is called whenever the pulse sequence changes. It updates the view to reflect the changes."""
        logger.debug(
            "Updating pulse sequence to %s", self.module.model.pulse_sequence.name
        )
        self.title.setText(f"Pulse Sequence: {self.module.model.pulse_sequence.name}")

    @pyqtSlot()
    def on_new_event_button_clicked(self) -> None:
        """This method is called whenever the new event button is clicked. It creates a new event and adds it to the pulse sequence."""
        # Create a QDialog for the new event
        logger.debug("New event button clicked")
        dialog = AddEventDialog(self)
        result = dialog.exec()
        if result:
            event_name = dialog.get_name()
            duration = dialog.get_duration()
            logger.debug(
                "Adding new event with name %s, duration %s", event_name, duration
            )
            self.module.model.add_event(event_name, duration)

    @pyqtSlot()
    def on_events_changed(self) -> None:
        """This method is called whenever the events in the pulse sequence change. It updates the view to reflect the changes."""

        pulse_parameter_options = (
            self.module.model.pulse_sequence.pulse_parameter_options
        )

        logger.debug(
            "Updating pulse parameter options to %s",
            pulse_parameter_options.keys(),
        )
        # We set it to the length of the pulse parameter options + 1 because we want to add a row for the parameter option buttons
        self.pulse_table.setRowCount(len(pulse_parameter_options) + 1)
        # Move the vertical header labels on row down
        pulse_options = [""]
        pulse_options.extend(list(pulse_parameter_options.keys()))
        self.pulse_table.setVerticalHeaderLabels(pulse_options)

        logger.debug("Updating events to %s", self.module.model.pulse_sequence.events)

        # Add label for the event lengths
        event_layout = QVBoxLayout()
        event_parameters_label = QLabel("Event lengths:")
        event_layout.addWidget(event_parameters_label)

        for event in self.module.model.pulse_sequence.events:
            logger.debug("Adding event to pulseprogrammer view: %s", event.name)
            # Create a label for the event
            event_label = QLabel(f"{event.name} : {event.duration * 1e6:.16g} µs")
            event_layout.addWidget(event_label)

        # Delete the old widget and create a new one
        self.event_widget.deleteLater()
        self.event_widget = QWidget()
        self.event_widget.setLayout(event_layout)
        self.layout().addWidget(self.event_widget)

        self.pulse_table.setColumnCount(len(self.module.model.pulse_sequence.events))
        self.pulse_table.setHorizontalHeaderLabels(
            [event.name for event in self.module.model.pulse_sequence.events]
        )

        self.set_parameter_icons()

    def set_parameter_icons(self) -> None:
        """This method sets the icons for the pulse parameter options."""
        pulse_parrameter_options = (
            self.module.model.pulse_sequence.pulse_parameter_options
        )

        for column_idx, event in enumerate(self.module.model.pulse_sequence.events):
            for row_idx, parameter in enumerate(pulse_parrameter_options.keys()):
                if row_idx == 0:
                    event_options_widget = EventOptionsWidget(event)
                    # Connect the delete_event signal to the on_delete_event slot
                    func = functools.partial(
                        self.module.controller.delete_event, event_name=event.name
                    )
                    event_options_widget.delete_event.connect(func)
                    # Connect the change_event_duration signal to the on_change_event_duration slot
                    event_options_widget.change_event_duration.connect(
                        self.module.controller.change_event_duration
                    )
                    # Connect the change_event_name signal to the on_change_event_name slot
                    event_options_widget.change_event_name.connect(
                        self.module.controller.change_event_name
                    )
                    # Connect the move_event_left signal to the on_move_event_left slot
                    event_options_widget.move_event_left.connect(
                        self.module.controller.on_move_event_left
                    )
                    # Connect the move_event_right signal to the on_move_event_right slot
                    event_options_widget.move_event_right.connect(
                        self.module.controller.on_move_event_right
                    )

                    self.pulse_table.setCellWidget(
                        row_idx, column_idx, event_options_widget
                    )
                    self.pulse_table.setRowHeight(
                        row_idx, event_options_widget.layout().sizeHint().height()
                    )

                logger.debug(
                    "Adding button for event %s and parameter %s", event, parameter
                )
                logger.debug("Parameter object id: %s", id(event.parameters[parameter]))
                button = QPushButton()

                icon = VisualParameter(event.parameters[parameter]).get_pixmap()
                logger.debug("Icon size: %s", icon.availableSizes())
                button.setIcon(icon)
                button.setIconSize(icon.availableSizes()[0])
                button.setFixedSize(icon.availableSizes()[0])

                # We add 1 to the row index because the first row is used for the event options
                self.pulse_table.setCellWidget(row_idx + 1, column_idx, button)
                self.pulse_table.setRowHeight(
                    row_idx + 1, icon.availableSizes()[0].height()
                )
                self.pulse_table.setColumnWidth(
                    column_idx, icon.availableSizes()[0].width()
                )

                # Connect the button to the on_button_clicked slot
                func = functools.partial(
                    self.on_table_button_clicked, event=event, parameter=parameter
                )
                button.clicked.connect(func)

    @pyqtSlot()
    def on_table_button_clicked(self, event, parameter) -> None:
        """This method is called whenever a button in the pulse table is clicked.

        It opens a dialog to set the options for the parameter.

        Args:
            event (PulseSequence.Event): The event for which the parameter options should be set.
            parameter (str): The name of the parameter for which the options should be set.
        """
        logger.debug("Button for event %s and parameter %s clicked", event, parameter)
        # We assume the pulse sequence was updated
        self.module.model.pulse_sequence.update_options()

        # Create a QDialog to set the options for the parameter.
        description = f"Set options for {parameter}"
        dialog = DuckFormBuilder(parameter, description=description, parent=self)

        # Adding fields for the options
        form_options = []
        for option in event.parameters[parameter].options:
            logger.debug(f"Option value is {option.value}")
            if isinstance(option, TableOption):
                # Every option is it's own column. Every column has a dedicated number of rows.
                # Get the option name:
                name = option.name
                table = DuckTableField(name, tooltip=None)

                columns = option.columns

                for column in columns:
                    # Every table option has a number of rows
                    fields = []
                    for row in column.options:
                        fields.append(self.get_field_for_option(row, event))

                    name = column.name

                    logger.debug(f"Adding column {name} with fields {fields}")
                    table.add_column(option=column, fields=fields)

                form_options.append(table)
                dialog.add_field(table)

            else:
                field = self.get_field_for_option(option, event)
                form_options.append(field)
                dialog.add_field(field)

        result = dialog.exec()

        options = event.parameters[parameter].options

        if result:
            values = dialog.get_values()
            for i, value in enumerate(values):
                logger.debug(f"Setting value {value} for option {options[i]}")
                options[i].set_value(value)

            self.set_parameter_icons()

    def get_field_for_option(self, option, event):
        """Returns the field for the given option.

        Args:
            option (Option): The option for which the field should be created.
            event (PulseSequence.Event): The event for which the option should be created.

        Returns:
            DuckFormField: The field for the option
        """
        logger.debug(f"Creating field with value {option.value}")
        if isinstance(option, BooleanOption):
            field = DuckFormCheckboxField(
                option.name, tooltip=None, default=option.value
            )
        elif isinstance(option, NumericOption):
            # We only show the slider if both min and max values are set
            if option.min_value is not None and option.max_value is not None:
                slider = True
            else:
                slider = False

            if slider:
                slider = option.slider

            field = DuckFormFloatField(
                option.name,
                tooltip=None,
                default=option.value,
                min_value=option.min_value,
                max_value=option.max_value,
                slider=slider,
            )

        elif isinstance(option, FunctionOption):
            logger.debug(f"Functions: {option.functions}")

            # When loading a pulse sequence, the instance of the objects will be different
            # Therefore we need to operate on the classes
            for function in option.functions:
                if function.__class__.__name__ == option.value.__class__.__name__:
                    default_function = function

            index = option.functions.index(default_function)

            field = DuckFormFunctionSelectionField(
                option.name,
                tooltip=None,
                functions=option.functions,
                duration=event.duration,
                default_function=index,
            )

        logger.debug(f"Returning Field: {field}")
        return field

    @pyqtSlot()
    def on_save_button_clicked(self) -> None:
        """This method is called whenever the save button is clicked. It opens a dialog to select a file to save the pulse sequence to."""
        logger.debug("Save button clicked")
        file_manager = self.FileManager(self.module.model.FILE_EXTENSION, parent=self)
        file_name = file_manager.saveFileDialog()
        if file_name:
            self.module.controller.save_pulse_sequence(file_name)

    @pyqtSlot()
    def on_load_button_clicked(self) -> None:
        """This method is called whenever the load button is clicked. It opens a dialog to select a file to load the pulse sequence from."""
        logger.debug("Load button clicked")
        file_manager = self.FileManager(self.module.model.FILE_EXTENSION, parent=self)
        file_name = file_manager.loadFileDialog()
        if file_name:
            try:
                self.module.controller.load_pulse_sequence(file_name)
            except KeyError:
                self.module.nqrduck_signal.emit(
                    "notification",
                    [
                        "Error",
                        "Error loading pulse sequence -  maybe the version of the pulse sequence is not compatible?",
                    ],
                )


class EventOptionsWidget(QWidget):
    """This class is a widget that can be used to set the options for a pulse parameter.

    This widget is then added to the the first row of the according event column in the pulse table.
    It has a edit button that opens a dialog that allows the user to change the options for the event (name and duration).
    Furthermore it has a delete button that deletes the event from the pulse sequence.

    Signals:
        delete_event: Emitted when the delete button is clicked.
        change_event_duration: Emitted when the duration of the event is changed.
        change_event_name: Emitted when the name of the event is changed.
        move_event_left: Emitted when the move left button is clicked.
        move_event_right: Emitted when the move right button is clicked.
    """

    delete_event = pyqtSignal(str)
    change_event_duration = pyqtSignal(str, str)
    change_event_name = pyqtSignal(str, str)
    move_event_left = pyqtSignal(str)
    move_event_right = pyqtSignal(str)

    def __init__(self, event):
        """Initializes the EventOptionsWidget."""
        super().__init__()
        self.event = event

        layout = QVBoxLayout()
        upper_layout = QHBoxLayout()
        # Edit button
        self.edit_button = QToolButton()
        icon = Logos.Pen12x12()
        self.edit_button.setIcon(icon)
        self.edit_button.setIconSize(icon.availableSizes()[0])
        self.edit_button.setFixedSize(icon.availableSizes()[0])
        self.edit_button.clicked.connect(self.edit_event)

        # Delete button
        self.delete_button = QToolButton()
        icon = Logos.Garbage12x12()
        self.delete_button.setIcon(icon)
        self.delete_button.setIconSize(icon.availableSizes()[0])
        self.delete_button.setFixedSize(icon.availableSizes()[0])
        self.delete_button.clicked.connect(self.create_delete_event_dialog)

        upper_layout.addWidget(self.edit_button)
        upper_layout.addWidget(self.delete_button)

        lower_layout = QHBoxLayout()
        # Move left button
        self.move_left_button = QToolButton()
        icon = Logos.ArrowLeft12x12()
        self.move_left_button.setIcon(icon)
        self.move_left_button.setIconSize(icon.availableSizes()[0])
        self.move_left_button.setFixedSize(icon.availableSizes()[0])
        self.move_left_button.clicked.connect(self.move_event_left_button_clicked)

        # Move right button
        self.move_right_button = QToolButton()
        icon = Logos.ArrowRight12x12()
        self.move_right_button.setIcon(icon)
        self.move_right_button.setIconSize(icon.availableSizes()[0])
        self.move_right_button.setFixedSize(icon.availableSizes()[0])
        self.move_right_button.clicked.connect(self.move_event_right_button_clicked)

        lower_layout.addWidget(self.move_left_button)
        lower_layout.addWidget(self.move_right_button)

        layout.addLayout(upper_layout)
        layout.addLayout(lower_layout)

        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    @pyqtSlot()
    def edit_event(self) -> None:
        """This method is called when the edit button is clicked. It opens a dialog that allows the user to change the event name and duration.

        If the user clicks ok, the change_event_name and change_event_duration signals are emitted.
        """
        logger.debug("Edit button clicked for event %s", self.event.name)

        # Create a QDialog to edit the event
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit event")
        layout = QVBoxLayout()
        label = QLabel(f"Edit event: {self.event.name}")
        layout.addWidget(label)

        # Create the inputs for event name, duration
        event_form_layout = QFormLayout()
        name_label = QLabel("Name:")
        name_lineedit = QLineEdit(self.event.name)
        event_form_layout.addRow(name_label, name_lineedit)

        duration_label = QLabel("Duration (µs):")
        duration_lineedit = QLineEdit()

        duration_lineedit.setText("%.16g" % (self.event.duration * 1e6))

        event_form_layout.addRow(duration_label, duration_lineedit)
        layout.addLayout(event_form_layout)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        dialog.setLayout(layout)
        result = dialog.exec()
        if result:
            logger.debug("Editing event %s", self.event.name)
            if name_lineedit.text() != self.event.name:
                self.change_event_name.emit(self.event.name, name_lineedit.text())
            if duration_lineedit.text() != str(self.event.duration):
                self.change_event_duration.emit(
                    self.event.name, duration_lineedit.text()
                )

    @pyqtSlot()
    def create_delete_event_dialog(self) -> None:
        """This method is called when the delete button is clicked.

        It creates a dialog that asks the user if he is sure he wants to delete the event.
        If the user clicks yes, the delete_event signal is emitted.
        """
        # Create an 'are you sure' dialog
        logger.debug("Delete button clicked")
        dialog = QDialog(self)
        dialog.setWindowTitle("Delete event")
        layout = QVBoxLayout()
        label = QLabel(f"Are you sure you want to delete event {self.event.name}?")
        layout.addWidget(label)
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Yes | QDialogButtonBox.StandardButton.No
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        dialog.setLayout(layout)
        result = dialog.exec()
        if result:
            self.delete_event.emit(self.event.name)

    @pyqtSlot()
    def move_event_left_button_clicked(self) -> None:
        """This method is called when the move left button is clicked."""
        logger.debug("Move event left: %s", self.event.name)
        self.move_event_left.emit(self.event.name)

    def move_event_right_button_clicked(self) -> None:
        """This method is called when the move right button is clicked."""
        logger.debug("Move event right: %s", self.event.name)
        self.move_event_right.emit(self.event.name)


class AddEventDialog(QDialog):
    """This dialog is created whenever a new event is added to the pulse sequence. It allows the user to enter a name for the event."""

    def __init__(self, parent=None):
        """Initializes the AddEventDialog."""
        super().__init__(parent)

        self.setWindowTitle("Add Event")

        self.layout = QFormLayout(self)

        self.name_layout = QHBoxLayout()

        self.label = QLabel("Enter event name:")
        self.name_input = DuckEdit()
        self.name_input.validator = self.NameInputValidator(self)

        self.name_layout.addWidget(self.label)
        self.name_layout.addStretch(1)
        self.name_layout.addWidget(self.name_input)

        self.layout.addRow(self.name_layout)

        self.duration_layout = QHBoxLayout()

        self.duration_label = QLabel("Duration (µs):")
        self.duration_lineedit = DuckFloatEdit(min_value=0)
        self.duration_lineedit.setText("20")

        self.duration_layout.addWidget(self.duration_label)
        self.duration_layout.addStretch(1)
        self.duration_layout.addWidget(self.duration_lineedit)

        self.layout.addRow(self.duration_layout)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
            self,
        )

        self.buttons.accepted.connect(self.check_input)
        self.buttons.rejected.connect(self.reject)

        self.layout.addWidget(self.buttons)

    def get_name(self) -> str:
        """Returns the name entered by the user.

        Returns:
        str: The name entered by the user
        """
        return self.name_input.text()

    def get_duration(self) -> float:
        """Returns the duration entered by the user, or a fallback value.

        Returns:
            float: The duration value provided by the user, or 20
        """
        return self.duration_lineedit.text() or 20

    def check_input(self) -> None:
        """Checks if the name and duration entered by the user is valid. If it is, the dialog is accepted. If not, the user is informed of the error."""
        if (
            self.duration_lineedit.validator.validate(self.duration_lineedit.text(), 0)[
                0
            ]
            == QValidator.State.Acceptable
            and self.name_input.validator.validate(self.name_input.text(), 0)[0]
            == QValidator.State.Acceptable
        ):
            self.accept()

    class NameInputValidator(QValidator):
        """A validator for the name input field.

        This is used to validate the input of the QLineEdit widget.
        """

        def validate(self, value, position):
            """Validates the input value.

            Args:
                value (str): The input value
                position (int): The position of the cursor

            Returns:
                Tuple[QValidator.State, str, int]: The validation state, the fixed value, and the position
            """
            if not value:
                return (QValidator.State.Intermediate, value, position)

            if any(
                [
                    event.name == value
                    for event in self.parent()
                    .parent()
                    .module.model.pulse_sequence.events
                ]
            ):
                return (QValidator.State.Invalid, value, position)

            return (QValidator.State.Acceptable, value, position)
