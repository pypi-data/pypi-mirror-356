#!/usr/bin/env python3

"""Module containing the IntraHelParCorrelation class and the command line interface."""
import argparse
from typing import Optional

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import settings
from biobb_common.tools.file_utils import launchlogger
from biobb_dna.utils.loader import load_data


class IntraHelParCorrelation(BiobbObject):
    """
    | biobb_dna IntraHelParCorrelation
    | Calculate correlation between helical parameters for a single intra-base pair.
    | Calculate correlation between helical parameters for a single intra-base pair.

    Args:
        input_filename_shear (str): Path to .csv file with data for helical parameter 'shear'. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/correlation/series_shear_A.csv>`_. Accepted formats: csv (edam:format_3752).
        input_filename_stretch (str): Path to .csv file with data for helical parameter 'stretch'. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/correlation/series_stretch_A.csv>`_. Accepted formats: csv (edam:format_3752).
        input_filename_stagger (str): Path to .csv file with data for helical parameter 'stagger'. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/correlation/series_stagger_A.csv>`_. Accepted formats: csv (edam:format_3752).
        input_filename_buckle (str): Path to .csv file with data for helical parameter 'buckle'. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/correlation/series_buckle_A.csv>`_. Accepted formats: csv (edam:format_3752).
        input_filename_propel (str): Path to .csv file with data for helical parameter 'propeller'. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/correlation/series_propel_A.csv>`_. Accepted formats: csv (edam:format_3752).
        input_filename_opening (str): Path to .csv file with data for helical parameter 'opening'. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/correlation/series_opening_A.csv>`_. Accepted formats: csv (edam:format_3752).
        output_csv_path (str): Path to directory where output is saved. File type: output. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/reference/correlation/intra_hpcorr_ref.csv>`_. Accepted formats: csv (edam:format_3752).
        output_jpg_path (str): Path to .jpg file where output is saved. File type: output. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/reference/correlation/intra_hpcorr_ref.jpg>`_. Accepted formats: jpg (edam:format_3579).
        properties (dict):
            * **base** (*str*) - (None) Name of base analyzed.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_dna.intrabp_correlations.intrahpcorr import intrahpcorr

            prop = {
                'base': 'A',
            }
            intrahpcorr(
                input_filename_shear='path/to/shear.csv',
                input_filename_stretch='path/to/stretch.csv',
                input_filename_stagger='path/to/stagger.csv',
                input_filename_buckle='path/to/buckle.csv',
                input_filename_propel='path/to/propel.csv',
                input_filename_opening='path/to/opening.csv',
                output_csv_path='path/to/output/file.csv',
                output_jpg_path='path/to/output/file.jpg',
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
            self, input_filename_shear, input_filename_stretch,
            input_filename_stagger, input_filename_buckle,
            input_filename_propel, input_filename_opening,
            output_csv_path, output_jpg_path,
            properties=None, **kwargs) -> None:
        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            'in': {
                'input_filename_shear': input_filename_shear,
                'input_filename_stretch': input_filename_stretch,
                'input_filename_stagger': input_filename_stagger,
                'input_filename_buckle': input_filename_buckle,
                'input_filename_propel': input_filename_propel,
                'input_filename_opening': input_filename_opening
            },
            'out': {
                'output_csv_path': output_csv_path,
                'output_jpg_path': output_jpg_path
            }
        }

        self.properties = properties
        self.base = properties.get("base", None)

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`IntraHelParCorrelation <intrabp_correlations.intrahpcorr.IntraHelParCorrelation>` object."""

        # Setup Biobb
        if self.check_restart():
            return 0
        self.stage_files()

        # read input
        shear = load_data(self.stage_io_dict["in"]["input_filename_shear"])
        stretch = load_data(self.stage_io_dict["in"]["input_filename_stretch"])
        stagger = load_data(self.stage_io_dict["in"]["input_filename_stagger"])
        buckle = load_data(self.stage_io_dict["in"]["input_filename_buckle"])
        propel = load_data(self.stage_io_dict["in"]["input_filename_propel"])
        opening = load_data(self.stage_io_dict["in"]["input_filename_opening"])

        # get base
        if self.base is None:
            self.base = shear.columns[0]

        # make matrix
        # coordinates = ["shear", "stretch", "stagger", "buckle", "propel", "opening"]
        coordinates = [
            "shear", "stretch", "stagger", "buckle", "propel", "opening"]
        corr_matrix = pd.DataFrame(
            np.eye(6, 6), index=coordinates, columns=coordinates)

        # shear
        # corr_matrix["shear"]["stretch"] = shear.corrwith(stretch, method="pearson")
        corr_matrix.loc["stretch", "shear"] = shear.corrwith(stretch, method="pearson").values[0]
        # corr_matrix["shear"]["stagger"] = shear.corrwith(stagger, method="pearson")
        corr_matrix.loc["stagger", "shear"] = shear.corrwith(stagger, method="pearson").values[0]
        # corr_matrix["shear"]["buckle"] = shear.corrwith(buckle, method=self.circlineal)
        corr_matrix.loc["buckle", "shear"] = shear.corrwith(buckle, method=self.circlineal).values[0]  # type: ignore
        # corr_matrix["shear"]["propel"] = shear.corrwith(propel, method=self.circlineal)
        corr_matrix.loc["propel", "shear"] = shear.corrwith(propel, method=self.circlineal).values[0]  # type: ignore
        # corr_matrix["shear"]["opening"] = shear.corrwith(opening, method=self.circlineal)
        corr_matrix.loc["opening", "shear"] = shear.corrwith(opening, method=self.circlineal).values[0]  # type: ignore
        # symmetric values
        # corr_matrix["stretch"]["shear"] = corr_matrix["shear"]["stretch"]
        corr_matrix.loc["shear", "stretch"] = corr_matrix.loc["stretch", "shear"]
        # corr_matrix["stagger"]["shear"] = corr_matrix["shear"]["stagger"]
        corr_matrix.loc["shear", "stagger"] = corr_matrix.loc["stagger", "shear"]
        # corr_matrix["buckle"]["shear"] = corr_matrix["shear"]["buckle"]
        corr_matrix.loc["shear", "buckle"] = corr_matrix.loc["buckle", "shear"]
        # corr_matrix["propel"]["shear"] = corr_matrix["shear"]["propel"]
        corr_matrix.loc["shear", "propel"] = corr_matrix.loc["propel", "shear"]
        # corr_matrix["opening"]["shear"] = corr_matrix["shear"]["opening"]
        corr_matrix.loc["shear", "opening"] = corr_matrix.loc["opening", "shear"]

        # stretch
        # corr_matrix["stretch"]["stagger"] = stretch.corrwith(stagger, method="pearson")
        corr_matrix.loc["stagger", "stretch"] = stretch.corrwith(stagger, method="pearson").values[0]
        # corr_matrix["stretch"]["buckle"] = stretch.corrwith(buckle, method=self.circlineal)
        corr_matrix.loc["buckle", "stretch"] = stretch.corrwith(buckle, method=self.circlineal).values[0]  # type: ignore
        # corr_matrix["stretch"]["propel"] = stretch.corrwith(propel, method=self.circlineal)
        corr_matrix.loc["propel", "stretch"] = stretch.corrwith(propel, method=self.circlineal).values[0]  # type: ignore
        # corr_matrix["stretch"]["opening"] = stretch.corrwith(opening, method=self.circlineal)
        corr_matrix.loc["opening", "stretch"] = stretch.corrwith(opening, method=self.circlineal).values[0]  # type: ignore
        # symmetric values
        # corr_matrix["stagger"]["stretch"] = corr_matrix["stretch"]["stagger"]
        corr_matrix.loc["stretch", "stagger"] = corr_matrix.loc["stagger", "stretch"]
        # corr_matrix["buckle"]["stretch"] = corr_matrix["stretch"]["buckle"]
        corr_matrix.loc["stretch", "buckle"] = corr_matrix.loc["buckle", "stretch"]
        # corr_matrix["propel"]["stretch"] = corr_matrix["stretch"]["propel"]
        corr_matrix.loc["stretch", "propel"] = corr_matrix.loc["propel", "stretch"]
        # corr_matrix["opening"]["stretch"] = corr_matrix["stretch"]["opening"]
        corr_matrix.loc["stretch", "opening"] = corr_matrix.loc["opening", "stretch"]

        # stagger
        # corr_matrix["stagger"]["buckle"] = stagger.corrwith(buckle, method=self.circlineal)
        corr_matrix.loc["buckle", "stagger"] = stagger.corrwith(buckle, method=self.circlineal).values[0]  # type: ignore
        # corr_matrix["stagger"]["propel"] = stagger.corrwith(propel, method=self.circlineal)
        corr_matrix.loc["propel", "stagger"] = stagger.corrwith(propel, method=self.circlineal).values[0]  # type: ignore
        # corr_matrix["stagger"]["opening"] = stagger.corrwith(opening, method=self.circlineal)
        corr_matrix.loc["opening", "stagger"] = stagger.corrwith(opening, method=self.circlineal).values[0]  # type: ignore
        # symmetric values
        # corr_matrix["buckle"]["stagger"] = corr_matrix["stagger"]["buckle"]
        corr_matrix.loc["stagger", "buckle"] = corr_matrix.loc["buckle", "stagger"]
        # corr_matrix["propel"]["stagger"] = corr_matrix["stagger"]["propel"]
        corr_matrix.loc["stagger", "propel"] = corr_matrix.loc["propel", "stagger"]
        # corr_matrix["opening"]["stagger"] = corr_matrix["stagger"]["opening"]
        corr_matrix.loc["stagger", "opening"] = corr_matrix.loc["opening", "stagger"]

        # buckle
        # corr_matrix["buckle"]["propel"] = buckle.corrwith(propel, method=self.circular)
        corr_matrix.loc["propel", "buckle"] = buckle.corrwith(propel, method=self.circular).values[0]  # type: ignore
        # corr_matrix["buckle"]["opening"] = buckle.corrwith(opening, method=self.circular)
        corr_matrix.loc["opening", "buckle"] = buckle.corrwith(opening, method=self.circular).values[0]  # type: ignore
        # symmetric values
        # corr_matrix["propel"]["buckle"] = corr_matrix["buckle"]["propel"]
        corr_matrix.loc["buckle", "propel"] = corr_matrix.loc["propel", "buckle"]
        # corr_matrix["opening"]["buckle"] = corr_matrix["buckle"]["opening"]
        corr_matrix.loc["buckle", "opening"] = corr_matrix.loc["opening", "buckle"]

        # propel
        # corr_matrix["propel"]["opening"] = propel.corrwith(opening, method=self.circular)
        corr_matrix.loc["opening", "propel"] = propel.corrwith(opening, method=self.circular).values[0]  # type: ignore
        # symmetric values
        # corr_matrix["opening"]["propel"] = corr_matrix["propel"]["opening"]
        corr_matrix.loc["propel", "opening"] = corr_matrix.loc["opening", "propel"]

        # save csv data
        corr_matrix.to_csv(self.stage_io_dict["out"]["output_csv_path"])

        # create heatmap
        fig, axs = plt.subplots(1, 1, dpi=300, tight_layout=True)
        axs.pcolor(corr_matrix)
        # Loop over data dimensions and create text annotations.
        for i in range(len(corr_matrix)):
            for j in range(len(corr_matrix)):
                axs.text(
                    j+.5,
                    i+.5,
                    f"{corr_matrix[coordinates[j]].loc[coordinates[i]]:.2f}",
                    ha="center",
                    va="center",
                    color="w")
        axs.set_xticks([i + 0.5 for i in range(len(corr_matrix))])
        axs.set_xticklabels(corr_matrix.columns, rotation=90)
        axs.set_yticks([i+0.5 for i in range(len(corr_matrix))])
        axs.set_yticklabels(corr_matrix.index)
        axs.set_title(
            "Helical Parameter Correlation "
            f"for Base Pair Step \'{self.base}\'")
        fig.tight_layout()
        fig.savefig(
            self.stage_io_dict['out']['output_jpg_path'],
            format="jpg")
        plt.close()

        # Copy files to host
        self.copy_to_host()

        # Remove temporary file(s)
        # self.tmp_files.extend([
        #     self.stage_io_dict.get("unique_dir", "")
        # ])
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return 0

    def get_corr_method(self, corrtype1, corrtype2):
        if corrtype1 == "circular" and corrtype2 == "linear":
            method = self.circlineal
        if corrtype1 == "linear" and corrtype2 == "circular":
            method = self.circlineal
        elif corrtype1 == "circular" and corrtype2 == "circular":
            method = self.circular
        else:
            method = "pearson"
        return method

    @staticmethod
    def circular(x1, x2):
        x1 = x1 * np.pi / 180
        x2 = x2 * np.pi / 180
        diff_1 = np.sin(x1 - x1.mean())
        diff_2 = np.sin(x2 - x2.mean())
        num = (diff_1 * diff_2).sum()
        den = np.sqrt((diff_1 ** 2).sum() * (diff_2 ** 2).sum())
        return num / den

    @staticmethod
    def circlineal(x1, x2):
        x2 = x2 * np.pi / 180
        rc = np.corrcoef(x1, np.cos(x2))[1, 0]
        rs = np.corrcoef(x1, np.sin(x2))[1, 0]
        rcs = np.corrcoef(np.sin(x2), np.cos(x2))[1, 0]
        num = (rc ** 2) + (rs ** 2) - 2 * rc * rs * rcs
        den = 1 - (rcs ** 2)
        correlation = np.sqrt(num / den)
        if np.corrcoef(x1, x2)[1, 0] < 0:
            correlation *= -1
        return correlation


