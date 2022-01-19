from typing import List, Type

from PySide6.QtCore import Signal
from __feature__ import true_property  # noqa
from PySide6.QtWidgets import QVBoxLayout, QWidget

from converter.connector import BaseConnector, CsvConnector
from converter.runner import BaseRunner, DaskRunner, ModinRunner, PandasRunner
from converter.ui.config_tab.mapping import MappingGroupBox
from converter.ui.fields.dynamic import DynamicClassFormBlock


CONNECTOR_CLASSES: List[Type[BaseConnector]] = list(
    sorted(
        [
            CsvConnector,
        ],
        key=lambda c: c.name,
    )
)

RUNNER_CLASSES: List[Type[BaseRunner]] = list(
    sorted(
        [
            PandasRunner,
            DaskRunner,
            ModinRunner,
        ],
        key=lambda c: c.name,
    )
)


class ConfigTab(QWidget):
    show_all_updated = Signal(bool)

    def __init__(self, parent, root_config_path, force_all_fields=False):
        super().__init__(parent=parent)

        self.root_config_path = root_config_path
        self.force_all_fields = force_all_fields
        self.show_all_fields = force_all_fields
        self.main_window = parent

        self.layout = QVBoxLayout(self)

        # setup mapping config
        self.layout.addWidget(MappingGroupBox(self, root_config_path))

        # setup extractor config
        self.layout.addWidget(
            DynamicClassFormBlock(
                self, "Extractor", f"{root_config_path}.extractor", CONNECTOR_CLASSES
            )
        )

        # setup loader config
        self.layout.addWidget(
            DynamicClassFormBlock(self, "Loader", f"{root_config_path}.loader", CONNECTOR_CLASSES)
        )

        # add runner config
        self.layout.addWidget(
            DynamicClassFormBlock(
                self,
                "Runner",
                f"{root_config_path}.runner",
                RUNNER_CLASSES,
                default_class=PandasRunner,
            )
        )

        self.main_window.running_changed.connect(
            lambda b: self.setEnabled(not b)
        )
