from silx.gui import qt


class SelectionFilterGroupBox(qt.QGroupBox):
    """GroupBox for configuring the filtering of selected scans"""

    def __init__(self, parent: qt.QWidget | None = None):
        super().__init__("Filter Selection", parent)
        self.setCheckable(True)
        self.setChecked(False)

        layout = qt.QHBoxLayout(self)
        layout.addWidget(qt.QLabel("Scan title patterns:"))
        self._scanTitlePatternsLineEdit = qt.QLineEdit()
        self._scanTitlePatternsLineEdit.setToolTip(
            "Comma-separated list of scan command patterns to keep in selection"
        )
        self._scanTitlePatternsLineEdit.setPlaceholderText("scancommand")
        layout.addWidget(self._scanTitlePatternsLineEdit)

    def getScanTitlePatterns(self) -> tuple[str, ...]:
        """Returns patterns that scan title dataset should match"""
        if not self.isChecked():
            return ()
        text = self._scanTitlePatternsLineEdit.text()
        patterns = [pattern.strip() for pattern in text.split(",")]
        return tuple(p for p in patterns if p)

    def loadSettings(self) -> None:
        settings = qt.QSettings()
        self.setChecked(settings.value("filterSelection/checked", False, type=bool))
        self._scanTitlePatternsLineEdit.setText(
            settings.value("filterSelection/scanTitlePatterns", "", type=str)
        )

    def saveSettings(self) -> None:
        settings = qt.QSettings()
        settings.setValue("filterSelection/checked", self.isChecked())
        settings.setValue(
            "filterSelection/scanTitlePatterns", self._scanTitlePatternsLineEdit.text()
        )
