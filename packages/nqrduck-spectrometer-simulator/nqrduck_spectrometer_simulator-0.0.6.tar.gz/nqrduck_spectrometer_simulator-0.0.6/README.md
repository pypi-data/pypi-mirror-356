# NQRduck Module: Spectrometer Simulator
This module is a part of the NQRduck project. It is a submodule of the [spectrometer module](https://git.private.coffee/nqrduck/nqrduck-spectrometer) for the NQRduck project. It is designed to be used with the [NQRduck](https://git.private.coffee/nqrduck) project.

The module is used to simulate magnetic resonance experiments. It is based on the Bloch simulator by C. Graf [2].

## Installation


### Requirements
The requirements for the module are handled by the pyproject.toml file. The user needs to install the NQRduck core.
The simulator module uses the [nqr-blochsimulator](https://git.private.coffee/nqrduck/nqr-blochsimulator) project for simulation of the bloch equation. This  module is automatically installed when installing the simulator module.

### Setup
To install the module you need the NQRduck core. You can find the installation instructions for the NQRduck core [here](https://git.private.coffee/nqrduck/nqrduck).

Ideally you should install the module in a virtual environment. You can create a virtual environment by running the following command in the terminal:
```bash
python -m venv nqrduck
```

You can install this module and the dependencies by running the following command in the terminal after cloning the repository and navigating to the root directory of the project:
```bash
pip install .
```

Alternatively you can install the module via PyPI:
```bash
pip install nqrduck-spectrometer-simulator
```

## Usage
The pulse sequence is graphically programmed using the [nqrduck-pulseprogrammer](htpps://git.private.coffee/nqrduck-pulseprogrammer) within the NQRduck program under the 'Spectrometer' tab. 


### Notes
The simulator is only usable for Nuclear Quadrupole Resonance (NQR) experiments. It is not intended for Nuclear Magnetic Resonance (NMR) experiments at the moment. This is because the signal equation is different for NMR and NQR. The current implementation does not include the (permanent) $B_0$ field or the z-gradient. I hope to implement NMR simulations in the future.

Additionally this simulator has only been  verified for one sample (BiPh3 at 300K). The simulator should therefore be used with caution and the results should be verified with a real spectrometer.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.