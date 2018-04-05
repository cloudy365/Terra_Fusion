
"""
Case: show all spectral channel images for each instrument
"""

from my_module import np, plt, Basemap, toimage
from my_module.plot import enhance_rgb
import my_module.data.basic_fusion as bf


bf_file = '/Users/yizhe/Data&Results/TERRA_BF_L1B_O55180_20100503123308_F000_V001.h5'
granule_ASTER = 'granule_05032010130341'
granule_MODIS = 'granule_2010123_1300'
block_MISR = 38
granule_MOPITT = 'granule_20100503'

flag_ASTER = False
flag_MODIS = False
flag_MISR = False
flag_MOPITT = False


# ASTER
if flag_ASTER:
    for iband in range(1, 16):
        rad, _, _ = bf.get_rad_latlon(bf_file, 'ASTER', granule_ASTER, iband)
        if len(rad) != 0:
            toimage(rad).save("/Users/yizhe/Desktop/Case2/ASTER/band_{}.png".format(iband))
        
        
# MODIS
if flag_MODIS:
    for iband in [13.5, 14.5]:
        rad, _, _ = bf.get_rad_latlon(bf_file, 'MODIS', granule_MODIS, iband)
        if len(rad) != 0:
            toimage(rad, cmin=rad.min(), cmax=rad.max()).save("/Users/yizhe/Desktop/Case2/MODIS/band_{}.png".format(iband))


# MOPITT
if flag_MOPITT:
    rad, lat, lon = bf.get_rad_latlon(bf_file, 'MOPITT', granule_MOPITT)
    for iband in range(1, 9):
        rad_avg = rad[:, :, :, iband-1].ravel()
        lat_flat = lat.ravel()
        lon_flat = lon.ravel()
        idx_valid = np.where(rad_avg > 0)[0]
        rad_valid = rad_avg[idx_valid]
        lat_valid = lat_flat[idx_valid]
        lon_valid = lon_flat[idx_valid]
        
        plt.figure(figsize=(15, 10))
        m = bf.Basemap(projection='ortho',lon_0=-40,lat_0=40,resolution='l')
        m.drawcoastlines(color='k', linewidth=0.9)
        m.drawmeridians(np.arange(-180.,181,15.))
        m.drawparallels(np.arange(90.,-81,-15.))
        m.bluemarble(alpha=0.5)
        im = m.scatter(lon_valid[:],lat_valid[:],c=rad_valid[:],latlon=True,marker='s',s=55, 
                        cmap='coolwarm', alpha=0.2)
        plt.colorbar(im, orientation='vertical')
        plt.savefig("/Users/yizhe/Desktop/Case2/MOPITT/band_{}.png".format(iband))


# MISR
if flag_MISR:
    for i, iangle in enumerate(['DF', 'CF', 'BF', 'AF', 'AN', 'AA', 'BA', 'CA', 'DA']):
        rad, _, _ = bf.get_rad_latlon(bf_file, 'MISR', block_MISR, 'Red', iangle)
        if len(rad) != 0:
            toimage(rad, cmin=rad.min(), cmax=rad.max()).save("/Users/yizhe/Desktop/Case2/MISR/{}_red_{}.png".format(i, iangle))