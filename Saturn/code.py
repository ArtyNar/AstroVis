from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np

# Load the .fits file
fits_file = "data/SAT_f322w2-f323n_i2d.fits"

with fits.open(fits_file) as hdul:
    # Display file info
    hdul.info()

    # Extract the image from file
    image_data = hdul[1].data  

    print("Capture date:", hdul[0].header.get('DATE', 'Unknown'))
    print("Target:", hdul[0].header.get('TARGNAME', 'Unknown'))
    print("Image Shape:", image_data.shape)

    # Replace NaNs with zeros if there are any
    image_data = np.nan_to_num(image_data)

    # Make a figure
    plt.figure(figsize=(10, 8))

    # Show the image
    plt.imshow(image_data, cmap='inferno', origin='lower')

    # This adjusts the colormap in a way that shows the important stuff
    # plt.imshow(image_data, cmap='inferno', origin='lower',
    #           vmin=np.nanpercentile(image_data, 1), vmax=np.nanpercentile(image_data, 99))

    plt.colorbar(label="Intensity")
    plt.title("JWST NIRCam Image")
    plt.savefig("results/output.png", dpi=600, bbox_inches='tight') # Note the DPI. Will determine the quality and processing time
    plt.show()

print("Done")