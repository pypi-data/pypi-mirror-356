"""Creation of the Simulator Spectrometer."""

from nqrduck_spectrometer.base_spectrometer import BaseSpectrometer
from .model import DuckSimulatorModel
from .view import DuckSimulatorView
from .controller import DuckSimulatorController

Simulator = BaseSpectrometer(DuckSimulatorModel, DuckSimulatorView, DuckSimulatorController)
