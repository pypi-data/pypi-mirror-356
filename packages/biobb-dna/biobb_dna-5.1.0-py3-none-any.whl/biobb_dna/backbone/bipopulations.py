#!/usr/bin/env python3
"""Module containing the BIPopulations class and the command line interface."""

import argparse
from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd
from biobb_common.configuration import settings
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.tools.file_utils import launchlogger
from numpy import nan

from biobb_dna.utils.common import _from_string_to_list
from biobb_dna.utils.loader import read_series
from biobb_dna.utils.transform import inverse_complement


class BIPopulations(BiobbObject):
    """
    | biobb_dna BIPopulations
    | Calculate BI/BII populations from epsilon and zeta parameters.
    | Calculate BI/BII populations from epsilon and zeta parameters.

    Args:
        input_epsilC_path (str): Path to .ser file for helical parameter 'epsilC'. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/backbone/canal_output_epsilC.ser>`_. Accepted formats: ser (edam:format_2330).
        input_epsilW_path (str): Path to .ser file for helical parameter 'epsilW'. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/backbone/canal_output_epsilW.ser>`_. Accepted formats: ser (edam:format_2330).
        input_zetaC_path (str): Path to .ser file for helical parameter 'zetaC'. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/backbone/canal_output_zetaC.ser>`_. Accepted formats: ser (edam:format_2330).
        input_zetaW_path (str): Path to .ser file for helical parameter 'zetaW'. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/backbone/canal_output_zetaW.ser>`_. Accepted formats: ser (edam:format_2330).
        output_csv_path (str): Path to .csv file where output is saved. File type: output. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/reference/backbone/bipop_ref.csv>`_. Accepted formats: csv (edam:format_3752).
        output_jpg_path (str): Path to .jpg file where output is saved. File type: output. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/reference/backbone/bipop_ref.jpg>`_. Accepted formats: jpg (edam:format_3579).
        properties (dict):
            * **sequence** (*str*) - (None) Nucleic acid sequence corresponding to the input .ser file. Length of sequence is expected to be the same as the total number of columns in the .ser file, minus the index column (even if later on a subset of columns is selected with the *seqpos* option).
            * **seqpos** (*list*) - (None) list of sequence positions (columns indices starting by 0) to analyze.  If not specified it will analyse the complete sequence.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_dna.backbone.bipopulations import bipopulations

            prop = {
                'sequence': 'GCAT',
            }
            bipopulations(
                input_epsilC_path='/path/to/epsilC.ser',
                input_epsilW_path='/path/to/epsilW.ser',
                input_zetaC_path='/path/to/zetaC.ser',
                input_zetaW_path='/path/to/zetaW.ser',
                output_csv_path='/path/to/table/output.csv',
                output_jpg_path='/path/to/table/output.jpg',
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
        input_epsilC_path,
        input_epsilW_path,
        input_zetaC_path,
        input_zetaW_path,
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
            "in": {
                "input_epsilC_path": input_epsilC_path,
                "input_epsilW_path": input_epsilW_path,
                "input_zetaC_path": input_zetaC_path,
                "input_zetaW_path": input_zetaW_path,
            },
            "out": {
                "output_csv_path": output_csv_path,
                "output_jpg_path": output_jpg_path,
            },
        }

        self.properties = properties
        self.sequence = properties.get("sequence")
        # self.seqpos = properties.get("seqpos", None)
        self.seqpos = [
            int(elem) for elem in _from_string_to_list(properties.get("seqpos", None))
        ]
        print("seqpos::::::::")
        print(self.seqpos)
        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`BIPopulations <backbone.bipopulations.BIPopulations>` object."""

        # Setup Biobb
        if self.check_restart():
            return 0
        self.stage_files()

        # check sequence
        if self.sequence is None or len(self.sequence) < 2:
            raise ValueError("sequence is null or too short!")

        # check seqpos
        if self.seqpos:
            if (max(self.seqpos) > len(self.sequence) - 2) or (min(self.seqpos) < 1):
                raise ValueError(
                    f"seqpos values must be between 1 and {len(self.sequence) - 2}"
                )
            if not (isinstance(self.seqpos, list) and len(self.seqpos) > 1):
                raise ValueError("seqpos must be a list of at least two integers")
        else:
            self.seqpos = None  # type: ignore

        # read input files
        epsilC = read_series(
            self.stage_io_dict["in"]["input_epsilC_path"], usecols=self.seqpos
        )
        epsilW = read_series(
            self.stage_io_dict["in"]["input_epsilW_path"], usecols=self.seqpos
        )
        zetaC = read_series(
            self.stage_io_dict["in"]["input_zetaC_path"], usecols=self.seqpos
        )
        zetaW = read_series(
            self.stage_io_dict["in"]["input_zetaW_path"], usecols=self.seqpos
        )

        # calculate difference between epsil and zeta parameters
        xlabels = self.get_xlabels(self.sequence, inverse_complement(self.sequence))
        diff_epsil_zeta = self.get_angles_difference(epsilC, zetaC, epsilW, zetaW)

        # calculate BI population
        BI = (diff_epsil_zeta < 0).sum(axis=0) * 100 / len(diff_epsil_zeta)
        BII = 100 - BI

        # save table
        Bpopulations_df = pd.DataFrame(
            {"Nucleotide": xlabels, "BI population": BI, "BII population": BII}
        )
        Bpopulations_df.to_csv(
            self.stage_io_dict["out"]["output_csv_path"], index=False
        )

        # save plot
        fig, axs = plt.subplots(1, 1, dpi=300, tight_layout=True)
        axs.bar(range(len(xlabels)), BI, label="BI")
        axs.bar(range(len(xlabels)), BII, bottom=BI, label="BII")
        # empty bar to divide both sequences
        axs.bar([len(BI) // 2], [100], color="white", label=None)
        axs.legend()
        axs.set_xticks(range(len(xlabels)))
        axs.set_xticklabels(xlabels, rotation=90)
        axs.set_xlabel("Nucleotide Sequence")
        axs.set_ylabel("BI/BII Population (%)")
        axs.set_title("Nucleotide parameter: BI/BII Population")
        fig.savefig(self.stage_io_dict["out"]["output_jpg_path"], format="jpg")
        plt.close()

        # Copy files to host
        self.copy_to_host()

        # Remove temporary file(s)
        # self.tmp_files.extend([self.stage_io_dict.get("unique_dir", "")])
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return 0

    def get_xlabels(self, strand1, strand2):
        # get list of tetramers, except first and last two bases
        labelsW = list(strand1)
        labelsW[0] = f"{labelsW[0]}5'"
        labelsW[-1] = f"{labelsW[-1]}3'"
        labelsW = [f"{i}-{j}" for i, j in zip(labelsW, range(1, len(labelsW) + 1))]
        labelsC = list(strand2)[::-1]
        labelsC[0] = f"{labelsC[0]}5'"
        labelsC[-1] = f"{labelsC[-1]}3'"
        labelsC = [f"{i}-{j}" for i, j in zip(labelsC, range(len(labelsC), 0, -1))]

        if self.seqpos is not None:
            labelsC = [labelsC[i] for i in self.seqpos]
            labelsW = [labelsW[i] for i in self.seqpos]
        xlabels = labelsW + ["-"] + labelsC
        return xlabels

    def get_angles_difference(self, epsilC, zetaC, epsilW, zetaW):
        # concatenate zeta and epsil arrays
        separator_df = pd.DataFrame({"-": nan}, index=range(len(zetaW)))
        zeta = pd.concat([zetaW, separator_df, zetaC[zetaC.columns[::-1]]], axis=1)
        epsil = pd.concat([epsilW, separator_df, epsilC[epsilC.columns[::-1]]], axis=1)

        # difference between epsilon and zeta coordinates
        diff_epsil_zeta = epsil - zeta
        return diff_epsil_zeta


def bipopulations(
    input_epsilC_path: str,
    input_epsilW_path: str,
    input_zetaC_path: str,
    input_zetaW_path: str,
    output_csv_path: str,
    output_jpg_path: str,
    properties: Optional[dict] = None,
    **kwargs,
) -> int:
    """Create :class:`BIPopulations <dna.backbone.bipopulations.BIPopulations>` class and
    execute the: meth: `launch() <dna.backbone.bipopulations.BIPopulations.launch>` method."""

    return BIPopulations(
        input_epsilC_path=input_epsilC_path,
        input_epsilW_path=input_epsilW_path,
        input_zetaC_path=input_zetaC_path,
        input_zetaW_path=input_zetaW_path,
        output_csv_path=output_csv_path,
        output_jpg_path=output_jpg_path,
        properties=properties,
        **kwargs,
    ).launch()

    bipopulations.__doc__ = BIPopulations.__doc__


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(
        description="Calculate BI/BII populations.",
        formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999),
    )
    parser.add_argument("--config", required=False, help="Configuration file")

    required_args = parser.add_argument_group("required arguments")
    required_args.add_argument(
        "--input_epsilC_path",
        required=True,
        help="Helical parameter <epsilC> input ser file path. Accepted formats: ser.",
    )
    required_args.add_argument(
        "--input_epsilW_path",
        required=True,
        help="Helical parameter <epsilW> input ser file path. Accepted formats: ser.",
    )
    required_args.add_argument(
        "--input_zetaC_path",
        required=True,
        help="Helical parameter <zetaC> input ser file path. Accepted formats: ser.",
    )
    required_args.add_argument(
        "--input_zetaW_path",
        required=True,
        help="Helical parameter <zetaW> input ser file path. Accepted formats: ser.",
    )
    required_args.add_argument(
        "--output_csv_path",
        required=True,
        help="Path to output csv file. Accepted formats: csv.",
    )
    required_args.add_argument(
        "--output_jpg_path",
        required=True,
        help="Path to output jpg file. Accepted formats: jpg.",
    )

    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    bipopulations(
        input_epsilC_path=args.input_epsilC_path,
        input_epsilW_path=args.input_epsilW_path,
        input_zetaC_path=args.input_zetaC_path,
        input_zetaW_path=args.input_zetaW_path,
        output_csv_path=args.output_csv_path,
        output_jpg_path=args.output_jpg_path,
        properties=properties,
    )


if __name__ == "__main__":
    main()
