from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider
import matplotlib.colors as colors
from matplotlib.colors import LinearSegmentedColormap

# Change to load a different .fits file
FITS_FILE = "data/jw01247-o341_t637_nircam_f322w2-f323n_i2d.fits"

# Styling options
plt.rcParams.update({
        "text.color": "white",       # Titles and labels
        "axes.labelcolor": "white",  # Axis labels
        "xtick.color": "white",      # X-axis ticks
        "ytick.color": "white",      # Y-axis ticks
    })


def resize(image_data, factor):
    rows, cols = image_data.shape
    start_row = (rows - rows//factor) // 2
    end_row = start_row + rows//factor
    start_col = (cols - rows//factor) // 2
    end_col = start_col + rows//factor
    return image_data[start_row:end_row, start_col:end_col]

with fits.open(FITS_FILE) as hdul:
    # Extract the image from file
    image_data = hdul[1].data

    # Display file info
    #hdul.info()
    
    # Extract metadata
    capture_date  =  hdul[0].header.get('DATE', 'Unknown')
    target = hdul[0].header.get('TARGNAME', 'Unknown')
    instrument = "JWST NIRCam F323N"

    # Resize
    image_data = resize(image_data,1)

    # Replace NaNs with zeros if there are any
    image_data = np.nan_to_num(image_data)
    
    # Create a figure
    fig = plt.figure(figsize=(12, 8), facecolor='black')
    ax = plt.subplot()
    

    min_percentile = 28
    max_percentile = np.nanpercentile(image_data, 100)

    linthresh = 50
    linscale = 1

    #cmap = 'magma'
    cmap = LinearSegmentedColormap.from_list("saturn", 
            [(0, 0, 0), (0.5, 0.25, 0), (0.8, 0.6, 0.2), (1, 0.9, 0.6)])

    #im = plt.imshow(image_data, cmap=cmap, origin='lower', vmin=min_percentile, vmax=max_percentile)
    im = plt.imshow(image_data, norm=colors.SymLogNorm(linthresh=linthresh, linscale=linscale, vmin=min_percentile, vmax=max_percentile, base=1.001), cmap=cmap)
    
    # Add space for sliders
    plt.subplots_adjust(bottom=0.2)  

    # Slider Axes
    ax_vmin = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor='lightgoldenrodyellow')
    ax_vmax = plt.axes([0.2, 0.05, 0.65, 0.03], facecolor='lightgoldenrodyellow')

    # Create sliders
    slider_vmin = Slider(ax_vmin, 'vmin', np.nanmin(image_data), np.nanmax(image_data), valinit=min_percentile)
    slider_vmax = Slider(ax_vmax, 'vmax', np.nanmin(image_data), np.nanmax(image_data), valinit=max_percentile)

    # Update function
    def update(val):
        im.set_clim([slider_vmin.val, slider_vmax.val])
        fig.canvas.draw_idle()

    # Connect sliders to update function
    slider_vmin.on_changed(update)
    slider_vmax.on_changed(update)

    # Sets the colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label("Intensity", fontsize=12) 
    
    # Other plot settings
    plt.axis('off')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(f"Saturn\n{instrument}\n{capture_date}", 
                color='white', fontsize=14)
    plt.savefig("results/output.png", dpi=600, bbox_inches='tight') # Note the DPI. Will determine the quality and processing time
    plt.show()

