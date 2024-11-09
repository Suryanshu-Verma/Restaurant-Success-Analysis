# Problem Statment :
## In the competitive restaurant industry, stakeholders often lack clear insights into which user engagement factors contribute most to business success. This project seeks to address the question: How do user engagement metrics (e.g., reviews, tips, and check-ins) correlate with key business performance indicators (such as review count and ratings) for How do user engagement metrics, such as reviews, tips, and check-ins, influence key business performance indicators like review counts and ratings for restaurants? In the highly competitive restaurant industry, understanding these relationships is crucial for stakeholders aiming to enhance business success. providing data-driven insights that can guide strategic decision-making and promote sustainable growth .? By analyzing the Yelp dataset, the goal is to identify actionable patterns that can guide strategic decisions and enhance restaurant performance.

# General Research Objectives :
## Quantify the Correlation Between User Engagement and Business Metrics: Assess the relationship between user engagement factors—such as reviews, tips, and check-ins—and business metrics, including review count and average star rating. This will reveal whether restaurants with higher user engagement tend to have higher ratings and more reviews.

## Analyze the Impact of Sentiment on Business Performance: Investigate whether positive sentiment in reviews and tips is associated with higher star ratings and an increase in the total number of reviews. This analysis will help determine if sentiment influences business success.

## Identify Time Trends in User Engagement: Explore whether consistent user engagement over time serves as a stronger indicator of long-term success compared to sporadic bursts of activity. This will provide insights into engagement patterns that contribute to sustained business growth.

## Adapt Research Based on Emerging Insights: Modify the research focus as necessary, based on findings and insights gained during analysis, to capture additional factors relevant to business success.


# Hypothesis Testing :
## User Engagement and Business Performance: Higher levels of user engagement, such as increased reviews, tips, and check-ins, are positively correlated with higher review counts and ratings for restaurants.

## Sentiment Impact on Ratings and Review Counts: Positive sentiments expressed in reviews and tips contribute to higher overall ratings and increased review counts for restaurants.

## Consistent Engagement and Long-term Success: Consistent user engagement over time is positively associated with sustained business success for restaurants.

# About Dataset :
## This Yelp dataset contains information across eight metropolitan areas in the USA and Canada, organized into five primary tables for analysis:

## `Business`: Contains details on 131,930 businesses, including over 1.2 million attributes like hours, parking, availability, and ambiance.
## `Review`: Includes user-generated reviews with star ratings, text, and timestamps.
## `User`: Information on 1,987,897 users, including activity and interaction data.
## `Tip`: Contains 908,915 tips from users, providing short advice about businesses.
## `Check`-in: Aggregates check-in data over time for each business, enabling time-based analysis of user visits.

## Importing Necessary Libraries Below :



```python
from inspect import stack

import pandas as pd
import numpy as np
from matplotlib.pyplot import subplot
from rich.jupyter import display
from sqlalchemy import create_engine, text
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
from datetime import datetime
import folium
from geopy.geocoders import Nominatim 
import warnings
warnings.filterwarnings('ignore')

```

## Creating MySQL connection Using SQLAlchemy Engine :


```python
from sqlalchemy import create_engine

# Create an engine that connects to your MySQL database
engine = create_engine('mysql+mysqlconnector://root:Vermasuryanshu%40110906@localhost:3306/yelp_db?connect_timeout=600')

# Verify connection
try:
    
    # Here, you can use pandas to directly interact with the database
    print("Successfully connected to the database using SQLAlchemy!")
except Exception as e:
    print(f"Error: {e}")
```

    Successfully connected to the database using SQLAlchemy!
    

## Reading the tables using sqlAlchemy :



```python
try:
    # Open the connection using the engine and use it as a context manager
    with engine.connect() as sql:
        print("Successfully connected to the database using SQLAlchemy!") 
        # Execute SHOW TABLES query
        result = sql.execute(text("SHOW TABLES;"))
        
        # Fetch and print the tables
        print("Tables in the database:")
        for row in result:
            print(row[0])  # Print the name of each table

except Exception as e:
    print(f"Error: {e}")

```

    Successfully connected to the database using SQLAlchemy!
    Tables in the database:
    business
    checkin
    checkin_df_csv
    review
    tip
    user
    


```python
# Reading data from the 'business' table using pandas
business = pd.read_sql("SELECT * FROM business;", engine)
business # Display the first few rows of the DataFrame

```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>business_id</th>
      <th>name</th>
      <th>address</th>
      <th>city</th>
      <th>state</th>
      <th>postal_code</th>
      <th>latitude</th>
      <th>longitude</th>
      <th>stars</th>
      <th>review_count</th>
      <th>is_open</th>
      <th>categories</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Pns2l4eNsfO8kk83dixA6A</td>
      <td>Abby Rappoport, LAC, CMQ</td>
      <td>1616 Chapala St, Ste 2</td>
      <td>Santa Barbara</td>
      <td>CA</td>
      <td>93101</td>
      <td>34.426679</td>
      <td>-119.711197</td>
      <td>5.0</td>
      <td>7</td>
      <td>0</td>
      <td>Doctors, Traditional Chinese Medicine, Naturop...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>mpf3x-BjTdTEA3yCZrAYPw</td>
      <td>The UPS Store</td>
      <td>87 Grasso Plaza Shopping Center</td>
      <td>Affton</td>
      <td>MO</td>
      <td>63123</td>
      <td>38.551126</td>
      <td>-90.335695</td>
      <td>3.0</td>
      <td>15</td>
      <td>1</td>
      <td>Shipping Centers, Local Services, Notaries, Ma...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>tUFrWirKiKi_TAnsVWINQQ</td>
      <td>Target</td>
      <td>5255 E Broadway Blvd</td>
      <td>Tucson</td>
      <td>AZ</td>
      <td>85711</td>
      <td>32.223236</td>
      <td>-110.880452</td>
      <td>3.5</td>
      <td>22</td>
      <td>0</td>
      <td>Department Stores, Shopping, Fashion, Home &amp; G...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>MTSW4McQd7CbVtyjqoe9mw</td>
      <td>St Honore Pastries</td>
      <td>935 Race St</td>
      <td>Philadelphia</td>
      <td>PA</td>
      <td>19107</td>
      <td>39.955505</td>
      <td>-75.155564</td>
      <td>4.0</td>
      <td>80</td>
      <td>1</td>
      <td>Restaurants, Food, Bubble Tea, Coffee &amp; Tea, B...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>mWMc6_wTdE0EUBKIGXDVfA</td>
      <td>Perkiomen Valley Brewery</td>
      <td>101 Walnut St</td>
      <td>Green Lane</td>
      <td>PA</td>
      <td>18054</td>
      <td>40.338183</td>
      <td>-75.471659</td>
      <td>4.5</td>
      <td>13</td>
      <td>1</td>
      <td>Brewpubs, Breweries, Food</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>150341</th>
      <td>IUQopTMmYQG-qRtBk-8QnA</td>
      <td>Binh's Nails</td>
      <td>3388 Gateway Blvd</td>
      <td>Edmonton</td>
      <td>AB</td>
      <td>T6J 5H2</td>
      <td>53.468419</td>
      <td>-113.492054</td>
      <td>3.0</td>
      <td>13</td>
      <td>1</td>
      <td>Nail Salons, Beauty &amp; Spas</td>
    </tr>
    <tr>
      <th>150342</th>
      <td>c8GjPIOTGVmIemT7j5_SyQ</td>
      <td>Wild Birds Unlimited</td>
      <td>2813 Bransford Ave</td>
      <td>Nashville</td>
      <td>TN</td>
      <td>37204</td>
      <td>36.115118</td>
      <td>-86.766925</td>
      <td>4.0</td>
      <td>5</td>
      <td>1</td>
      <td>Pets, Nurseries &amp; Gardening, Pet Stores, Hobby...</td>
    </tr>
    <tr>
      <th>150343</th>
      <td>_QAMST-NrQobXduilWEqSw</td>
      <td>Claire's Boutique</td>
      <td>6020 E 82nd St, Ste 46</td>
      <td>Indianapolis</td>
      <td>IN</td>
      <td>46250</td>
      <td>39.908707</td>
      <td>-86.065088</td>
      <td>3.5</td>
      <td>8</td>
      <td>1</td>
      <td>Shopping, Jewelry, Piercing, Toy Stores, Beaut...</td>
    </tr>
    <tr>
      <th>150344</th>
      <td>mtGm22y5c2UHNXDFAjaPNw</td>
      <td>Cyclery &amp; Fitness Center</td>
      <td>2472 Troy Rd</td>
      <td>Edwardsville</td>
      <td>IL</td>
      <td>62025</td>
      <td>38.782351</td>
      <td>-89.950558</td>
      <td>4.0</td>
      <td>24</td>
      <td>1</td>
      <td>Fitness/Exercise Equipment, Eyewear &amp; Optician...</td>
    </tr>
    <tr>
      <th>150345</th>
      <td>jV_XOycEzSlTx-65W906pg</td>
      <td>Sic Ink</td>
      <td>238 Apollo Beach Blvd</td>
      <td>Apollo beach</td>
      <td>FL</td>
      <td>33572</td>
      <td>27.771002</td>
      <td>-82.394910</td>
      <td>4.5</td>
      <td>9</td>
      <td>1</td>
      <td>Beauty &amp; Spas, Permanent Makeup, Piercing, Tattoo</td>
    </tr>
  </tbody>
</table>
<p>150346 rows × 12 columns</p>
</div>




```python
# Reading data from the 'checkin' table using pandas
checkin = pd.read_sql("SELECT * FROM checkin;", engine)
checkin # Display the first few rows of the DataFrame

```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>business_id</th>
      <th>date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>---kPU91CF4Lq2-WlRu9Lw</td>
      <td>2020-03-13 21:10:56, 2020-06-02 22:18:06, 2020...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>--0iUa4sNDFiZFrAdIWhZQ</td>
      <td>2010-09-13 21:43:09, 2011-05-04 23:08:15, 2011...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>--30_8IhuyMHbSOcNWd6DQ</td>
      <td>2013-06-14 23:29:17, 2014-08-13 23:20:22</td>
    </tr>
    <tr>
      <th>3</th>
      <td>--7PUidqRWpRSpXebiyxTg</td>
      <td>2011-02-15 17:12:00, 2011-07-28 02:46:10, 2012...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>--7jw19RH9JKXgFohspgQw</td>
      <td>2014-04-21 20:42:11, 2014-04-28 21:04:46, 2014...</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>131718</th>
      <td>zznJox6-nmXlGYNWgTDwQQ</td>
      <td>2013-03-23 16:22:47, 2013-04-07 02:03:12, 2013...</td>
    </tr>
    <tr>
      <th>131719</th>
      <td>zznZqH9CiAznbkV6fXyHWA</td>
      <td>2021-06-12 01:16:12</td>
    </tr>
    <tr>
      <th>131720</th>
      <td>zzu6_r3DxBJuXcjnOYVdTw</td>
      <td>2011-05-24 01:35:13, 2012-01-01 23:44:33, 2012...</td>
    </tr>
    <tr>
      <th>131721</th>
      <td>zzw66H6hVjXQEt0Js3Mo4A</td>
      <td>2016-12-03 23:33:26, 2018-12-02 19:08:45</td>
    </tr>
    <tr>
      <th>131722</th>
      <td>zzyx5x0Z7xXWWvWnZFuxlQ</td>
      <td>2015-01-06 17:51:53</td>
    </tr>
  </tbody>
</table>
<p>131723 rows × 2 columns</p>
</div>




```python
# Reading data from the 'review' table using pandas
review = pd.read_sql("SELECT * FROM review;", engine) # Display the first few rows of the DataFrame
review
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>review_id</th>
      <th>user_id</th>
      <th>business_id</th>
      <th>stars</th>
      <th>useful</th>
      <th>funny</th>
      <th>cool</th>
      <th>text</th>
      <th>date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>KU_O5udG6zpxOg-VcAEodg</td>
      <td>mh_-eMZ6K5RLWhZyISBhwA</td>
      <td>XQfwVwDr-v0ZS3_CbbE5Xw</td>
      <td>3.0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>If you decide to eat here, just be aware it is...</td>
      <td>2018-07-07 22:09:11</td>
    </tr>
    <tr>
      <th>1</th>
      <td>BiTunyQ73aT9WBnpR9DZGw</td>
      <td>OyoGAe7OKpv6SyGZT5g77Q</td>
      <td>7ATYjTIgM3jUlt4UM3IypQ</td>
      <td>5.0</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>I've taken a lot of spin classes over the year...</td>
      <td>2012-01-03 15:28:18</td>
    </tr>
    <tr>
      <th>2</th>
      <td>saUsX_uimxRlCVr67Z4Jig</td>
      <td>8g_iMtfSiwikVnbP2etR0A</td>
      <td>YjUWPpI6HXG530lwP-fb2A</td>
      <td>3.0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>Family diner. Had the buffet. Eclectic assortm...</td>
      <td>2014-02-05 20:30:30</td>
    </tr>
    <tr>
      <th>3</th>
      <td>AqPFMleE6RsU23_auESxiA</td>
      <td>_7bHUi9Uuf5__HHc_Q8guQ</td>
      <td>kxX2SOes4o-D3ZQBkiMRfA</td>
      <td>5.0</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>Wow!  Yummy, different,  delicious.   Our favo...</td>
      <td>2015-01-04 00:01:03</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Sx8TMOWLNuJBWer-0pcmoA</td>
      <td>bcjbaE6dDog4jkNY91ncLQ</td>
      <td>e4Vwtrqf-wpJfwesgvdgxQ</td>
      <td>4.0</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>Cute interior and owner (?) gave us tour of up...</td>
      <td>2017-01-14 20:54:15</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>6990275</th>
      <td>H0RIamZu0B0Ei0P4aeh3sQ</td>
      <td>qskILQ3k0I_qcCMI-k6_QQ</td>
      <td>jals67o91gcrD4DC81Vk6w</td>
      <td>5.0</td>
      <td>1</td>
      <td>2</td>
      <td>1</td>
      <td>Latest addition to services from ICCU is Apple...</td>
      <td>2014-12-17 21:45:20</td>
    </tr>
    <tr>
      <th>6990276</th>
      <td>shTPgbgdwTHSuU67mGCmZQ</td>
      <td>Zo0th2m8Ez4gLSbHftiQvg</td>
      <td>2vLksaMmSEcGbjI5gywpZA</td>
      <td>5.0</td>
      <td>2</td>
      <td>1</td>
      <td>2</td>
      <td>This spot offers a great, affordable east week...</td>
      <td>2021-03-31 16:55:10</td>
    </tr>
    <tr>
      <th>6990277</th>
      <td>YNfNhgZlaaCO5Q_YJR4rEw</td>
      <td>mm6E4FbCMwJmb7kPDZ5v2Q</td>
      <td>R1khUUxidqfaJmcpmGd4aw</td>
      <td>4.0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>This Home Depot won me over when I needed to g...</td>
      <td>2019-12-30 03:56:30</td>
    </tr>
    <tr>
      <th>6990278</th>
      <td>i-I4ZOhoX70Nw5H0FwrQUA</td>
      <td>YwAMC-jvZ1fvEUum6QkEkw</td>
      <td>Rr9kKArrMhSLVE9a53q-aA</td>
      <td>5.0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>For when I'm feeling like ignoring my calorie-...</td>
      <td>2022-01-19 18:59:27</td>
    </tr>
    <tr>
      <th>6990279</th>
      <td>RwcKOdEuLRHNJe4M9-qpqg</td>
      <td>6JehEvdoCvZPJ_XIxnzIIw</td>
      <td>VAeEXLbEcI9Emt9KGYq9aA</td>
      <td>3.0</td>
      <td>10</td>
      <td>3</td>
      <td>7</td>
      <td>Located in the 'Walking District' in Nashville...</td>
      <td>2018-01-02 22:50:47</td>
    </tr>
  </tbody>
</table>
<p>6990280 rows × 9 columns</p>
</div>




```python
# Reading data from the 'tip' table using pandas
tip = pd.read_sql("SELECT * FROM tip;", engine) # Display the first few rows of the DataFrame
tip
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>user_id</th>
      <th>business_id</th>
      <th>text</th>
      <th>date</th>
      <th>compliment_count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>AGNUgVwnZUey3gcPCJ76iw</td>
      <td>3uLgwr0qeCNMjKenHJwPGQ</td>
      <td>Avengers time with the ladies.</td>
      <td>2012-05-18 02:17:21</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>NBN4MgHP9D3cw--SnauTkA</td>
      <td>QoezRbYQncpRqyrLH6Iqjg</td>
      <td>They have lots of good deserts and tasty cuban...</td>
      <td>2013-02-05 18:35:10</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>-copOvldyKh1qr-vzkDEvw</td>
      <td>MYoRNLb5chwjQe3c_k37Gg</td>
      <td>It's open even when you think it isn't</td>
      <td>2013-08-18 00:56:08</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>FjMQVZjSqY8syIO-53KFKw</td>
      <td>hV-bABTK-glh5wj31ps_Jw</td>
      <td>Very decent fried chicken</td>
      <td>2017-06-27 23:05:38</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>ld0AperBXk1h6UbqmM80zw</td>
      <td>_uN0OudeJ3Zl_tf6nxg5ww</td>
      <td>Appetizers.. platter special for lunch</td>
      <td>2012-10-06 19:43:09</td>
      <td>0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>908910</th>
      <td>eYodOTF8pkqKPzHkcxZs-Q</td>
      <td>3lHTewuKFt5IImbXJoFeDQ</td>
      <td>Disappointed in one of your managers.</td>
      <td>2021-09-11 19:18:57</td>
      <td>0</td>
    </tr>
    <tr>
      <th>908911</th>
      <td>1uxtQAuJ2T5Xwa_wp7kUnA</td>
      <td>OaGf0Dp56ARhQwIDT90w_g</td>
      <td>Great food and service.</td>
      <td>2021-10-30 11:54:36</td>
      <td>0</td>
    </tr>
    <tr>
      <th>908912</th>
      <td>v48Spe6WEpqehsF2xQADpg</td>
      <td>hYnMeAO77RGyTtIzUSKYzQ</td>
      <td>Love their Cubans!!</td>
      <td>2021-11-05 13:18:56</td>
      <td>0</td>
    </tr>
    <tr>
      <th>908913</th>
      <td>ckqKGM2hl7I9Chp5IpAhkw</td>
      <td>s2eyoTuJrcP7I_XyjdhUHQ</td>
      <td>Great pizza great price</td>
      <td>2021-11-20 16:11:44</td>
      <td>0</td>
    </tr>
    <tr>
      <th>908914</th>
      <td>4tF1CWdMxvvwpUIgGsDygA</td>
      <td>_cb1Vg1NIWry8UA0jyuXnQ</td>
      <td>Food is good value but a bit hot!</td>
      <td>2021-12-07 22:30:00</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
<p>908915 rows × 5 columns</p>
</div>




