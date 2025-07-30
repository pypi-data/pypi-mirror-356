"""
Usage:

    python scripts/reprocess_xrpd.py --proposal ma5876 \
        --samples 02_cell1 03_cell2 \
        --pyfai-config /data/visitor/ma5876/id31/20231117/PROCESSED_DATA/calibration_good/20231117_json_good_bottom_beam_q_MM.json \
        --run reprocess_q_folder

    python scripts/reprocess_xrpd.py --proposal ma5876 \
        --samples 02_cell1 03_cell2 \
        --pyfai-config /data/visitor/ma5876/id31/20231117/PROCESSED_DATA/calibration_good/20231117_json_good_bottom_beam_2th_MM.json \
        --run reprocess_2th_folder

"""

import json
import os
import sys
from glob import glob
import argparse
import traceback

import h5py
from ewoks import execute_graph
from ewoksjob.client import submit
from ewoksutils.task_utils import task_inputs


from .utils import FLATFIELD_DEFAULT_DIR, NEWFLAT_FILENAME, OLDFLAT_FILENAME


WORKFLOW = "integrate_with_saving_with_flat.json"
WORKFLOW_LOAD_OPTIONS = {"root_module": "ewoksid31.workflows"}

DETECTOR = "p3"
BEACON_HOST = "id31:25000"
ENERGY_POSITIONER = "energy"


def get_parameters(
    dataset_filename,
    scan_number,
    detector_name,
    pyfai_config,
    pyfai_method,
    energy,
    monitor_name=None,
    reference_counts=None,
    run="",
    save_as_ascii=False,
):
    if run:
        output_filename = dataset_filename.replace("RAW_DATA", f"PROCESSED_DATA/{run}")
        convert_destination = dataset_filename.replace(
            "RAW_DATA", f"PROCESSED_DATA/{run}"
        )
    else:
        output_filename = dataset_filename.replace("RAW_DATA", "PROCESSED_DATA")
        convert_destination = dataset_filename.replace("RAW_DATA", "PROCESSED_DATA")

    output_filename_template = output_filename.replace(
        ".h5", f"_{scan_number}_{detector_name}_%04d.xye"
    )

    convert_destination = convert_destination.replace(
        ".h5", f"_{scan_number}_{detector_name}.json"
    )

    inputs = [
        {
            "task_identifier": "FlatFieldFromEnergy",
            "name": "newflat",
            "value": os.path.join(FLATFIELD_DEFAULT_DIR, NEWFLAT_FILENAME),
        },
        {
            "task_identifier": "FlatFieldFromEnergy",
            "name": "oldflat",
            "value": os.path.join(FLATFIELD_DEFAULT_DIR, OLDFLAT_FILENAME),
        },
        {"task_identifier": "FlatFieldFromEnergy", "name": "energy", "value": energy},
        {"task_identifier": "PyFaiConfig", "name": "filename", "value": pyfai_config},
        {
            "task_identifier": "PyFaiConfig",
            "name": "integration_options",
            "value": {"method": pyfai_method},
        },
        {
            "task_identifier": "IntegrateBlissScan",
            "name": "filename",
            "value": dataset_filename,
        },
        {"task_identifier": "IntegrateBlissScan", "name": "scan", "value": scan_number},
        {
            "task_identifier": "IntegrateBlissScan",
            "name": "output_filename",
            "value": output_filename,
        },
        {
            "task_identifier": "IntegrateBlissScan",
            "name": "monitor_name",
            "value": monitor_name,
        },
        {
            "task_identifier": "IntegrateBlissScan",
            "name": "reference",
            "value": reference_counts,
        },
        {
            "task_identifier": "IntegrateBlissScan",
            "name": "maximum_persistent_workers",
            "value": 1,
        },
        {
            # Use a very long retry timeout to mitigate issues
            # with multiple workflows accessing the same files
            "task_identifier": "IntegrateBlissScan",
            "name": "retry_timeout",
            "value": 6 * 3600,  # 6h hours
        },
        {
            "task_identifier": "IntegrateBlissScan",
            "name": "detector_name",
            "value": detector_name,
        },
        {
            "task_identifier": "SaveNexusPatternsAsAscii",
            "name": "output_filename_template",
            "value": output_filename_template,
        },
        {
            "task_identifier": "SaveNexusPatternsAsAscii",
            "name": "enabled",
            "value": save_as_ascii,
        },
    ]

    inputs += task_inputs(
        task_identifier="SaveNexusPatternsAsId31TomoHdf5",
        inputs={
            "enabled": False,
            "scan_entry_url": "",
            "rot_name": "",
            "y_name": "",
            "output_filename": "",
        },
    )

    return {"inputs": inputs, "convert_destination": convert_destination}


