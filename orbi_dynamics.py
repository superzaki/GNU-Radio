#%%

from skyfield.api import Topos, load, EarthSatellite
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
import numpy as np
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
TLE1 = """
COSMOS 1621             
1 15473U 85003E   17072.52328256  .00000005  00000-0 -27757-4 0  9994
2 15473  82.6072  73.9825 0011127 283.0600 194.6746 12.64470084484348
"""
lines = TLE1.strip().splitlines()
c1621 = EarthSatellite(lines[1], lines[2], 
lines[0])
print(c1621)
TLE2 = """
COSMOS 1691 DEB         
1 16271U 85094Q   17068.86632328 +.00000032 +00000-0 +11971-3 0  9990
2 16271 082.6034 269.3400 0005097 261.5742 160.4431 12.62966342448033
"""
lines = TLE2.strip().splitlines()
c1691 = EarthSatellite(lines[1], lines[2], lines[0])
print(c1691)
ts = load.timescale()
t = ts.utc(2017, 2, 24, 4, 16, 40) # Rough datetime starting point
x1 = [] # Ugh, variables - better way?
y1 = []
z1 = []
x1d = []
y1d = []
z1d = []
v1m = []
x2 = []
y2 = []
z2 = []
x2d = []
y2d = []
z2d = []
v2m = []
dp = []
dpm = []
dv = []
dvm = []
t_save = []
t_save_1=[]
for m in range (16,18):
    ss=np.asarray(range(6000))
    sss=.01*ss
    for s in sss:
        t = ts.utc(2017, 2, 24, 4, m, s)
        temp = mdates.date2num(t) # Convert time to number
        t_save.append(temp) # Save said number
        t_save_1.append(temp-mdates.date2num(ts.utc(2017, 2, 24, 4, 16, 0)))
        p1x = c1621.ITRF_position_velocity_error(t)[0][0]*1.496e+8 # AU to km
        p1y = c1621.ITRF_position_velocity_error(t)[0][1]*1.496e+8
        p1z = c1621.ITRF_position_velocity_error(t)[0][2]*1.496e+8
        x1.append(p1x) # Save for plotting
        y1.append(p1y)
        z1.append(p1z)
        v1x = c1621.ITRF_position_velocity_error(t)[1][0]*1731.46 # AU/day to km/s
        v1y = c1621.ITRF_position_velocity_error(t)[1][1]*1731.46
        v1z = c1621.ITRF_position_velocity_error(t)[1][2]*1731.46
        x1d.append(v1x) # Save for plotting
        y1d.append(v1y)
        z1d.append(v1z)
        temp = np.array([v1x, v1y, v1z]) # Calc velocity vector mags, correct units
        v1m.append(np.linalg.norm(temp)) # Save for plotting
        p2x = c1691.ITRF_position_velocity_error(t)[0][0]*1.496e+8 # Rinse / repeat for Aeolus
        p2y = c1691.ITRF_position_velocity_error(t)[0][1]*1.496e+8
        p2z = c1691.ITRF_position_velocity_error(t)[0][2]*1.496e+8
        x2.append(p2x)
        y2.append(p2y)
        z2.append(p2z)
        v2x = c1691.ITRF_position_velocity_error(t)[1][0]*1731.46
        v2y = c1691.ITRF_position_velocity_error(t)[1][1]*1731.46
        v2z = c1691.ITRF_position_velocity_error(t)[1][2]*1731.46
        x2d.append(v2x)
        y2d.append(v2y)
        z2d.append(v2z)
        temp = np.array([v2x, v2y, v2z]) # Calc vector mags, correct units
        v2m.append(np.linalg.norm(temp)) # Save for plotting
        temp = np.array([p1x, p1y, p1z]) - np.array([p2x, p2y, p2z])
        dp.append(temp)
        temp = np.linalg.norm(temp)
        dpm.append(temp) # save relative distance in m
        temp = np.array([v1x, v1y, v1z]) - np.array([v2x, v2y, v2z])
        dv.append(temp)
        temp = np.linalg.norm(temp)
        dvm.append(temp) # save relative velocity in m/s
# export to a file        
np.savetxt('orbit_dynamics',np.matrix.transpose(np.asarray(dpm))[None], delimiter=',')

