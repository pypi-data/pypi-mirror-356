"""Controller for the measurement module."""

import logging
import json
from PyQt6.QtCore import pyqtSlot, pyqtSignal
from PyQt6.QtWidgets import QApplication

from nqrduck.module.module_controller import ModuleController
from quackseq.measurement import Measurement

from .signalprocessing_options import Apodization, Fitting

logger = logging.getLogger(__name__)


class MeasurementController(ModuleController):
    """Controller for the measurement module.

    This class is responsible for handling the signals from the view and the module and updating the model.

    Args:
        module (Module): The module instance.

    Attributes:
        set_frequency_failure (pyqtSignal): Signal emitted when setting the frequency fails.
        set_averages_failure (pyqtSignal): Signal emitted when setting the averages fails.

    Signals:
        set_frequency_failure: Signal emitted when setting the frequency fails.
        set_averages_failure: Signal emitted when setting the averages fails.
    """

    set_frequency_failure = pyqtSignal()
    set_averages_failure = pyqtSignal()

    def __init__(self, module):
        """Initialize the controller."""
        super().__init__(module)

    @pyqtSlot(bool, str)
    def set_frequency(self, state: bool, value: str) -> None:
        """Set frequency in MHz.

        Args:
            value (str): Frequency in MHz.
            state (bool): State of the input (valid or not).

        Raises:
        ValueError: If value cannot be converted to float.
        """
        # Use validator
        if state:
            self.module.model.frequency_valid = True
            self.module.model.measurement_frequency = float(value) * 1e6
            self.module.nqrduck_signal.emit(
                "set_frequency", str(self.module.model.measurement_frequency)
            )
        else:
            self.module.model.frequency_valid = False

        self.toggle_start_button()

    @pyqtSlot(bool, str)
    def set_averages(self, state: bool, value: str) -> None:
        """Set number of averages.

        Args:
            value (str): Number of averages.
            state (bool): State of the input (valid or not).
        """
        logger.debug("Setting averages to: " + value)
        # self.module.nqrduck_signal.emit("set_averages", value)
        if state:
            self.module.model.averages_valid = True
            self.module.model.averages = int(value)
            self.module.nqrduck_signal.emit(
                "set_averages", str(self.module.model.averages)
            )
        else:
            self.module.model.averages_valid = False

        self.toggle_start_button()

    @pyqtSlot()
    def change_view_mode(self) -> None:
        """Change view mode between time and frequency domain."""
        logger.debug("Changing view mode.")
        if self.module.model.view_mode == self.module.model.FFT_VIEW:
            self.module.model.view_mode = self.module.model.TIME_VIEW
        else:
            self.module.model.view_mode = self.module.model.FFT_VIEW

        logger.debug("View mode changed to: " + self.module.model.view_mode)

    def start_measurement(self) -> None:
        """Emit the start measurement signal."""
        logger.debug("Start measurement clicked")
        self.module.view.measurement_dialog.show()
        QApplication.processEvents()

        # Set the measurement parameters again in case the user switches spectrometer
        self.module.nqrduck_signal.emit(
            "set_frequency", str(self.module.model.measurement_frequency)
        )
        self.module.nqrduck_signal.emit("set_averages", str(self.module.model.averages))
        QApplication.processEvents()

        self.module.nqrduck_signal.emit("start_measurement", None)

    def toggle_start_button(self) -> None:
        """Based on wether the Validators for frequency and averages are in an acceptable state, the start button is enabled or disabled."""
        logger.debug(self.module.model.frequency_valid)
        logger.debug(self.module.model.averages_valid)
        if self.module.model.frequency_valid and self.module.model.averages_valid:
            self.module.view._ui_form.buttonStart.setEnabled(True)
        else:
            self.module.view._ui_form.buttonStart.setEnabled(False)

    def process_signals(self, key: str, value: object) -> None:
        """Process incoming signal from the nqrduck module.

        Args:
            key (str): The key of the signal.
            value (object): The value of the signal.
        """
        logger.debug(
            "Measurement Dialog is visible: "
            + str(self.module.view.measurement_dialog.isVisible())
        )

        if (
            key == "measurement_data"
            and self.module.view.measurement_dialog.isVisible()
        ):
            logger.debug("Received single measurement.")
            self.module.model.add_measurement(value)
            self.module.view.measurement_dialog.hide()

        elif (
            key == "measurement_error"
            and self.module.view.measurement_dialog.isVisible()
        ):
            logger.debug("Received measurement error.")
            self.module.view.measurement_dialog.hide()
            self.module.nqrduck_signal.emit("notification", ["Error", value])

        elif (
            key == "failure_set_frequency"
            and self.module.view._ui_form.frequencyEdit.text() == value
        ):
            logger.debug("Received set frequency failure.")
            self.set_frequency_failure.emit()

        elif (
            key == "failure_set_averages"
            and self.module.view._ui_form.averagesEdit.text() == value
        ):
            logger.debug("Received set averages failure.")
            self.set_averages_failure.emit()
        elif key == "active_spectrometer_changed":
            self.module.view._ui_form.spectrometerLabel.setText(
                f"Spectrometer: {value}"
            )

    def save_measurement(self, file_name: str) -> None:
        """Save measurement to file.

        Args:
            file_name (str): Path to file.
        """
        logger.debug("Saving measurement.")
        if not self.module.model.measurements:
            logger.debug("No measurement to save.")
            return

        measurement = self.module.model.measurements[-1].to_json()

        with open(file_name, "w") as f:
            json.dump(measurement, f)

    def load_measurement(self, file_name: str) -> None:
        """Load measurement from file.

        Args:
            file_name (str): Path to file.
        """
        logger.debug("Loading measurement.")

        try:
            with open(file_name) as f:
                measurement = Measurement.from_json(json.load(f))
                self.module.model.add_measurement(measurement)
                self.module.model.displayed_measurement = measurement
        except FileNotFoundError:
            logger.debug("File not found.")
            self.module.nqrduck_signal.emit(
                "notification", ["Error", "File not found."]
            )
        except (json.JSONDecodeError, KeyError):
            logger.debug("File is not a valid measurement file.")
            self.module.nqrduck_signal.emit(
                "notification", ["Error", "File is not a valid measurement file."]
            )

    def show_apodization_dialog(self) -> None:
        """Show apodization dialog."""
        logger.debug("Showing apodization dialog.")
        # First we  check if there is a measurement.
        if not self.module.model.displayed_measurement:
            logger.debug("No measurement to apodize.")
            self.module.nqrduck_signal.emit(
                "notification", ["Error", "No measurement to apodize."]
            )
            return

        measurement = self.module.model.displayed_measurement

        dialog = Apodization(measurement, parent=self.module.view)
        result = dialog.exec()

        logger.debug("Dialog result: %s", result)
        if not result:
            return

        function = dialog.get_function()

        logger.debug("Apodization function: %s", function)

        apodized_measurement = measurement.apodization(function)

        dialog.deleteLater()

        self.module.model.displayed_measurement = apodized_measurement
        self.module.model.add_measurement(apodized_measurement)

    def show_fitting_dialog(self) -> None:
        """Show fitting dialog."""
        logger.debug("Showing fitting dialog.")
        # First we  check if there is a measurement.
        if not self.module.model.displayed_measurement:
            logger.debug("No measurement to fit.")
            self.module.nqrduck_signal.emit(
                "notification", ["Error", "No measurement to fit."]
            )
            return

        measurement = self.module.model.displayed_measurement

        dialog = Fitting(measurement, parent=self.module.view)
        result = dialog.exec()

        logger.debug("Dialog result: %s", result)
        if not result:
            return

        fit = dialog.get_fit()[1]

        logger.debug("Fitting function: %s", fit)

        measurement.add_fit(fit)

        self.module.view.update_displayed_measurement()

        dialog.deleteLater()

    @pyqtSlot(Measurement)
    def change_displayed_measurement(self, measurement) -> None:
        """Change the displayed measurement.

        If no measurement is provided, the displayed measurement is changed to the selected measurement in the selection box.

        Args:
            measurement (Measurement, optional): The measurement to display.
        """
        logger.debug("Changing displayed measurement.")
        if not self.module.model.measurements:
            logger.debug("No measurements to display.")
            return
        
        self.module.model.displayed_measurement = measurement

        # Adjust the min and max value of the selection box
        n_datasets = measurement.tdy.shape[1]
        self.module.view._ui_form.selectionBox.setRange(0, n_datasets - 1)

        logger.debug(f"Number of datasets: {n_datasets}")

        self.module.model.dataset_index = n_datasets - 1

        self.module.view.update_displayed_measurement()

    @pyqtSlot()
    def change_displayed_dataset(self) -> None:
        """Change the displayed dataset.

        If no dataset is provided, the displayed dataset is changed to the selected dataset in the selection box.
        """
        logger.debug("Changing displayed dataset.")
        if not self.module.model.displayed_measurement:
            logger.debug("No measurement to display.")
            return

        index = self.module.view._ui_form.selectionBox.value()
        self.module.model.dataset_index = index

        self.module.view.update_displayed_measurement()

    @pyqtSlot(Measurement)
    def delete_measurement(self, measurement: Measurement) -> None:
        """Delete a measurement.

        The measurement is removed from the list of measurements. Then the displayed measurement is updated.

        Args:
            measurement (Measurement): The measurement to delete.
        """
        logger.debug("Deleting measurement.")
        self.module.model.remove_measurement(measurement)

        if measurement == self.module.model.displayed_measurement:
            if self.module.model.measurements:
                self.module.model.displayed_measurement = (
                    self.module.model.measurements[-1]
                )
            else:
                self.module.model.displayed_measurement = None

    def edit_measurement(
        self, old_measurement: Measurement, new_measurement: Measurement
    ) -> None:
        """Edit a measurement.

        Args:
            old_measurement (Measurement): The measurement to edit.
            new_measurement (Measurement): The new measurement.
        """
        logger.debug("Editing measurement.")
        # Delete the old measurement
        self.delete_measurement(old_measurement)

        # Add the new measurement
        self.module.model.add_measurement(new_measurement)
        self.module.model.displayed_measurement = new_measurement