```python
# Reading data from the 'user' table using pandas
user = pd.read_sql("SELECT * FROM user;", engine) # Display the first few rows of the DataFrame
user
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>user_id</th>
      <th>name</th>
      <th>review_count</th>
      <th>yelping_since</th>
      <th>C5</th>
      <th>funny</th>
      <th>cool</th>
      <th>elite</th>
      <th>friends</th>
      <th>fans</th>
      <th>...</th>
      <th>compliment_more</th>
      <th>compliment_profile</th>
      <th>compliment_cute</th>
      <th>compliment_list</th>
      <th>compliment_note</th>
      <th>compliment_plain</th>
      <th>compliment_cool</th>
      <th>compliment_funny</th>
      <th>compliment_writer</th>
      <th>compliment_photos</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>qVc8ODYU5SZjKXVBgXdI7w</td>
      <td>Walker</td>
      <td>585</td>
      <td>2007-01-25 16:47:26</td>
      <td>7217</td>
      <td>1259</td>
      <td>5994</td>
      <td>2007</td>
      <td>NSCy54eWehBJyZdG2iE84w, pe42u7DcCH2QmI81NX-8qA...</td>
      <td>267</td>
      <td>...</td>
      <td>65</td>
      <td>55</td>
      <td>56</td>
      <td>18</td>
      <td>232</td>
      <td>844</td>
      <td>467</td>
      <td>467</td>
      <td>239</td>
      <td>180</td>
    </tr>
    <tr>
      <th>1</th>
      <td>j14WgRoU_-2ZE1aw1dXrJg</td>
      <td>Daniel</td>
      <td>4333</td>
      <td>2009-01-25 04:35:42</td>
      <td>43091</td>
      <td>13066</td>
      <td>27281</td>
      <td>2009,2010,2011,2012,2013,2014,2015,2016,2017,2...</td>
      <td>ueRPE0CX75ePGMqOFVj6IQ, 52oH4DrRvzzl8wh5UXyU0A...</td>
      <td>3138</td>
      <td>...</td>
      <td>264</td>
      <td>184</td>
      <td>157</td>
      <td>251</td>
      <td>1847</td>
      <td>7054</td>
      <td>3131</td>
      <td>3131</td>
      <td>1521</td>
      <td>1946</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2WnXYQFK0hXEoTxPtV2zvg</td>
      <td>Steph</td>
      <td>665</td>
      <td>2008-07-25 10:41:00</td>
      <td>2086</td>
      <td>1010</td>
      <td>1003</td>
      <td>2009,2010,2011,2012,2013</td>
      <td>LuO3Bn4f3rlhyHIaNfTlnA, j9B4XdHUhDfTKVecyWQgyA...</td>
      <td>52</td>
      <td>...</td>
      <td>13</td>
      <td>10</td>
      <td>17</td>
      <td>3</td>
      <td>66</td>
      <td>96</td>
      <td>119</td>
      <td>119</td>
      <td>35</td>
      <td>18</td>
    </tr>
    <tr>
      <th>3</th>
      <td>SZDeASXq7o05mMNLshsdIA</td>
      <td>Gwen</td>
      <td>224</td>
      <td>2005-11-29 04:38:33</td>
      <td>512</td>
      <td>330</td>
      <td>299</td>
      <td>2009,2010,2011</td>
      <td>enx1vVPnfdNUdPho6PH_wg, 4wOcvMLtU6a9Lslggq74Vg...</td>
      <td>28</td>
      <td>...</td>
      <td>4</td>
      <td>1</td>
      <td>6</td>
      <td>2</td>
      <td>12</td>
      <td>16</td>
      <td>26</td>
      <td>26</td>
      <td>10</td>
      <td>9</td>
    </tr>
    <tr>
      <th>4</th>
      <td>hA5lMy-EnncsH4JoR-hFGQ</td>
      <td>Karen</td>
      <td>79</td>
      <td>2007-01-05 19:40:59</td>
      <td>29</td>
      <td>15</td>
      <td>7</td>
      <td>None</td>
      <td>PBK4q9KEEBHhFvSXCUirIw, 3FWPpM7KU1gXeOM_ZbYMbA...</td>
      <td>1</td>
      <td>...</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>1983818</th>
      <td>fB3jbHi3m0L2KgGOxBv6uw</td>
      <td>Jerrold</td>
      <td>23</td>
      <td>2015-01-06 00:31:31</td>
      <td>7</td>
      <td>0</td>
      <td>0</td>
      <td>None</td>
      <td>None</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1983819</th>
      <td>68czcr4BxJyMQ9cJBm6C7Q</td>
      <td>Jane</td>
      <td>1</td>
      <td>2016-06-14 07:20:52</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>None</td>
      <td>None</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1983820</th>
      <td>1x3KMskYxOuJCjRz70xOqQ</td>
      <td>Shomari</td>
      <td>4</td>
      <td>2017-02-04 15:31:58</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>None</td>
      <td>None</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1983821</th>
      <td>ulfGl4tdbrH05xKzh5lnog</td>
      <td>Susanne</td>
      <td>2</td>
      <td>2011-01-14 00:29:08</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>None</td>
      <td>None</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1983822</th>
      <td>wL5jPrLRVCK_Pmo4lM1zpA</td>
      <td>Isa</td>
      <td>2</td>
      <td>2020-12-19 02:32:39</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>None</td>
      <td>None</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
<p>1983823 rows × 22 columns</p>
</div>



#  Data Analysis :


```python
business_Open_Restaurants=pd.read_sql("select * from business where is_open = 1 AND  lower(categories) like '%restaurant%';",engine) # Data of Open Restaurants
```


```python
business_Open_Restaurants # Open Restaurants
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>business_id</th>
      <th>name</th>
      <th>address</th>
      <th>city</th>
      <th>state</th>
      <th>postal_code</th>
      <th>latitude</th>
      <th>longitude</th>
      <th>stars</th>
      <th>review_count</th>
      <th>is_open</th>
      <th>categories</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>MTSW4McQd7CbVtyjqoe9mw</td>
      <td>St Honore Pastries</td>
      <td>935 Race St</td>
      <td>Philadelphia</td>
      <td>PA</td>
      <td>19107</td>
      <td>39.955505</td>
      <td>-75.155564</td>
      <td>4.0</td>
      <td>80</td>
      <td>1</td>
      <td>Restaurants, Food, Bubble Tea, Coffee &amp; Tea, B...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>CF33F8-E6oudUQ46HnavjQ</td>
      <td>Sonic Drive-In</td>
      <td>615 S Main St</td>
      <td>Ashland City</td>
      <td>TN</td>
      <td>37015</td>
      <td>36.269593</td>
      <td>-87.058943</td>
      <td>2.0</td>
      <td>6</td>
      <td>1</td>
      <td>Burgers, Fast Food, Sandwiches, Food, Ice Crea...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>bBDDEgkFA1Otx9Lfe7BZUQ</td>
      <td>Sonic Drive-In</td>
      <td>2312 Dickerson Pike</td>
      <td>Nashville</td>
      <td>TN</td>
      <td>37207</td>
      <td>36.208102</td>
      <td>-86.768170</td>
      <td>1.5</td>
      <td>10</td>
      <td>1</td>
      <td>Ice Cream &amp; Frozen Yogurt, Fast Food, Burgers,...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>eEOYSgkmpB90uNA7lDOMRA</td>
      <td>Vietnamese Food Truck</td>
      <td>None</td>
      <td>Tampa Bay</td>
      <td>FL</td>
      <td>33602</td>
      <td>27.955269</td>
      <td>-82.456320</td>
      <td>4.0</td>
      <td>10</td>
      <td>1</td>
      <td>Vietnamese, Food, Restaurants, Food Trucks</td>
    </tr>
    <tr>
      <th>4</th>
      <td>il_Ro8jwPlHresjw9EGmBg</td>
      <td>Denny's</td>
      <td>8901 US 31 S</td>
      <td>Indianapolis</td>
      <td>IN</td>
      <td>46227</td>
      <td>39.637133</td>
      <td>-86.127217</td>
      <td>2.5</td>
      <td>28</td>
      <td>1</td>
      <td>American (Traditional), Restaurants, Diners, B...</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>34999</th>
      <td>w_4xUt-1AyY2ZwKtnjW0Xg</td>
      <td>Bittercreek Alehouse</td>
      <td>246 N 8th St</td>
      <td>Boise</td>
      <td>ID</td>
      <td>83702</td>
      <td>43.616590</td>
      <td>-116.202383</td>
      <td>4.5</td>
      <td>998</td>
      <td>1</td>
      <td>Bars, Gastropubs, Sandwiches, Nightlife, Resta...</td>
    </tr>
    <tr>
      <th>35000</th>
      <td>l9eLGG9ZKpLJzboZq-9LRQ</td>
      <td>Wawa</td>
      <td>19 N Bishop Ave</td>
      <td>Clifton Heights</td>
      <td>PA</td>
      <td>19018</td>
      <td>39.925656</td>
      <td>-75.310344</td>
      <td>3.0</td>
      <td>11</td>
      <td>1</td>
      <td>Restaurants, Sandwiches, Convenience Stores, C...</td>
    </tr>
    <tr>
      <th>35001</th>
      <td>cM6V90ExQD6KMSU3rRB5ZA</td>
      <td>Dutch Bros Coffee</td>
      <td>1181 N Milwaukee St</td>
      <td>Boise</td>
      <td>ID</td>
      <td>83704</td>
      <td>43.615401</td>
      <td>-116.284689</td>
      <td>4.0</td>
      <td>33</td>
      <td>1</td>
      <td>Cafes, Juice Bars &amp; Smoothies, Coffee &amp; Tea, R...</td>
    </tr>
    <tr>
      <th>35002</th>
      <td>WnT9NIzQgLlILjPT0kEcsQ</td>
      <td>Adelita Taqueria &amp; Restaurant</td>
      <td>1108 S 9th St</td>
      <td>Philadelphia</td>
      <td>PA</td>
      <td>19147</td>
      <td>39.935982</td>
      <td>-75.158665</td>
      <td>4.5</td>
      <td>35</td>
      <td>1</td>
      <td>Restaurants, Mexican</td>
    </tr>
    <tr>
      <th>35003</th>
      <td>2O2K6SXPWv56amqxCECd4w</td>
      <td>The Plum Pit</td>
      <td>4405 Pennell Rd</td>
      <td>Aston</td>
      <td>DE</td>
      <td>19014</td>
      <td>39.856185</td>
      <td>-75.427725</td>
      <td>4.5</td>
      <td>14</td>
      <td>1</td>
      <td>Restaurants, Comfort Food, Food, Food Trucks, ...</td>
    </tr>
  </tbody>
</table>
<p>35004 rows × 12 columns</p>
</div>



### Out of 150K Businesses, 35K are Restaurant Business and are Open.

# Q. What is the descriptive stats for review count and star rating for businesses ?


```python
query = """
SELECT 
    AVG(review_count) AS average_review,
    MIN(review_count) AS min_review,
    MAX(review_count) AS max_review,
    AVG(stars) AS average_star_rating,
    MIN(stars) AS min_star_rating,
    MAX(stars) AS max_star_rating
FROM (
    SELECT * 
    FROM business 
    WHERE is_open = 1 
    AND LOWER(categories) LIKE '%restaurant%'
) AS business_Open_Restaurants;
"""


# Execute the query and display the result
review_business = pd.read_sql(query, engine)

```


```python
# Calculating the median for the both Stars & Review_count
review_business.insert(3,'median_review',[business['review_count'].median()])
review_business.insert(7,'median_stars',[business['stars'].median()])

```


```python
review_business # As per the stats, We can conclude that the review columns includes outliers
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>average_review</th>
      <th>min_review</th>
      <th>max_review</th>
      <th>median_review</th>
      <th>average_star_rating</th>
      <th>min_star_rating</th>
      <th>max_star_rating</th>
      <th>median_stars</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>104.0978</td>
      <td>5</td>
      <td>7568</td>
      <td>15.0</td>
      <td>3.523969</td>
      <td>1.0</td>
      <td>5.0</td>
      <td>3.5</td>
    </tr>
  </tbody>
</table>
</div>




```python
review_business=review_business.T
```


```python
review_business
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>average_review</th>
      <td>104.097800</td>
    </tr>
    <tr>
      <th>min_review</th>
      <td>5.000000</td>
    </tr>
    <tr>
      <th>max_review</th>
      <td>7568.000000</td>
    </tr>
    <tr>
      <th>median_review</th>
      <td>15.000000</td>
    </tr>
    <tr>
      <th>average_star_rating</th>
      <td>3.523969</td>
    </tr>
    <tr>
      <th>min_star_rating</th>
      <td>1.000000</td>
    </tr>
    <tr>
      <th>max_star_rating</th>
      <td>5.000000</td>
    </tr>
    <tr>
      <th>median_stars</th>
      <td>3.500000</td>
    </tr>
  </tbody>
</table>
</div>



### The Max_review is outlier and data is skewed, To address this I decided to remove restaurants with outlier review counts, For this I created a Function to identify & remove outliers using IQR method.


```python
# Convert column to integer, if it contains boolean values by mistake
business_Open_Restaurants['review_count'] = business_Open_Restaurants['review_count'].astype(int)

```


```python
#  Removing Outliers using IQR 
# Defining a function called --> remove_outlier
def remove_outlier(df,col):
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3-q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
    return df


# calling the function 
business_Open_Restaurants = remove_outlier(business_Open_Restaurants,'review_count')



```


```python
business_Open_Restaurants
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>business_id</th>
      <th>name</th>
      <th>address</th>
      <th>city</th>
      <th>state</th>
      <th>postal_code</th>
      <th>latitude</th>
      <th>longitude</th>
      <th>stars</th>
      <th>review_count</th>
      <th>is_open</th>
      <th>categories</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>MTSW4McQd7CbVtyjqoe9mw</td>
      <td>St Honore Pastries</td>
      <td>935 Race St</td>
      <td>Philadelphia</td>
      <td>PA</td>
      <td>19107</td>
      <td>39.955505</td>
      <td>-75.155564</td>
      <td>4.0</td>
      <td>80</td>
      <td>1</td>
      <td>Restaurants, Food, Bubble Tea, Coffee &amp; Tea, B...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>CF33F8-E6oudUQ46HnavjQ</td>
      <td>Sonic Drive-In</td>
      <td>615 S Main St</td>
      <td>Ashland City</td>
      <td>TN</td>
      <td>37015</td>
      <td>36.269593</td>
      <td>-87.058943</td>
      <td>2.0</td>
      <td>6</td>
      <td>1</td>
      <td>Burgers, Fast Food, Sandwiches, Food, Ice Crea...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>bBDDEgkFA1Otx9Lfe7BZUQ</td>
      <td>Sonic Drive-In</td>
      <td>2312 Dickerson Pike</td>
      <td>Nashville</td>
      <td>TN</td>
      <td>37207</td>
      <td>36.208102</td>
      <td>-86.768170</td>
      <td>1.5</td>
      <td>10</td>
      <td>1</td>
      <td>Ice Cream &amp; Frozen Yogurt, Fast Food, Burgers,...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>eEOYSgkmpB90uNA7lDOMRA</td>
      <td>Vietnamese Food Truck</td>
      <td>None</td>
      <td>Tampa Bay</td>
      <td>FL</td>
      <td>33602</td>
      <td>27.955269</td>
      <td>-82.456320</td>
      <td>4.0</td>
      <td>10</td>
      <td>1</td>
      <td>Vietnamese, Food, Restaurants, Food Trucks</td>
    </tr>
    <tr>
      <th>4</th>
      <td>il_Ro8jwPlHresjw9EGmBg</td>
      <td>Denny's</td>
      <td>8901 US 31 S</td>
      <td>Indianapolis</td>
      <td>IN</td>
      <td>46227</td>
      <td>39.637133</td>
      <td>-86.127217</td>
      <td>2.5</td>
      <td>28</td>
      <td>1</td>
      <td>American (Traditional), Restaurants, Diners, B...</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>34998</th>
      <td>sf_oQ62L8UEnOOLf00nNGA</td>
      <td>Pizza Hut</td>
      <td>5028 Old Hickory</td>
      <td>Hermitage</td>
      <td>TN</td>
      <td>37076</td>
      <td>36.193201</td>
      <td>-86.614748</td>
      <td>3.0</td>
      <td>6</td>
      <td>1</td>
      <td>Restaurants, Pizza, Fast Food, Chicken Wings, ...</td>
    </tr>
    <tr>
      <th>35000</th>
      <td>l9eLGG9ZKpLJzboZq-9LRQ</td>
      <td>Wawa</td>
      <td>19 N Bishop Ave</td>
      <td>Clifton Heights</td>
      <td>PA</td>
      <td>19018</td>
      <td>39.925656</td>
      <td>-75.310344</td>
      <td>3.0</td>
      <td>11</td>
      <td>1</td>
      <td>Restaurants, Sandwiches, Convenience Stores, C...</td>
    </tr>
    <tr>
      <th>35001</th>
      <td>cM6V90ExQD6KMSU3rRB5ZA</td>
      <td>Dutch Bros Coffee</td>
      <td>1181 N Milwaukee St</td>
      <td>Boise</td>
      <td>ID</td>
      <td>83704</td>
      <td>43.615401</td>
      <td>-116.284689</td>
      <td>4.0</td>
      <td>33</td>
      <td>1</td>
      <td>Cafes, Juice Bars &amp; Smoothies, Coffee &amp; Tea, R...</td>
    </tr>
    <tr>
      <th>35002</th>
      <td>WnT9NIzQgLlILjPT0kEcsQ</td>
      <td>Adelita Taqueria &amp; Restaurant</td>
      <td>1108 S 9th St</td>
      <td>Philadelphia</td>
      <td>PA</td>
      <td>19147</td>
      <td>39.935982</td>
      <td>-75.158665</td>
      <td>4.5</td>
      <td>35</td>
      <td>1</td>
      <td>Restaurants, Mexican</td>
    </tr>
    <tr>
      <th>35003</th>
      <td>2O2K6SXPWv56amqxCECd4w</td>
      <td>The Plum Pit</td>
      <td>4405 Pennell Rd</td>
      <td>Aston</td>
      <td>DE</td>
      <td>19014</td>
      <td>39.856185</td>
      <td>-75.427725</td>
      <td>4.5</td>
      <td>14</td>
      <td>1</td>
      <td>Restaurants, Comfort Food, Food, Food Trucks, ...</td>
    </tr>
  </tbody>
</table>
<p>31537 rows × 12 columns</p>
</div>




```python
business_Open_Restaurants['review_count'].describe() # its reflected the change and the outlier are remove and the max is 284
```




    count    31537.000000
    mean        55.975426
    std         56.559679
    min          5.000000
    25%         14.000000
    50%         33.000000
    75%         79.000000
    max        248.000000
    Name: review_count, dtype: float64



### After Removing outliers, Now I get average review count as 55.975 for the restaurant business.

# Open Businesses Which Are Restaurant :


```python
business_Open_Restaurants
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>business_id</th>
      <th>name</th>
      <th>address</th>
      <th>city</th>
      <th>state</th>
      <th>postal_code</th>
      <th>latitude</th>
      <th>longitude</th>
      <th>stars</th>
      <th>review_count</th>
      <th>is_open</th>
      <th>categories</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>MTSW4McQd7CbVtyjqoe9mw</td>
      <td>St Honore Pastries</td>
      <td>935 Race St</td>
      <td>Philadelphia</td>
      <td>PA</td>
      <td>19107</td>
      <td>39.955505</td>
      <td>-75.155564</td>
      <td>4.0</td>
      <td>80</td>
      <td>1</td>
      <td>Restaurants, Food, Bubble Tea, Coffee &amp; Tea, B...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>CF33F8-E6oudUQ46HnavjQ</td>
      <td>Sonic Drive-In</td>
      <td>615 S Main St</td>
      <td>Ashland City</td>
      <td>TN</td>
      <td>37015</td>
      <td>36.269593</td>
      <td>-87.058943</td>
      <td>2.0</td>
      <td>6</td>
      <td>1</td>
      <td>Burgers, Fast Food, Sandwiches, Food, Ice Crea...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>bBDDEgkFA1Otx9Lfe7BZUQ</td>
      <td>Sonic Drive-In</td>
      <td>2312 Dickerson Pike</td>
      <td>Nashville</td>
      <td>TN</td>
      <td>37207</td>
      <td>36.208102</td>
      <td>-86.768170</td>
      <td>1.5</td>
      <td>10</td>
      <td>1</td>
      <td>Ice Cream &amp; Frozen Yogurt, Fast Food, Burgers,...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>eEOYSgkmpB90uNA7lDOMRA</td>
      <td>Vietnamese Food Truck</td>
      <td>None</td>
      <td>Tampa Bay</td>
      <td>FL</td>
      <td>33602</td>
      <td>27.955269</td>
      <td>-82.456320</td>
      <td>4.0</td>
      <td>10</td>
      <td>1</td>
      <td>Vietnamese, Food, Restaurants, Food Trucks</td>
    </tr>
    <tr>
      <th>4</th>
      <td>il_Ro8jwPlHresjw9EGmBg</td>
      <td>Denny's</td>
      <td>8901 US 31 S</td>
      <td>Indianapolis</td>
      <td>IN</td>
      <td>46227</td>
      <td>39.637133</td>
      <td>-86.127217</td>
      <td>2.5</td>
      <td>28</td>
      <td>1</td>
      <td>American (Traditional), Restaurants, Diners, B...</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>34998</th>
      <td>sf_oQ62L8UEnOOLf00nNGA</td>
      <td>Pizza Hut</td>
      <td>5028 Old Hickory</td>
      <td>Hermitage</td>
      <td>TN</td>
      <td>37076</td>
      <td>36.193201</td>
      <td>-86.614748</td>
      <td>3.0</td>
      <td>6</td>
      <td>1</td>
      <td>Restaurants, Pizza, Fast Food, Chicken Wings, ...</td>
    </tr>
    <tr>
      <th>35000</th>
      <td>l9eLGG9ZKpLJzboZq-9LRQ</td>
      <td>Wawa</td>
      <td>19 N Bishop Ave</td>
      <td>Clifton Heights</td>
      <td>PA</td>
      <td>19018</td>
      <td>39.925656</td>
      <td>-75.310344</td>
      <td>3.0</td>
      <td>11</td>
      <td>1</td>
      <td>Restaurants, Sandwiches, Convenience Stores, C...</td>
    </tr>
    <tr>
      <th>35001</th>
      <td>cM6V90ExQD6KMSU3rRB5ZA</td>
      <td>Dutch Bros Coffee</td>
      <td>1181 N Milwaukee St</td>
      <td>Boise</td>
      <td>ID</td>
      <td>83704</td>
      <td>43.615401</td>
      <td>-116.284689</td>
      <td>4.0</td>
      <td>33</td>
      <td>1</td>
      <td>Cafes, Juice Bars &amp; Smoothies, Coffee &amp; Tea, R...</td>
    </tr>
    <tr>
      <th>35002</th>
      <td>WnT9NIzQgLlILjPT0kEcsQ</td>
      <td>Adelita Taqueria &amp; Restaurant</td>
      <td>1108 S 9th St</td>
      <td>Philadelphia</td>
      <td>PA</td>
      <td>19147</td>
      <td>39.935982</td>
      <td>-75.158665</td>
      <td>4.5</td>
      <td>35</td>
      <td>1</td>
      <td>Restaurants, Mexican</td>
    </tr>
    <tr>
      <th>35003</th>
      <td>2O2K6SXPWv56amqxCECd4w</td>
      <td>The Plum Pit</td>
      <td>4405 Pennell Rd</td>
      <td>Aston</td>
      <td>DE</td>
      <td>19014</td>
      <td>39.856185</td>
      <td>-75.427725</td>
      <td>4.5</td>
      <td>14</td>
      <td>1</td>
      <td>Restaurants, Comfort Food, Food, Food Trucks, ...</td>
    </tr>
  </tbody>
