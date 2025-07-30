"""Base class for all spectrometer controllers."""

import logging
import ast
from nqrduck.module.module_controller import ModuleController

logger = logging.getLogger(__name__)

class BaseSpectrometerController(ModuleController):
    """The base class for all spectrometer controllers."""

    def __init__(self, module):
        """Initializes the spectrometer controller."""
        super().__init__(module)

    def on_loading(self):
        """Called when the module is loading."""
        logger.debug("Loading spectrometer controller")
        self.module.model.load_default_settings()

    def save_settings(self, path: str) -> None:
        """Saves the settings of the spectrometer."""
        # We get the different settings objects from the model
        settings = self.module.model.quackseq_model.settings

        json = {}
        json["name"] = self.module.model.name

        for setting in settings.values():
            json[setting.name] = setting.value

        with open(path, "w") as f:
            f.write(str(json))

    def load_settings(self, path: str) -> None:
        """Loads the settings of the spectrometer."""
        if path is None:
            logger.error("No settings file selected")
            return
        
        with open(path) as f:
            json = f.read()

        # string to dict
        json = ast.literal_eval(json)

        module_name = self.module.model.name
        json_name = json["name"]

        # For some reason the notification is shown twice
        if module_name != json_name:
            message = f"Module: {module_name} not compatible with module specified in settings file: {json_name}. Did you select the correct settings file?"
            self.module.nqrduck_signal.emit("notification", ["Error", message])
            return

        visual_settings = self.module.model.quackseq_visuals
        for visual_setting in visual_settings.values():
            if visual_setting.setting.name in json:
                visual_setting.value = json[visual_setting.setting.name]
            else:
                message = f"Setting {visual_setting.setting.name} not found in settings file. A change in settings might have broken compatibility."
                self.module.nqrduck_signal.emit("notification", ["Error", message])

    def start_measurement(self):
        """Starts the measurement.

        This method should be called when the measurement is started.
        """
        raise NotImplementedError

    def set_frequency(self, value):
        """Sets the frequency of the spectrometer."""
        raise NotImplementedError

    def set_averages(self, value):
        """Sets the number of averages."""
        raise NotImplementedError
