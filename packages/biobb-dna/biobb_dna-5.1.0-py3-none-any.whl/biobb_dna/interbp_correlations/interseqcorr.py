#!/usr/bin/env python3

"""Module containing the InterSequenceCorrelation class and the command line interface."""

import argparse
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
from biobb_common.configuration import settings
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.tools.file_utils import launchlogger

from biobb_dna.utils import constants
from biobb_dna.utils.common import _from_string_to_list
from biobb_dna.utils.loader import read_series


class InterSequenceCorrelation(BiobbObject):
    """
    | biobb_dna InterSequenceCorrelation
    | Calculate correlation between all base pairs of a single sequence and for a single helical parameter.
    | Calculate correlation between all base pairs of a single sequence and for a single helical parameter.

    Args:
        input_ser_path (str): Path to .ser file with data for single helical parameter. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/correlation/canal_output_roll.ser>`_. Accepted formats: ser (edam:format_2330).
        output_csv_path (str): Path to directory where output is saved. File type: output. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/reference/correlation/inter_seqcorr_roll.csv>`_. Accepted formats: csv (edam:format_3752).
        output_jpg_path (str): Path to .jpg file where output is saved. File type: output. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/reference/correlation/inter_seqcorr_roll.jpg>`_. Accepted formats: jpg (edam:format_3579).
        properties (dict):
            * **sequence** (*str*) - (None) Nucleic acid sequence for the input .ser file. Length of sequence is expected to be the same as the total number of columns in the .ser file, minus the index column (even if later on a subset of columns is selected with the *seqpos* option).
            * **helpar_name** (*str*) - (None) helical parameter name to add to plot title.
            * **seqpos** (*list*) - (None) list of sequence positions (columns indices starting by 0) to analyze.  If not specified it will analyse the complete sequence.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_dna.interbp_correlations.interseqcorr import interseqcorr

            prop = {
                "helpar_name": "helpar",
                "sequence": "CGTAATCG"
            }
            interseqcorr(
                input_ser_path='path/to/input/file.ser',
                output_csv_path='path/to/output/file.csv',
                output_jpg_path='path/to/output/plot.jpg',
                properties=prop)
    Info:
        * wrapped_software:
            * name: In house
            * license: Apache-2.0
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """

    def __init__(
        self,
        input_ser_path,
        output_csv_path,
        output_jpg_path,
        properties=None,
        **kwargs,
    ) -> None:
        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            "in": {"input_ser_path": input_ser_path},
            "out": {
                "output_csv_path": output_csv_path,
                "output_jpg_path": output_jpg_path,
            },
        }

        self.properties = properties
        self.sequence = properties.get("sequence", None)
        self.seqpos = [
            int(elem) for elem in _from_string_to_list(properties.get("seqpos", None))
        ]
        self.helpar_name = properties.get("helpar_name", None)

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`HelParCorrelation <interbp_correlations.interseqcorr.InterSequenceCorrelation>` object."""

        # Setup Biobb
        if self.check_restart():
            return 0
        self.stage_files()

        # check sequence
        if self.sequence is None or len(self.sequence) < 2:
            raise ValueError("sequence is null or too short!")

        # get helical parameter from filename if not specified
        if self.helpar_name is None:
            for hp in constants.helical_parameters:
                if (
                    hp.lower()
                    in Path(self.stage_io_dict["in"]["input_ser_path"]).name.lower()
                ):
                    self.helpar_name = hp
            if self.helpar_name is None:
                raise ValueError(
                    "Helical parameter name can't be inferred from file, "
                    "so it must be specified!"
                )
        else:
            if self.helpar_name not in constants.helical_parameters:
                raise ValueError(
                    "Helical parameter name is invalid! "
                    f"Options: {constants.helical_parameters}"
                )

        # get base length and unit from helical parameter name
        if self.helpar_name in constants.hp_angular:
            self.method = "pearson"
        else:
            self.method = self.circular  # type: ignore

        # check seqpos
        if self.seqpos:
            if not (isinstance(self.seqpos, list) and len(self.seqpos) > 1):
                raise ValueError("seqpos must be a list of at least two integers")
        else:
            self.seqpos = None  # type: ignore

        # read input .ser file
        ser_data = read_series(
            self.stage_io_dict["in"]["input_ser_path"], usecols=self.seqpos
        )
        if not self.seqpos:
            ser_data = ser_data[ser_data.columns[1:-1]]
            # discard first and last base(pairs) from strands
            sequence = self.sequence[1:]
            labels = [f"{i+1}_{sequence[i:i+2]}" for i in range(len(ser_data.columns))]
        else:
            labels = [f"{i+1}_{self.sequence[i:i+2]}" for i in self.seqpos]
        ser_data.columns = labels

        # make matrix
        corr_data = ser_data.corr(method=self.method)

        # save csv data
        corr_data.to_csv(self.stage_io_dict["out"]["output_csv_path"])

        # create heatmap
        fig, axs = plt.subplots(1, 1, dpi=300, tight_layout=True)
        axs.pcolor(corr_data)
        # Loop over data dimensions and create text annotations.
        for i in range(len(corr_data)):
            for j in range(len(corr_data)):
                axs.text(
                    j + 0.5,
                    i + 0.5,
                    f"{corr_data[corr_data.columns[j]].iloc[i]:.2f}",
                    ha="center",
                    va="center",
                    color="w",
                )
        axs.set_xticks([i + 0.5 for i in range(len(corr_data))])
        axs.set_xticklabels(labels, rotation=90)
        axs.set_yticks([i + 0.5 for i in range(len(corr_data))])
        axs.set_yticklabels(labels)
        axs.set_title(
            "Base Pair Correlation " f"for Helical Parameter '{self.helpar_name}'"
        )
        fig.tight_layout()
        fig.savefig(self.stage_io_dict["out"]["output_jpg_path"], format="jpg")
        plt.close()

        # Copy files to host
        self.copy_to_host()

        # Remove temporary file(s)
        # self.tmp_files.extend([self.stage_io_dict.get("unique_dir", "")])
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return 0

    @staticmethod
    def circular(x1, x2):
        x1 = x1 * np.pi / 180
        x2 = x2 * np.pi / 180
        diff_1 = np.sin(x1 - x1.mean())
        diff_2 = np.sin(x2 - x2.mean())
        num = (diff_1 * diff_2).sum()
        den = np.sqrt((diff_1**2).sum() * (diff_2**2).sum())
        return num / den


def interseqcorr(
    input_ser_path: str,
    output_csv_path: str,
    output_jpg_path: str,
    properties: Optional[dict] = None,
    **kwargs,
) -> int:
    """Create :class:`HelParCorrelation <interbp_correlations.interseqcorr.InterSequenceCorrelation>` class and
    execute the :meth:`launch() <interbp_correlations.interseqcorr.InterSequenceCorrelation.launch>` method."""

    return InterSequenceCorrelation(
        input_ser_path=input_ser_path,
        output_csv_path=output_csv_path,
        output_jpg_path=output_jpg_path,
        properties=properties,
        **kwargs,
    ).launch()

    interseqcorr.__doc__ = InterSequenceCorrelation.__doc__


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(
        description="Load .ser file from Canal output and calculate correlation between base pairs of the corresponding sequence.",
        formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999),
    )
    parser.add_argument("--config", required=False, help="Configuration file")

    required_args = parser.add_argument_group("required arguments")
    required_args.add_argument(
        "--input_ser_path",
        required=True,
        help="Path to ser file with inputs. Accepted formats: ser.",
    )
    required_args.add_argument(
        "--output_csv_path",
        required=True,
        help="Path to output file. Accepted formats: csv.",
    )
    required_args.add_argument(
        "--output_jpg_path",
        required=True,
        help="Path to output plot. Accepted formats: jpg.",
    )

    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    interseqcorr(
        input_ser_path=args.input_ser_path,
        output_csv_path=args.output_csv_path,
        output_jpg_path=args.output_jpg_path,
        properties=properties,
    )


if __name__ == "__main__":
    main()