</table>
<p>31537 rows × 12 columns</p>
</div>



# Q. Which restaurant have the higest number of reviews ?


```python
pd.read_sql(""" select name, SUM(review_count) AS Higest_Review_Counts, AVG(stars) AS Average_Rating from (select * from business where is_open = 1 AND  lower(categories) like '%restaurant%') AS business_Open_Restaurants group by name order by Higest_Review_Counts desc limit 10;""",engine)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>Higest_Review_Counts</th>
      <th>Average_Rating</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>McDonald's</td>
      <td>16490.0</td>
      <td>1.868702</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Chipotle Mexican Grill</td>
      <td>9071.0</td>
      <td>2.381757</td>
    </tr>
    <tr>
      <th>2</th>
      <td>First Watch</td>
      <td>8688.0</td>
      <td>3.896552</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Acme Oyster House</td>
      <td>8343.0</td>
      <td>4.000000</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Taco Bell</td>
      <td>8017.0</td>
      <td>2.141813</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Chick-fil-A</td>
      <td>7967.0</td>
      <td>3.373418</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Oceana Grill</td>
      <td>7400.0</td>
      <td>4.000000</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Buffalo Wild Wings</td>
      <td>6810.0</td>
      <td>2.347458</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Panera Bread</td>
      <td>6613.0</td>
      <td>2.661905</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Hattie B’s Hot Chicken - Nashville</td>
      <td>6093.0</td>
      <td>4.500000</td>
    </tr>
  </tbody>
</table>
</div>



# Q. Which restaurant have the highest number of highest rating ? 


```python
pd.read_sql(""" select name, SUM(review_count) AS Higest_Review_Counts, AVG(stars) AS Average_Rating from (select * from business where is_open = 1 AND  lower(categories) like '%restaurant%') AS business_Open_Restaurants group by name order by Average_Rating desc limit 10;""",engine).sort_values('Higest_Review_Counts',ascending=False)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>Higest_Review_Counts</th>
      <th>Average_Rating</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>7</th>
      <td>Vegan International Co. Kitchen &amp; Market</td>
      <td>269.0</td>
      <td>5.0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>The Foundry Bakery</td>
      <td>185.0</td>
      <td>5.0</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Jet City Espresso Hyde Park</td>
      <td>152.0</td>
      <td>5.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>bb.q Chicken - O'Fallon</td>
      <td>42.0</td>
      <td>5.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Asia Mix Restaurant</td>
      <td>10.0</td>
      <td>5.0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Healthy Soul Indy</td>
      <td>9.0</td>
      <td>5.0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Antojitos Carmen Restaurante Y Taqueria</td>
      <td>9.0</td>
      <td>5.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Tacos Don Vicente</td>
      <td>8.0</td>
      <td>5.0</td>
    </tr>
    <tr>
      <th>0</th>
      <td>YWCA Corazon Cafe &amp; Catering</td>
      <td>5.0</td>
      <td>5.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>In and Out Express Food Market</td>
      <td>5.0</td>
      <td>5.0</td>
    </tr>
  </tbody>
</table>
</div>



## NOTE :
### No direct correlation:  Higher rating do not guarantee a higher review count and vice versa, The review cannot reflect user engagement, but do not necessarily States the overall customer satisfaction or business performance, Successes in the restaurant business is not solely determined by rating or review counts.   

# Q. Do restaurants with higer engagement tends to have higher rating ?


```python
pd.read_sql(""" select business_id, sum(length(date) - length(replace(date, ',', '')) + 1 ) as checkin_count from checkin group by business_id order by checkin_count desc ;""",engine)

```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>business_id</th>
      <th>checkin_count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>3wo9jODQnuvBm8Gkem6qXg</td>
      <td>3110.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>MkF4gosEaJqJ3tNk1BZiwg</td>
      <td>3106.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>ctHjyadbDQAtUFfkcAFEHw</td>
      <td>3104.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>h6IzeUVASeDtvKhd2PEsKA</td>
      <td>3101.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>6dDC5PSmPEoJYuM8r8dN_A</td>
      <td>3096.0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>131718</th>
      <td>i5tex_2_UNEsPUh6oaVREA</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>131719</th>
      <td>i6-xjNGY_8Co3DwHDrBZ4w</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>131720</th>
      <td>i69x-7o4wuLbWC3sf4ek7Q</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>131721</th>
      <td>i6n5Cv7C2OOfrgGAj5weiw</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>131722</th>
      <td>i6nsOTszsTWJw_vRrBkAJg</td>
      <td>1.0</td>
    </tr>
  </tbody>
</table>
<p>131723 rows × 2 columns</p>
</div>




```python
# tip_counts per business_id
pd.read_sql(""" select business_id, count(*) as tip_counts from  tip group by business_id order by tip_counts desc;""",engine)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>business_id</th>
      <th>tip_counts</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>FEXhWNCMkv22qG04E83Qjg</td>
      <td>2571</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-QI8Qi8XWH3D8y8ethnajA</td>
      <td>1011</td>
    </tr>
    <tr>
      <th>2</th>
      <td>_ab50qdWOk0DdB6XOrBitw</td>
      <td>932</td>
    </tr>
    <tr>
      <th>3</th>
      <td>ytynqOUb3hjKeJfRj5Tshw</td>
      <td>827</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Eb1XmmLWyt_way5NNZ7-Pw</td>
      <td>826</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>106188</th>
      <td>54hp8YAMnI0baeSwbnBxDA</td>
      <td>1</td>
    </tr>
    <tr>
      <th>106189</th>
      <td>GP9X_N5vMHYTuwcEiz-Xnw</td>
      <td>1</td>
    </tr>
    <tr>
      <th>106190</th>
      <td>qgZtdbGuASSA-Av7_-rgCw</td>
      <td>1</td>
    </tr>
    <tr>
      <th>106191</th>
      <td>H5TSeRUNkoCRtL2RcB9WKQ</td>
      <td>1</td>
    </tr>
    <tr>
      <th>106192</th>
      <td>uE_4H__4kj4Xjb115_LBvA</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
<p>106193 rows × 2 columns</p>
</div>




```python
review_counts = pd.read_sql(F""" select total.avg_rating as rating,
AVG(total.review_count) as avg_review_count,
AVG(total.checkin_count) as avg_checkin_count,
AVG(total.tip_count) as avg_tip_count
from
(select 
    business.business_id,
    SUM(business.review_count) AS review_count,
    AVG(business.stars) AS avg_rating,
    SUM(LENGTH(checkin.date) - LENGTH(replace(checkin.date, ',', '')) +1) AS checkin_count,
    SUM(tip.tip_count) as tip_count
from 
    business
left join 
    checkin ON business.business_id = checkin.business_id
left join 
    (select business_id, count(business_id) as tip_count from tip GROUP BY business_id ORDER BY tip_count) as tip ON business.business_id = tip.business_id 
where business.business_id IN {tuple(business_Open_Restaurants['business_id'])}
GROUP BY 
    business.business_id) as total 
GROUP BY total.avg_rating 
 """,engine)
```


```python
review_counts=review_counts.sort_values('rating', ascending=False)
```

# Ploting `Bar` Graphs :


```python
# Creating Void and Axis for ploting the graphs
plt.figure(figsize=(25,8))
plt.title('AVG Engagement Based On Rating\n\n')
plt.xticks([])
plt.yticks([])

# Review Count Plot
plt.subplot(1,3,1)
plt.title('Review Count')
plt.barh(review_counts['rating'].astype('str'), review_counts['avg_review_count'], edgecolor= 'k', color = 'RED')
plt.gca().spines['right'].set_visible(False)
for i, value in enumerate(review_counts['avg_review_count']):
    plt.text(value+3,i,str(round(value)), color='Black', va = 'center')
plt.xticks([])

# Checkin Count Plot
plt.subplot(1,3,2)
plt.title('Checkin Count')
plt.barh(review_counts['rating'].astype('str'), review_counts['avg_checkin_count'], edgecolor= 'k', color = 'BLUE')
plt.gca().spines['right'].set_visible(False)
for i, value in enumerate(review_counts['avg_checkin_count']):
    plt.text(value+3,i,str(round(value)), color='Black', va = 'center')
plt.xticks([])

# Tip Count Plot
plt.subplot(1,3,3)
plt.title('Tip Count')
plt.barh(review_counts['rating'].astype('str'), review_counts['avg_tip_count'], edgecolor= 'k', color = 'CYAN')
plt.gca().spines['right'].set_visible(False)
for i, value in enumerate(review_counts['avg_tip_count']):
    plt.text(value+0.05,i,str(round(value)), color='Black', va = 'center')
plt.xticks([])
plt.show()

```


    
![png](main_files/main_44_0.png)
    


## NOTE :
### Data show a general increase in average review check in and tip counts as rating improves from one to four stars, restaurants created four stars. Exhibit the highest engagement across reviews, check insurance and tips, suggesting a peak in user interaction, interestingly, engagement matrix. ( Review, check in ). Dip for restaurant rated 4.5 and significantly more at five stars, They dropped an engagement at 5 stars might suggest either a situation point where fewer customer feel compended or to add their reviews for a selective believer only a small satisfied audience. Frequents these establishment. 

# Q. Is there a correclation between the number of reviews, tip, and check - ins for a business ?


```python
engage_df = pd.read_sql(F""" select business.business_id,
 sum(business.review_count) as review_count,
 AVG(business.stars) as avg_rating,
 SUM(LENGTH(checkin.date) - LENGTH(replace(checkin.date, ',', '')) +1) as checkin_count,
 SUM(tip.tip_count) as tip_count
 from 
 business 
 left join 
    checkin ON business.business_id = checkin.business_id
left join 
    (select business_id, count(business_id) as tip_count from tip GROUP BY business_id ORDER BY tip_count) as tip ON business.business_id = tip.business_id 
where business.business_id IN {tuple(business_Open_Restaurants['business_id'])}
GROUP BY 
    business.business_id
 
 
 """,engine).dropna()


```


```python
engage_df_corr = engage_df[['review_count','checkin_count','tip_count']].corr()
```


```python
# Ploting the HeatMap
sns.heatmap(engage_df_corr,cmap='seismic', annot=True, linewidths=0.5,linecolor='white')

```




    <Axes: >




    
![png](main_files/main_49_1.png)
    



```python
engage_dff = pd.read_sql(F"""
    SELECT 
        business.business_id,
        SUM(business.review_count) AS review_count,
        AVG(business.stars) AS avg_rating,
        SUM(LENGTH(checkin.date) - LENGTH(REPLACE(checkin.date, ',', '')) + 1) AS checkin_count,
        SUM(tip.tip_count) AS tip_count,
        CASE 
            WHEN business.stars >= 3.5 THEN 'High-Rated' 
            ELSE 'Low-Rated' 
        END AS category
    FROM 
        business 
    LEFT JOIN 
        checkin ON business.business_id = checkin.business_id
    LEFT JOIN 
        (SELECT business_id, COUNT(business_id) AS tip_count 
         FROM tip 
         GROUP BY business_id) AS tip ON business.business_id = tip.business_id 
    WHERE 
        business.business_id IN {tuple(business_Open_Restaurants['business_id'])}
    GROUP BY 
        business.business_id, business.stars
""", engine).dropna()

```


```python
engage_dff.groupby('category')[['review_count','tip_count','checkin_count']].mean() 
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>review_count</th>
      <th>tip_count</th>
      <th>checkin_count</th>
    </tr>
    <tr>
      <th>category</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>High-Rated</th>
      <td>72.274446</td>
      <td>10.148378</td>
      <td>121.375576</td>
    </tr>
    <tr>
      <th>Low-Rated</th>
      <td>42.123420</td>
      <td>6.541689</td>
      <td>88.880828</td>
    </tr>
  </tbody>
</table>
</div>



## NOTE :
### The data set shows a strong positive correlation among review counts, checking counts and tip counts, These correlations suggest that user engagement across different platforms, such as reviews, tips and check insurance is interlinked, Higher activity in one area tends to be associated with higher activity others. Businesses should focus on strategies that boost all types of user investment as increases in one type of engagement are likely to drive increase in others. And hence, in overall visibility and interaction with customers.


```python
# Function to calculate the sucess score based on the avg rating and total review count.
def calculate_sucess_metric(df):
    sucess_score=[]
    for idx, row in df.iterrows():
        score = row['avg_rating'] * np.log(row['review_count'] + 1 )
        sucess_score.append(score)
    return sucess_score
```

# MAP Plot :

# Q. How do the sucess metrics (review_count or avg_rating) of restaurant vary across different states and cities?


```python
city_df = pd.read_sql(F""" 
SELECT
    city, 
    state, 
    latitude, 
    longitude, 
    AVG(stars) AS avg_rating, 
    SUM(review_count) AS review_count, 
    COUNT(*) AS restaurant_count 
FROM business 
WHERE business_id IN {tuple(business_Open_Restaurants['business_id'])} 
GROUP BY state, city, latitude, longitude
ORDER BY review_count DESC
LIMIT 10
""", engine)


```


```python
city_df = city_df.reset_index()
```


```python
city_df = city_df.drop('index',axis = 1)
```


```python
city_df['success_score'] = calculate_sucess_metric(city_df)
```


