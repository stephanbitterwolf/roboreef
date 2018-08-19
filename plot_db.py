import pymysql as DB
import pandas as pd
import matplotlib

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation


def pull_current_data():
    db = DB.connect(host='localhost', user='admin', passwd='bitterwolf', db='roboreef_db')
    cursor = db.cursor()
    cursor.execute('select ID, Date, Time, Temp, pH, ORP, DO,DO2, EC, EC2 from robo_data order by ID desc limit 5000');
    rows = cursor.fetchall()
    df = pd.DataFrame([[ij for ij in i] for i in rows])
    df.rename(columns={0: 'ID', 1: 'Date', 2: 'Time', 3: 'Temp', 4: 'pH', 5: 'ORP', 6: 'DO',
                       7: 'DO2', 8: 'EC', 9: 'EC2'}, inplace=True);
    return df


fig = plt.figure()

ax1 = fig.add_subplot(4, 1, 1)
ax2 = fig.add_subplot(4, 1, 2)
ax3 = fig.add_subplot(4, 1, 3)
ax4 = fig.add_subplot(4, 1, 4)


def animate(i):
    x = pull_current_data()
    Date = pd.to_datetime(x['Date'] + ' ' + x['Time'])
    ax2.clear()
    ax1.clear()
    ax3.clear()
    ax4.clear()
    ax1.plot(Date[::-1], x['Temp'])
    ax1.set_ylabel('Temp (c)')
    ax1.get_xaxis().set_visible(False)
    ax2.plot(Date[::-1], x['pH'])
    ax2.set_ylabel('pH')
    ax2.get_xaxis().set_visible(False)
    ax3.plot(Date[::-1], x['DO'])
    ax3.set_ylabel('DO')
    ax3.get_xaxis().set_visible(False)
    ax4.plot(Date, x['EC2'])
    ax4.set_ylabel('PSU')


ani = animation.FuncAnimation(fig, animate, interval=1000)
ax4.get_xaxis().axes.invert_xaxis()
plt.show()
