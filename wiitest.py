import cwiid
import time

import matplotlib.pyplot as plt
import numpy as np
from scipy import integrate

size = 1000000
t = np.zeros(size)
acc_x = np.zeros(size)
acc_y = np.zeros(size)
acc_z = np.zeros(size)

wm = cwiid.Wiimote()
wm.led= 1
wm.rumble = 1
wm.rpt_mode = cwiid.RPT_ACC
time.sleep(1)
wm.rumble = 0
print("Get ready")

def get_acc(i, f=1):
    global acc_y,acc_x,acc_z
    a = wm.state['acc']
    acc_x[i] = a[0] - f*acc_x[0]
    acc_y[i] = a[1] - f*acc_y[0]
    acc_z[i] = a[2] - f*acc_z[0]

time.sleep(2)
print("Start polling data")
for i in range(size):
    get_acc(i)
    t[i] = time.clock()
    time.sleep(0.000001)
    if i%size/100 == 0:
        print(100*i/size)
t = t - t[0]
print("End polling data")
print(acc_x[0], acc_y[0], acc_z[0])

print ("Disconnecting wiimote")
wm.close()

print("Integrate accelerations")
vel_x = integrate.cumtrapz(acc_x, t)
vel_y = integrate.cumtrapz(acc_y, t)
vel_z = integrate.cumtrapz(acc_z, t)

print("Graphing acceleration")
f, aplot = plt.subplots(3)
aplot[0].plot(t, acc_x, color='r')
aplot[0].plot(t, acc_y, color='g')
aplot[0].plot(t, acc_z, color='b')

print("Graphing velocity")
aplot[1].plot(t[1:], vel_x, color='r')
aplot[1].plot(t[1:], vel_y, color='g')
aplot[1].plot(t[1:], vel_z, color='b')

pos_x = integrate.cumtrapz(vel_x, t[:-1])
pos_y = integrate.cumtrapz(vel_y, t[:-1])
pos_z = integrate.cumtrapz(vel_z, t[:-1])

aplot[2].plot(t[1:-1], pos_x, color='r')
aplot[2].plot(t[1:-1], pos_y, color='g')
aplot[2].plot(t[1:-1], pos_z, color='b')