```python
city_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>city</th>
      <th>state</th>
      <th>latitude</th>
      <th>longitude</th>
      <th>avg_rating</th>
      <th>review_count</th>
      <th>restaurant_count</th>
      <th>success_score</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Philadelphia</td>
      <td>PA</td>
      <td>39.953159</td>
      <td>-75.159098</td>
      <td>4.000000</td>
      <td>541.0</td>
      <td>6</td>
      <td>25.181064</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Nashville</td>
      <td>TN</td>
      <td>36.163685</td>
      <td>-86.782598</td>
      <td>4.000000</td>
      <td>517.0</td>
      <td>3</td>
      <td>24.999901</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Carmel</td>
      <td>IN</td>
      <td>39.978599</td>
      <td>-86.128981</td>
      <td>4.166667</td>
      <td>503.0</td>
      <td>3</td>
      <td>25.927401</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Sparks</td>
      <td>NV</td>
      <td>39.541452</td>
      <td>-119.716242</td>
      <td>3.000000</td>
      <td>452.0</td>
      <td>4</td>
      <td>18.347676</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Hendersonville</td>
      <td>TN</td>
      <td>36.302820</td>
      <td>-86.619056</td>
      <td>4.375000</td>
      <td>431.0</td>
      <td>4</td>
      <td>26.549362</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Nashville</td>
      <td>TN</td>
      <td>36.170064</td>
      <td>-86.665561</td>
      <td>3.625000</td>
      <td>424.0</td>
      <td>4</td>
      <td>21.938823</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Nashville</td>
      <td>TN</td>
      <td>36.138603</td>
      <td>-86.800358</td>
      <td>4.000000</td>
      <td>417.0</td>
      <td>2</td>
      <td>24.141926</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Philadelphia</td>
      <td>PA</td>
      <td>39.958359</td>
      <td>-75.195393</td>
      <td>4.250000</td>
      <td>416.0</td>
      <td>6</td>
      <td>25.640616</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Indianapolis</td>
      <td>IN</td>
      <td>39.858230</td>
      <td>-85.978565</td>
      <td>4.250000</td>
      <td>411.0</td>
      <td>2</td>
      <td>25.589349</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Philadelphia</td>
      <td>PA</td>
      <td>39.949756</td>
      <td>-75.148062</td>
      <td>3.583333</td>
      <td>379.0</td>
      <td>12</td>
      <td>21.285614</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Create a base Map
m = folium.Map(location = [city_df['latitude'].mean(), city_df['longitude'].mean()], zoom_start = 4)

# Define a color scale
color_scale = folium.LinearColormap(colors=['green','yellow','#E54F29'], vmin = city_df['success_score'].min(), vmax = city_df['success_score'].max())

# Add markers to the map

for idx, row in city_df.iterrows():
    folium.CircleMarker(
        location = [row['latitude'], row['longitude']],
        radius = 5,
        color = color_scale(row['success_score']),
        fill = True,
        fill_color = color_scale(row['success_score']),
        fill_opacity = 0.7,
        popup=F"Success Score: {row ['success_score']}"
    ).add_to(m)

# Add color scale to the map

m.add_child(color_scale)




```




<div style="width:100%;"><div style="position:relative;width:100%;height:0;padding-bottom:60%;"><span style="color:#565656">Make this Notebook Trusted to load map: File -> Trust Notebook</span><iframe srcdoc="&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;

    &lt;meta http-equiv=&quot;content-type&quot; content=&quot;text/html; charset=UTF-8&quot; /&gt;

        &lt;script&gt;
            L_NO_TOUCH = false;
            L_DISABLE_3D = false;
        &lt;/script&gt;

    &lt;style&gt;html, body {width: 100%;height: 100%;margin: 0;padding: 0;}&lt;/style&gt;
    &lt;style&gt;#map {position:absolute;top:0;bottom:0;right:0;left:0;}&lt;/style&gt;
    &lt;script src=&quot;https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/leaflet.js&quot;&gt;&lt;/script&gt;
    &lt;script src=&quot;https://code.jquery.com/jquery-3.7.1.min.js&quot;&gt;&lt;/script&gt;
    &lt;script src=&quot;https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/js/bootstrap.bundle.min.js&quot;&gt;&lt;/script&gt;
    &lt;script src=&quot;https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.js&quot;&gt;&lt;/script&gt;
    &lt;link rel=&quot;stylesheet&quot; href=&quot;https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/leaflet.css&quot;/&gt;
    &lt;link rel=&quot;stylesheet&quot; href=&quot;https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css&quot;/&gt;
    &lt;link rel=&quot;stylesheet&quot; href=&quot;https://netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap-glyphicons.css&quot;/&gt;
    &lt;link rel=&quot;stylesheet&quot; href=&quot;https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.2.0/css/all.min.css&quot;/&gt;
    &lt;link rel=&quot;stylesheet&quot; href=&quot;https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.css&quot;/&gt;
    &lt;link rel=&quot;stylesheet&quot; href=&quot;https://cdn.jsdelivr.net/gh/python-visualization/folium/folium/templates/leaflet.awesome.rotate.min.css&quot;/&gt;

            &lt;meta name=&quot;viewport&quot; content=&quot;width=device-width,
                initial-scale=1.0, maximum-scale=1.0, user-scalable=no&quot; /&gt;
            &lt;style&gt;
                #map_e6d88feae9ea1b50db47dad246224236 {
                    position: relative;
                    width: 100.0%;
                    height: 100.0%;
                    left: 0.0%;
                    top: 0.0%;
                }
                .leaflet-container { font-size: 1rem; }
            &lt;/style&gt;

    &lt;script src=&quot;https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.5/d3.min.js&quot;&gt;&lt;/script&gt;
&lt;/head&gt;
&lt;body&gt;


            &lt;div class=&quot;folium-map&quot; id=&quot;map_e6d88feae9ea1b50db47dad246224236&quot; &gt;&lt;/div&gt;

