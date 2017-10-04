import os
import sys
from osgeo import gdal, osr
import numpy as np
from PIL import Image


def movement(im_1, im_2, out_dir=None, CMV=True, GIF=True): 
    """ Highlight scene movement between overlapping raster images by creating
    different visual outputs, including Color-Multiview and GIF animation

    Input images are assumed to be Planet 4-band (RGBA) GeoTiff images that have 
    overlapping geometric footprints and equal pixel size

    Args:
        im1 (str): Path to Planet 4-band GeoTiff image
        im2 (str): Path to Planet 4-band GeoTiff image
    """

    # Set outputs
    if not out_dir:
        out_dir = os.path.dirname(im_1) + os.path.sep
    basename =  os.path.splitext(os.path.basename(im_1))[0] + \
                '__' + \
                os.path.splitext(os.path.basename(im_2))[0]
    print(basename)

    # Open image datasets
    ds_1 = gdal.Open(im_1)
    ds_2 = gdal.Open(im_2)

    # Geotransform data
    gt_1 = ds_1.GetGeoTransform()   
    gt_2 = ds_2.GetGeoTransform()

    # Spatial reference data
    srs_1 = osr.SpatialReference()
    srs_1.ImportFromWkt(ds_1.GetProjectionRef())
    srs_2 = osr.SpatialReference()
    srs_2.ImportFromWkt(ds_1.GetProjectionRef())

    # Determine image intersect
    r1 = [gt_1[0], 
          gt_1[3], 
          gt_1[0] + (gt_1[1] * ds_1.RasterXSize), 
          gt_1[3] + (gt_1[5] * ds_1.RasterYSize)]
    r2 = [gt_2[0], 
          gt_2[3], 
          gt_2[0] + (gt_2[1] * ds_2.RasterXSize), 
          gt_2[3] + (gt_2[5] * ds_2.RasterYSize)]
    intersect = [max(r1[0], r2[0]), 
                    min(r1[1], r2[1]), 
                    min(r1[2], r2[2]), 
                    max(r1[3], r2[3])]

    # Read image 1 intersect region
    left1 = int(round((intersect[0] - r1[0]) / gt_1[1])) 
    top1 = int(round((intersect[1] - r1[1]) / gt_1[5]))
    col1 = int(round((intersect[2] - r1[0]) / gt_1[1])) - left1
    row1 = int(round((intersect[3] - r1[1]) / gt_1[5])) - top1
    array_1 = ds_1.ReadAsArray(left1,top1,col1,row1)

    # Read image 2 intersect region
    left2 = int(round((intersect[0]-r2[0]) / gt_2[1])) 
    top2 = int(round((intersect[1]-r2[1]) / gt_2[5]))
    col2 = int(round((intersect[2]-r2[0]) / gt_2[1])) - left2
    row2 = int(round((intersect[3]-r2[1]) / gt_2[5])) - top2
    array_2 = ds_2.ReadAsArray(left2,top2,col2,row2)

    # Mask data to overlapped pixels
    mask = ((array_1[3,:,:] == 255) * 
            (array_2[3,:,:] == 255)).astype('uint8')
    array_1 *= mask
    array_2 *= mask

    # intersect image dimensions
    shape = array_1.shape
    cols = shape[2]
    rows = shape[1]

    # New geotransform offsets
    rand_px = left1
    rand_py = top1
    originX = gt_1[0] + (rand_px * gt_1[1]) + (rand_py * gt_1[2])
    originY = gt_1[3] + (rand_px * gt_1[4]) + (rand_py * gt_1[5])

    # Save color multi-view image
    outname = out_dir + basename + '.tif' 
    driver = gdal.GetDriverByName('GTiff')
    outRaster = driver.Create(outname, cols, rows, 4, gdal.GDT_Byte)
    outRaster.SetGeoTransform((originX, gt_1[1], 0, originY, 0, gt_1[5]))
    outRaster.GetRasterBand(1).WriteArray(array_1[0,:,:])
    outRaster.GetRasterBand(2).WriteArray(array_2[0,:,:])
    outRaster.GetRasterBand(3).WriteArray(array_2[0,:,:])
    outRaster.GetRasterBand(4).WriteArray(mask * 255)
    outRaster.SetProjection(srs_1.ExportToWkt())
    outRaster.FlushCache()

    # Save gif image
    gif_1 = np.zeros((rows,cols,4), dtype='uint8')
    gif_2 = np.zeros((rows,cols,4), dtype='uint8')
    for i in range(3):
        gif_1[:,:,i] = array_1[i,:,:].astype('uint8')
        gif_2[:,:,i] = array_2[i,:,:].astype('uint8')
    gif_1[:,:,3] = mask * 255
    gif_2[:,:,3] = mask * 255

    im_1 = Image.fromarray(gif_1).convert('L')
    im_2 = Image.fromarray(gif_2).convert('L')

    outname = out_dir + basename + '.gif'
    im_1.save(outname, 'GIF', save_all=True, optimize=False, quality=100, 
              append_images=[im_2], loop=0, duration=500)


# Main function
if __name__ == "__main__":

    # Run movement function with command line inputs
    movement(sys.argv[1], sys.argv[2])


