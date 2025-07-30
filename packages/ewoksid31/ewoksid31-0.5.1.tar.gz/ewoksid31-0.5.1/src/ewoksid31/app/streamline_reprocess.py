"""
Usage:

python streamline_autocalib.py -v -o output_folder \
    --calibrant LaB6_SRM660c --max_rings 35 \
    --calibration /data/visitor/in1176/id31/20241022/RAW_DATA/ESRF_HR_01/ESRF_HR_01_0003/ESRF_HR_01_0003.h5 \
    --flat-dir /data/visitor/in1176/id31/20241022/PROCESSED_DATA/extra_files/ \
    --pyfai-config /data/visitor/in1176/id31/20241022/PROCESSED_DATA/calibration/PDF.json

"""

import argparse
import logging
import os

import h5py
from ewoks import execute_graph
from ewoksutils.task_utils import task_inputs

try:
    from ewoksjob.client import submit
except ImportError:
    submit = None

from .utils import (
    FLATFIELD_DEFAULT_DIR,
    NEWFLAT_FILENAME,
    OLDFLAT_FILENAME,
    print_inputs,
)


def generate_inputs(
    workflow,
    output_dir,
    pyfai_config,
    integration_options,
    detector_name,
    energy,
    newflat,
    oldflat,
    bliss_scan_url,
    integrate_image_url,
    calibrant,
    calib_ring_detector_name,
    calibrate_image_url,
    max_rings,
):
    inputs = [
        {
            "task_identifier": "PyFaiConfig",
            "name": "filename",
            "value": pyfai_config,
        },
        {
            "task_identifier": "PyFaiConfig",
            "name": "integration_options",
            "value": integration_options,
        },
        {
            "task_identifier": "FlatFieldFromEnergy",
            "name": "newflat",
            "value": newflat,
        },
        {
            "task_identifier": "FlatFieldFromEnergy",
            "name": "oldflat",
            "value": oldflat,
        },
        {
            "task_identifier": "FlatFieldFromEnergy",
            "name": "energy",
            "value": energy,
        },
        {
            "task_identifier": "Integrate1D",
            "name": "image",
            "value": integrate_image_url,
        },
        {
            "task_identifier": "SaveNexusPattern1D",
            "name": "url",
            "value": os.path.join(output_dir, "result.h5"),
        },
        {
            "task_identifier": "SaveNexusPattern1D",
            "name": "bliss_scan_url",
            "value": bliss_scan_url,
        },
        {
            "task_identifier": "DiagnoseIntegrate1D",
            "name": "filename",
            "value": os.path.join(output_dir, "integrate.png"),
        },
    ]

    if calibrant:
        inputs += [
            {
                "task_identifier": "CalibrateSingle",
                "name": "image",
                "value": calibrate_image_url,
            },
            {
                "task_identifier": "CalibrateSingle",
                "name": "fixed",
                "value": ["energy"],
            },
            {
                "task_identifier": "CalibrateSingle",
                "name": "robust",
                "value": False,
            },
            {
                "task_identifier": "CalibrateSingle",
                "name": "ring_detector",
                "value": calib_ring_detector_name,
            },
            {
                "task_identifier": "CalibrateSingle",
                "name": "max_rings",
                "value": max_rings,
            },
            {
                "task_identifier": "DiagnoseCalibrateSingleResults",
                "name": "image",
                "value": calibrate_image_url,
            },
            {
                "task_identifier": "DiagnoseCalibrateSingleResults",
                "name": "filename",
                "value": os.path.join(output_dir, "ring_detection.png"),
            },
            {
                "task_identifier": "PyFaiConfig",
                "name": "calibrant",
                "value": calibrant,
            },
            {
                "task_identifier": "DiagnoseIntegrate1D",
                "name": "calibrant",
                "value": calibrant,
            },
            {
                "task_identifier": "DiagnoseIntegrate1D",
                "label": "diagnose_calibrate",
                "name": "filename",
                "value": os.path.join(output_dir, "calibrate.png"),
            },
        ]

    for unit in ("q", "2th", "q_no_sigmaclip"):
        inputs += task_inputs(
            task_identifier="SaveNexusPattern1D",
            label=f"save_{unit}_hdf5",
            inputs={
                "nxprocess_name": f"{detector_name}_integrate_{unit}",
                "nxmeasurement_name": f"{detector_name}_integrated_{unit}",
                "metadata": {
                    f"{detector_name}_integrate_{unit}": {
                        "configuration": {"workflow": workflow}
                    }
                },
            },
        )

    for unit in ("q", "2th"):
        inputs += [
            {
                "task_identifier": "SaveAsciiPattern1D",
                "label": f"save_{unit}_ascii",
                "name": "filename",
                "value": os.path.join(output_dir, f"{unit}_result.xye"),
            },
        ]

    return inputs


