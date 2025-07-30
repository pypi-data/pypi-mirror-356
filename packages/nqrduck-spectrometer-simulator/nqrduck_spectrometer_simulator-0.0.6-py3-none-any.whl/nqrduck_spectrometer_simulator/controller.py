"""The controller module for the simulator spectrometer."""

import logging
from nqrduck_spectrometer.base_spectrometer_controller import BaseSpectrometerController
from quackseq_simulator.simulator import Simulator
from quackseq.measurement import MeasurementError

logger = logging.getLogger(__name__)


class DuckSimulatorController(BaseSpectrometerController):
    """The controller class for the nqrduck simulator module."""

    def __init__(self, module):
        """Initializes the SimulatorController."""
        super().__init__(module)

    def start_measurement(self):
        """This method is called when the start_measurement signal is received."""
        sequence = self.module.model.pulse_programmer.model.pulse_sequence

        simulator = Simulator()

        simulator.model = self.module.model.quackseq_model

        simulator.model.target_frequency = self.module.model.target_frequency
        simulator.model.averages = self.module.model.averages

        measurement_data = simulator.run_sequence(sequence)

        if isinstance(measurement_data, MeasurementError):
            error_message = measurement_data.error_message
            logger.error("Error during simulation: %s", error_message)
            self.module.nqrduck_signal.emit("measurement_error", error_message)
            return

        if measurement_data:
            # Emit the data to the nqrduck core
            logger.debug("Emitting measurement data")
            self.module.nqrduck_signal.emit("statusbar_message", "Finished Simulation")

            self.module.nqrduck_signal.emit("measurement_data", measurement_data)
        else:
            logger.warning("No measurement data was returned from the simulator")
            self.module.nqrduck_signal.emit(
                "measurement_error",
                "No measurement data was returned from the simulator. Did you set a TX pulse?",
            )

    def set_frequency(self, value: str) -> None:
        """This method is called when the set_frequency signal is received from the core.

        For the simulator this just prints a  warning that the simulator is selected.

        Args:
            value (str) : The new frequency in MHz.
        """
        logger.debug("Setting frequency to: %s", value)
        try:
            self.module.model.target_frequency = float(value)
            logger.debug("Successfully set frequency to: %s", value)
        except ValueError:
            logger.warning("Could not set frequency to: %s", value)
            self.module.nqrduck_signal.emit(
                "notification", ["Error", "Could not set frequency to: " + value]
            )
            self.module.nqrduck_signal.emit("failure_set_frequency", value)

    def set_averages(self, value: str) -> None:
        """This method is called when the set_averages signal is received from the core.

        It sets the averages in the model used for the simulation.

        Args:
            value (str): The value to set the averages to.
        """
        logger.debug("Setting averages to: %s", value)
        try:
            self.module.model.averages = int(value)
            logger.debug("Successfully set averages to: %s", value)
        except ValueError:
            logger.warning("Could not set averages to: %s", value)
            self.module.nqrduck_signal.emit(
                "notification", ["Error", "Could not set averages to: " + value]
            )
            self.module.nqrduck_signal.emit("failure_set_averages", value)
