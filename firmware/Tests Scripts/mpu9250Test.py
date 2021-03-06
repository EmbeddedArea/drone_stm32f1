import serial, time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

serialPort = serial.Serial(port = "COM7", baudrate=115200,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

serialData = ""   # Used to hold data coming over UART
received_data = []

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)
xs = []
ys = []
zs = []


# This function is called periodically from FuncAnimation
def animate(i, xs, ys, zs):
    if(serialPort.in_waiting > 0):
        # Read data out of the buffer until a carraige return / new line is found
        serialData = serialPort.readline()  # Read 10 bytes
        s = serialData.decode("utf-8") .split(':')
        roll = int(s[1])
        pitch = int(s[3])
        #print(roll, pitch)
        # Add x and y to lists
        xs.append(i)
        ys.append(pitch)
        zs.append(roll)
        # Limit x and y lists to 20 items
        xs = xs[-100:]
        ys = ys[-100:]
        zs = zs[-100:]

        # Draw x and y lists
        ax.plot(xs, ys, color='blue', label='Pitch')
        
        ax2.plot(xs, zs, color='red', label='Roll')



# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys, zs), interval=10)

plt.show()
