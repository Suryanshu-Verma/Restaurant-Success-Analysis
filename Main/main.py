#%% md
# # Problem Statment :
# ## In the competitive restaurant industry, stakeholders often lack clear insights into which user engagement factors contribute most to business success. This project seeks to address the question: How do user engagement metrics (e.g., reviews, tips, and check-ins) correlate with key business performance indicators (such as review count and ratings) for How do user engagement metrics, such as reviews, tips, and check-ins, influence key business performance indicators like review counts and ratings for restaurants? In the highly competitive restaurant industry, understanding these relationships is crucial for stakeholders aiming to enhance business success. providing data-driven insights that can guide strategic decision-making and promote sustainable growth .? By analyzing the Yelp dataset, the goal is to identify actionable patterns that can guide strategic decisions and enhance restaurant performance.
#%% md
# # General Research Objectives :
# ## Quantify the Correlation Between User Engagement and Business Metrics: Assess the relationship between user engagement factors—such as reviews, tips, and check-ins—and business metrics, including review count and average star rating. This will reveal whether restaurants with higher user engagement tend to have higher ratings and more reviews.
# 
# ## Analyze the Impact of Sentiment on Business Performance: Investigate whether positive sentiment in reviews and tips is associated with higher star ratings and an increase in the total number of reviews. This analysis will help determine if sentiment influences business success.
# 
# ## Identify Time Trends in User Engagement: Explore whether consistent user engagement over time serves as a stronger indicator of long-term success compared to sporadic bursts of activity. This will provide insights into engagement patterns that contribute to sustained business growth.
# 
# ## Adapt Research Based on Emerging Insights: Modify the research focus as necessary, based on findings and insights gained during analysis, to capture additional factors relevant to business success.
#%% md
# 
# # Hypothesis Testing :
# ## User Engagement and Business Performance: Higher levels of user engagement, such as increased reviews, tips, and check-ins, are positively correlated with higher review counts and ratings for restaurants.
# 
# ## Sentiment Impact on Ratings and Review Counts: Positive sentiments expressed in reviews and tips contribute to higher overall ratings and increased review counts for restaurants.
# 
# ## Consistent Engagement and Long-term Success: Consistent user engagement over time is positively associated with sustained business success for restaurants.
#%% md
# # About Dataset :
# ## This Yelp dataset contains information across eight metropolitan areas in the USA and Canada, organized into five primary tables for analysis:
# 
# ## `Business`: Contains details on 131,930 businesses, including over 1.2 million attributes like hours, parking, availability, and ambiance.
# ## `Review`: Includes user-generated reviews with star ratings, text, and timestamps.
# ## `User`: Information on 1,987,897 users, including activity and interaction data.
# ## `Tip`: Contains 908,915 tips from users, providing short advice about businesses.
# ## `Check`-in: Aggregates check-in data over time for each business, enabling time-based analysis of user visits.
#%% md
# ## Importing Necessary Libraries Below :
# 
#%%
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

#%% md
# ## Creating MySQL connection Using SQLAlchemy Engine :
#%%
from sqlalchemy import create_engine

# Create an engine that connects to your MySQL database
engine = create_engine('mysql+mysqlconnector://root:Vermasuryanshu%40110906@localhost:3306/yelp_db?connect_timeout=600')

# Verify connection
try:
    
    # Here, you can use pandas to directly interact with the database
    print("Successfully connected to the database using SQLAlchemy!")
except Exception as e:
    print(f"Error: {e}")
#%% md
# ## Reading the tables using sqlAlchemy :
# 
#%%
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

#%%
# Reading data from the 'business' table using pandas
business = pd.read_sql("SELECT * FROM business;", engine)
business # Display the first few rows of the DataFrame

#%%
# Reading data from the 'checkin' table using pandas
checkin = pd.read_sql("SELECT * FROM checkin;", engine)
checkin # Display the first few rows of the DataFrame