def iter_scan_info(dataset_filename, detector_name, monitor_name=None):
    with h5py.File(dataset_filename, "r") as nxroot:
        for scan_name in nxroot:
            try:
                scan = nxroot[scan_name]
                if detector_name not in scan["measurement"]:
                    continue
                if monitor_name and monitor_name not in scan["measurement"]:
                    continue
                energy = scan[f"instrument/positioners/{ENERGY_POSITIONER}"][()]
            except Exception:
                print(f"Skip invalid scan {dataset_filename}::/{scan_name}")
                continue
            yield int(float(scan_name)), energy


def create_argument_parser():
    parser = argparse.ArgumentParser(
        description="",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--beamline", type=str.lower, default="id31", help="Beamline name"
    )

    parser.add_argument(
        "--proposal", type=str.lower, required=True, help="Proposal name"
    )

    parser.add_argument(
        "--monitor",
        type=str,
        default="scaled_mondio",
        required=False,
        help="Flux monitor name",
    )

    parser.add_argument(
        "--reference", type=float, default=1, required=False, help="Reference counts"
    )

    parser.add_argument(
        "--samples",
        type=str,
        required=False,
        nargs="+",
        help="Samples to reprocess",
    )

    parser.add_argument(
        "-c",
        "--pyfai-config",
        type=str,
        required=True,
        help="PyFAI config file (.json)",
        metavar="FILE",
    )

    parser.add_argument(
        "--pyfai-method",
        type=str,
        default="full_csr_ocl_gpu",
        required=False,
        help="PyFAI integrator method",
    )

    parser.add_argument(
        "--worker",
        action="store_true",
        help="Execute workflows on ewoks worker instead of current environment",
    )

    parser.add_argument(
        "--save-ascii",
        action="store_true",
        help="Export integrated patterns as text files",
    )

    parser.add_argument(
        "--run",
        type=str,
        default="test",
        required=False,
        help="Processed sub-directory name",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not run anything but print which datasets would be processed",
    )

    return parser


def main(argv=None) -> int:
    if argv is None:
        argv = sys.argv

    parser = create_argument_parser()
    args = parser.parse_args(argv[1:])

    session_pattern = os.path.join(
        os.sep, "data", "visitor", args.proposal, args.beamline, "*"
    )
    sessions = glob(os.path.join(session_pattern))

    if len(sessions) > 1:
        session = input(f"Select session {sessions}: ")
    elif sessions:
        session = sessions[0]
    else:
        print("Proposal has no sessions")
        return 1

    samples = args.samples
    if not samples:
        sample_pattern = os.path.join(session, "RAW_DATA", "*", "*.h5")
        samples = [
            os.path.basename(os.path.dirname(sample_filename))
            for sample_filename in glob(sample_pattern)
        ]

    if args.worker:
        os.environ["BEACON_HOST"] = BEACON_HOST

    failed = list()
    futures = list()
    for sample in samples:
        dataset_pattern = os.path.join(session, "RAW_DATA", sample, "*", "*.h5")
        for dataset_filename in glob(dataset_pattern):
            scans = list(
                iter_scan_info(dataset_filename, DETECTOR, monitor_name=args.monitor)
            )
            for scan_number, energy in scans:
                kwargs = get_parameters(
                    dataset_filename,
                    scan_number,
                    DETECTOR,
                    args.pyfai_config,
                    args.pyfai_method,
                    energy,
                    monitor_name=args.monitor,
                    reference_counts=args.reference,
                    run=args.run,
                    save_as_ascii=args.save_ascii,
                )
                kwargs["load_options"] = WORKFLOW_LOAD_OPTIONS
                if args.dry_run:
                    print(f"Would process {dataset_filename}::/{scan_number}.1 with:")
                    print(json.dumps(kwargs, indent=2, sort_keys=True))
                elif args.worker:
                    future = submit(args=(WORKFLOW,), kwargs=kwargs)
                    futures.append((future, dataset_filename, scan_number))
                    print(f"Submitted {dataset_filename}::/{scan_number}.1")
                else:
                    try:
                        print(f"Processing {dataset_filename}::/{scan_number}.1 ...")
                        execute_graph(WORKFLOW, **kwargs)
                    except Exception as e:
                        traceback.print_exc()
                        failed.append(f"{dataset_filename}::/{scan_number}.1 ({e})")

    for future, dataset_filename, scan_number in futures:
        try:
            future.get()
        except Exception as e:
            print(f"FAILED {dataset_filename}::/{scan_number}.1")
            traceback.print_exc()
            failed.append(f"{dataset_filename}::/{scan_number}.1 ({e})")
        else:
            print(f"COMPLETED {dataset_filename}::/{scan_number}.1")

    if failed:
        print("FAILED:")
        print("\n".join(failed))
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