&lt;/body&gt;
&lt;script&gt;


            var map_e6d88feae9ea1b50db47dad246224236 = L.map(
                &quot;map_e6d88feae9ea1b50db47dad246224236&quot;,
                {
                    center: [38.4014726, -86.41939162],
                    crs: L.CRS.EPSG3857,
                    zoom: 4,
                    zoomControl: true,
                    preferCanvas: false,
                }
            );





            var tile_layer_27037ffc382db7a3d024731f13623359 = L.tileLayer(
                &quot;https://tile.openstreetmap.org/{z}/{x}/{y}.png&quot;,
                {&quot;attribution&quot;: &quot;\u0026copy; \u003ca href=\&quot;https://www.openstreetmap.org/copyright\&quot;\u003eOpenStreetMap\u003c/a\u003e contributors&quot;, &quot;detectRetina&quot;: false, &quot;maxNativeZoom&quot;: 19, &quot;maxZoom&quot;: 19, &quot;minZoom&quot;: 0, &quot;noWrap&quot;: false, &quot;opacity&quot;: 1, &quot;subdomains&quot;: &quot;abc&quot;, &quot;tms&quot;: false}
            );


            tile_layer_27037ffc382db7a3d024731f13623359.addTo(map_e6d88feae9ea1b50db47dad246224236);


            var circle_marker_cc90156dd422ead794d209f64b92b7bd = L.circleMarker(
                [39.9531593, -75.1590984],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;#ee8a1bff&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#ee8a1bff&quot;, &quot;fillOpacity&quot;: 0.7, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 5, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_e6d88feae9ea1b50db47dad246224236);


        var popup_fbd5e8e9e3139a19e0d6d6b094fa240f = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});



                var html_6e4d1c58701c4b7c770e954ddb3b20bf = $(`&lt;div id=&quot;html_6e4d1c58701c4b7c770e954ddb3b20bf&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Success Score: 25.181064005758586&lt;/div&gt;`)[0];
                popup_fbd5e8e9e3139a19e0d6d6b094fa240f.setContent(html_6e4d1c58701c4b7c770e954ddb3b20bf);



        circle_marker_cc90156dd422ead794d209f64b92b7bd.bindPopup(popup_fbd5e8e9e3139a19e0d6d6b094fa240f)
        ;




            var circle_marker_81394f5bd9be159b531b62b36a6dd5d1 = L.circleMarker(
                [36.163685, -86.7825982],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;#ef9219ff&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#ef9219ff&quot;, &quot;fillOpacity&quot;: 0.7, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 5, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_e6d88feae9ea1b50db47dad246224236);


        var popup_a87f1774c4e36dea8e3721e2ea760d18 = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});



                var html_e970282ca4f18f643cccd092a8d7cd1d = $(`&lt;div id=&quot;html_e970282ca4f18f643cccd092a8d7cd1d&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Success Score: 24.99990096903793&lt;/div&gt;`)[0];
                popup_a87f1774c4e36dea8e3721e2ea760d18.setContent(html_e970282ca4f18f643cccd092a8d7cd1d);



        circle_marker_81394f5bd9be159b531b62b36a6dd5d1.bindPopup(popup_a87f1774c4e36dea8e3721e2ea760d18)
        ;




            var circle_marker_cdf6267457914a4938d0591c9c833b37 = L.circleMarker(
                [39.9785986, -86.1289815],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;#e96a22ff&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#e96a22ff&quot;, &quot;fillOpacity&quot;: 0.7, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 5, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_e6d88feae9ea1b50db47dad246224236);


        var popup_b0137b4827d97b08c9f9a93a59dad2bb = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});



                var html_cd8e6bef7bcf2a2dd2b0c301d255d37a = $(`&lt;div id=&quot;html_cd8e6bef7bcf2a2dd2b0c301d255d37a&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Success Score: 25.927401116964038&lt;/div&gt;`)[0];
                popup_b0137b4827d97b08c9f9a93a59dad2bb.setContent(html_cd8e6bef7bcf2a2dd2b0c301d255d37a);



        circle_marker_cdf6267457914a4938d0591c9c833b37.bindPopup(popup_b0137b4827d97b08c9f9a93a59dad2bb)
        ;




            var circle_marker_d5777477a12b2f43c5fd77c92c704dde = L.circleMarker(
                [39.5414516, -119.716242],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;#008000ff&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#008000ff&quot;, &quot;fillOpacity&quot;: 0.7, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 5, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_e6d88feae9ea1b50db47dad246224236);


        var popup_b7f22057f4de6b2261abff355702dc28 = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});



                var html_320cb755a8d7a6de1c2485fb2b8868a0 = $(`&lt;div id=&quot;html_320cb755a8d7a6de1c2485fb2b8868a0&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Success Score: 18.3476763764491&lt;/div&gt;`)[0];
                popup_b7f22057f4de6b2261abff355702dc28.setContent(html_320cb755a8d7a6de1c2485fb2b8868a0);



        circle_marker_d5777477a12b2f43c5fd77c92c704dde.bindPopup(popup_b7f22057f4de6b2261abff355702dc28)
        ;




            var circle_marker_11889ad1cbbc57562e561af98111091b = L.circleMarker(
                [36.30282, -86.619056],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;#e54f29ff&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#e54f29ff&quot;, &quot;fillOpacity&quot;: 0.7, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 5, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_e6d88feae9ea1b50db47dad246224236);


        var popup_9b09d431939359eec9a7075f2ac5a0c8 = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});



                var html_3d733be20c17393daad71355e6069b95 = $(`&lt;div id=&quot;html_3d733be20c17393daad71355e6069b95&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Success Score: 26.549361948567984&lt;/div&gt;`)[0];
                popup_9b09d431939359eec9a7075f2ac5a0c8.setContent(html_3d733be20c17393daad71355e6069b95);



        circle_marker_11889ad1cbbc57562e561af98111091b.bindPopup(popup_9b09d431939359eec9a7075f2ac5a0c8)
        ;




            var circle_marker_2193c293375fb8a7a4214d7a998f311e = L.circleMarker(
                [36.170064, -86.6655607],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;#e0f000ff&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#e0f000ff&quot;, &quot;fillOpacity&quot;: 0.7, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 5, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_e6d88feae9ea1b50db47dad246224236);


        var popup_4b554e504d16ad8898d1887a54ce171f = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});



                var html_dd85730731b81e429b8d10f31d634458 = $(`&lt;div id=&quot;html_dd85730731b81e429b8d10f31d634458&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Success Score: 21.938823237351013&lt;/div&gt;`)[0];
                popup_4b554e504d16ad8898d1887a54ce171f.setContent(html_dd85730731b81e429b8d10f31d634458);



        circle_marker_2193c293375fb8a7a4214d7a998f311e.bindPopup(popup_4b554e504d16ad8898d1887a54ce171f)
        ;




            var circle_marker_7abf00b0582aa92658adf5d272b3bef9 = L.circleMarker(
                [36.1386026, -86.8003583],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;#f5b710ff&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#f5b710ff&quot;, &quot;fillOpacity&quot;: 0.7, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 5, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_e6d88feae9ea1b50db47dad246224236);


        var popup_ab8cfa2ea1a153f6157657de2b07e283 = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});



                var html_0b82563d0497a45baaaad89b8f96ee78 = $(`&lt;div id=&quot;html_0b82563d0497a45baaaad89b8f96ee78&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Success Score: 24.141925730099025&lt;/div&gt;`)[0];
                popup_ab8cfa2ea1a153f6157657de2b07e283.setContent(html_0b82563d0497a45baaaad89b8f96ee78);



        circle_marker_7abf00b0582aa92658adf5d272b3bef9.bindPopup(popup_ab8cfa2ea1a153f6157657de2b07e283)
        ;




            var circle_marker_732f58c6c1f8b32249808cd717d57dfe = L.circleMarker(
                [39.9583587, -75.1953934],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;#eb7620ff&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#eb7620ff&quot;, &quot;fillOpacity&quot;: 0.7, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 5, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_e6d88feae9ea1b50db47dad246224236);


        var popup_443934dd2e88b4f5c7fcb4bc41a3da62 = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});



                var html_ca89f148449b434f7922623f7568aeda = $(`&lt;div id=&quot;html_ca89f148449b434f7922623f7568aeda&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Success Score: 25.640616442644905&lt;/div&gt;`)[0];
                popup_443934dd2e88b4f5c7fcb4bc41a3da62.setContent(html_ca89f148449b434f7922623f7568aeda);



        circle_marker_732f58c6c1f8b32249808cd717d57dfe.bindPopup(popup_443934dd2e88b4f5c7fcb4bc41a3da62)
        ;




            var circle_marker_d5520d0d38953b80ad47689c25fd9448 = L.circleMarker(
                [39.8582299, -85.9785654],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;#ec781fff&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#ec781fff&quot;, &quot;fillOpacity&quot;: 0.7, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 5, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_e6d88feae9ea1b50db47dad246224236);


        var popup_c0fbff852abb9476278c916d6eb24183 = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});



                var html_ce880625131beba1320e741bffb53a3f = $(`&lt;div id=&quot;html_ce880625131beba1320e741bffb53a3f&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Success Score: 25.589349234735487&lt;/div&gt;`)[0];
                popup_c0fbff852abb9476278c916d6eb24183.setContent(html_ce880625131beba1320e741bffb53a3f);



        circle_marker_d5520d0d38953b80ad47689c25fd9448.bindPopup(popup_c0fbff852abb9476278c916d6eb24183)
        ;




            var circle_marker_995fdc1f9ba7f2601eb0a70346844ee7 = L.circleMarker(
                [39.9497563, -75.1480623],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;#b7db00ff&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#b7db00ff&quot;, &quot;fillOpacity&quot;: 0.7, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 5, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_e6d88feae9ea1b50db47dad246224236);


        var popup_13e2f2ea4dc94f117a9fe37e5dcaca64 = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});



                var html_1a9e90bdc96c4e47956dc6bbb5c7cacb = $(`&lt;div id=&quot;html_1a9e90bdc96c4e47956dc6bbb5c7cacb&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Success Score: 21.285613655581546&lt;/div&gt;`)[0];
                popup_13e2f2ea4dc94f117a9fe37e5dcaca64.setContent(html_1a9e90bdc96c4e47956dc6bbb5c7cacb);



        circle_marker_995fdc1f9ba7f2601eb0a70346844ee7.bindPopup(popup_13e2f2ea4dc94f117a9fe37e5dcaca64)
        ;




    var color_map_f5be162352e84aea137419a2fcc7e4dc = {};


    color_map_f5be162352e84aea137419a2fcc7e4dc.color = d3.scale.threshold()
              .domain([18.3476763764491, 18.3641126200806, 18.380548863712104, 18.396985107343603, 18.413421350975103, 18.429857594606606, 18.446293838238105, 18.462730081869605, 18.479166325501108, 18.495602569132608, 18.512038812764107, 18.52847505639561, 18.54491130002711, 18.561347543658613, 18.577783787290112, 18.594220030921612, 18.610656274553115, 18.627092518184615, 18.643528761816114, 18.659965005447617, 18.676401249079117, 18.692837492710616, 18.70927373634212, 18.72570997997362, 18.74214622360512, 18.75858246723662, 18.77501871086812, 18.79145495449962, 18.807891198131124, 18.824327441762623, 18.840763685394123, 18.857199929025626, 18.873636172657125, 18.890072416288625, 18.906508659920128, 18.922944903551628, 18.939381147183127, 18.95581739081463, 18.97225363444613, 18.988689878077633, 19.005126121709132, 19.021562365340632, 19.037998608972135, 19.054434852603634, 19.070871096235134, 19.087307339866637, 19.103743583498137, 19.120179827129636, 19.13661607076114, 19.15305231439264, 19.16948855802414, 19.18592480165564, 19.20236104528714, 19.21879728891864, 19.235233532550144, 19.251669776181643, 19.268106019813143, 19.284542263444646, 19.300978507076145, 19.317414750707645, 19.333850994339148, 19.350287237970647, 19.36672348160215, 19.38315972523365, 19.39959596886515, 19.416032212496653, 19.432468456128152, 19.44890469975965, 19.465340943391155, 19.481777187022654, 19.498213430654154, 19.514649674285657, 19.531085917917157, 19.547522161548656, 19.56395840518016, 19.58039464881166, 19.59683089244316, 19.61326713607466, 19.62970337970616, 19.64613962333766, 19.662575866969163, 19.679012110600663, 19.695448354232163, 19.711884597863666, 19.728320841495165, 19.744757085126665, 19.761193328758168, 19.777629572389667, 19.794065816021167, 19.81050205965267, 19.82693830328417, 19.84337454691567, 19.859810790547172, 19.87624703417867, 19.892683277810175, 19.909119521441674, 19.925555765073174, 19.941992008704677, 19.958428252336176, 19.974864495967676, 19.99130073959918, 20.00773698323068, 20.024173226862178, 20.04060947049368, 20.05704571412518, 20.07348195775668, 20.089918201388183, 20.106354445019683, 20.122790688651182, 20.139226932282686, 20.155663175914185, 20.172099419545688, 20.188535663177188, 20.204971906808687, 20.22140815044019, 20.23784439407169, 20.25428063770319, 20.270716881334693, 20.287153124966192, 20.30358936859769, 20.320025612229195, 20.336461855860694, 20.352898099492194, 20.369334343123697, 20.385770586755196, 20.402206830386696, 20.4186430740182, 20.4350793176497, 20.451515561281198, 20.4679518049127, 20.4843880485442, 20.5008242921757, 20.517260535807203, 20.533696779438703, 20.550133023070202, 20.566569266701705, 20.583005510333205, 20.599441753964705, 20.615877997596208, 20.632314241227707, 20.64875048485921, 20.66518672849071, 20.68162297212221, 20.698059215753712, 20.714495459385212, 20.73093170301671, 20.74736794664821, 20.763804190279714, 20.780240433911214, 20.796676677542717, 20.813112921174216, 20.829549164805716, 20.84598540843722, 20.86242165206872, 20.878857895700218, 20.89529413933172, 20.91173038296322, 20.928166626594724, 20.944602870226223, 20.961039113857723, 20.977475357489226, 20.993911601120725, 21.010347844752225, 21.026784088383728, 21.043220332015228, 21.059656575646727, 21.07609281927823, 21.09252906290973, 21.10896530654123, 21.125401550172732, 21.141837793804232, 21.15827403743573, 21.174710281067235, 21.191146524698734, 21.207582768330234, 21.224019011961737, 21.240455255593236, 21.256891499224736, 21.27332774285624, 21.28976398648774, 21.306200230119238, 21.32263647375074, 21.33907271738224, 21.35550896101374, 21.371945204645243, 21.388381448276743, 21.404817691908242, 21.421253935539745, 21.437690179171245, 21.454126422802748, 21.470562666434247, 21.486998910065747, 21.50343515369725, 21.51987139732875, 21.53630764096025, 21.55274388459175, 21.569180128223252, 21.58561637185475, 21.602052615486254, 21.618488859117754, 21.634925102749254, 21.651361346380757, 21.667797590012256, 21.684233833643756, 21.70067007727526, 21.71710632090676, 21.73354256453826, 21.74997880816976, 21.76641505180126, 21.782851295432764, 21.799287539064263, 21.815723782695763, 21.832160026327266, 21.848596269958765, 21.865032513590265, 21.881468757221768, 21.897905000853267, 21.914341244484767, 21.93077748811627, 21.94721373174777, 21.96364997537927, 21.980086219010772, 21.99652246264227, 22.01295870627377, 22.029394949905274, 22.045831193536774, 22.062267437168273, 22.078703680799777, 22.095139924431276, 22.111576168062776, 22.12801241169428, 22.144448655325778, 22.160884898957278, 22.17732114258878, 22.19375738622028, 22.21019362985178, 22.226629873483283, 22.243066117114783, 22.259502360746286, 22.275938604377785, 22.292374848009285, 22.308811091640784, 22.325247335272287, 22.341683578903787, 22.358119822535286, 22.37455606616679, 22.39099230979829, 22.407428553429792, 22.42386479706129, 22.44030104069279, 22.456737284324294, 22.473173527955794, 22.489609771587293, 22.506046015218796, 22.522482258850296, 22.538918502481796, 22.5553547461133, 22.571790989744798, 22.588227233376298, 22.6046634770078, 22.6210997206393, 22.637535964270803, 22.653972207902303, 22.670408451533802, 22.686844695165306, 22.703280938796805, 22.719717182428305, 22.736153426059808, 22.752589669691307, 22.769025913322807, 22.78546215695431, 22.80189840058581, 22.81833464421731, 22.834770887848812, 22.85120713148031, 22.86764337511181, 22.884079618743314, 22.900515862374814, 22.916952106006313, 22.933388349637816, 22.949824593269316, 22.966260836900815, 22.98269708053232, 22.999133324163818, 23.015569567795318, 23.03200581142682, 23.04844205505832, 23.06487829868982, 23.081314542321323, 23.097750785952822, 23.114187029584322, 23.130623273215825, 23.147059516847325, 23.163495760478824, 23.179932004110327, 23.196368247741827, 23.212804491373326, 23.22924073500483, 23.24567697863633, 23.262113222267832, 23.27854946589933, 23.29498570953083, 23.311421953162334, 23.327858196793834, 23.344294440425333, 23.360730684056836, 23.377166927688336, 23.393603171319835, 23.41003941495134, 23.426475658582838, 23.44291190221434, 23.45934814584584, 23.47578438947734, 23.492220633108843, 23.508656876740343, 23.525093120371842, 23.541529364003345, 23.557965607634845, 23.574401851266344, 23.590838094897848, 23.607274338529347, 23.623710582160847, 23.64014682579235, 23.65658306942385, 23.67301931305535, 23.689455556686852, 23.70589180031835, 23.72232804394985, 23.738764287581354, 23.755200531212854, 23.771636774844353, 23.788073018475856, 23.804509262107356, 23.820945505738855, 23.83738174937036, 23.853817993001858, 23.870254236633357, 23.88669048026486, 23.90312672389636, 23.91956296752786, 23.935999211159363, 23.952435454790862, 23.96887169842236, 23.985307942053865, 24.001744185685364, 24.018180429316864, 24.034616672948367, 24.051052916579867, 24.06748916021137, 24.08392540384287, 24.10036164747437, 24.116797891105872, 24.13323413473737, 24.14967037836887, 24.166106622000374, 24.182542865631873, 24.198979109263373, 24.215415352894876, 24.231851596526376, 24.24828784015788, 24.26472408378938, 24.281160327420878, 24.29759657105238, 24.31403281468388, 24.33046905831538, 24.346905301946883, 24.363341545578383, 24.379777789209882, 24.396214032841385, 24.412650276472885, 24.429086520104384, 24.445522763735887, 24.461959007367387, 24.478395250998886, 24.49483149463039, 24.51126773826189, 24.52770398189339, 24.54414022552489, 24.56057646915639, 24.57701271278789, 24.593448956419394, 24.609885200050893, 24.626321443682393, 24.642757687313896, 24.659193930945396, 24.675630174576895, 24.692066418208398, 24.708502661839898, 24.724938905471397, 24.7413751491029, 24.7578113927344, 24.7742476363659, 24.790683879997403, 24.807120123628902, 24.8235563672604, 24.839992610891905, 24.856428854523404, 24.872865098154907, 24.889301341786407, 24.905737585417906, 24.92217382904941, 24.93861007268091, 24.95504631631241, 24.97148255994391, 24.98791880357541, 25.00435504720691, 25.020791290838414, 25.037227534469913, 25.053663778101416, 25.070100021732916, 25.086536265364415, 25.10297250899592, 25.119408752627418, 25.135844996258918, 25.15228123989042, 25.16871748352192, 25.18515372715342, 25.201589970784923, 25.218026214416422, 25.234462458047922, 25.250898701679425, 25.267334945310925, 25.283771188942424, 25.300207432573927, 25.316643676205427, 25.333079919836926, 25.34951616346843, 25.36595240709993, 25.38238865073143, 25.39882489436293, 25.41526113799443, 25.43169738162593, 25.448133625257434, 25.464569868888933, 25.481006112520433, 25.497442356151936, 25.513878599783435, 25.530314843414935, 25.546751087046438, 25.563187330677938, 25.579623574309437, 25.59605981794094, 25.61249606157244, 25.62893230520394, 25.645368548835442, 25.661804792466942, 25.678241036098445, 25.694677279729945, 25.711113523361444, 25.727549766992947, 25.743986010624447, 25.760422254255946, 25.77685849788745, 25.79329474151895, 25.80973098515045, 25.82616722878195, 25.84260347241345, 25.859039716044954, 25.875475959676454, 25.891912203307953, 25.908348446939456, 25.924784690570956, 25.941220934202455, 25.95765717783396, 25.974093421465458, 25.990529665096958, 26.00696590872846, 26.02340215235996, 26.03983839599146, 26.056274639622963, 26.072710883254462, 26.089147126885962, 26.105583370517465, 26.122019614148964, 26.138455857780464, 26.154892101411967, 26.171328345043467, 26.187764588674966, 26.20420083230647, 26.22063707593797, 26.23707331956947, 26.25350956320097, 26.26994580683247, 26.28638205046397, 26.302818294095474, 26.319254537726973, 26.335690781358473, 26.352127024989976, 26.368563268621475, 26.384999512252975, 26.401435755884478, 26.41787199951598, 26.434308243147477, 26.45074448677898, 26.467180730410483, 26.48361697404198, 26.500053217673482, 26.516489461304985, 26.53292570493648, 26.549361948567984])
              .range([&#x27;#008000ff&#x27;, &#x27;#018100ff&#x27;, &#x27;#028100ff&#x27;, &#x27;#038200ff&#x27;, &#x27;#048200ff&#x27;, &#x27;#058300ff&#x27;, &#x27;#068300ff&#x27;, &#x27;#078400ff&#x27;, &#x27;#088400ff&#x27;, &#x27;#098500ff&#x27;, &#x27;#0a8500ff&#x27;, &#x27;#0b8600ff&#x27;, &#x27;#0c8600ff&#x27;, &#x27;#0d8700ff&#x27;, &#x27;#0e8700ff&#x27;, &#x27;#0f8800ff&#x27;, &#x27;#108800ff&#x27;, &#x27;#118900ff&#x27;, &#x27;#128900ff&#x27;, &#x27;#138a00ff&#x27;, &#x27;#148a00ff&#x27;, &#x27;#158b00ff&#x27;, &#x27;#168b00ff&#x27;, &#x27;#178c00ff&#x27;, &#x27;#188c00ff&#x27;, &#x27;#198d00ff&#x27;, &#x27;#1a8d00ff&#x27;, &#x27;#1b8e00ff&#x27;, &#x27;#1c8e00ff&#x27;, &#x27;#1d8f00ff&#x27;, &#x27;#1e8f00ff&#x27;, &#x27;#1f9000ff&#x27;, &#x27;#209000ff&#x27;, &#x27;#219100ff&#x27;, &#x27;#229100ff&#x27;, &#x27;#239200ff&#x27;, &#x27;#249200ff&#x27;, &#x27;#259300ff&#x27;, &#x27;#269300ff&#x27;, &#x27;#289400ff&#x27;, &#x27;#299400ff&#x27;, &#x27;#2a9500ff&#x27;, &#x27;#2b9500ff&#x27;, &#x27;#2c9600ff&#x27;, &#x27;#2d9600ff&#x27;, &#x27;#2e9700ff&#x27;, &#x27;#2f9800ff&#x27;, &#x27;#309800ff&#x27;, &#x27;#319900ff&#x27;, &#x27;#329900ff&#x27;, &#x27;#339a00ff&#x27;, &#x27;#349a00ff&#x27;, &#x27;#359b00ff&#x27;, &#x27;#369b00ff&#x27;, &#x27;#379c00ff&#x27;, &#x27;#389c00ff&#x27;, &#x27;#399d00ff&#x27;, &#x27;#3a9d00ff&#x27;, &#x27;#3b9e00ff&#x27;, &#x27;#3c9e00ff&#x27;, &#x27;#3d9f00ff&#x27;, &#x27;#3e9f00ff&#x27;, &#x27;#3fa000ff&#x27;, &#x27;#40a000ff&#x27;, &#x27;#41a100ff&#x27;, &#x27;#42a100ff&#x27;, &#x27;#43a200ff&#x27;, &#x27;#44a200ff&#x27;, &#x27;#45a300ff&#x27;, &#x27;#46a300ff&#x27;, &#x27;#47a400ff&#x27;, &#x27;#48a400ff&#x27;, &#x27;#49a500ff&#x27;, &#x27;#4aa500ff&#x27;, &#x27;#4ba600ff&#x27;, &#x27;#4ca600ff&#x27;, &#x27;#4da700ff&#x27;, &#x27;#4fa700ff&#x27;, &#x27;#50a800ff&#x27;, &#x27;#51a800ff&#x27;, &#x27;#52a900ff&#x27;, &#x27;#53a900ff&#x27;, &#x27;#54aa00ff&#x27;, &#x27;#55aa00ff&#x27;, &#x27;#56ab00ff&#x27;, &#x27;#57ab00ff&#x27;, &#x27;#58ac00ff&#x27;, &#x27;#59ac00ff&#x27;, &#x27;#5aad00ff&#x27;, &#x27;#5bad00ff&#x27;, &#x27;#5cae00ff&#x27;, &#x27;#5daf00ff&#x27;, &#x27;#5eaf00ff&#x27;, &#x27;#5fb000ff&#x27;, &#x27;#60b000ff&#x27;, &#x27;#61b100ff&#x27;, &#x27;#62b100ff&#x27;, &#x27;#63b200ff&#x27;, &#x27;#64b200ff&#x27;, &#x27;#65b300ff&#x27;, &#x27;#66b300ff&#x27;, &#x27;#67b400ff&#x27;, &#x27;#68b400ff&#x27;, &#x27;#69b500ff&#x27;, &#x27;#6ab500ff&#x27;, &#x27;#6bb600ff&#x27;, &#x27;#6cb600ff&#x27;, &#x27;#6db700ff&#x27;, &#x27;#6eb700ff&#x27;, &#x27;#6fb800ff&#x27;, &#x27;#70b800ff&#x27;, &#x27;#71b900ff&#x27;, &#x27;#72b900ff&#x27;, &#x27;#73ba00ff&#x27;, &#x27;#74ba00ff&#x27;, &#x27;#75bb00ff&#x27;, &#x27;#77bb00ff&#x27;, &#x27;#78bc00ff&#x27;, &#x27;#79bc00ff&#x27;, &#x27;#7abd00ff&#x27;, &#x27;#7bbd00ff&#x27;, &#x27;#7cbe00ff&#x27;, &#x27;#7dbe00ff&#x27;, &#x27;#7ebf00ff&#x27;, &#x27;#7fbf00ff&#x27;, &#x27;#80c000ff&#x27;, &#x27;#81c000ff&#x27;, &#x27;#82c100ff&#x27;, &#x27;#83c100ff&#x27;, &#x27;#84c200ff&#x27;, &#x27;#85c200ff&#x27;, &#x27;#86c300ff&#x27;, &#x27;#87c300ff&#x27;, &#x27;#88c400ff&#x27;, &#x27;#89c400ff&#x27;, &#x27;#8ac500ff&#x27;, &#x27;#8bc500ff&#x27;, &#x27;#8cc600ff&#x27;, &#x27;#8dc700ff&#x27;, &#x27;#8ec700ff&#x27;, &#x27;#8fc800ff&#x27;, &#x27;#90c800ff&#x27;, &#x27;#91c900ff&#x27;, &#x27;#92c900ff&#x27;, &#x27;#93ca00ff&#x27;, &#x27;#94ca00ff&#x27;, &#x27;#95cb00ff&#x27;, &#x27;#96cb00ff&#x27;, &#x27;#97cc00ff&#x27;, &#x27;#98cc00ff&#x27;, &#x27;#99cd00ff&#x27;, &#x27;#9acd00ff&#x27;, &#x27;#9bce00ff&#x27;, &#x27;#9cce00ff&#x27;, &#x27;#9ecf00ff&#x27;, &#x27;#9fcf00ff&#x27;, &#x27;#a0d000ff&#x27;, &#x27;#a1d000ff&#x27;, &#x27;#a2d100ff&#x27;, &#x27;#a3d100ff&#x27;, &#x27;#a4d200ff&#x27;, &#x27;#a5d200ff&#x27;, &#x27;#a6d300ff&#x27;, &#x27;#a7d300ff&#x27;, &#x27;#a8d400ff&#x27;, &#x27;#a9d400ff&#x27;, &#x27;#aad500ff&#x27;, &#x27;#abd500ff&#x27;, &#x27;#acd600ff&#x27;, &#x27;#add600ff&#x27;, &#x27;#aed700ff&#x27;, &#x27;#afd700ff&#x27;, &#x27;#b0d800ff&#x27;, &#x27;#b1d800ff&#x27;, &#x27;#b2d900ff&#x27;, &#x27;#b3d900ff&#x27;, &#x27;#b4da00ff&#x27;, &#x27;#b5da00ff&#x27;, &#x27;#b6db00ff&#x27;, &#x27;#b7db00ff&#x27;, &#x27;#b8dc00ff&#x27;, &#x27;#b9dc00ff&#x27;, &#x27;#badd00ff&#x27;, &#x27;#bbde00ff&#x27;, &#x27;#bcde00ff&#x27;, &#x27;#bddf00ff&#x27;, &#x27;#bedf00ff&#x27;, &#x27;#bfe000ff&#x27;, &#x27;#c0e000ff&#x27;, &#x27;#c1e100ff&#x27;, &#x27;#c2e100ff&#x27;, &#x27;#c3e200ff&#x27;, &#x27;#c5e200ff&#x27;, &#x27;#c6e300ff&#x27;, &#x27;#c7e300ff&#x27;, &#x27;#c8e400ff&#x27;, &#x27;#c9e400ff&#x27;, &#x27;#cae500ff&#x27;, &#x27;#cbe500ff&#x27;, &#x27;#cce600ff&#x27;, &#x27;#cde600ff&#x27;, &#x27;#cee700ff&#x27;, &#x27;#cfe700ff&#x27;, &#x27;#d0e800ff&#x27;, &#x27;#d1e800ff&#x27;, &#x27;#d2e900ff&#x27;, &#x27;#d3e900ff&#x27;, &#x27;#d4ea00ff&#x27;, &#x27;#d5ea00ff&#x27;, &#x27;#d6eb00ff&#x27;, &#x27;#d7eb00ff&#x27;, &#x27;#d8ec00ff&#x27;, &#x27;#d9ec00ff&#x27;, &#x27;#daed00ff&#x27;, &#x27;#dbed00ff&#x27;, &#x27;#dcee00ff&#x27;, &#x27;#ddee00ff&#x27;, &#x27;#deef00ff&#x27;, &#x27;#dfef00ff&#x27;, &#x27;#e0f000ff&#x27;, &#x27;#e1f000ff&#x27;, &#x27;#e2f100ff&#x27;, &#x27;#e3f100ff&#x27;, &#x27;#e4f200ff&#x27;, &#x27;#e5f200ff&#x27;, &#x27;#e6f300ff&#x27;, &#x27;#e7f300ff&#x27;, &#x27;#e8f400ff&#x27;, &#x27;#e9f500ff&#x27;, &#x27;#eaf500ff&#x27;, &#x27;#ebf600ff&#x27;, &#x27;#edf600ff&#x27;, &#x27;#eef700ff&#x27;, &#x27;#eff700ff&#x27;, &#x27;#f0f800ff&#x27;, &#x27;#f1f800ff&#x27;, &#x27;#f2f900ff&#x27;, &#x27;#f3f900ff&#x27;, &#x27;#f4fa00ff&#x27;, &#x27;#f5fa00ff&#x27;, &#x27;#f6fb00ff&#x27;, &#x27;#f7fb00ff&#x27;, &#x27;#f8fc00ff&#x27;, &#x27;#f9fc00ff&#x27;, &#x27;#fafd00ff&#x27;, &#x27;#fbfd00ff&#x27;, &#x27;#fcfe00ff&#x27;, &#x27;#fdfe00ff&#x27;, &#x27;#feff00ff&#x27;, &#x27;#ffff00ff&#x27;, &#x27;#ffff00ff&#x27;, &#x27;#fffe00ff&#x27;, &#x27;#fffe00ff&#x27;, &#x27;#fffd00ff&#x27;, &#x27;#fffc00ff&#x27;, &#x27;#fffc00ff&#x27;, &#x27;#fffb01ff&#x27;, &#x27;#fffa01ff&#x27;, &#x27;#fff901ff&#x27;, &#x27;#fff901ff&#x27;, &#x27;#fef801ff&#x27;, &#x27;#fef701ff&#x27;, &#x27;#fef702ff&#x27;, &#x27;#fef602ff&#x27;, &#x27;#fef502ff&#x27;, &#x27;#fef502ff&#x27;, &#x27;#fef402ff&#x27;, &#x27;#fef302ff&#x27;, &#x27;#fef203ff&#x27;, &#x27;#fdf203ff&#x27;, &#x27;#fdf103ff&#x27;, &#x27;#fdf003ff&#x27;, &#x27;#fdf003ff&#x27;, &#x27;#fdef03ff&#x27;, &#x27;#fdee04ff&#x27;, &#x27;#fded04ff&#x27;, &#x27;#fded04ff&#x27;, &#x27;#fdec04ff&#x27;, &#x27;#fdeb04ff&#x27;, &#x27;#fceb04ff&#x27;, &#x27;#fcea05ff&#x27;, &#x27;#fce905ff&#x27;, &#x27;#fce805ff&#x27;, &#x27;#fce805ff&#x27;, &#x27;#fce705ff&#x27;, &#x27;#fce605ff&#x27;, &#x27;#fce606ff&#x27;, &#x27;#fce506ff&#x27;, &#x27;#fbe406ff&#x27;, &#x27;#fbe406ff&#x27;, &#x27;#fbe306ff&#x27;, &#x27;#fbe206ff&#x27;, &#x27;#fbe107ff&#x27;, &#x27;#fbe107ff&#x27;, &#x27;#fbe007ff&#x27;, &#x27;#fbdf07ff&#x27;, &#x27;#fbdf07ff&#x27;, &#x27;#fbde07ff&#x27;, &#x27;#fadd08ff&#x27;, &#x27;#fadc08ff&#x27;, &#x27;#fadc08ff&#x27;, &#x27;#fadb08ff&#x27;, &#x27;#fada08ff&#x27;, &#x27;#fada08ff&#x27;, &#x27;#fad908ff&#x27;, &#x27;#fad809ff&#x27;, &#x27;#fad709ff&#x27;, &#x27;#f9d709ff&#x27;, &#x27;#f9d609ff&#x27;, &#x27;#f9d509ff&#x27;, &#x27;#f9d509ff&#x27;, &#x27;#f9d40aff&#x27;, &#x27;#f9d30aff&#x27;, &#x27;#f9d30aff&#x27;, &#x27;#f9d20aff&#x27;, &#x27;#f9d10aff&#x27;, &#x27;#f9d00aff&#x27;, &#x27;#f8d00bff&#x27;, &#x27;#f8cf0bff&#x27;, &#x27;#f8ce0bff&#x27;, &#x27;#f8ce0bff&#x27;, &#x27;#f8cd0bff&#x27;, &#x27;#f8cc0bff&#x27;, &#x27;#f8cb0cff&#x27;, &#x27;#f8cb0cff&#x27;, &#x27;#f8ca0cff&#x27;, &#x27;#f7c90cff&#x27;, &#x27;#f7c90cff&#x27;, &#x27;#f7c80cff&#x27;, &#x27;#f7c70dff&#x27;, &#x27;#f7c60dff&#x27;, &#x27;#f7c60dff&#x27;, &#x27;#f7c50dff&#x27;, &#x27;#f7c40dff&#x27;, &#x27;#f7c40dff&#x27;, &#x27;#f7c30eff&#x27;, &#x27;#f6c20eff&#x27;, &#x27;#f6c20eff&#x27;, &#x27;#f6c10eff&#x27;, &#x27;#f6c00eff&#x27;, &#x27;#f6bf0eff&#x27;, &#x27;#f6bf0fff&#x27;, &#x27;#f6be0fff&#x27;, &#x27;#f6bd0fff&#x27;, &#x27;#f6bd0fff&#x27;, &#x27;#f6bc0fff&#x27;, &#x27;#f5bb0fff&#x27;, &#x27;#f5ba10ff&#x27;, &#x27;#f5ba10ff&#x27;, &#x27;#f5b910ff&#x27;, &#x27;#f5b810ff&#x27;, &#x27;#f5b810ff&#x27;, &#x27;#f5b710ff&#x27;, &#x27;#f5b611ff&#x27;, &#x27;#f5b511ff&#x27;, &#x27;#f4b511ff&#x27;, &#x27;#f4b411ff&#x27;, &#x27;#f4b311ff&#x27;, &#x27;#f4b311ff&#x27;, &#x27;#f4b212ff&#x27;, &#x27;#f4b112ff&#x27;, &#x27;#f4b112ff&#x27;, &#x27;#f4b012ff&#x27;, &#x27;#f4af12ff&#x27;, &#x27;#f4ae12ff&#x27;, &#x27;#f3ae13ff&#x27;, &#x27;#f3ad13ff&#x27;, &#x27;#f3ac13ff&#x27;, &#x27;#f3ac13ff&#x27;, &#x27;#f3ab13ff&#x27;, &#x27;#f3aa13ff&#x27;, &#x27;#f3a914ff&#x27;, &#x27;#f3a914ff&#x27;, &#x27;#f3a814ff&#x27;, &#x27;#f2a714ff&#x27;, &#x27;#f2a714ff&#x27;, &#x27;#f2a614ff&#x27;, &#x27;#f2a515ff&#x27;, &#x27;#f2a415ff&#x27;, &#x27;#f2a415ff&#x27;, &#x27;#f2a315ff&#x27;, &#x27;#f2a215ff&#x27;, &#x27;#f2a215ff&#x27;, &#x27;#f2a116ff&#x27;, &#x27;#f1a016ff&#x27;, &#x27;#f1a016ff&#x27;, &#x27;#f19f16ff&#x27;, &#x27;#f19e16ff&#x27;, &#x27;#f19d16ff&#x27;, &#x27;#f19d17ff&#x27;, &#x27;#f19c17ff&#x27;, &#x27;#f19b17ff&#x27;, &#x27;#f19b17ff&#x27;, &#x27;#f09a17ff&#x27;, &#x27;#f09917ff&#x27;, &#x27;#f09818ff&#x27;, &#x27;#f09818ff&#x27;, &#x27;#f09718ff&#x27;, &#x27;#f09618ff&#x27;, &#x27;#f09618ff&#x27;, &#x27;#f09518ff&#x27;, &#x27;#f09418ff&#x27;, &#x27;#f09419ff&#x27;, &#x27;#ef9319ff&#x27;, &#x27;#ef9219ff&#x27;, &#x27;#ef9119ff&#x27;, &#x27;#ef9119ff&#x27;, &#x27;#ef9019ff&#x27;, &#x27;#ef8f1aff&#x27;, &#x27;#ef8f1aff&#x27;, &#x27;#ef8e1aff&#x27;, &#x27;#ef8d1aff&#x27;, &#x27;#ee8c1aff&#x27;, &#x27;#ee8c1aff&#x27;, &#x27;#ee8b1bff&#x27;, &#x27;#ee8a1bff&#x27;, &#x27;#ee8a1bff&#x27;, &#x27;#ee891bff&#x27;, &#x27;#ee881bff&#x27;, &#x27;#ee871bff&#x27;, &#x27;#ee871cff&#x27;, &#x27;#ee861cff&#x27;, &#x27;#ed851cff&#x27;, &#x27;#ed851cff&#x27;, &#x27;#ed841cff&#x27;, &#x27;#ed831cff&#x27;, &#x27;#ed831dff&#x27;, &#x27;#ed821dff&#x27;, &#x27;#ed811dff&#x27;, &#x27;#ed801dff&#x27;, &#x27;#ed801dff&#x27;, &#x27;#ed7f1dff&#x27;, &#x27;#ec7e1eff&#x27;, &#x27;#ec7e1eff&#x27;, &#x27;#ec7d1eff&#x27;, &#x27;#ec7c1eff&#x27;, &#x27;#ec7b1eff&#x27;, &#x27;#ec7b1eff&#x27;, &#x27;#ec7a1fff&#x27;, &#x27;#ec791fff&#x27;, &#x27;#ec791fff&#x27;, &#x27;#eb781fff&#x27;, &#x27;#eb771fff&#x27;, &#x27;#eb761fff&#x27;, &#x27;#eb7620ff&#x27;, &#x27;#eb7520ff&#x27;, &#x27;#eb7420ff&#x27;, &#x27;#eb7420ff&#x27;, &#x27;#eb7320ff&#x27;, &#x27;#eb7220ff&#x27;, &#x27;#eb7221ff&#x27;, &#x27;#ea7121ff&#x27;, &#x27;#ea7021ff&#x27;, &#x27;#ea6f21ff&#x27;, &#x27;#ea6f21ff&#x27;, &#x27;#ea6e21ff&#x27;, &#x27;#ea6d22ff&#x27;, &#x27;#ea6d22ff&#x27;, &#x27;#ea6c22ff&#x27;, &#x27;#ea6b22ff&#x27;, &#x27;#e96a22ff&#x27;, &#x27;#e96a22ff&#x27;, &#x27;#e96923ff&#x27;, &#x27;#e96823ff&#x27;, &#x27;#e96823ff&#x27;, &#x27;#e96723ff&#x27;, &#x27;#e96623ff&#x27;, &#x27;#e96523ff&#x27;, &#x27;#e96524ff&#x27;, &#x27;#e96424ff&#x27;, &#x27;#e86324ff&#x27;, &#x27;#e86324ff&#x27;, &#x27;#e86224ff&#x27;, &#x27;#e86124ff&#x27;, &#x27;#e86125ff&#x27;, &#x27;#e86025ff&#x27;, &#x27;#e85f25ff&#x27;, &#x27;#e85e25ff&#x27;, &#x27;#e85e25ff&#x27;, &#x27;#e75d25ff&#x27;, &#x27;#e75c26ff&#x27;, &#x27;#e75c26ff&#x27;, &#x27;#e75b26ff&#x27;, &#x27;#e75a26ff&#x27;, &#x27;#e75926ff&#x27;, &#x27;#e75926ff&#x27;, &#x27;#e75827ff&#x27;, &#x27;#e75727ff&#x27;, &#x27;#e75727ff&#x27;, &#x27;#e65627ff&#x27;, &#x27;#e65527ff&#x27;, &#x27;#e65427ff&#x27;, &#x27;#e65428ff&#x27;, &#x27;#e65328ff&#x27;, &#x27;#e65228ff&#x27;, &#x27;#e65228ff&#x27;, &#x27;#e65128ff&#x27;, &#x27;#e65028ff&#x27;, &#x27;#e65028ff&#x27;, &#x27;#e54f29ff&#x27;]);


    color_map_f5be162352e84aea137419a2fcc7e4dc.x = d3.scale.linear()
              .domain([18.3476763764491, 26.549361948567984])
              .range([0, 450 - 50]);

    color_map_f5be162352e84aea137419a2fcc7e4dc.legend = L.control({position: &#x27;topright&#x27;});
    color_map_f5be162352e84aea137419a2fcc7e4dc.legend.onAdd = function (map) {var div = L.DomUtil.create(&#x27;div&#x27;, &#x27;legend&#x27;); return div};
    color_map_f5be162352e84aea137419a2fcc7e4dc.legend.addTo(map_e6d88feae9ea1b50db47dad246224236);

    color_map_f5be162352e84aea137419a2fcc7e4dc.xAxis = d3.svg.axis()
        .scale(color_map_f5be162352e84aea137419a2fcc7e4dc.x)
        .orient(&quot;top&quot;)
        .tickSize(1)
        .tickValues([18.3476763764491, 22.448519162508543, 26.549361948567984]);

    color_map_f5be162352e84aea137419a2fcc7e4dc.svg = d3.select(&quot;.legend.leaflet-control&quot;).append(&quot;svg&quot;)
        .attr(&quot;id&quot;, &#x27;legend&#x27;)
        .attr(&quot;width&quot;, 450)
        .attr(&quot;height&quot;, 40);

    color_map_f5be162352e84aea137419a2fcc7e4dc.g = color_map_f5be162352e84aea137419a2fcc7e4dc.svg.append(&quot;g&quot;)
        .attr(&quot;class&quot;, &quot;key&quot;)
        .attr(&quot;fill&quot;, &quot;black&quot;)
        .attr(&quot;transform&quot;, &quot;translate(25,16)&quot;);

    color_map_f5be162352e84aea137419a2fcc7e4dc.g.selectAll(&quot;rect&quot;)
        .data(color_map_f5be162352e84aea137419a2fcc7e4dc.color.range().map(function(d, i) {
          return {
            x0: i ? color_map_f5be162352e84aea137419a2fcc7e4dc.x(color_map_f5be162352e84aea137419a2fcc7e4dc.color.domain()[i - 1]) : color_map_f5be162352e84aea137419a2fcc7e4dc.x.range()[0],
            x1: i &lt; color_map_f5be162352e84aea137419a2fcc7e4dc.color.domain().length ? color_map_f5be162352e84aea137419a2fcc7e4dc.x(color_map_f5be162352e84aea137419a2fcc7e4dc.color.domain()[i]) : color_map_f5be162352e84aea137419a2fcc7e4dc.x.range()[1],
            z: d
          };
        }))
      .enter().append(&quot;rect&quot;)
        .attr(&quot;height&quot;, 40 - 30)
        .attr(&quot;x&quot;, function(d) { return d.x0; })
        .attr(&quot;width&quot;, function(d) { return d.x1 - d.x0; })
        .style(&quot;fill&quot;, function(d) { return d.z; });

    color_map_f5be162352e84aea137419a2fcc7e4dc.g.call(color_map_f5be162352e84aea137419a2fcc7e4dc.xAxis).append(&quot;text&quot;)
        .attr(&quot;class&quot;, &quot;caption&quot;)
        .attr(&quot;y&quot;, 21)
        .attr(&quot;fill&quot;, &quot;black&quot;)
        .text(&quot;&quot;);
&lt;/script&gt;
&lt;/html&gt;" style="position:absolute;width:100%;height:100%;left:0;top:0;border:none !important;" allowfullscreen webkitallowfullscreen mozallowfullscreen></iframe></div></div>



## NOTE :
### Philadelphia emerges as the top city with the highest success code, indicating a combination of high ratings and active user engagements. following Philadelphia, Tampa, Indianapolis and tucson rank among the top cities with significant success score, suggesting thriving restaurant success in these areas. The success matrix vary significantly across different state and cities, highlighting regional differences in dining Preferences, culinary sceneries and customer engagement levels, identifying city with the highest success score present opportunities for Restaurant chains to Expend or invest further while areas with low score may require targeted efforts to improve rating and increase user engagement. 

# Time :

# Q. Are there any patterns in the user engagement over time for sucessfull business compared to less sucessfull ones, Are there any seasonal trends in the user engagement for restaurant ?


```python
high_rated_engagement = pd.read_sql_query(f"""
SELECT review.month_year, review.review_count, tip.tip_count FROM
(SELECT DATE_FORMAT(date, '%m-%Y') AS month_year, COUNT(*) AS review_count
FROM review
WHERE business_id IN {tuple(business_Open_Restaurants['business_id'])} AND stars >= 3.5
GROUP BY month_year
ORDER BY month_year) AS review
JOIN
(SELECT AVG(b.stars) AS avg_stars, DATE_FORMAT(tip.date, '%m-%Y') AS month_year, COUNT(*) AS tip_count
FROM tip
JOIN business AS b
ON tip.business_id = b.business_id
WHERE tip.business_id IN {tuple(business_Open_Restaurants['business_id'])} AND b.stars >= 3.5
GROUP BY month_year
ORDER BY month_year) AS tip
ON review.month_year = tip.month_year
;""", engine)

low_rated_engagement = pd.read_sql_query(f"""
SELECT review.month_year, review.review_count, tip.tip_count FROM
(SELECT DATE_FORMAT(date, '%m-%Y') AS month_year, COUNT(*) AS review_count
FROM review
WHERE business_id IN {tuple(business_Open_Restaurants['business_id'])} AND stars < 3.5
GROUP BY month_year
ORDER BY month_year) AS review
JOIN
(SELECT AVG(b.stars) AS avg_stars, DATE_FORMAT(tip.date, '%m-%Y') AS month_year, COUNT(*) AS tip_count
FROM tip
JOIN business AS b
ON tip.business_id = b.business_id
WHERE tip.business_id IN {tuple(business_Open_Restaurants['business_id'])} AND b.stars < 3.5
GROUP BY month_year
ORDER BY month_year) AS tip
ON review.month_year = tip.month_year
;""", engine)


```


```python
high_rated_engagement
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>month_year</th>
      <th>review_count</th>
      <th>tip_count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>01-2010</td>
      <td>1218</td>
      <td>79</td>
    </tr>
    <tr>
      <th>1</th>
      <td>01-2011</td>
      <td>2171</td>
      <td>621</td>
    </tr>
    <tr>
      <th>2</th>
      <td>01-2012</td>
      <td>3086</td>
      <td>1321</td>
    </tr>
    <tr>
      <th>3</th>
      <td>01-2013</td>
      <td>3801</td>
      <td>1230</td>
    </tr>
    <tr>
      <th>4</th>
      <td>01-2014</td>
      <td>4973</td>
      <td>1357</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>149</th>
      <td>12-2017</td>
      <td>10161</td>
      <td>1477</td>
    </tr>
    <tr>
      <th>150</th>
      <td>12-2018</td>
      <td>12870</td>
      <td>1163</td>
    </tr>
    <tr>
      <th>151</th>
      <td>12-2019</td>
      <td>13756</td>
      <td>1161</td>
    </tr>
    <tr>
      <th>152</th>
      <td>12-2020</td>
      <td>11294</td>
      <td>937</td>
    </tr>
    <tr>
      <th>153</th>
      <td>12-2021</td>
      <td>12652</td>
      <td>652</td>
    </tr>
  </tbody>
</table>
<p>154 rows × 3 columns</p>
</div>




```python
low_rated_engagement
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>month_year</th>
      <th>review_count</th>
      <th>tip_count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>01-2010</td>
      <td>613</td>
      <td>25</td>
    </tr>
    <tr>
      <th>1</th>
      <td>01-2011</td>
      <td>1103</td>
      <td>297</td>
    </tr>
    <tr>
      <th>2</th>
      <td>01-2012</td>
      <td>1748</td>
      <td>538</td>
    </tr>
    <tr>
      <th>3</th>
      <td>01-2013</td>
      <td>2196</td>
      <td>548</td>
    </tr>
    <tr>
      <th>4</th>
      <td>01-2014</td>
      <td>2769</td>
      <td>607</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>149</th>
      <td>12-2017</td>
      <td>5970</td>
      <td>441</td>
    </tr>
    <tr>
      <th>150</th>
      <td>12-2018</td>
      <td>7574</td>
      <td>338</td>
    </tr>
    <tr>
      <th>151</th>
      <td>12-2019</td>
      <td>7591</td>
      <td>275</td>
    </tr>
    <tr>
      <th>152</th>
      <td>12-2020</td>
      <td>5014</td>
      <td>148</td>
    </tr>
    <tr>
      <th>153</th>
      <td>12-2021</td>
      <td>6937</td>
      <td>122</td>
    </tr>
  </tbody>
</table>
<p>154 rows × 3 columns</p>
</div>




```python
time_rating = pd.read_sql(f"""
SELECT DATE_FORMAT(date, '%m-%Y') AS month_year, AVG(stars) AS avg_rating
FROM review
WHERE business_id IN {tuple(business_Open_Restaurants['business_id'])}
GROUP BY month_year
ORDER BY month_year;
""", engine)

```


```python
time_rating
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>month_year</th>
      <th>avg_rating</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>01-2006</td>
      <td>4.000000</td>
    </tr>
    <tr>
      <th>1</th>
      <td>01-2007</td>
      <td>3.897436</td>
    </tr>
    <tr>
      <th>2</th>
      <td>01-2008</td>
      <td>3.603960</td>
    </tr>
    <tr>
      <th>3</th>
      <td>01-2009</td>
      <td>3.690661</td>
    </tr>
    <tr>
      <th>4</th>
      <td>01-2010</td>
      <td>3.724194</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>198</th>
      <td>12-2017</td>
      <td>3.613415</td>
    </tr>
    <tr>
      <th>199</th>
      <td>12-2018</td>
      <td>3.608687</td>
    </tr>
    <tr>
      <th>200</th>
      <td>12-2019</td>
      <td>3.665246</td>
    </tr>
    <tr>
      <th>201</th>
      <td>12-2020</td>
      <td>3.833701</td>
    </tr>
    <tr>
      <th>202</th>
      <td>12-2021</td>
      <td>3.672673</td>
    </tr>
  </tbody>
</table>
<p>203 rows × 2 columns</p>
</div>




```python
# time_rating
time_rating['month_year'] = pd.to_datetime(time_rating['month_year'])
time_rating.sort_values('month_year',inplace= True)
time_rating = time_rating[time_rating['month_year']>'2017']

# high_rated_engagement
high_rated_engagement['month_year'] = pd.to_datetime(high_rated_engagement['month_year'])
high_rated_engagement.sort_values('month_year',inplace=True)
high_rated_engagement = high_rated_engagement[high_rated_engagement['month_year']>'2017']

# low_rated_engagement 
low_rated_engagement['month_year'] =  pd.to_datetime(low_rated_engagement['month_year'])
low_rated_engagement.sort_values('month_year',inplace=True)
low_rated_engagement = low_rated_engagement[low_rated_engagement['month_year']>'2017']

```


```python
# Creating a col called avg_rating in high_rated_engagement
high_rated_engagement['avg_rating'] = time_rating['avg_rating'].values
```


```python
# ploting the time trends
plt.figure(figsize=(20, 15))
plt.subplot(3,1,1)
plt.title('Tip Engagement Over Time')
plt.plot(high_rated_engagement['month_year'], high_rated_engagement['tip_count'], label = 'High Rated', color = 'RED')
plt.plot(low_rated_engagement['month_year'], low_rated_engagement['tip_count'], label = 'Low Rated', color = 'BLUE')
plt.legend()

plt.subplot(3,1,2)
plt.title('Review Engagement Over Time')
plt.plot(high_rated_engagement['month_year'], high_rated_engagement['review_count'], label = 'High Rated', color = 'RED')
plt.plot(low_rated_engagement['month_year'], low_rated_engagement['review_count'], label = 'Low Rated', color = 'BLUE')
plt.legend()

plt.subplot(3,1,3)
plt.title('Avg Rating Over Time')
plt.plot(time_rating['month_year'], time_rating['avg_rating'], color = 'ORANGE')
plt.tight_layout()
plt.show()

```


    
![png](main_files/main_72_0.png)
    



```python
tip_high_rated = high_rated_engagement[['month_year','tip_count']].set_index('month_year')
review_high_rated = high_rated_engagement[['month_year', 'review_count']].set_index('month_year')
rating_df = time_rating[['month_year', 'avg_rating']].set_index('month_year')
```


```python
# seasonal_decompose of tip_high_rated
from statsmodels.tsa.seasonal import seasonal_decompose
multiplication_decompose = seasonal_decompose(tip_high_rated, model = 'multiplication', period = 12)
plt.rcParams.update({'figure.figsize':(16,12)})
multiplication_decompose.plot()
plt.show()
```


    
![png](main_files/main_74_0.png)
    



```python
# seasonal_decompose of  review_high_rated
from statsmodels.tsa.seasonal import seasonal_decompose
multiplication_decompose = seasonal_decompose(review_high_rated, model = 'multiplication', period = 12)
plt.rcParams.update({'figure.figsize':(16,12)})
multiplication_decompose.plot()
plt.show()


```


    
![png](main_files/main_75_0.png)
    


## NOTE : 
### Successful businesses, particularly those with higher ratings above 3.5 exhibit consistent and possibly increase user engagement overtime, High rated restaurants maintain a steady or blowing level of user management over time, reflecting ongoing customer interest and satisfaction, Keep count is showing a downward trend, whereas review count is showing an up on trend with time, Years starting at year ending from around November and March is highly engaging in seasonal. 

# Sentiment Analysis Using NLTK :

# Q. Retrive Top Five Restaurant with High Success Score And Sentiments Included ( Positive, Negetive & Neutral )


```python
# import nltk
# from nltk.sentiment import SentimentIntensityAnalyzer
# 
# # Create a sentiment col
# sentiment = review['text']
# 
# # Perform sentiment analysis using SentimentIntensityAnalyzer:
# 
# sia = SentimentIntensityAnalyzer()
# 
# # Define a function to get sentiment score
# def get_sentiment(comment):
#     score = sia.polarity_scores(comment)
#     return score['compound']  # compound score for overall sentiment
# 
# # Apply sentiment analysis to the 'comments' column
# sentiment_score = sentiment.apply(get_sentiment)
# sentiments = sentiment_score.apply(lambda x: 'Positive' if x > 0 else ('Negative' if x < 0 else 'Neutral'))
# 
# sentiments


```


```python
sentim = pd.read_csv('D:\\VSCODE\\SQL_PROJECT\\Senti.csv')
```


```python
senti = pd.concat([review[['business_id','text']], sentim], axis = 1)
```


```python
# Sentiments
senti
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>business_id</th>
      <th>text</th>
      <th>Unnamed: 0.1</th>
      <th>Unnamed: 0</th>
      <th>text</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>XQfwVwDr-v0ZS3_CbbE5Xw</td>
      <td>If you decide to eat here, just be aware it is...</td>
      <td>0</td>
      <td>0</td>
      <td>Positive</td>
    </tr>
    <tr>
      <th>1</th>
      <td>7ATYjTIgM3jUlt4UM3IypQ</td>
      <td>I've taken a lot of spin classes over the year...</td>
      <td>1</td>
      <td>1</td>
      <td>Positive</td>
    </tr>
    <tr>
      <th>2</th>
      <td>YjUWPpI6HXG530lwP-fb2A</td>
      <td>Family diner. Had the buffet. Eclectic assortm...</td>
      <td>2</td>
      <td>2</td>
      <td>Positive</td>
    </tr>
    <tr>
      <th>3</th>
      <td>kxX2SOes4o-D3ZQBkiMRfA</td>
      <td>Wow!  Yummy, different,  delicious.   Our favo...</td>
      <td>3</td>
      <td>3</td>
      <td>Positive</td>
    </tr>
    <tr>
      <th>4</th>
      <td>e4Vwtrqf-wpJfwesgvdgxQ</td>
      <td>Cute interior and owner (?) gave us tour of up...</td>
      <td>4</td>
      <td>4</td>
      <td>Positive</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>6990275</th>
      <td>jals67o91gcrD4DC81Vk6w</td>
      <td>Latest addition to services from ICCU is Apple...</td>
      <td>6990275</td>
      <td>6990275</td>
      <td>Negative</td>
    </tr>
    <tr>
      <th>6990276</th>
      <td>2vLksaMmSEcGbjI5gywpZA</td>
      <td>This spot offers a great, affordable east week...</td>
      <td>6990276</td>
      <td>6990276</td>
      <td>Positive</td>
    </tr>
    <tr>
      <th>6990277</th>
      <td>R1khUUxidqfaJmcpmGd4aw</td>
      <td>This Home Depot won me over when I needed to g...</td>
      <td>6990277</td>
      <td>6990277</td>
      <td>Positive</td>
    </tr>
    <tr>
      <th>6990278</th>
      <td>Rr9kKArrMhSLVE9a53q-aA</td>
      <td>For when I'm feeling like ignoring my calorie-...</td>
      <td>6990278</td>
      <td>6990278</td>
      <td>Positive</td>
    </tr>
    <tr>
      <th>6990279</th>
      <td>VAeEXLbEcI9Emt9KGYq9aA</td>
      <td>Located in the 'Walking District' in Nashville...</td>
      <td>6990279</td>
      <td>6990279</td>
      <td>Positive</td>
    </tr>
  </tbody>
</table>
<p>6990280 rows × 5 columns</p>
</div>




```python
business
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>business_id</th>
      <th>name</th>
      <th>address</th>
      <th>city</th>
      <th>state</th>
      <th>postal_code</th>
      <th>latitude</th>
      <th>longitude</th>
      <th>stars</th>
      <th>review_count</th>
      <th>is_open</th>
      <th>categories</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Pns2l4eNsfO8kk83dixA6A</td>
      <td>Abby Rappoport, LAC, CMQ</td>
      <td>1616 Chapala St, Ste 2</td>
      <td>Santa Barbara</td>
      <td>CA</td>
      <td>93101</td>
      <td>34.426679</td>
      <td>-119.711197</td>
      <td>5.0</td>
      <td>7</td>
      <td>0</td>
      <td>Doctors, Traditional Chinese Medicine, Naturop...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>mpf3x-BjTdTEA3yCZrAYPw</td>
      <td>The UPS Store</td>
      <td>87 Grasso Plaza Shopping Center</td>
      <td>Affton</td>
      <td>MO</td>
      <td>63123</td>
      <td>38.551126</td>
      <td>-90.335695</td>
      <td>3.0</td>
      <td>15</td>
      <td>1</td>
      <td>Shipping Centers, Local Services, Notaries, Ma...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>tUFrWirKiKi_TAnsVWINQQ</td>
      <td>Target</td>
      <td>5255 E Broadway Blvd</td>
      <td>Tucson</td>
      <td>AZ</td>
      <td>85711</td>
      <td>32.223236</td>
      <td>-110.880452</td>
      <td>3.5</td>
      <td>22</td>
      <td>0</td>
      <td>Department Stores, Shopping, Fashion, Home &amp; G...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>MTSW4McQd7CbVtyjqoe9mw</td>
      <td>St Honore Pastries</td>
      <td>935 Race St</td>
      <td>Philadelphia</td>
      <td>PA</td>
      <td>19107</td>
      <td>39.955505</td>
      <td>-75.155564</td>
      <td>4.0</td>
      <td>80</td>
      <td>1</td>
      <td>Restaurants, Food, Bubble Tea, Coffee &amp; Tea, B...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>mWMc6_wTdE0EUBKIGXDVfA</td>
      <td>Perkiomen Valley Brewery</td>
      <td>101 Walnut St</td>
      <td>Green Lane</td>
      <td>PA</td>
      <td>18054</td>
      <td>40.338183</td>
      <td>-75.471659</td>
      <td>4.5</td>
      <td>13</td>
      <td>1</td>
      <td>Brewpubs, Breweries, Food</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>150341</th>
      <td>IUQopTMmYQG-qRtBk-8QnA</td>
      <td>Binh's Nails</td>
      <td>3388 Gateway Blvd</td>
      <td>Edmonton</td>
      <td>AB</td>
      <td>T6J 5H2</td>
      <td>53.468419</td>
      <td>-113.492054</td>
      <td>3.0</td>
      <td>13</td>
      <td>1</td>
      <td>Nail Salons, Beauty &amp; Spas</td>
    </tr>
    <tr>
      <th>150342</th>
      <td>c8GjPIOTGVmIemT7j5_SyQ</td>
      <td>Wild Birds Unlimited</td>
      <td>2813 Bransford Ave</td>
      <td>Nashville</td>
      <td>TN</td>
      <td>37204</td>
      <td>36.115118</td>
      <td>-86.766925</td>
      <td>4.0</td>
      <td>5</td>
      <td>1</td>
      <td>Pets, Nurseries &amp; Gardening, Pet Stores, Hobby...</td>
    </tr>
    <tr>
      <th>150343</th>
      <td>_QAMST-NrQobXduilWEqSw</td>
      <td>Claire's Boutique</td>
      <td>6020 E 82nd St, Ste 46</td>
      <td>Indianapolis</td>
      <td>IN</td>
      <td>46250</td>
      <td>39.908707</td>
      <td>-86.065088</td>
      <td>3.5</td>
      <td>8</td>
      <td>1</td>
      <td>Shopping, Jewelry, Piercing, Toy Stores, Beaut...</td>
    </tr>
    <tr>
      <th>150344</th>
      <td>mtGm22y5c2UHNXDFAjaPNw</td>
      <td>Cyclery &amp; Fitness Center</td>
      <td>2472 Troy Rd</td>
      <td>Edwardsville</td>
      <td>IL</td>
      <td>62025</td>
      <td>38.782351</td>
      <td>-89.950558</td>
      <td>4.0</td>
      <td>24</td>
      <td>1</td>
      <td>Fitness/Exercise Equipment, Eyewear &amp; Optician...</td>
    </tr>
    <tr>
      <th>150345</th>
      <td>jV_XOycEzSlTx-65W906pg</td>
      <td>Sic Ink</td>
      <td>238 Apollo Beach Blvd</td>
      <td>Apollo beach</td>
      <td>FL</td>
      <td>33572</td>
      <td>27.771002</td>
      <td>-82.394910</td>
      <td>4.5</td>
      <td>9</td>
      <td>1</td>
      <td>Beauty &amp; Spas, Permanent Makeup, Piercing, Tattoo</td>
    </tr>
  </tbody>
</table>
<p>150346 rows × 12 columns</p>
</div>




```python
business_data = business[['business_id','name']]
senti = senti.iloc[:,[0,4]]

```


```python
senti
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>business_id</th>
      <th>text</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>XQfwVwDr-v0ZS3_CbbE5Xw</td>
      <td>Positive</td>
    </tr>
    <tr>
      <th>1</th>
      <td>7ATYjTIgM3jUlt4UM3IypQ</td>
      <td>Positive</td>
    </tr>
    <tr>
      <th>2</th>
      <td>YjUWPpI6HXG530lwP-fb2A</td>
      <td>Positive</td>
    </tr>
    <tr>
      <th>3</th>
      <td>kxX2SOes4o-D3ZQBkiMRfA</td>
      <td>Positive</td>
    </tr>
    <tr>
      <th>4</th>
      <td>e4Vwtrqf-wpJfwesgvdgxQ</td>
      <td>Positive</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>6990275</th>
      <td>jals67o91gcrD4DC81Vk6w</td>
      <td>Negative</td>
    </tr>
    <tr>
      <th>6990276</th>
      <td>2vLksaMmSEcGbjI5gywpZA</td>
      <td>Positive</td>
    </tr>
    <tr>
      <th>6990277</th>
      <td>R1khUUxidqfaJmcpmGd4aw</td>
      <td>Positive</td>
    </tr>
    <tr>
      <th>6990278</th>
      <td>Rr9kKArrMhSLVE9a53q-aA</td>
      <td>Positive</td>
    </tr>
    <tr>
      <th>6990279</th>
      <td>VAeEXLbEcI9Emt9KGYq9aA</td>
      <td>Positive</td>
    </tr>
  </tbody>
</table>
<p>6990280 rows × 2 columns</p>
</div>




```python
real_sentiments = pd.merge(business_data,senti, how='inner', on= ['business_id'])
```


```python
real_sentiments
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>business_id</th>
      <th>name</th>
      <th>text</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Pns2l4eNsfO8kk83dixA6A</td>
      <td>Abby Rappoport, LAC, CMQ</td>
      <td>Positive</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Pns2l4eNsfO8kk83dixA6A</td>
      <td>Abby Rappoport, LAC, CMQ</td>
      <td>Positive</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Pns2l4eNsfO8kk83dixA6A</td>
      <td>Abby Rappoport, LAC, CMQ</td>
      <td>Positive</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Pns2l4eNsfO8kk83dixA6A</td>
      <td>Abby Rappoport, LAC, CMQ</td>
      <td>Positive</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Pns2l4eNsfO8kk83dixA6A</td>
      <td>Abby Rappoport, LAC, CMQ</td>
      <td>Positive</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>6990275</th>
      <td>jV_XOycEzSlTx-65W906pg</td>
      <td>Sic Ink</td>
      <td>Positive</td>
    </tr>
    <tr>
      <th>6990276</th>
      <td>jV_XOycEzSlTx-65W906pg</td>
      <td>Sic Ink</td>
      <td>Positive</td>
    </tr>
    <tr>
      <th>6990277</th>
      <td>jV_XOycEzSlTx-65W906pg</td>
      <td>Sic Ink</td>
      <td>Positive</td>
    </tr>
    <tr>
      <th>6990278</th>
      <td>jV_XOycEzSlTx-65W906pg</td>
      <td>Sic Ink</td>
      <td>Positive</td>
    </tr>
    <tr>
      <th>6990279</th>
      <td>jV_XOycEzSlTx-65W906pg</td>
      <td>Sic Ink</td>
      <td>Negative</td>
    </tr>
  </tbody>
</table>
<p>6990280 rows × 3 columns</p>
</div>




```python
real_sentiments = real_sentiments.groupby(['business_id','name','text']).value_counts()
```


```python
real_sentiments_df = real_sentiments.reset_index()
```


```python
#Success_Business
success_business = pd.read_sql(F""" 
SELECT 
    business_id, name,
    AVG(stars) AS avg_rating, 
    SUM(review_count) AS review_count, 
    COUNT(*) AS restaurant_count 
FROM business 
WHERE business_id IN {tuple(business_Open_Restaurants['business_id'])} 
GROUP BY business_id, name
ORDER BY review_count DESC
""", engine)
```


```python
success_business
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>business_id</th>
      <th>name</th>
      <th>avg_rating</th>
      <th>review_count</th>
      <th>restaurant_count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>wPQWqLxY6t3-yRBNPPAmkQ</td>
      <td>Shallos Antique Restaurant &amp; Brewhouse</td>
      <td>4.0</td>
      <td>248.0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>y8gjlpJA89qDRCLC0JQaew</td>
      <td>Giuseppe &amp; Sons</td>
      <td>4.0</td>
      <td>248.0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>gkZ6iiEfnO7I2UzOHbkzrA</td>
      <td>Ulysses American Gastro Pub</td>
      <td>3.5</td>
      <td>248.0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>98WBvrn7wzu_93zc7fRfzQ</td>
      <td>Vero Amore - Dove</td>
      <td>4.0</td>
      <td>248.0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>30OhTA38fp8xuqW4O2D6Eg</td>
      <td>Homegrown Taproom &amp; Kitchen</td>
      <td>4.0</td>
      <td>248.0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>31532</th>
      <td>3xoCPDgE5dEretLD4yFpRw</td>
      <td>The Juice Pod</td>
      <td>2.5</td>
      <td>5.0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>31533</th>
      <td>nPruiFveAtUcGrUbFBeQuQ</td>
      <td>Bark Busters Dog Home Training</td>
      <td>4.0</td>
      <td>5.0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>31534</th>
      <td>Hk_EjFDeK5u7rlYEUx6a_g</td>
      <td>Jaggie's Restaurant</td>
      <td>3.0</td>
      <td>5.0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>31535</th>
      <td>qv6TSnK4iXZAXxG13mjv-w</td>
      <td>Angelina's Panini Bar</td>
      <td>2.0</td>
      <td>5.0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>31536</th>
      <td>rwZ-1fH9vdh1KRAowovXOQ</td>
      <td>Subway</td>
      <td>3.5</td>
      <td>5.0</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
<p>31537 rows × 5 columns</p>
</div>




```python
success_business['Success_score'] = calculate_sucess_metric(success_business)
```


```python
success_business
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>business_id</th>
      <th>name</th>
      <th>avg_rating</th>
      <th>review_count</th>
      <th>restaurant_count</th>
      <th>Success_score</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>wPQWqLxY6t3-yRBNPPAmkQ</td>
      <td>Shallos Antique Restaurant &amp; Brewhouse</td>
      <td>4.0</td>
      <td>248.0</td>
      <td>1</td>
      <td>22.069812</td>
    </tr>
    <tr>
      <th>1</th>
      <td>y8gjlpJA89qDRCLC0JQaew</td>
      <td>Giuseppe &amp; Sons</td>
      <td>4.0</td>
      <td>248.0</td>
      <td>1</td>
      <td>22.069812</td>
    </tr>
    <tr>
      <th>2</th>
      <td>gkZ6iiEfnO7I2UzOHbkzrA</td>
      <td>Ulysses American Gastro Pub</td>
      <td>3.5</td>
      <td>248.0</td>
      <td>1</td>
      <td>19.311085</td>
    </tr>
    <tr>
      <th>3</th>
      <td>98WBvrn7wzu_93zc7fRfzQ</td>
      <td>Vero Amore - Dove</td>
      <td>4.0</td>
      <td>248.0</td>
      <td>1</td>
      <td>22.069812</td>
    </tr>
    <tr>
      <th>4</th>
      <td>30OhTA38fp8xuqW4O2D6Eg</td>
      <td>Homegrown Taproom &amp; Kitchen</td>
      <td>4.0</td>
      <td>248.0</td>
      <td>1</td>
      <td>22.069812</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>31532</th>
      <td>3xoCPDgE5dEretLD4yFpRw</td>
      <td>The Juice Pod</td>
      <td>2.5</td>
      <td>5.0</td>
      <td>1</td>
      <td>4.479399</td>
    </tr>
    <tr>
      <th>31533</th>
      <td>nPruiFveAtUcGrUbFBeQuQ</td>
      <td>Bark Busters Dog Home Training</td>
      <td>4.0</td>
      <td>5.0</td>
      <td>1</td>
      <td>7.167038</td>
    </tr>
    <tr>
      <th>31534</th>
      <td>Hk_EjFDeK5u7rlYEUx6a_g</td>
      <td>Jaggie's Restaurant</td>
      <td>3.0</td>
      <td>5.0</td>
      <td>1</td>
      <td>5.375278</td>
    </tr>
    <tr>
      <th>31535</th>
      <td>qv6TSnK4iXZAXxG13mjv-w</td>
      <td>Angelina's Panini Bar</td>
      <td>2.0</td>
      <td>5.0</td>
      <td>1</td>
      <td>3.583519</td>
    </tr>
    <tr>
      <th>31536</th>
      <td>rwZ-1fH9vdh1KRAowovXOQ</td>
      <td>Subway</td>
      <td>3.5</td>
      <td>5.0</td>
      <td>1</td>
      <td>6.271158</td>
    </tr>
  </tbody>
</table>
<p>31537 rows × 6 columns</p>
</div>




```python
success_business = success_business.sort_values('Success_score',ascending=False)
```


```python
success_business

```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>business_id</th>
      <th>name</th>
      <th>avg_rating</th>
      <th>review_count</th>
      <th>restaurant_count</th>
      <th>Success_score</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>204</th>
      <td>bjQrmBSu1A7f5vprEikOKA</td>
      <td>Healthy N Fresh Cafe</td>
      <td>5.0</td>
      <td>238.0</td>
      <td>1</td>
      <td>27.382318</td>
    </tr>
    <tr>
      <th>399</th>
      <td>S5LnH1njwFBlq77tIkjI1g</td>
      <td>Yolk White &amp; Associates</td>
      <td>5.0</td>
      <td>229.0</td>
      <td>1</td>
      <td>27.190397</td>
    </tr>
    <tr>
      <th>508</th>
      <td>emrUsUZvqCkytUu4i3kjLw</td>
      <td>Sundae's Ice Cream &amp; Coffee</td>
      <td>5.0</td>
      <td>225.0</td>
      <td>1</td>
      <td>27.102675</td>
    </tr>
    <tr>
      <th>557</th>
      <td>0I9XZD7JTqY9iTF8nXRnXw</td>
      <td>Ali'i Poke Indy</td>
      <td>5.0</td>
      <td>223.0</td>
      <td>1</td>
      <td>27.058230</td>
    </tr>
    <tr>
      <th>611</th>
      <td>jh8j-DWqgWkbRe_a2XtKFQ</td>
      <td>Barrio Bread</td>
      <td>5.0</td>
      <td>221.0</td>
      <td>1</td>
      <td>27.013387</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>31139</th>
      <td>Q4OTSH9DaoeqtYcg6qYtZg</td>
      <td>Subway</td>
      <td>1.0</td>
      <td>5.0</td>
      <td>1</td>
      <td>1.791759</td>
    </tr>
    <tr>
      <th>30725</th>
      <td>F6zk6xPTLQZFdA0hu6nLgA</td>
      <td>Hungry Howie's Pizza &amp; Subs</td>
      <td>1.0</td>
      <td>5.0</td>
      <td>1</td>
      <td>1.791759</td>
    </tr>
    <tr>
      <th>31157</th>
      <td>BJ0Z74sTz9sxRr1R533Inw</td>
      <td>Best Rate Home Services</td>
      <td>1.0</td>
      <td>5.0</td>
      <td>1</td>
      <td>1.791759</td>
    </tr>
    <tr>
      <th>30715</th>
      <td>ogoe6WcXJnW96rvc3NyMfw</td>
      <td>Burger King</td>
      <td>1.0</td>
      <td>5.0</td>
      <td>1</td>
      <td>1.791759</td>
    </tr>
    <tr>
      <th>31362</th>
      <td>2HLZfbL-6lcr9jhriW6GeA</td>
      <td>Subway Restaurants</td>
      <td>1.0</td>
      <td>5.0</td>
      <td>1</td>
      <td>1.791759</td>
    </tr>
  </tbody>
</table>
<p>31537 rows × 6 columns</p>
</div>




```python
real_sentiments_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>business_id</th>
      <th>name</th>
      <th>text</th>
      <th>count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>---kPU91CF4Lq2-WlRu9Lw</td>
      <td>Frankie's Raw Bar</td>
      <td>Negative</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>---kPU91CF4Lq2-WlRu9Lw</td>
      <td>Frankie's Raw Bar</td>
      <td>Positive</td>
      <td>23</td>
    </tr>
    <tr>
      <th>2</th>
      <td>--0iUa4sNDFiZFrAdIWhZQ</td>
      <td>Pupuseria Y Restaurant Melba</td>
      <td>Negative</td>
      <td>3</td>
    </tr>
    <tr>
      <th>3</th>
      <td>--0iUa4sNDFiZFrAdIWhZQ</td>
      <td>Pupuseria Y Restaurant Melba</td>
      <td>Positive</td>
      <td>11</td>
    </tr>
    <tr>
      <th>4</th>
      <td>--30_8IhuyMHbSOcNWd6DQ</td>
      <td>Action Karate</td>
      <td>Negative</td>
      <td>4</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>351933</th>
      <td>zzu6_r3DxBJuXcjnOYVdTw</td>
      <td>Cafe Diblasi</td>
      <td>Positive</td>
      <td>7</td>
    </tr>
    <tr>
      <th>351934</th>
      <td>zzw66H6hVjXQEt0Js3Mo4A</td>
      <td>Sullivan Farms Christmas Trees</td>
      <td>Negative</td>
      <td>1</td>
    </tr>
    <tr>
      <th>351935</th>
      <td>zzw66H6hVjXQEt0Js3Mo4A</td>
      <td>Sullivan Farms Christmas Trees</td>
      <td>Positive</td>
      <td>4</td>
    </tr>
    <tr>
      <th>351936</th>
      <td>zzyx5x0Z7xXWWvWnZFuxlQ</td>
      <td>Walnut Street Pizza</td>
      <td>Negative</td>
      <td>3</td>
    </tr>
    <tr>
      <th>351937</th>
      <td>zzyx5x0Z7xXWWvWnZFuxlQ</td>
      <td>Walnut Street Pizza</td>
      <td>Positive</td>
      <td>5</td>
    </tr>
  </tbody>
</table>
<p>351938 rows × 4 columns</p>
</div>




```python
main_sentiment_df = pd.merge(real_sentiments_df,success_business, how='inner',on=['business_id','name']).sort_values(['Success_score'],ascending=False)
```


```python
main_sentiment_df.sort_values('count',ascending=False)
main_sentiment_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>business_id</th>
      <th>name</th>
      <th>text</th>
      <th>count</th>
      <th>avg_rating</th>
      <th>review_count</th>
      <th>restaurant_count</th>
      <th>Success_score</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>50059</th>
      <td>bjQrmBSu1A7f5vprEikOKA</td>
      <td>Healthy N Fresh Cafe</td>
      <td>Positive</td>
      <td>234</td>
      <td>5.0</td>
      <td>238.0</td>
      <td>1</td>
      <td>27.382318</td>
    </tr>
    <tr>
      <th>50058</th>
      <td>bjQrmBSu1A7f5vprEikOKA</td>
      <td>Healthy N Fresh Cafe</td>
      <td>Neutral</td>
      <td>1</td>
      <td>5.0</td>
      <td>238.0</td>
      <td>1</td>
      <td>27.382318</td>
    </tr>
    <tr>
      <th>50057</th>
      <td>bjQrmBSu1A7f5vprEikOKA</td>
      <td>Healthy N Fresh Cafe</td>
      <td>Negative</td>
      <td>5</td>
      <td>5.0</td>
      <td>238.0</td>
      <td>1</td>
      <td>27.382318</td>
    </tr>
    <tr>
      <th>36579</th>
      <td>S5LnH1njwFBlq77tIkjI1g</td>
      <td>Yolk White &amp; Associates</td>
      <td>Positive</td>
      <td>219</td>
      <td>5.0</td>
      <td>229.0</td>
      <td>1</td>
      <td>27.190397</td>
    </tr>
    <tr>
      <th>36577</th>
      <td>S5LnH1njwFBlq77tIkjI1g</td>
      <td>Yolk White &amp; Associates</td>
      <td>Negative</td>
      <td>7</td>
      <td>5.0</td>
      <td>229.0</td>
      <td>1</td>
      <td>27.190397</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>31365</th>
      <td>NxB8M1wnJQ5xoXDiUgqmIg</td>
      <td>Burger King</td>
      <td>Neutral</td>
      <td>1</td>
      <td>1.0</td>
      <td>5.0</td>
      <td>1</td>
      <td>1.791759</td>
    </tr>
    <tr>
      <th>34051</th>
      <td>Q4OTSH9DaoeqtYcg6qYtZg</td>
      <td>Subway</td>
      <td>Negative</td>
      <td>4</td>
      <td>1.0</td>
      <td>5.0</td>
      <td>1</td>
      <td>1.791759</td>
    </tr>
    <tr>
      <th>19745</th>
      <td>ESUwN81iNYvm0yqYCxSivg</td>
      <td>Jack in the Box</td>
      <td>Negative</td>
      <td>2</td>
      <td>1.0</td>
      <td>5.0</td>
      <td>1</td>
      <td>1.791759</td>
    </tr>
    <tr>
      <th>19746</th>
      <td>ESUwN81iNYvm0yqYCxSivg</td>
      <td>Jack in the Box</td>
      <td>Positive</td>
      <td>3</td>
      <td>1.0</td>
      <td>5.0</td>
      <td>1</td>
      <td>1.791759</td>
    </tr>
    <tr>
      <th>3476</th>
      <td>1dpjXnlEKc-Ihgku6CtY5w</td>
      <td>Little Caesars Pizza Barataria Blvd</td>
      <td>Positive</td>
      <td>3</td>
      <td>1.0</td>
      <td>5.0</td>
      <td>1</td>
      <td>1.791759</td>
    </tr>
  </tbody>
</table>
<p>80616 rows × 8 columns</p>
</div>




```python
# Top Five Highest Sucess Score Restaurant  
main_sentiment_df.head(14)[['name']].drop_duplicates('name').sort_values('name').values
```




    array([["Ali'i Poke Indy"],
           ['Barrio Bread'],
           ['Healthy N Fresh Cafe'],
           ["Sundae's Ice Cream & Coffee"],
           ['Yolk White & Associates']], dtype=object)




```python
# Pivot the DataFrame to prepare for stacked bar plot
pivot_df = main_sentiment_df.head(14).pivot_table(index='name', columns='text', values='count', fill_value=0)

# Plot Stacked Bar 
pivot_df.plot(kind='bar', stacked=True, figsize=(18, 10))
plt.title('Top Five Highest Sucess Score Restaurant With Sentiments')
plt.xlabel('Restaurant Name')
plt.ylabel('Count of Sentiments')
plt.xticks(rotation=45, ha='right')
plt.legend(title='Sentiment')
plt.tight_layout()
plt.show()
```


    
![png](main_files/main_100_0.png)
    


## NOTE :
### There are top five highest success score restaurants, including not only the higher rating and higher review counts, but also having a higher positive sentiments In compare to the other negative and neutral sentiments. These five restaurant may be the best restaurants in overall comparison. 

# Distribution Of Data Based On Elite And Non ELite :

# Q. Is there any difference in engagement of elite users and non-elite users?


```python
elite_df = pd.read_sql("""
    SELECT
        elite,
        COUNT(*) AS num_users,
        SUM(review_count) AS total_review_count
    FROM (
        SELECT
            CASE
                WHEN elite = 'None' OR elite = '' OR elite IS NUll THEN 'Not Elite'
                ELSE 'Elite'
            END AS elite,
            user.review_count
        FROM
            user
    ) AS user_elite
    GROUP BY
        elite;
""", engine)

```


```python
# Elite 
elite_df

```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>elite</th>
      <th>num_users</th>
      <th>total_review_count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Elite</td>
      <td>90969</td>
      <td>20450520.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Not Elite</td>
      <td>1892854</td>
      <td>25963868.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Pie Plot of User Distribution
plt.figure(figsize=(10,15))
plt.subplot(2,1,1)
plt.title('User Distribution')
plt.pie(elite_df['num_users'],labels = elite_df['elite'], autopct = '%0.2f%%', startangle= 180, colors = ['RED', 'BLUE'])

# Pie Plot of Review Distribution
plt.figure(figsize=(10,15))
plt.subplot(2,1,2)
plt.title('Review Distribution')
plt.pie(elite_df['total_review_count'],labels = elite_df['elite'], autopct = '%0.2f%%', startangle= 90, colors = ['RED', 'BLUE'])
plt.show()
```


    
![png](main_files/main_106_0.png)
    



    
![png](main_files/main_106_1.png)
    


## NOTE :
###  `Elite` users are individual who have been recognized and awarded the `Elite` status by the Yelp and their active and high quality contribution to the platform, such as frequent and detailed review photos and check insurance. Among the others criteria. `Elite` users despite being significant fewer in numbers, contributed a substantial proportion of the total account compared to the non-elite users. `Elite` users often provide detailed and insightful reviews, which can influence other users perceptions and decision regarding a business. review from `Elite` users may receive more attention and visibility on the real platform due to their status potentially leading to the higher exposure through business.Establishing a positive relationship with `Elite` users can lead a repeat visit and loyalty, as they have more likely to continue supporting widgets they have had good experience with. 

# Time Based Analysis :

## Q. What are the busiest hours for restaurants ?


```python
review_engagement = pd.read_sql_query("""
SELECT 
    HOUR(STR_TO_DATE(date, '%Y-%m-%d %H:%i:%s')) AS hour,
    COUNT(*) AS review_count
FROM review
GROUP BY hour;
""", engine)

tip_engagement = pd.read_sql_query("""
SELECT 
    HOUR(STR_TO_DATE(date, '%Y-%m-%d %H:%i:%s')) AS hour,
    COUNT(*) AS tip_count
FROM tip
GROUP BY hour;
""", engine)

checkin = pd.read_sql_query("SELECT date FROM checkin", engine)
checkin_engagement = []

for i in checkin['date']:
    checkin_engagement.extend(
        [datetime.strptime(j.strip(), "%Y-%m-%d %H:%M:%S").strftime("%H") 
         for j in i.split(',')]
    )

checkin_engagement = pd.DataFrame(checkin_engagement).astype(int).groupby(0)[0].count()

```


```python
checkin_engagement.name = 'Values'
checkin_engagement
```




    0
    0     1060009
    1      853147
    2      602632
    3      388609
    4      233305
    5      133875
    6       74652
    7       46172
    8       30390
    9       29614
    10      51960
    11     100839
    12     180490
    13     267501
    14     368108
    15     532775
    16     794471
    17     924978
    18     900055
    19     833639
    20     775722
    21     827312
    22     984501
    23    1109237
    Name: Values, dtype: int64




```python
# Bar Plot 
# tip_engagement
plt.subplot(3,1,1)
plt.title("Tip Engagement")
plt.bar(tip_engagement['hour'], tip_engagement['tip_count'], color = 'RED')

# review_engagement
plt.subplot(3,1,2)
plt.title("Review Engagement")
plt.bar(review_engagement['hour'], review_engagement['review_count'], color = 'BLUE')

# Checkin Engagement
plt.subplot(3,1,3)
plt.title("Checkin Engagement")
plt.bar(checkin_engagement.index, checkin_engagement  , color = 'YELLOW')
plt.tight_layout()
plt.show()


```


    
![png](main_files/main_112_0.png)
    


## NOTE :
### The busiest R4 restaurants based on user engagement spanned from 3:00 PM to 1:00 AM, Knowing the peak hours allowed businesses to optimize their staffing level and resources accolation allocation during the during this. time to ensure defensiency of resident and quality service delivery. The concentration of user engagement during the evening and night hours suggest a higher demand for dining out, dining these times potentially driven by the factor such as work schedules, Social gathering and leisure activities.  

# RECOMMENDATIONS :

### 1. Utilizing inssights from the analysis of various metrics such as user engagement, sentiment of reviews, peak hours, and the impact of eilte users, businesses can make informed decisions to drive sucess.
### 2. Collaborating With light users and leveraging their influence can amplify proportional efforts, increase brand awareness and the drive customer acquisition. 
### 3. Businesses can adjust their operating hours or introduce special promotions to capitalize on increased demand during peak hours. 
### 4. Less successful businesses may  need to focus on strategies to enhance user engagement over time, such as improving service quality responding to customer feedback. 
### 5. Cities with high success scores presents opportunities for restaurant chains to expand or invest further. 
### 6. Understanding customer preferences behavior and satisfaction level is paramount. Businesses should focus on delivery exponential experience to meet customer expectations.
### 7. Positive reviews from Elite users and high user engagement can boost a business online visibility and reputation. Maintaining an active engagement with customers and responding promptly to feedback is crucial for building credibility and attracting a new customers.
 