#%%
# Reading data from the 'review' table using pandas
review = pd.read_sql("SELECT * FROM review;", engine) # Display the first few rows of the DataFrame
review
#%%
# Reading data from the 'tip' table using pandas
tip = pd.read_sql("SELECT * FROM tip;", engine) # Display the first few rows of the DataFrame
tip
#%%
# Reading data from the 'user' table using pandas
user = pd.read_sql("SELECT * FROM user;", engine) # Display the first few rows of the DataFrame
user
#%% md
# #  Data Analysis :
#%%
business_Open_Restaurants=pd.read_sql("select * from business where is_open = 1 AND  lower(categories) like '%restaurant%';",engine) # Data of Open Restaurants
#%%
business_Open_Restaurants # Open Restaurants
#%% md
# ### Out of 150K Businesses, 35K are Restaurant Business and are Open.
#%% md
# # Q. What is the descriptive stats for review count and star rating for businesses ?
#%%
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

#%%
# Calculating the median for the both Stars & Review_count
review_business.insert(3,'median_review',[business['review_count'].median()])
review_business.insert(7,'median_stars',[business['stars'].median()])

#%%
review_business # As per the stats, We can conclude that the review columns includes outliers
#%%
review_business=review_business.T
#%%
review_business
#%% md
# ### The Max_review is outlier and data is skewed, To address this I decided to remove restaurants with outlier review counts, For this I created a Function to identify & remove outliers using IQR method.
#%%
# Convert column to integer, if it contains boolean values by mistake
business_Open_Restaurants['review_count'] = business_Open_Restaurants['review_count'].astype(int)

#%%
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



#%%
business_Open_Restaurants
#%%
business_Open_Restaurants['review_count'].describe() # its reflected the change and the outlier are remove and the max is 284
#%% md
# ### After Removing outliers, Now I get average review count as 55.975 for the restaurant business.
#%% md
# # Open Businesses Which Are Restaurant :
#%%
business_Open_Restaurants
#%% md
# # Q. Which restaurant have the higest number of reviews ?
#%%
pd.read_sql(""" select name, SUM(review_count) AS Higest_Review_Counts, AVG(stars) AS Average_Rating from (select * from business where is_open = 1 AND  lower(categories) like '%restaurant%') AS business_Open_Restaurants group by name order by Higest_Review_Counts desc limit 10;""",engine)
#%% md
# # Q. Which restaurant have the highest number of highest rating ? 
#%%
pd.read_sql(""" select name, SUM(review_count) AS Higest_Review_Counts, AVG(stars) AS Average_Rating from (select * from business where is_open = 1 AND  lower(categories) like '%restaurant%') AS business_Open_Restaurants group by name order by Average_Rating desc limit 10;""",engine).sort_values('Higest_Review_Counts',ascending=False)
#%% md
# ## NOTE :
# ### No direct correlation:  Higher rating do not guarantee a higher review count and vice versa, The review cannot reflect user engagement, but do not necessarily States the overall customer satisfaction or business performance, Successes in the restaurant business is not solely determined by rating or review counts.   
#%% md
# # Q. Do restaurants with higer engagement tends to have higher rating ?
#%%
pd.read_sql(""" select business_id, sum(length(date) - length(replace(date, ',', '')) + 1 ) as checkin_count from checkin group by business_id order by checkin_count desc ;""",engine)

#%%
# tip_counts per business_id
pd.read_sql(""" select business_id, count(*) as tip_counts from  tip group by business_id order by tip_counts desc;""",engine)
#%%
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
#%%
review_counts=review_counts.sort_values('rating', ascending=False)
#%% md
# # Ploting `Bar` Graphs :
#%%
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

#%% md
# ## NOTE :
# ### Data show a general increase in average review check in and tip counts as rating improves from one to four stars, restaurants created four stars. Exhibit the highest engagement across reviews, check insurance and tips, suggesting a peak in user interaction, interestingly, engagement matrix. ( Review, check in ). Dip for restaurant rated 4.5 and significantly more at five stars, They dropped an engagement at 5 stars might suggest either a situation point where fewer customer feel compended or to add their reviews for a selective believer only a small satisfied audience. Frequents these establishment. 
#%% md
# # Q. Is there a correclation between the number of reviews, tip, and check - ins for a business ?
#%%
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


#%%
engage_df_corr = engage_df[['review_count','checkin_count','tip_count']].corr()
#%%
# Ploting the HeatMap
sns.heatmap(engage_df_corr,cmap='seismic', annot=True, linewidths=0.5,linecolor='white')

