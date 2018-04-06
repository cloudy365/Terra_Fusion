

from my_module import np, plt, Basemap, Polygon
import my_module.data.basic_fusion as bf


def draw_screen_poly( lats, lons, m, facecolor ):
    x, y = m( lons, lats )
    xy = zip(x,y)
    poly = Polygon( xy, facecolor=facecolor, alpha=0.4 )
    plt.gca().add_patch(poly)



bf_file = '/Users/yizhe/Data&Results/TERRA_BF_L1B_O55180_20100503123308_F000_V001.h5'

granule_MOPITT = 'granule_20100503'
granule_ASTER = 'granule_05032010130341'
block_MISR_0 = 36
block_MISR_1 = 37
block_MISR_2 = 38
block_MISR_3 = 39
granule_MODIS_1 = 'granule_2010123_1255'
granule_MODIS_2 = 'granule_2010123_1300'
granule_MODIS_3 = 'granule_2010123_1305'
granule_MODIS_4 = 'granule_2010123_1310'


rad, lat, lon = bf.get_rad_latlon(bf_file, 'MOPITT', granule_MOPITT)
rad_avg = rad[:, :, :, 5].ravel()
lat_flat = lat.ravel()
lon_flat = lon.ravel()
idx_valid = np.where(rad_avg > 0)[0]
rad_valid = rad_avg[idx_valid]
lat_valid = lat_flat[idx_valid]
lon_valid = lon_flat[idx_valid]

plt.figure(figsize=(15, 10))
m = Basemap(projection='ortho',lon_0=-40,lat_0=40,resolution='l')
m.drawcoastlines(color='k', linewidth=0.9)
m.drawmeridians(np.arange(-180.,181,15.))
m.drawparallels(np.arange(90.,-81,-15.))
m.bluemarble(alpha=0.5)
im = m.scatter(lon_valid[:],lat_valid[:],c=rad_valid[:],latlon=True,marker='s',s=55, 
                cmap='coolwarm', alpha=0.2)
plt.colorbar(im, orientation='vertical')


lats, lons = bf.get_bounding_latlon(bf_file, 'ASTER', granule_ASTER)
draw_screen_poly( lats, lons, m, 'red' )

lats, lons = bf.get_bounding_latlon(bf_file, 'MISR', block_MISR_0)
draw_screen_poly( lats, lons, m, 'blue' ) 
lats, lons = bf.get_bounding_latlon(bf_file, 'MISR', block_MISR_1)
draw_screen_poly( lats, lons, m, 'cyan' ) 
lats, lons = bf.get_bounding_latlon(bf_file, 'MISR', block_MISR_2)
draw_screen_poly( lats, lons, m, 'brown' )
lats, lons = bf.get_bounding_latlon(bf_file, 'MISR', block_MISR_3)
draw_screen_poly( lats, lons, m, 'cyan' ) 

lats, lons = bf.get_bounding_latlon(bf_file, 'MODIS', granule_MODIS_1)
draw_screen_poly( lats, lons, m, 'black' )
lats, lons = bf.get_bounding_latlon(bf_file, 'MODIS', granule_MODIS_2)
draw_screen_poly( lats, lons, m, 'black' ) 
lats, lons = bf.get_bounding_latlon(bf_file, 'MODIS', granule_MODIS_3)
draw_screen_poly( lats, lons, m, 'black' ) 
lats, lons = bf.get_bounding_latlon(bf_file, 'MODIS', granule_MODIS_4)
draw_screen_poly( lats, lons, m, 'black' ) 

plt.show()