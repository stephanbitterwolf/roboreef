
# coding: utf-8

# In[47]:


import smtplib 
from email.mime.text import MIMEText
import numpy as np
import pandas as pd
import datetime 
import time
import pickle


# In[48]:


def email_template(subject, body):
    gmail_user = 'roboreefpi@gmail.com'  
    gmail_password = '---'
    sent_from = gmail_user  
    to = ['scunningham@mlml.calstate.edu', 'sbitterw@ucsc.edu']  # make as many as you want within []
    message = 'Subject: {}\n\n{}'.format(subject, body)

    try:  
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, message)
        server.close()

        return ('Email sent!')
    except:  
        pass


# In[49]:


def warning_log(time,status,notice):
    warninglog = open('errorlog.csv', 'a')
    loglog = [time, status, notice, '\n']
    loglog = ','.join(loglog)
    warninglog.write(loglog)
    warninglog.close
    
def check_last_log():
    warninglog = open('errorlog.csv', 'a')
    loglog = [time, status, notice, '\n']
    loglog = ','.join(loglog)
    loglog=loglog[1]
    warninglog.close
    return loglog[-1]
    

# In[147]:




def email_alert(val_list): # var is the variable in loop, variables need to stay in same order always
    score=[]
    for index, var in enumerate(val_list):
        #set threasholds 
        TRD_high = 29.5
        TRD_low = 16
        pH_high = 9
        pH_low = 7
        ORP_high = 400
        ORP_low =100
        DO1_high = 10
        DO1_low = 1
        DO2_high = 150
        DO2_low = 40
        EC1_high = 60000
        EC1_low = 30000
        EC2_high = 37
        EC2_low = 32
        ts=time.time()
        time_stamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        #make a report log

        if index ==0:
            if float(var) >= TRD_high:
                alert=('Roboreef is too hot. Temp = %s C  ' %var)
                notice=email_template(alert, alert +var+ time_stamp)
                warning_log(time_stamp,alert, notice)
            elif float(var) <= TRD_low:
                alert =('Roboreef is too cold. Temp = %s c ' %var)
                notice=email_template(alert, alert+var + time_stamp)
                warning_log(time_stamp,alert, notice)
            elif pd.isnull(np.array(var, dtype=float)) == True:
                alert =('Temp sensor error')
                notice=email_template(alert, alert +var+ time_stamp)
                warning_log(time_stamp,alert, notice)
            else:
                score.append(1)
                

        if index ==1:
            if float(var) >=pH_high:
                alert =('Roboreef is too basic')
                notice=email_template(alert, alert+var + time_stamp)
                warning_log(time_stamp,alert, notice)
            elif float(var) <= pH_low:
                alert = ('Roboreef is too acidic')
                notice=email_template(alert, alert+var + time_stamp)
                warning_log(time_stamp,alert, notice)
            elif pd.isnull(np.array(var, dtype=float)) == True:
                alert=('pH sensor error')
                notice=email_template(alert, alert +var+ time_stamp)
                warning_log(time_stamp,alert, notice)
            else:
                score.append(1)
               
        if index==2:
            if float(var) >=ORP_high:
                alert = ('Roboreef ORP is too high')
                notice=email_template(alert, alert+var + time_stamp)
                warning_log(time_stamp,alert, notice)
            elif float(var) <=ORP_low:
                alert =('Roboreef ORP is too low')
                notice=email_template(alert, alert+var + time_stamp)
                warning_log(time_stamp,alert, notice)
            elif pd.isnull(np.array(var, dtype=float)) == True:
                alert=('ORP sensor error')
                notice=email_template(alert, alert+var + time_stamp)
                warning_log(time_stamp,alert, notice)
            else:
                score.append(1)
                

        if index==3:
            if float(var) >=DO1_high:
                alert =('Roboreef DO is too high')
                notice=email_template(alert, alert+var + time_stamp)
                warning_log(time_stamp,alert, notice)
            elif float(var) <=DO1_low:
                alert =('Roboreef DO is too low')
                notice=email_template(alert, alert +var+ time_stamp)
                warning_log(time_stamp,alert, notice)
            elif pd.isnull(np.array(var, dtype=float)) == True:
                alert =('DO sensor error')
                notice=email_template(alert, alert+var + time_stamp)
                warning_log(time_stamp,alert, notice)
            else: 
                score.append(1)
               
        if index==4:
            if float(var) >=DO2_high:
                alert = ('Roboreef DO2 is too high')
                notice=email_template(alert, alert +var+ time_stamp)
                warning_log(time_stamp,alert, notice)
            elif float(var) <=DO2_low:
                alert =('Roboreef DO2 is too low')
                notice=email_template(alert, alert+var + time_stamp)
                warning_log(time_stamp,alert, notice)
            elif pd.isnull(np.array(var, dtype=float)) == True:
                alert = ('DO2 sensor error')
                notice=email_template(alert, alert+var+ time_stamp)
                warning_log(time_stamp,alert, notice)
            else:
                score.append(1)
               
        if index==5:
            if float(var) >=EC1_high:
                alert = ('Roboreef EC1 is too high')
                notice=email_template(alert, alert +var+ time_stamp)
                warning_log(time_stamp,alert, notice)
            elif float(var) <=EC1_low:
                alert = ('Roboreef EC1 is too low')
                notice=email_template(alert, alert +var+ time_stamp)
                warning_log(time_stamp,alert, notice)
            elif pd.isnull(np.array(var, dtype=float)) == True:
                alert = ('DO sensor error')
                notice=email_template(alert, alert +var+ time_stamp)
                warning_log(time_stamp,alert, notice)
            else:
                score.append(1)
                
        if index==6:
            if float(var) >=EC2_high:
                alert= ('Roboreef EC2 is too high')
                notice=email_template(alert, alert+var + time_stamp)
                warning_log(time_stamp,alert, notice)
            elif float(var) <=EC2_low:
                alert = ('Roboreef EC2 is too low')
                notice=email_template(alert, alert + var+ time_stamp)
                warning_log(time_stamp,alert, notice)
            elif pd.isnull(np.array(var, dtype=float)) == True: 
                alert =  ('DO sensor error')
                notice=email_template(alert, alert + var+ time_stamp)
                warning_log(time_stamp,alert, notice)
            else:
                score.append(1)
                if sum(score) ==7 and time_stamp[11:13] =='09' and time_stamp[14:16] <='02':
                    email_template('All is well', 'Good morning \n All sensors are reporting within specified parameters \n %s ' %val_list)
                if sum(score) ==7 and time_stamp[11:13] =='18' and time_stamp[14:16] <='02':
                    notice=email_template('All is well', 'Good evening \n All sensors are reporting within specified parameters \n %s ' %val_list)
                    warning_log(time_stamp, 'All good', notice)

