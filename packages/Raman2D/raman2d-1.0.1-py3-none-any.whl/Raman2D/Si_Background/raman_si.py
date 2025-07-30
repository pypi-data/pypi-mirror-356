"""
Module for Raman Spectrum Correction and Processing.
"""

import os
import pandas as pd
from scipy import signal
from Raman2D.Si_Background.Si_background import REFERENCE_SPECTRUM


def load_spectrum(file_path):
    """
    Load a spectrum file.

    Parameters:
        file_path (str): Path to the spectrum file.

    Returns:
        pd.DataFrame: DataFrame containing the spectrum data.
    """
    return pd.read_csv(file_path, delimiter=';', header=None)


class RamanSpectrumProcessor:
    """
    A class to handle Raman spectrum correction and processing.
    """

    def __init__(self, dirname):
        """
        Initialize the RamanSpectrumProcessor class.

        Parameters:
            dirname (str): Path to the directory containing spectrum files.
        """
        self.dirname = dirname
        self.reference_spectrum = pd.DataFrame(
            REFERENCE_SPECTRUM, columns=[0, 1]
        )  # Load reference spectrum

    def calculate_correction_factor(self, spectrum):
        """
        Calculate the correction factor based
         on the spectrum and reference spectrum.

        Parameters:
            spectrum (pd.DataFrame): DataFrame of the spectrum.

        Returns:
            float: Correction factor.
        """
        max_y_spectrum = spectrum[1].max()
        max_y_ref = self.reference_spectrum[1].max()

        return max_y_spectrum / max_y_ref

    def correct_spectrum(self, spectrum, correction_factor):
        """
        Correct the spectrum based on the reference
         spectrum and correction factor.

        Parameters:
            spectrum (pd.DataFrame): DataFrame of the spectrum to correct.
            correction_factor (float): Correction factor.

        Returns:
            pd.DataFrame: DataFrame containing the corrected spectrum.
        """
        # Apply correction only up to a specific range (470 cm-1)
        cor_spectrum = spectrum[1].copy()

        mask = spectrum[0] <= 470
        cor_spectrum[mask] = spectrum[1][mask] - \
                             correction_factor * \
                             self.reference_spectrum[1][mask]


        # Ensure continuity at 470 cm⁻¹
        below_470 = cor_spectrum[spectrum[0] < 470].iloc[-1]  # Last point below 470
        above_470 = cor_spectrum[spectrum[0] > 470].iloc[0]  # First point above 470

        print(below_470,above_470)

        ratio = below_470 / above_470

        mask_cor=spectrum[0] > 470

        print(cor_spectrum[mask_cor])

        cor_spectrum[mask_cor] = cor_spectrum[mask_cor] * ratio

        print(cor_spectrum[mask_cor])


        # Smooth the spectrum for x > 700
        mask_smooth = spectrum[0] > 570
        cor_spectrum[mask_smooth] = signal.savgol_filter(cor_spectrum[mask_smooth],
                                                  window_length=40,
                                                  polyorder=3)

        return pd.DataFrame({0: spectrum[0], 'Corrected_Y': cor_spectrum})



    def process_spectra(self, wafers=None):
        """
        Process all spectra in the directory and apply corrections.

        Parameters:
            wafers (list): A list of wafer names to process.
        """
        if wafers is None:
            wafers = []  # Default to an empty list if no wafers are provided

        wafers_str = [str(w).lower() for w in
                      wafers]  # Convert wafer names to lowercase

        for dirpath, _, filenames in os.walk(self.dirname):
            subdir_name = os.path.basename(dirpath).strip().lower()

            # Skip directories not in the wafer list
            if subdir_name not in wafers_str:
                continue

            for filename in filenames:
                if filename.endswith('.txt') and not filename.startswith(
                        'corrected') and not filename.startswith("cor"):
                    file_path = os.path.join(dirpath, filename)
                    spectrum = load_spectrum(file_path)
                    print(f"Processing file: {file_path}")
                    correction_factor = self.calculate_correction_factor(
                        spectrum)
                    corrected_spectrum = self.correct_spectrum(
                        spectrum, correction_factor)

                    # Save the corrected spectrum to a file
                    output_file = os.path.join(dirpath, f"{filename}")
                    corrected_spectrum.to_csv(output_file, sep=';', index=False,
                                              header=False)
                    print(f"Corrected spectrum saved: {output_file}")

    def process_spectra_sample(self):
        """
        Process all spectra in the directory and apply corrections.
        """
        for dirpath, _, filenames in os.walk(self.dirname):
            for filename in filenames:
                if filename.endswith('.txt') and not filename.startswith(
                        'corrected'):
                    file_path = os.path.join(dirpath, filename)
                    spectrum = load_spectrum(file_path)
                    print(f"Processing file: {file_path}")
                    correction_factor = self.calculate_correction_factor(
                        spectrum)
                    corrected_spectrum = self.correct_spectrum(
                        spectrum, correction_factor)

                    # Save the corrected spectrum to a file
                    output_file = os.path.join(dirpath, f"{filename}")
                    corrected_spectrum.to_csv(output_file, sep=';', index=False,
                                              header=False)
                    print(f"Corrected spectrum saved: {output_file}")


# Example usage
if __name__ == "__main__":
    # Initialize with the parent directory path
    PARENT = r'C:\Users\TM273821\Desktop\Calibration\CALIB'
    processor = RamanSpectrumProcessor(PARENT)

    # Specify the wafers to process
    WAFERS = [2,4,6,8,10,12,14,16,18,20]

    # Process the spectra without smoothing
    processor.process_spectra(wafers=WAFERS)