#%%
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

#%%
engage_dff.groupby('category')[['review_count','tip_count','checkin_count']].mean() 
#%% md
# ## NOTE :
# ### The data set shows a strong positive correlation among review counts, checking counts and tip counts, These correlations suggest that user engagement across different platforms, such as reviews, tips and check insurance is interlinked, Higher activity in one area tends to be associated with higher activity others. Businesses should focus on strategies that boost all types of user investment as increases in one type of engagement are likely to drive increase in others. And hence, in overall visibility and interaction with customers.
#%%
# Function to calculate the sucess score based on the avg rating and total review count.
def calculate_sucess_metric(df):
    sucess_score=[]
    for idx, row in df.iterrows():
        score = row['avg_rating'] * np.log(row['review_count'] + 1 )
        sucess_score.append(score)
    return sucess_score
#%% md
# # MAP Plot :
#%% md
# # Q. How do the sucess metrics (review_count or avg_rating) of restaurant vary across different states and cities?
#%%
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


#%%
city_df = city_df.reset_index()
#%%
city_df = city_df.drop('index',axis = 1)
#%%
city_df['success_score'] = calculate_sucess_metric(city_df)
#%%
city_df
#%%
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




#%% md
# ## NOTE :
# ### Philadelphia emerges as the top city with the highest success code, indicating a combination of high ratings and active user engagements. following Philadelphia, Tampa, Indianapolis and tucson rank among the top cities with significant success score, suggesting thriving restaurant success in these areas. The success matrix vary significantly across different state and cities, highlighting regional differences in dining Preferences, culinary sceneries and customer engagement levels, identifying city with the highest success score present opportunities for Restaurant chains to Expend or invest further while areas with low score may require targeted efforts to improve rating and increase user engagement. 
#%% md
# # Time :
#%% md
# # Q. Are there any patterns in the user engagement over time for sucessfull business compared to less sucessfull ones, Are there any seasonal trends in the user engagement for restaurant ?
#%%
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


#%%
high_rated_engagement
#%%
low_rated_engagement
#%%
time_rating = pd.read_sql(f"""
SELECT DATE_FORMAT(date, '%m-%Y') AS month_year, AVG(stars) AS avg_rating
FROM review
WHERE business_id IN {tuple(business_Open_Restaurants['business_id'])}
GROUP BY month_year
ORDER BY month_year;
""", engine)

#%%
time_rating
#%%
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

#%%
# Creating a col called avg_rating in high_rated_engagement
high_rated_engagement['avg_rating'] = time_rating['avg_rating'].values
#%%
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

#%%
tip_high_rated = high_rated_engagement[['month_year','tip_count']].set_index('month_year')
review_high_rated = high_rated_engagement[['month_year', 'review_count']].set_index('month_year')
rating_df = time_rating[['month_year', 'avg_rating']].set_index('month_year')
#%%
# seasonal_decompose of tip_high_rated
from statsmodels.tsa.seasonal import seasonal_decompose
multiplication_decompose = seasonal_decompose(tip_high_rated, model = 'multiplication', period = 12)
plt.rcParams.update({'figure.figsize':(16,12)})
multiplication_decompose.plot()
plt.show()
#%%
# seasonal_decompose of  review_high_rated
from statsmodels.tsa.seasonal import seasonal_decompose
multiplication_decompose = seasonal_decompose(review_high_rated, model = 'multiplication', period = 12)
plt.rcParams.update({'figure.figsize':(16,12)})
multiplication_decompose.plot()
plt.show()


#%% md
# ## NOTE : 
# ### Successful businesses, particularly those with higher ratings above 3.5 exhibit consistent and possibly increase user engagement overtime, High rated restaurants maintain a steady or blowing level of user management over time, reflecting ongoing customer interest and satisfaction, Keep count is showing a downward trend, whereas review count is showing an up on trend with time, Years starting at year ending from around November and March is highly engaging in seasonal. 
#%% md
# # Sentiment Analysis Using NLTK :
#%% md
# # Q. Retrive Top Five Restaurant with High Success Score And Sentiments Included ( Positive, Negetive & Neutral )
#%%
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


