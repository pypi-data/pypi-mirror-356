"""The model module for the simulator spectrometer."""

import logging
from nqrduck_spectrometer.base_spectrometer_model import BaseSpectrometerModel
from quackseq_simulator.simulator_model import  SimulatorModel


logger = logging.getLogger(__name__)


class DuckSimulatorModel(BaseSpectrometerModel):


    def __init__(self, module):
        """Initializes the SimulatorModel."""
        super().__init__(module)

        self.quackseq_model = SimulatorModel()
        self.visualize_settings()

        # Try to load the pulse programmer module
        try:
            from nqrduck_pulseprogrammer.pulseprogrammer import pulse_programmer

            self.pulse_programmer = pulse_programmer
            logger.debug("Pulse programmer found.")
            self.pulse_programmer.controller.on_loading()
        except ImportError:
            logger.warning("No pulse programmer found.")

    @property
    def averages(self):
        """The number of averages used for the simulation.

        More averages improve the signal-to-noise ratio of the simulated signal.
        """
        return self._averages

    @averages.setter
    def averages(self, value):
        self._averages = value

    @property
    def target_frequency(self):
        """The target frequency for the simulation.

        Doesn't do anything at the moment.
        """
        return self._target_frequency

    @target_frequency.setter
    def target_frequency(self, value):
        self._target_frequency = value
