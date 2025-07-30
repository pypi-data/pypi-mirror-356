import fnmatch
import logging

import hdf5plugin  # noqa
import h5py

from silx.gui import qt
from silx.gui.data.DataViewerFrame import DataViewerFrame
import silx.io

from .hdf5treeview import Hdf5TreeView
from .selection_filter_groupbox import SelectionFilterGroupBox
from .utils import extractScanNumber, ScanEntry


_logger = logging.getLogger(__name__)


class Hdf5Widget(qt.QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.__loadedFiles: set[str] = set()

        self.__treeview = Hdf5TreeView(self)

        self.__dataViewer = DataViewerFrame(self)
        self.__treeview.h5NodeActivated.connect(self.__dataViewer.setData)

        self.__treeview.setMinimumSize(150, 200)
        self.__dataViewer.setMinimumSize(200, 200)

        splitter = qt.QSplitter(self)
        splitter.addWidget(self.__treeview)
        splitter.addWidget(self.__dataViewer)

        splitter.setCollapsible(0, False)
        splitter.setCollapsible(1, False)

        splitter.setHandleWidth(10)
        splitter.setStretchFactor(1, 1)

        self._selectionFilterGroupBox = SelectionFilterGroupBox(self)

        layout = qt.QVBoxLayout(self)
        layout.setContentsMargins(qt.QMargins())
        layout.addWidget(splitter, stretch=1)
        layout.addWidget(self._selectionFilterGroupBox, stretch=0)

    def addFile(self, filename: str) -> None:
        """
        Add a file to the HDF5 tree viewer.

        Prevents adding duplicate files by checking if the file is already loaded.

        Args:
            filename: Path to the HDF5 file to add.
        """
        if filename in self.__loadedFiles:
            qt.QMessageBox.information(
                self,
                "Duplicate File",
                f"This file {filename} is already loaded.",
            )
            return

        self.__treeview.findHdf5TreeModel().appendFile(filename)
        self.__loadedFiles.add(filename)

    def clearFiles(self) -> None:
        """
        Remove and close all files currently loaded in the HDF5 tree viewer.

        Resets the internal file tracking list.
        """
        self.__treeview.findHdf5TreeModel().clear()
        self.__loadedFiles.clear()

    def getLoadedFiles(self) -> set[str]:
        """
        Get the set of currently loaded files in the HDF5 tree viewer.

        Returns:
            A set containing the file paths of all loaded files.
        """
        return self.__loadedFiles

    def isEmpty(self) -> bool:
        """
        Check if the HDF5 tree viewer contains any loaded files.

        Returns:
            True if no files are currently loaded, False otherwise.
        """
        return len(self.__loadedFiles) == 0

    def reloadSelected(self) -> None:
        """
        Reload the currently selected HDF5 nodes.
        """
        model = self.__treeview.findHdf5TreeModel()
        for obj in tuple(self.__treeview.selectedH5Nodes()):
            if obj.ntype is h5py.File:
                model.synchronizeH5pyObject(obj.h5py_object)

    def _filterScans(self, scans: set[ScanEntry]) -> set[ScanEntry]:
        scanTitlePatterns = self._selectionFilterGroupBox.getScanTitlePatterns()
        if not scanTitlePatterns:
            return scans.copy()

        filteredScans = set()
        for scan in scans:
            with silx.io.open(scan.filename) as h5f:
                titleDataset = h5f.get(f"{scan.number}.1/title")
                if titleDataset is None:
                    continue
                scanTitle = titleDataset.asstr()[()]

            matchedPatterns = [
                pattern
                for pattern in scanTitlePatterns
                if fnmatch.fnmatch(scanTitle, f"{pattern}*")
            ]
            if matchedPatterns:
                filteredScans.add(scan)
        return filteredScans

    def getSelectedScans(self) -> tuple[ScanEntry, ...]:
        """Returns selected scans with selection filter applied"""
        selectedScans = set()
        for scan in self.__treeview.selectedH5Nodes():
            scanNumber = extractScanNumber(scan.physical_name)
            if scanNumber == -1:
                _logger.warning(
                    f"Skipping scan: Invalid scan number in {scan.physical_name}"
                )
                continue
            selectedScans.add(
                ScanEntry(filename=scan.physical_filename, number=scanNumber)
            )

        return tuple(sorted(self._filterScans(selectedScans)))

    def loadSettings(self) -> None:
        self._selectionFilterGroupBox.loadSettings()

    def saveSettings(self) -> None:
        self._selectionFilterGroupBox.saveSettings()