np.savetxt('time_skyfield',np.matrix.transpose(np.asarray(t_save_1))[None], delimiter=',')
fig, ax1 = plt.subplots(figsize=(15, 6))
ax1.plot_date(t_save,dpm,'b-')
ax1.set_xlabel("Time")
ax1.set_ylabel("Relative Postion Magnitude (km)", color="b")
ax2 = ax1.twinx() # Set axis to the same as the first
ax2.plot_date(t_save,dvm,'r-',alpha=0.3) #
ax2.set_ylabel("Relative Velocity Mangitude (km/s)", color="r")
# formatter = DateFormatter('%d-%m-%Y %H:%M:%S')
formatter = DateFormatter('%H:%M:%S')
plt.gcf().axes[0].xaxis.set_major_formatter(formatter)
ax1.set_ylim([0, 400]) # Set interesting limits
ax2.set_ylim([0, 15])
pmin=min(dpm)
xmin=np.argmin(dpm)
xmin=t_save[xmin+1] # Add an offset for plotting
ymin=pmin
vmax=dvm[np.argmin(dpm)]
#print(mdates.num2date(xmin), pmin, vmax) # Print the interesting bits
# print(dpm)
ax1.annotate('Position: %.3f km, Velocity: %.3f km/s'%(pmin, vmax),
xy=(mdates.num2date(xmin), ymin),
xytext=(mdates.num2date(xmin), ymin)) # Auto
plt.title('M0IEB, Post COSMOS 1621 vs 1691, Step=1s')
x3 = []
y3 = []
z3 = []
x4 = []
y4 = []
z4 = []
dp2m = []
t_save2 = []
cols = []
# for h in range (24): # 11,12
#     for m in range (60): # 0,6
#         for s in range (0,60,10):
#             t = ts.utc(2017, 2, 24, h, m, s)
#             temp = mdates.date2num(t)
#             t_save2.append(temp)
#             p1x = c1621.ITRF_position_velocity_error(t)[0][0]*1.496e+8 # AU to km
#             p1y = c1621.ITRF_position_velocity_error(t)[0][1]*1.496e+8
#             p1z = c1621.ITRF_position_velocity_error(t)[0][2]*1.496e+8
#             x3.append(p1x) # Save for plotting
#             y3.append(p1y)
#             z3.append(p1z)
#             p2x = c1691.ITRF_position_velocity_error(t)[0][0]*1.496e+8 # Repeat for Aeolus
#             p2y = c1691.ITRF_position_velocity_error(t)[0][1]*1.496e+8
#             p2z = c1691.ITRF_position_velocity_error(t)[0][2]*1.496e+8
#             x4.append(p2x)
#             y4.append(p2y)
#             z4.append(p2z)
#             temp = np.array([p1x, p1y, p1z]) - np.array([p2x, p2y, p2z])
#             temp = np.linalg.norm(temp)
#             dp2m.append(temp)
#             if temp > 1000: # Create some colours (yes coloUrs!) based on relative range
#                 cols.append('None')
#             elif temp > 500 and temp < 1000:
#                 cols.append('blue')
#             elif temp < 500:
#                 cols.append('red')
# #%matplotlib inline
# fig2 = plt.figure(figsize=(12, 12))
# ax2 = fig2.add_subplot(111, projection='3d')
# ax2.set_xlim([-7000, 7000])
# ax2.set_ylim([-7000, 7000])
# ax2.set_zlim([-7000, 7000])
# ax2.xaxis.pane.fill = False # Remove horrible gray coloured background
# ax2.yaxis.pane.fill = False
# ax2.zaxis.pane.fill = False
# ax2.azim = 65 # Pose for the camera
# ax2.elev = 25
# ax2.scatter(x3, y3, z3, s=2, c=cols) # Make lines small
# ax2.scatter(x4, y4, z4, s=2, c=cols)
# u, v = np.mgrid[0:2*np.pi:60j, 0:np.pi:30j] # Draw an 'Earth'
# x = np.cos(u)*np.sin(v)*6.371e3
# y = np.sin(u)*np.sin(v)*6.371e3
# z = np.cos(v)*6.371e3
# ax2.plot_wireframe(x, y, z, color="g", alpha=0.08)
# plt.title('M0IEB, Post COSMOS 1621 vs 1691 Event')




#%%
