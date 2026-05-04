

# To create a simple plot
import matplotlib.pyplot as plt

import numpy as np
import pickle
from time import time, sleep
import sys

# check for corret number of arguments
if len(sys.argv) != 2:
    print("Usage: python3 script.py measurement")
    sys.exit(1)

# get measurement file, check format/validity
filename = sys.argv[1].strip()

if not filename.replace("_", "").isdigit():
    sys.exit("Error: file must be in format DD_MM_YYYY_measurement#")

# Load sys params
with open('storage/'+filename+'/sysParams.pkl', 'rb') as inp:
    sysParams = pickle.load(inp, encoding='latin1')


print(('Bandwidth',sysParams.manualBW))

# Init variables
I1 = []
Q1 = []
I2 = []
Q2 = []
slowtime = []

# Load radar object
objs = []

with open('storage/'+filename+'/data.pkl', 'rb') as f:

    # Init A-scan plotting
    plt.figure()
    plt.grid(True)
    plt.title("Frequency domain data plot")
    plt.xlabel("Distance [m]")
    plt.ylabel("Magnitude [dBm]")

    frame_count = 0


    while 1:
        try:
            FD_Data = pickle.load(f)

            if len(FD_Data.data) == 0:
                print("Skipping empty frame")
                continue

            frame_count += 1


            # Plot the measured data dependent on the activated channels
            # Only magnitude data will be plotted
            mag_data = []
            if sysParams.FFT_data_type == 0:  # only magnitudes were transmitted
                mag_data = FD_Data.data

            if sysParams.FFT_data_type == 2:  # real/imaginary
                comp_data = [complex(float(FD_Data.data[n]), float(FD_Data.data[n + 1])) for n in
                             range(0, len(FD_Data.data), 2)]
                mag_data = np.abs(comp_data)

            if sysParams.FFT_data_type == 1 or sysParams.FFT_data_type == 3:  # magnitudes/phase or magnitudes/object angle
                mag_data = [FD_Data.data[n] for n in range(0, len(FD_Data.data), 2)]


            # print((FD_Data.time0/100)+(sysParams.start_time))
            # print((FD_Data.time0/100))



            # Convert to dBm
            min_dbm = -60  # [dBm]
            for n in range(len(mag_data)):
                try:
                    mag_data[n] = 20*np.log10(mag_data[n]/2.**21)
                except:
                    mag_data[n] = min_dbm

            # Sort for active channels
            fd_data = []
            n = 0
            for ch in range(4):  # maximum possible channels = 4
                if sysParams.active_RX_ch & (1 << ch):
                    ind1 = n * FD_Data.nSamples
                    ind2 = ind1 + FD_Data.nSamples
                    n += 1
                    fd_data.append(mag_data[ind1:ind2])
                else:
                    fd_data.append([0] * FD_Data.nSamples)

            I1.append(fd_data[0])
            Q1.append(fd_data[1])
            I2.append(fd_data[2])
            Q2.append(fd_data[3])
            slowtime.append(FD_Data.time0/1000)


            # subtract continuously updated mean value ## Work in progress
            # fd_data[0] = fd_data[0] - np.mean(I1, 0)
            # fd_data[1] = fd_data[1] - np.mean(Q1, 0)
            # fd_data[2] = fd_data[2] - np.mean(I2, 0)
            # fd_data[3] = fd_data[3] - np.mean(Q2, 0)


            # Generate x-axis data, here the distance in [m]
            x_data = [sysParams.tic * n / sysParams.zero_pad / 1.0e6 for n in range(FD_Data.nSamples)]
            plt.clf()
            # Add the data as lines to the plot
            plt.plot(x_data, fd_data[0], 'b',
                     x_data, fd_data[1], 'g',
                     x_data, fd_data[2], 'c',
                     x_data, fd_data[3], 'm')
            # plt.ylim(-40,40)

            #plt.pause(0.001)

            ##plt.savefig('storage/'+filename+'/fig1.pkl')
        except EOFError:



            break

print("Total frames read:", frame_count)


# Now lets make an array out of the data
slowtime = np.array(slowtime)

# Might want to combine several channels
# I1 = np.array(I1).T+np.array(I2).T+np.array(Q1).T+np.array(Q2).T

# print(slowtime-slowtime[0])

I1 = np.array(I1).T



plt.figure(2)

# More "SAR" looking orientation
plt.imshow(I1,extent=[slowtime[0]-slowtime[0],slowtime[len(slowtime)-1]-slowtime[0],x_data[0],x_data[len(x_data)-1]],origin='lower', interpolation='nearest')
#plt.savefig('storage/'+filename+'/fig2.pkl')

plt.figure(3)
# More "GPR" looking orientation
plt.imshow(I1,extent=[slowtime[0]-slowtime[0],slowtime[len(slowtime)-1]-slowtime[0],x_data[len(x_data)-1],x_data[0]],origin='upper', interpolation='nearest')
#plt.savefig('storage/'+filename+'/fig3.pkl')

# Subtract mean
I1 = np.array(I1 - np.einsum('ij->i',I1)[:,None]/I1.shape[1])


plt.figure(4)

# More "SAR" looking orientation
plt.imshow(I1,origin='lower', interpolation='nearest')

plt.show()
#plt.savefig('storage/'+filename+'/fig4.pkl')
