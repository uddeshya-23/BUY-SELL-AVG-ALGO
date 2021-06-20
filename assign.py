#!/usr/bin/env python
# coding: utf-8

# In[38]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')


# In[59]:


data = pd.read_csv (r'C:\Users\HP\Downloads\Copy of HINDALCO_1D.csv')   
df = pd.DataFrame(data, columns= ['datetime','close','high','low','open','volume','instrument'])

print(type(df.datetime))


# In[39]:


from pathlib import Path
Path('my_data.db').touch()


# In[41]:


import sqlite3
conn = sqlite3.connect('my_data.db')
c = conn.cursor()


# In[42]:


users = pd.read_csv(r'C:\Users\HP\Downloads\Copy of HINDALCO_1D.csv')
# write the data to a sqlite table
users.to_sql('users', conn, if_exists='append', index = False)


# In[43]:


c.execute('''SELECT * FROM users''').fetchall()


# In[44]:


pd.read_sql('''SELECT * FROM users''', conn)


# In[70]:


from datetime import datetime
df["new_date"] = df["datetime"].apply(lambda x:     datetime.strptime(x,"%Y-%m-%d %H:%M:%S"))
df


# In[72]:


df=df.set_index(df['new_date'].values)


# # THREE MOVING Average ALGORITHM

# In[73]:


plt.figure(figsize=(13.2, 5.5))
plt.title('Close Price', fontsize=18)
plt.plot(df['close'])
plt.xlabel('Date', fontsize = 18)
plt.ylabel('close price', fontsize=18)
plt.show()


# In[74]:


ShortEMA = df.close.ewm(span=5, adjust=False).mean()
MiddleEMA = df.close.ewm(span=21, adjust=False).mean()
longEMA = df.close.ewm(span=63, adjust=False).mean()


# In[80]:


plt.figure(figsize=(12.2, 4.5))
plt.title('Close Price', fontsize=18)
plt.plot(df['close'], label='close price', color= 'blue')
plt.plot(ShortEMA, label='Short/Fast EMA', color= 'red')
plt.plot(MiddleEMA, label='Middle/Medium EMA', color= 'orange')
plt.plot(longEMA, label='long EMA', color= 'green')
plt.plot(ShortEMA)
plt.plot(MiddleEMA)
plt.plot(longEMA)
plt.xlabel('Date', fontsize = 18)
plt.ylabel('close price', fontsize=18)
plt.show()


# In[139]:


df['Short'] = ShortEMA
df['Middle'] = MiddleEMA
df['Long'] = longEMA


# In[143]:


def buy_sell_function(data):
    buy_list =[]
    sell_list =[]
    flag_long =False
    flag_short =False
    
    for i in range(0, len(data)):
        if data['Middle'][i] < data['Long'][i] and data['Short'][i] < data['Middle'][i] and flag_long == False and flag_short == False:
            buy_list.append(data['close'][i])
            sell_list.append(np.nan)
            flag_short = True
        elif flag_short == True and data['Short'][i] > data['Middle'][i]:
            sell_list.append(data['close'][i])
            buy_list.append(np.nan)
            flag_short = False
        elif data['Middle'][i] > data['Long'][i] and data['Short'][i] > data['Middle'][i] and flag_long == False and flag_short == False:
            buy_list.append(data['close'][i])
            sell_list.append(np.nan)
            flag_long = True
        elif flag_long == True and data['Short'][i] < data['Middle'][i]:
            sell_list.append(data['close'][i])
            buy_list.append(np.nan)
            flag_long = False
        else:
            buy_list.append(np.nan)
            sell_list.append(np.nan)
    
    
    return (buy_list, sell_list)
            


# In[146]:


df['Buy'] = buy_sell_function(df)[0]
df['Sell'] = buy_sell_function(df)[1]


# In[156]:


plt.figure(figsize=(11.2, 4.5))
plt.title('BUY AND SELL PLOT', fontsize=18)
plt.plot(df['close'], label='close price', color= 'blue', alpha =0.35)
plt.plot(ShortEMA, label='Short/Fast EMA', color= 'red',alpha =0.35)
plt.plot(MiddleEMA, label='Middle/Medium EMA', color= 'orange',alpha =0.35)
plt.plot(longEMA, label='long/slow EMA', color= 'green',alpha =0.35)
plt.scatter(df.index, df['Buy'], color ='black', marker='^', alpha =1 )
plt.scatter(df.index, df['Sell'], color='red', marker='v', alpha =1 )

plt.xlabel('Date', fontsize = 18)
plt.ylabel('close price', fontsize=18)
plt.show()


# In[ ]:




