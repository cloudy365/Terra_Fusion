

"""
Case: show enhanced rgb images for each instrument
"""


from my_module import np, plt, Basemap, toimage
from my_module.plot import enhance_rgb
import my_module.data.basic_fusion as bf


bf_file = '/Users/yizhe/Data&Results/TERRA_BF_L1B_O55180_20100503123308_F000_V001.h5'
granule_ASTER = 'granule_05032010130341'
granule_MODIS = 'granule_2010123_1300'
block_MISR = [38]
granule_MOPITT = 'granule_20100503'
band_MOPITT = 5

flag_ASTER = True
flag_MODIS = True
flag_MISR = True
flag_MOPITT = True


# ASTER
if flag_ASTER:
    ASTER_rgb = bf.get_rgb(bf_file, 'ASTER', granule_ASTER)
    ASTER_enhanced_rgb = enhance_rgb(ASTER_rgb)
    
    toimage(ASTER_enhanced_rgb).save('/Users/yizhe/Desktop/ASTER_rgb.png')


# MODIS
if flag_MODIS:
    MODIS_rgb = bf.get_rgb(bf_file, 'MODIS', granule_MODIS)
    MODIS_enhanced_rgb = enhance_rgb(MODIS_rgb)
    
    toimage(MODIS_enhanced_rgb).save('/Users/yizhe/Desktop/MODIS_rgb.png')


# MISR
if flag_MISR:
    camera = 'AN'
    MISR_rgb = bf.get_rgb(bf_file, 'MISR', block_MISR, camera=camera)
    MISR_enhanced_rgb = enhance_rgb(MISR_rgb)
    
    # Accounting for the offset, handles successive two blocks.
    if MISR_rgb.shape[1] == 2048:
        offset = 64
        b1 = MISR_enhanced_rgb[:512]
        b2 = MISR_enhanced_rgb[512:]
    elif MISR_rgb.shape[1] == 512:
        offset = 16
        b1 = MISR_enhanced_rgb[:128]
        b2 = MISR_enhanced_rgb[128:]
    
    b3 = b1[:, :-1*offset, :]
    b4 = b2[:, offset:, :]
    b5 = np.vstack((b3, b4))
    
    toimage(b5).save('/Users/yizhe/Desktop/MISR_rgb_{}.png'.format(camera))


# MOPITT
if flag_MOPITT:
    rad, lat, lon = bf.get_rad_latlon(bf_file, 'MOPITT', granule_MOPITT)
    rad_avg = rad[:, :, :, band_MOPITT].ravel()
    lat_flat = lat.ravel()
    lon_flat = lon.ravel()
    idx_valid = np.where(rad_avg > 0)[0]
    rad_valid = rad_avg[idx_valid]
    lat_valid = lat_flat[idx_valid]
    lon_valid = lon_flat[idx_valid]
    
    plt.figure(figsize=(15, 10))
    # m = bf.Basemap(projection='cea', lon_0=0, llcrnrlat=0, urcrnrlat=85, llcrnrlon=-60, urcrnrlon=20)
    m = Basemap(projection='ortho',lon_0=-40,lat_0=40,resolution='l')
    m.drawcoastlines(color='k', linewidth=0.9)
    m.drawmeridians(np.arange(-180.,181,15.))#, labels=[False,True,True,False])
    m.drawparallels(np.arange(90.,-81,-15.))#, labels=[False,True,True,False])
    m.bluemarble(alpha=0.5)
    im = m.scatter(lon_valid[:],lat_valid[:],c=rad_valid[:],latlon=True,marker='s',s=55, 
                    cmap='coolwarm', alpha=0.2)
    plt.colorbar(im, orientation='vertical')
    plt.show()