def create_argument_parser():
    parser = argparse.ArgumentParser(description="")

    parser.add_argument(
        "-o",
        "--output-dir",
        type=str,
        required=True,
        help="Folder where to store the results",
        metavar="FOLDER",
    )
    parser.add_argument(
        "--worker",
        action="store_true",
        help="Execute workflows on ewoks worker instead of current environment",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity",
    )

    calibration_group = parser.add_argument_group("Calibration")
    calibration_group.add_argument(
        "--calibrant",
        type=str,
        required=True,
        help="Name of the calibrant used for calibration image",
    )
    calibration_group.add_argument(
        "--calibration",
        type=str,
        required=True,
        dest="calibration_filename",
        help="Dataset file to use for auto-calibration",
        metavar="FILE",
    )
    calibration_group.add_argument(
        "--max_rings",
        type=int,
        required=False,
        nargs="+",
        help="Number of rings to use. Use multiple values to refine over an increasing number of rings",
        default=[35],
    )

    integration_group = parser.add_argument_group("Integration")
    integration_group.add_argument(
        "-c",
        "--pyfai-config",
        type=str,
        required=True,
        help="PyFAI config file (.json)",
        metavar="FILE",
    )
    integration_group.add_argument(
        "-i",
        "--input",
        type=str,
        required=False,
        help="Dataset file to process (HDF5 format)",
        default="",
        metavar="FILE",
    )
    integration_group.add_argument(
        "--flat-dir",
        type=str,
        required=False,
        help="Folder containing flat field files: flats.mat and old_flats.mat",
        default=FLATFIELD_DEFAULT_DIR,
        metavar="FOLDER",
    )

    return parser


def main():
    logging.basicConfig(level=logging.WARNING)

    parser = create_argument_parser()
    options = parser.parse_args()

    if options.verbose != 0:
        logging.getLogger().setLevel(
            logging.INFO if options.verbose == 1 else logging.DEBUG
        )

    workflow = "streamline_with_calib_with_flat.json"
    workflow_load_options = {"root_module": "ewoksid31.workflows"}

    integration_options = {"nbpt_rad": 3000}
    detector_name = "p3"
    calib_ring_detector_name = "PilatusCdTe2M"

    input_filename = options.input if options.input else options.calibration_filename
    bliss_scan_url = f"{input_filename}::/1.1"
    integrate_image_url = (
        f"silx://{input_filename}?path=/1.1/measurement/{detector_name}&slice=0"
    )

    calibrate_image_url = f"silx://{options.calibration_filename}?path=/1.1/measurement/{detector_name}&slice=0"

    # ewoksxrpd CalibrateSingle compatibilty: list not supported
    max_rings = (
        options.max_rings[0] if len(options.max_rings) == 1 else options.max_rings
    )

    with h5py.File(input_filename, "r") as h5f:
        energy = h5f["/1.1/instrument/positioners/energy"][()]

    inputs = generate_inputs(
        workflow,
        os.path.abspath(options.output_dir),
        options.pyfai_config,
        integration_options,
        detector_name,
        energy,
        os.path.join(options.flat_dir, NEWFLAT_FILENAME),
        os.path.join(options.flat_dir, OLDFLAT_FILENAME),
        bliss_scan_url,
        integrate_image_url,
        options.calibrant,
        calib_ring_detector_name,
        calibrate_image_url,
        max_rings,
    )
    print("Worflow inputs:")
    print_inputs(inputs)

    if os.path.exists(options.output_dir):
        raise RuntimeError(f"Output directory already exists: {options.output_dir}")

    os.makedirs(options.output_dir)

    print("Execute workflow...")
    convert_destination = os.path.join(options.output_dir, "workflow.json")
    if options.worker:
        if submit is None:
            raise RuntimeError("Cannot submit workflow to worker: Install ewoksjob")
        _ = submit(
            args=(workflow,),
            kwargs={
                "inputs": inputs,
                "convert_destination": convert_destination,
                "load_options": workflow_load_options,
            },
        )
    else:
        _ = execute_graph(
            workflow,
            inputs=inputs,
            convert_destination=convert_destination,
            load_options=workflow_load_options,
        )
    print("Done")


if __name__ == "__main__":
    import sys

    sys.exit(main())
