"""The View class for the simulator module."""

from nqrduck_spectrometer.base_spectrometer_view import BaseSpectrometerView


class DuckSimulatorView(BaseSpectrometerView):
    """The View class for the simulator module."""

    def __init__(self, module):
        """Initializes the SimulatorView."""
        super().__init__(module)
        # This automatically generates the settings widget based on the settings in the model
        self.widget = self.load_settings_ui()
