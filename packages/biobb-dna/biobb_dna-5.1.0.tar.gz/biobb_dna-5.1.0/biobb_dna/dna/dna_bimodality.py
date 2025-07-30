#!/usr/bin/env python3

"""Module containing the HelParBimodality class and the command line interface."""
import os
import zipfile
import argparse
from typing import Optional
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture  # type: ignore
from biobb_dna.utils import constants
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import settings
from biobb_common.tools.file_utils import launchlogger
from biobb_dna.utils.loader import load_data


class HelParBimodality(BiobbObject):
    """
    | biobb_dna HelParBimodality
    | Determine binormality/bimodality from a helical parameter series dataset.
    | Determine binormality/bimodality from a helical parameter series dataset.

    Args:
        input_csv_file (str): Path to .csv file with helical parameter series. If `input_zip_file` is passed, this should be just the filename of the .csv file inside .zip.  File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/dna/series_shift_AT.csv>`_. Accepted formats: csv (edam:format_3752).
        input_zip_file (str) (Optional): .zip file containing the `input_csv_file` .csv file. File type: input. Accepted formats: zip (edam:format_3987).
        output_csv_path (str): Path to .csv file where output is saved. File type: output. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/reference/dna/AT_shift_bimod.csv>`_. Accepted formats: csv (edam:format_3752).
        output_jpg_path (str): Path to .jpg file where output is saved. File type: output. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/reference/dna/AT_shift_bimod.jpg>`_. Accepted formats: jpg (edam:format_3579).
        properties (dict):
            * **helpar_name** (*str*) - (Optional) helical parameter name.
            * **confidence_level** (*float*) - (5.0) Confidence level for Byes Factor test (in percentage).
            * **max_iter** (*int*) - (400) Number of maximum iterations for EM algorithm.
            * **tol** (*float*) - (1e-5) Tolerance value for EM algorithm.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.1

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_dna.dna.dna_bimodality import dna_bimodality

            prop = {
                'max_iter': 500,
            }
            dna_bimodality(
                input_csv_file='filename.csv',
                input_zip_file='/path/to/input.zip',
                output_csv_path='/path/to/output.csv',
                output_jpg_path='/path/to/output.jpg',
                properties=prop)
    Info:
        * wrapped_software:
            * name: In house
            * license: Apache-2.0
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """

    def __init__(self, input_csv_file, output_csv_path,
                 output_jpg_path, input_zip_file=None,
                 properties=None, **kwargs) -> None:
        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            'in': {
                'input_csv_file': input_csv_file,
                'input_zip_file': input_zip_file
            },
            'out': {
                'output_csv_path': output_csv_path,
                'output_jpg_path': output_jpg_path
            }
        }

        # Properties specific for BB
        self.confidence_level = properties.get(
            "confidence_level", 5.0)
        self.max_iter = properties.get(
            "max_iter", 400)
        self.tol = properties.get(
            "tol", 1e-5)
        self.helpar_name = properties.get("helpar_name", None)
        self.properties = properties

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`HelParBimodality <dna.dna_bimodality.HelParBimodality>` object."""

        # Setup Biobb
        if self.check_restart():
            return 0
        self.stage_files()

        # get helical parameter from filename if not specified
        if self.helpar_name is None:
            for hp in constants.helical_parameters:
                if self.stage_io_dict.get("in", {}).get("input_zip_file") is not None:
                    condition_2 = (
                        hp.lower() in Path(self.stage_io_dict['in']['input_zip_file']).name.lower())
                else:
                    condition_2 = False
                condition_1 = hp.lower() in Path(
                    self.stage_io_dict['in']['input_csv_file']).name.lower()
                if (condition_1 or condition_2):
                    self.helpar_name = hp
            if self.helpar_name is None:
                raise ValueError(
                    "Helical parameter name can't be inferred from file, "
                    "so it must be specified!")
        else:
            if self.helpar_name not in constants.helical_parameters:
                raise ValueError(
                    "Helical parameter name is invalid! "
                    f"Options: {constants.helical_parameters}")

        # get  unit from helical parameter name
        if self.helpar_name in constants.hp_angular:
            self.hp_unit = "Degrees"
        else:
            self.hp_unit = "Angstroms"

        # resolve output
        output_csv_path = Path(
            self.stage_io_dict['out']['output_csv_path']).resolve()
        output_jpg_path = Path(
            self.stage_io_dict['out']['output_jpg_path']).resolve()

        # change directory to temporary folder
        original_directory = os.getcwd()
        os.chdir(self.stage_io_dict.get("unique_dir", ""))

        # read input
        if self.stage_io_dict.get("in", {}).get("input_zip_file") is not None:
            # if zipfile is specified, extract to temporary folder
            with zipfile.ZipFile(
                    self.stage_io_dict['in']['input_zip_file'],
                    'r') as zip_ref:
                zip_ref.extractall(self.stage_io_dict.get("unique_dir", ""))

        data = load_data(Path(self.stage_io_dict['in']['input_csv_file']).name)

        means, variances, bics, weights = self.fit_to_model(data)
        uninormal, binormal, insuf_ev = self.bayes_factor_criteria(
            bics[0], bics[1])

        if binormal:
            maxm = np.argmax(means[1])
            minm = np.argmin(means[1])
            mean1 = means[1][minm]
            var1 = variances[1][minm]
            w1 = weights[1][minm]
            mean2 = means[1][maxm]
            var2 = variances[1][maxm]
            w2 = weights[1][maxm]
            bimodal = self.helguero_theorem(mean1, mean2, var1, var2)
        else:
            mean1 = means[0][0]
            var1 = variances[0][0]
            w1 = weights[0][0]
            mean2, var2, w2 = np.nan, np.nan, 0
            bimodal = False
        info = dict(
            binormal=binormal,
            uninormal=uninormal,
            insuf_ev=insuf_ev,
            bimodal=bimodal,
            mean1=mean1,
            mean2=mean2,
            var1=var1,
            var2=var2,
            w1=w1,
            w2=w2)

        # save tables
        pd.DataFrame(info, index=data.columns).to_csv(output_csv_path)

        # make and save plot
        data_size = len(data)
        synth1 = np.random.normal(
            loc=info['mean1'],
            scale=np.sqrt(info['var1']),
            size=int(data_size * info['w1']))
        synth2 = np.random.normal(
            loc=info['mean2'],
            scale=np.sqrt(info['var2']),
            size=int(data_size * info['w2']))

        plt.figure()
        alpha = 0.7
        bins = 100
        if binormal:
            label1 = "Low State"
        else:
            label1 = "Single State"
        out = plt.hist(
            synth1, bins=bins, alpha=alpha, density=True, label=label1)
        ylim = max(out[0])  # type: ignore
        plt.vlines(info['mean1'], 0, ylim, colors="r", linestyles="dashed")
        if binormal:
            out = plt.hist(
                synth2, bins=bins, alpha=alpha, density=True, label="high state")
            ylim = max(out[0])  # type: ignore
            plt.vlines(info['mean2'], 0, ylim, colors="r", linestyles="dashed")
        plt.legend()
        plt.ylabel("Density")
        plt.xlabel(f"{self.helpar_name.capitalize()} ({self.hp_unit})")
        plt.title(f"Distribution of {self.helpar_name} states")
        plt.savefig(output_jpg_path, format="jpg")
        plt.close()

        # change back to original directory
        os.chdir(original_directory)

        # Copy files to host
        self.copy_to_host()

        # Remove temporary file(s)
        # self.tmp_files.extend([
        #     self.stage_io_dict.get("unique_dir", "")
        # ])
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return 0

    def fit_to_model(self, data):
        """
        Fit data to Gaussian Mixture models.
        Return dictionary with distribution data.
        """
        means = []
        variances = []
        bics = []
        weights = []
        for n_components in (1, 2):
            gmm = GaussianMixture(
                n_components=n_components,
                max_iter=self.max_iter,
                tol=self.tol)
            gmm = gmm.fit(data)
            m = gmm.means_.flatten()  # type: ignore
            v = gmm.covariances_.flatten()  # type: ignore
            b = gmm.bic(data)
            w = gmm.weights_.flatten()  # type: ignore
            means.append(m)
            variances.append(v)
            bics.append(b)
            weights.append(w)
        return means, variances, bics, weights

    def bayes_factor_criteria(self, bic1, bic2):
        diff_bic = bic2 - bic1
        # probability of a two-component model
        p = 1 / (1 + np.exp(0.5*diff_bic))
        if p == np.nan:
            if bic1 == np.nan:
                p = 1
            elif bic2 == np.nan:
                p = 0

        uninormal = p < (self.confidence_level / 100)
        binormal = p > (1 - (self.confidence_level / 100))
        insuf_ev = True if (not uninormal and not binormal) else False
        return uninormal, binormal, insuf_ev

    def helguero_theorem(self, mean1, mean2, var1, var2):
        r = var1 / var2
        separation_factor = np.sqrt(
            -2 + 3*r + 3*r**2 - 2*r**3 + 2*(1 - r + r**2)**1.5
        ) / (
            np.sqrt(r)*(1+np.sqrt(r))
        )
        bimodal = abs(mean2-mean1) > separation_factor * \
            (np.sqrt(var1) + np.sqrt(var2))
        return bimodal


def dna_bimodality(
        input_csv_file, output_csv_path, output_jpg_path,
        input_zip_file: Optional[str] = None, properties: Optional[dict] = None, **kwargs) -> int:
    """Create :class:`HelParBimodality <dna.dna_bimodality.HelParBimodality>` class and
    execute the :meth:`launch() <dna.dna_bimodality.HelParBimodality.launch>` method."""

    return HelParBimodality(
        input_csv_file=input_csv_file,
        input_zip_file=input_zip_file,
        output_csv_path=output_csv_path,
        output_jpg_path=output_jpg_path,
        properties=properties, **kwargs).launch()

    dna_bimodality.__doc__ = HelParBimodality.__doc__


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description='Determine binormality/bimodality from a helical parameter dataset.',
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_csv_file', required=True,
                               help='Path to csv file with data. Accepted formats: csv.')
    parser.add_argument('--input_zip_file',
                        help='Path to zip file containing csv input files. Accepted formats: zip.')
    required_args.add_argument('--output_csv_path', required=True,
                               help='Filename and/or path of output csv file.')
    required_args.add_argument('--output_jpg_path', required=True,
                               help='Filename and/or path of output jpg file.')

    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    dna_bimodality(
        input_csv_file=args.input_csv_file,
        input_zip_file=args.input_zip_file,
        output_csv_path=args.output_csv_path,
        output_jpg_path=args.output_jpg_path,
        properties=properties)


if __name__ == '__main__':
    main()
