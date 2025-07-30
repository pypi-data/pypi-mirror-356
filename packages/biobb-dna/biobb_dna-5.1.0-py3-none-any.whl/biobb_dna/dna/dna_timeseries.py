#!/usr/bin/env python3

"""Module containing the HelParTimeSeries class and the command line interface."""

import argparse
import re
import zipfile
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd
from biobb_common.configuration import settings
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger

from biobb_dna.utils import constants
from biobb_dna.utils.common import _from_string_to_list
from biobb_dna.utils.loader import read_series


class HelParTimeSeries(BiobbObject):
    """
    | biobb_dna HelParTimeSeries
    | Created time series and histogram plots for each base pair from a helical parameter series file.
    | The helical parameter series file is expected to be a table, with the first column being an index and the rest the helical parameter values for each base/basepair.

    Args:
        input_ser_path (str): Path to .ser file for helical parameter. File is expected to be a table, with the first column being an index and the rest the helical parameter values for each base/basepair. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/dna/canal_output_shift.ser>`_. Accepted formats: ser (edam:format_2330).
        output_zip_path (str): Path to output .zip files where data is saved. File type: output. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/reference/dna/timeseries_output.zip>`_. Accepted formats: zip (edam:format_3987).
        properties (dict):
            * **sequence** (*str*) - (None) Nucleic acid sequence corresponding to the input .ser file. Length of sequence is expected to be the same as the total number of columns in the .ser file, minus the index column (even if later on a subset of columns is selected with the *usecols* option).
            * **bins** (*int*) - (None) Bins for histogram. Parameter has same options as matplotlib.pyplot.hist.
            * **helpar_name** (*str*) - (None) Helical parameter name. It must match the name of the helical parameter in the .ser input file. Values: majd, majw, mind, minw, inclin, tip, xdisp, ydisp, shear, stretch, stagger, buckle, propel, opening, rise, roll, twist, shift, slide, tilt, alphaC, alphaW, betaC, betaW, gammaC, gammaW, deltaC, deltaW, epsilC, epsilW, zetaC, zetaW, chiC, chiW, phaseC, phaseW.
            * **stride** (*int*) - (1000) granularity of the number of snapshots for plotting time series.
            * **seqpos** (*list*) - (None) list of sequence positions (columns indices starting by 1) to analyze.  If not specified it will analyse the complete sequence.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_dna.dna.dna_timeseries import dna_timeseries

            prop = {
                'helpar_name': 'twist',
                'seqpos': [1,2,3,4,5],
                'sequence': 'GCAACGTGCTATGGAAGC',
            }
            dna_timeseries(
                input_ser_path='/path/to/twist.ser',
                output_zip_path='/path/to/output/file.zip'
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
        self, input_ser_path, output_zip_path, properties=None, **kwargs
    ) -> None:
        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            "in": {
                "input_ser_path": input_ser_path,
            },
            "out": {"output_zip_path": output_zip_path},
        }

        self.properties = properties
        self.sequence = properties.get("sequence", None)
        self.bins = properties.get("bins", "auto")
        self.stride = properties.get("stride", 10)
        self.seqpos = [
            int(elem) for elem in _from_string_to_list(properties.get("seqpos", None))
        ]
        self.helpar_name = properties.get("helpar_name", None)

        # get helical parameter from filename if not specified
        if self.helpar_name is None:
            for hp in constants.helical_parameters:
                if hp.lower() in Path(input_ser_path).name.lower():
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

        # get base length from helical parameter name
        if self.helpar_name.lower() in constants.hp_singlebases:
            self.baselen = 0
        else:
            self.baselen = 1
        # get unit from helical parameter name
        if self.helpar_name in constants.hp_angular:
            self.hp_unit = "Degrees"
        else:
            self.hp_unit = "Angstroms"

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`HelParTimeSeries <dna.dna_timeseries.HelParTimeSeries>` object."""

        # Setup Biobb
        if self.check_restart():
            return 0
        self.stage_files()

        # check sequence
        if self.sequence is None or len(self.sequence) < 2:
            raise ValueError("sequence is null or too short!")

        # calculate cols with 0 index
        if self.seqpos:
            cols = [i - 1 for i in self.seqpos]
        else:
            cols = list(range(len(self.sequence)))

        # sort cols in ascending order
        cols.sort()

        # check seqpos for base pairs
        if self.seqpos and self.helpar_name in constants.hp_basepairs:
            if (max(cols) > len(self.sequence) - 2) or (min(cols) < 0):
                raise ValueError(
                    f"seqpos values must be between 1 and {len(self.sequence) - 1}"
                )
            if not (isinstance(self.seqpos, list) and len(self.seqpos) > 1):
                raise ValueError("seqpos must be a list of at least two integers")
        # check seqpos for non base pairs
        elif self.seqpos and self.helpar_name not in constants.hp_basepairs:
            if (max(cols) > len(self.sequence) - 1) or (min(cols) < 0):
                raise ValueError(
                    f"seqpos values must be between 1 and {len(self.sequence)}"
                )
            if not (isinstance(self.seqpos, list) and len(self.seqpos) > 1):
                raise ValueError("seqpos must be a list of at least two integers")

        if self.helpar_name in constants.hp_basepairs:
            # remove first and last base pairs from cols if they match 0 and len(sequence)
            if min(cols) == 0:
                cols.pop(0)
            if max(cols) == len(self.sequence) - 1:
                cols.pop(-1)

            # discard first and last base(pairs) from sequence
            sequence = self.sequence[1:-1]
            # create indices list
            indices = cols.copy()
            # create subunits list from cols
            subunits = [f"{i+1}_{sequence[i-1:i+self.baselen]}" for i in cols]
            # clean subunits (leave only basepairs)
            pattern = re.compile(r"\d+_[A-Za-z]{2}")
            # get removed items
            removed_items = [s for s in subunits if not pattern.fullmatch(s)]
            # get indices of removed items (in integer format and starting from 0)
            removed_numbers = [
                int(match.group())
                for item in removed_items
                if (match := re.match(r"\d+", item))
            ]
            removed_numbers = list(map(int, removed_numbers))
            removed_numbers = [int(i) - 1 for i in removed_numbers]
            # remove non basepairs from subunits and indices
            subunits = [s for s in subunits if pattern.fullmatch(s)]
            indices = [i for i in indices if i not in removed_numbers]
        else:
            sequence = self.sequence
            # create indices list
            indices = cols.copy()
            # trick for getting the index column from the .ser file
            indices.insert(0, 0)
            # create subunits list from cols
            subunits = [f"{i+1}_{sequence[i:i+1+self.baselen]}" for i in cols]

        # read input .ser file
        ser_data = read_series(
            self.stage_io_dict["in"]["input_ser_path"], usecols=indices
        )

        # get columns for selected bases
        ser_data.columns = subunits

        # write output files for all selected bases (one per column)
        zf = zipfile.ZipFile(Path(self.stage_io_dict["out"]["output_zip_path"]), "w")
        for col in ser_data.columns:
            # unstack columns to prevent errors from repeated base pairs
            column_data = ser_data[[col]].unstack().dropna().reset_index(drop=True)
            column_data.name = col
            fu.log(f"Computing base number {col}...")

            # column series
            series_colfn = f"series_{self.helpar_name}_{col}"
            column_data.to_csv(
                Path(self.stage_io_dict.get("unique_dir", "")) / f"{series_colfn}.csv"
            )
            # save table
            zf.write(
                Path(self.stage_io_dict.get("unique_dir", "")) / f"{series_colfn}.csv",
                arcname=f"{series_colfn}.csv",
            )

            fig, axs = plt.subplots(1, 1, dpi=300, tight_layout=True)
            reduced_data = column_data.iloc[:: self.stride]
            axs.plot(reduced_data.index, reduced_data.to_numpy())
            axs.set_xlabel("Time (Snapshots)")
            axs.set_ylabel(f"{self.helpar_name.capitalize()} ({self.hp_unit})")
            axs.set_title(
                f"Helical Parameter vs Time: {self.helpar_name.capitalize()} "
                "(base pair "
                f"{'step' if self.baselen==1 else ''} {col})"
            )
            fig.savefig(
                Path(self.stage_io_dict.get("unique_dir", "")) / f"{series_colfn}.jpg",
                format="jpg",
            )
            # save plot
            zf.write(
                Path(self.stage_io_dict.get("unique_dir", "")) / f"{series_colfn}.jpg",
                arcname=f"{series_colfn}.jpg",
            )
            plt.close()

            # columns histogram
            hist_colfn = f"hist_{self.helpar_name}_{col}"
            fig, axs = plt.subplots(1, 1, dpi=300, tight_layout=True)
            ybins, x, _ = axs.hist(column_data, bins=self.bins)
            pd.DataFrame({self.helpar_name: x[:-1], "density": ybins}).to_csv(
                Path(self.stage_io_dict.get("unique_dir", "")) / f"{hist_colfn}.csv",
                index=False,
            )
            # save table
            zf.write(
                Path(self.stage_io_dict.get("unique_dir", "")) / f"{hist_colfn}.csv",
                arcname=f"{hist_colfn}.csv",
            )

            axs.set_ylabel("Density")
            axs.set_xlabel(f"{self.helpar_name.capitalize()} ({self.hp_unit})")
            fig.savefig(
                Path(self.stage_io_dict.get("unique_dir", "")) / f"{hist_colfn}.jpg",
                format="jpg",
            )
            # save plot
            zf.write(
                Path(self.stage_io_dict.get("unique_dir", "")) / f"{hist_colfn}.jpg",
                arcname=f"{hist_colfn}.jpg",
            )
            plt.close()
        zf.close()

        # Copy files to host
        self.copy_to_host()

        # Remove temporary file(s)
        # self.tmp_files.extend([self.stage_io_dict.get("unique_dir", "")])
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return 0


def dna_timeseries(
    input_ser_path: str,
    output_zip_path: str,
    properties: Optional[dict] = None,
    **kwargs,
) -> int:
    """Create :class:`HelParTimeSeries <dna.dna_timeseries.HelParTimeSeries>` class and
    execute the :meth:`launch() <dna.dna_timeseries.HelParTimeSeries.launch>` method."""

    return HelParTimeSeries(
        input_ser_path=input_ser_path,
        output_zip_path=output_zip_path,
        properties=properties,
        **kwargs,
    ).launch()

    dna_timeseries.__doc__ = HelParTimeSeries.__doc__


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(
        description="Created time series and histogram plots for each base pair from a helical parameter series file.",
        formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999),
    )
    parser.add_argument("--config", required=False, help="Configuration file")

    required_args = parser.add_argument_group("required arguments")
    required_args.add_argument(
        "--input_ser_path",
        required=True,
        help="Helical parameter input ser file path. Accepted formats: ser.",
    )
    required_args.add_argument(
        "--output_zip_path", required=True, help="Path to output directory."
    )

    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    dna_timeseries(
        input_ser_path=args.input_ser_path,
        output_zip_path=args.output_zip_path,
        properties=properties,
    )


if __name__ == "__main__":
    main()
