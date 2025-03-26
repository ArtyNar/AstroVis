import vtk
from vtk.util import numpy_support
from astropy.io import fits
import numpy as np

FITS_FILE = "data/jw01247-o341_t637_nircam_f322w2-f323n_i2d.fits"

with fits.open(FITS_FILE) as hdul:
    image_data = np.nan_to_num(hdul[1].data)

    # Apparently ParaView does not like negative which fits files for some reason contain 
    shift = abs(image_data.min()) + 1e-6  # Small epsilon to avoid exact zero
    image_data = image_data + shift

    # Create a VTK image 
    vtk_image = vtk.vtkImageData()
    vtk_image.SetDimensions(image_data.shape[1], image_data.shape[0], 1)
    vtk_image.SetSpacing(1, 1, 1)
    vtk_image.SetOrigin(0, 0, 0)

    # Flatten the numpy array and convert to VTK array
    flat_data = image_data.flatten()
    vtk_array = numpy_support.numpy_to_vtk(flat_data)
    vtk_image.GetPointData().SetScalars(vtk_array)

    # Write the VTK file
    writer = vtk.vtkXMLImageDataWriter()
    writer.SetFileName("results/saturn_for_paraview.vti")
    writer.SetInputData(vtk_image)
    writer.Write()