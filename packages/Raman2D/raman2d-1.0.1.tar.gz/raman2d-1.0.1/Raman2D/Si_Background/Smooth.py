"""
Module to smooth the reference spectrum
"""

import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt


def smooth_reference_below_470(input_filepath, output_filepath):
    """
    Function to adjust X values, then smooth the reference spectrum for X values below 470 cm⁻¹,
    except for the range 295 ≤ X ≤ 305, using a Savitzky-Golay filter.

    Parameters:
    input_filepath (str): Path to the input file containing the reference spectrum.
    output_filepath (str): Path to save the smoothed spectrum.
    """
    try:
        # Load the data
        data = pd.read_csv(input_filepath, header=None, sep=';',
                           names=["X", "Y"])

        # Remove the last row
        data = data.iloc[:-1]

        # Apply X correction
        si_pic = data.iloc[999:1050]  # Selecting the region
        max_row = si_pic.loc[si_pic.iloc[:, 1].idxmax()]  # Find the max peak
        xmax, ymax = max_row.iloc[0], max_row.iloc[
            1]  # Extract X and Y max values
        offset = xmax - 520.7  # Compute the offset
        data.iloc[:, 0] = data.iloc[:, 0] - offset  # Apply offset correction

        print("Data with corrected X values:\n", data.head())

        # Filter data where X < 470 but exclude the range 295 ≤ X ≤ 305
        mask = (data["X"] < 470) & ~((data["X"] >= 297) & (data["X"] <= 307))
        x_smooth = data["X"][mask]
        y_smooth = data["Y"][mask]

        y_smoothed = signal.savgol_filter(y_smooth, window_length=40,
                                          polyorder=3)

        # Replace smoothed values in the original data
        data.loc[mask, "Y"] = y_smoothed

        # Save the smoothed data
        data.to_csv(output_filepath, sep=";", index=False, header=False)

        # Plot the original and smoothed spectra
        plt.figure(figsize=(8, 5))
        plt.plot(data["X"], data["Y"], label="Smoothed Spectrum", color="red")
        plt.scatter(x_smooth, y_smooth,
                    label="Original (X < 470, excluding 295-305)", color="blue",
                    s=10, alpha=0.5)
        plt.xlabel("X (cm⁻¹)")
        plt.ylabel("Y (Intensity)")
        plt.legend()
        plt.title(
            "Savitzky-Golay Smoothing for X < 470 cm⁻¹ (Excluding 295-305)")
        plt.show()

        print(f"Smoothed spectrum has been saved to '{output_filepath}'.")

    except Exception as err:
        print(f"An error occurred: {err}")

smooth_reference_below_470(r"C:/Users/TM273821/Desktop/Raman/Ref_Si/0.0_0.0.txt",r"C:/Users/TM273821/Desktop/Raman/Ref_Si/0.0_0.0_smoothed.txt")