#%%
sentim = pd.read_csv('D:\\VSCODE\\SQL_PROJECT\\Senti.csv')
#%%
senti = pd.concat([review[['business_id','text']], sentim], axis = 1)
#%%
# Sentiments
senti
#%%
business
#%%
business_data = business[['business_id','name']]
senti = senti.iloc[:,[0,4]]

#%%
senti
#%%
real_sentiments = pd.merge(business_data,senti, how='inner', on= ['business_id'])
#%%
real_sentiments
#%%
real_sentiments = real_sentiments.groupby(['business_id','name','text']).value_counts()
#%%
real_sentiments_df = real_sentiments.reset_index()
#%%
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
#%%
success_business
#%%
success_business['Success_score'] = calculate_sucess_metric(success_business)
#%%
success_business
#%%
success_business = success_business.sort_values('Success_score',ascending=False)
#%%
success_business

#%%
real_sentiments_df
#%%
main_sentiment_df = pd.merge(real_sentiments_df,success_business, how='inner',on=['business_id','name']).sort_values(['Success_score'],ascending=False)
#%%
main_sentiment_df.sort_values('count',ascending=False)
main_sentiment_df
#%%
# Top Five Highest Sucess Score Restaurant  
main_sentiment_df.head(14)[['name']].drop_duplicates('name').sort_values('name').values
#%%
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
#%% md
# ## NOTE :
# ### There are top five highest success score restaurants, including not only the higher rating and higher review counts, but also having a higher positive sentiments In compare to the other negative and neutral sentiments. These five restaurant may be the best restaurants in overall comparison. 
#%% md
# # Distribution Of Data Based On Elite And Non ELite :
#%% md
# # Q. Is there any difference in engagement of elite users and non-elite users?
#%%
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

#%%
# Elite 
elite_df

#%%
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
#%% md
# ## NOTE :
# ###  `Elite` users are individual who have been recognized and awarded the `Elite` status by the Yelp and their active and high quality contribution to the platform, such as frequent and detailed review photos and check insurance. Among the others criteria. `Elite` users despite being significant fewer in numbers, contributed a substantial proportion of the total account compared to the non-elite users. `Elite` users often provide detailed and insightful reviews, which can influence other users perceptions and decision regarding a business. review from `Elite` users may receive more attention and visibility on the real platform due to their status potentially leading to the higher exposure through business.Establishing a positive relationship with `Elite` users can lead a repeat visit and loyalty, as they have more likely to continue supporting widgets they have had good experience with. 
#%% md
# # Time Based Analysis :
#%% md
# ## Q. What are the busiest hours for restaurants ?
#%%
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

#%%
checkin_engagement.name = 'Values'
checkin_engagement
#%%
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


#%% md
# ## NOTE :
# ### The busiest R4 restaurants based on user engagement spanned from 3:00 PM to 1:00 AM, Knowing the peak hours allowed businesses to optimize their staffing level and resources accolation allocation during the during this. time to ensure defensiency of resident and quality service delivery. The concentration of user engagement during the evening and night hours suggest a higher demand for dining out, dining these times potentially driven by the factor such as work schedules, Social gathering and leisure activities.  
#%% md
# # RECOMMENDATIONS :
#%% md
# ### 1. Utilizing inssights from the analysis of various metrics such as user engagement, sentiment of reviews, peak hours, and the impact of eilte users, businesses can make informed decisions to drive sucess.
# ### 2. Collaborating With light users and leveraging their influence can amplify proportional efforts, increase brand awareness and the drive customer acquisition. 
# ### 3. Businesses can adjust their operating hours or introduce special promotions to capitalize on increased demand during peak hours. 
# ### 4. Less successful businesses may  need to focus on strategies to enhance user engagement over time, such as improving service quality responding to customer feedback. 
# ### 5. Cities with high success scores presents opportunities for restaurant chains to expand or invest further. 
# ### 6. Understanding customer preferences behavior and satisfaction level is paramount. Businesses should focus on delivery exponential experience to meet customer expectations.
# ### 7. Positive reviews from Elite users and high user engagement can boost a business online visibility and reputation. Maintaining an active engagement with customers and responding promptly to feedback is crucial for building credibility and attracting a new customers.
#  
#%% md
# 