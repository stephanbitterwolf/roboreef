import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.animation as animation
from datetime import datetime

fig = plt.figure()
rect = fig.patch
rect.set_facecolor('#0079E7')


def animate(i):
    ftemp = 'temp.csv'
    fh = open(ftemp)
    temp = list()
    timeC = list()
    for line in fh:
        pieces = line.split(',')
        degree = pieces[0]
        timeB = pieces[1]
        timeA = timeB[:8]
        # print timeA
        time_string = datetime.strptime(timeA, '%H:%M:%S')
        # print time_string
        try:
            temp.append(float(degree))
            timeC.append(time_string)
        except:
            print("dont know")

        ax1 = fig.add_subplot(1, 1, 1, axisbg='white')
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        ax1.clear()
        ax1.plot(timeC, temp, 'c', linewidth=3.3)
        plt.title('Temperature')
        plt.xlabel('Time')


ani = animation.FuncAnimation(fig, animate, interval=6000)
plt.show()

# I don't know what this does.
'''
*/

void setup() {
    
}
'''
