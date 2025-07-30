"""The Controller for the Spectrometer Module.

Careful - this is not the base class for the spectrometer submodules, but the controller for the spectrometer module itself.
"""

import logging
from PyQt6.QtCore import QObject, pyqtSignal, QThread
from nqrduck.module.module_controller import ModuleController
from nqrduck.core.main_controller import MainController
from nqrduck_spectrometer.base_spectrometer import BaseSpectrometer

logger = logging.getLogger(__name__)


class SpectrometerController(ModuleController):
    """This class is the controller for the spectrometer module."""

    def __init__(self, module):
        """This method initializes the controller."""
        super().__init__(module)
        self.measurement_thread = None
        self.measurement_worker = None

    def _load_spectrometer_modules(self) -> None:
        """This method loads the spectrometer (sub-)modules and adds them to the spectrometer model."""
        # Get the modules with entry points in the nqrduck group
        modules = MainController._get_modules()
        logger.debug("Found modules: %s", modules)

        for module_name, module in modules.items():
            # Check if the module instance is a spectrometer by checking if it inherits from BaseSpectrometer
            if not issubclass(type(module), BaseSpectrometer):
                logger.debug(
                    "Module is not a spectrometer: %s ... skipping", module_name
                )
                continue

            # Import the module
            logger.debug("Loading spectrometer module: %s", module_name)
            module.model.widget_changed.connect(
                self._module.view.on_spectrometer_widget_changed
            )
            logger.debug("Adding spectrometer to spectrometer model: %s", module_name)
            self._module.model.add_spectrometers(module_name, module)

            module.controller.on_loading()

        self._module.view.create_menu_entry()

    def process_signals(self, key: str, value: object) -> None:
        """This method processes the signals from the nqrduck module.

        It is called by the nqrduck module when a signal is emitted.
        It then calls the corresponding method of the spectrometer model.

        Args:
            key (str): Name of the signal.
            value (object): Value of the signal.
        """
        # This signal starts a measurement
        if key == "start_measurement":
            self.start_measurement_in_thread()
        # This signal sets the frequency
        elif key == "set_frequency":
            self.module.model.active_spectrometer.controller.set_frequency(value)
        # This signal sets the number of averages
        elif key == "set_averages":
            self.module.model.active_spectrometer.controller.set_averages(value)

    def on_loading(self) -> None:
        """This method is called when the module is loaded.

        It connects the signals from the spectrometer model to the view.
        """
        self._module.model.spectrometer_added.connect(
            self.module.view.on_spectrometer_added
        )
        self._module.model.active_spectrometer_changed.connect(
            self.module.view.on_active_spectrometer_changed
        )
        self._load_spectrometer_modules()

    def on_measurement_start(self) -> None:
        """This method is called when a measurement is started.

        It calls the on_measurement_start method of the active spectrometer.
        """
        logger.debug(
            "Measurement started with spectrometer: %s",
            self.module.model.active_spectrometer,
        )
        self.module.model.active_spectrometer.controller.start_measurement()

    def start_measurement_in_thread(self):
        """This method starts the measurement in a separate QThread."""
        self.measurement_thread = QThread()
        self.measurement_worker = MeasurementWorker(self)
        self.measurement_worker.moveToThread(self.measurement_thread)
        self.measurement_thread.started.connect(self.measurement_worker.run)
        self.measurement_worker.finished.connect(self.measurement_thread.quit)
        self.measurement_worker.finished.connect(self.measurement_worker.deleteLater)
        self.measurement_thread.finished.connect(self.measurement_thread.deleteLater)
        self.measurement_thread.start()


class MeasurementWorker(QObject):
    """Worker class to run the measurement in a separate thread."""

    finished = pyqtSignal()

    def __init__(self, controller):
        """Initialize the worker."""
        super().__init__()
        self.controller = controller

    def run(self):
        """Run the measurement."""
        self.controller.on_measurement_start()
        self.finished.emit()