def intrahpcorr(
        input_filename_shear: str, input_filename_stretch: str,
        input_filename_stagger: str, input_filename_buckle: str,
        input_filename_propel: str, input_filename_opening: str,
        output_csv_path: str, output_jpg_path: str,
        properties: Optional[dict] = None, **kwargs) -> int:
    """Create :class:`IntraHelParCorrelation <intrabp_correlations.intrahpcorr.IntraHelParCorrelation>` class and
    execute the :meth:`launch() <intrabp_correlations.intrahpcorr.IntraHelParCorrelation.launch>` method."""

    return IntraHelParCorrelation(
        input_filename_shear=input_filename_shear,
        input_filename_stretch=input_filename_stretch,
        input_filename_stagger=input_filename_stagger,
        input_filename_buckle=input_filename_buckle,
        input_filename_propel=input_filename_propel,
        input_filename_opening=input_filename_opening,
        output_csv_path=output_csv_path,
        output_jpg_path=output_jpg_path,
        properties=properties, **kwargs).launch()

    intrahpcorr.__doc__ = IntraHelParCorrelation.__doc__


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description='Load helical parameter file and save base data individually.',
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_filename_shear', required=True,
                               help='Path to csv file with inputs. Accepted formats: csv.')
    required_args.add_argument('--input_filename_stretch', required=True,
                               help='Path to csv file with inputs. Accepted formats: csv.')
    required_args.add_argument('--input_filename_stagger', required=True,
                               help='Path to csv file with inputs. Accepted formats: csv.')
    required_args.add_argument('--input_filename_buckle', required=True,
                               help='Path to csv file with inputs. Accepted formats: csv.')
    required_args.add_argument('--input_filename_propel', required=True,
                               help='Path to csv file with inputs. Accepted formats: csv.')
    required_args.add_argument('--input_filename_opening', required=True,
                               help='Path to csv file with inputs. Accepted formats: csv.')
    required_args.add_argument('--output_csv_path', required=True,
                               help='Path to output file. Accepted formats: csv.')
    required_args.add_argument('--output_jpg_path', required=True,
                               help='Path to output file. Accepted formats: csv.')

    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    intrahpcorr(
        input_filename_shear=args.input_filename_shear,
        input_filename_stretch=args.input_filename_stretch,
        input_filename_stagger=args.input_filename_stagger,
        input_filename_buckle=args.input_filename_buckle,
        input_filename_propel=args.input_filename_propel,
        input_filename_opening=args.input_filename_opening,
        output_csv_path=args.output_csv_path,
        output_jpg_path=args.output_jpg_path,
        properties=properties)


if __name__ == '__main__':
    main()
