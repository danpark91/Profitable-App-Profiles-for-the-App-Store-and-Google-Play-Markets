#!/usr/bin/env python
# coding: utf-8

# # Analyzing Mobile App Data
# 
# We only build apps that are free to download and install, and our main source of revenue consists of in-app ads. The number of users of our apps determines our revenue for any given app. Our goal for this project is to analyze data to help our developers understand what type of apps are likely to attract more users.

# ## Opening and Exploring the Data

# In[58]:


from csv import reader
def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line after each row

    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))

### The App Store Dataset ###
opened_file = open('AppleStore.csv')
read_file = reader(opened_file)
apple = list(read_file)
apple_header = apple[0]
apple = apple[1:]

print('App Store Dataset')
print(apple_header)
explore_data(apple, 0, 3, True)

### The Google Play Dataset ###
opened_file = open('googleplaystore.csv')
read_file = reader(opened_file)
google = list(read_file)
google_header = google[0]
google = google[1:]

print('\n')
print('Google Play Dataset')
print(google_header)
explore_data(google, 0, 3, True)

del google[10472]
print(google[10472])


# ## Removing Duplicate Entries and Deleting Wrong Data
# The Google Play dataset has duplicate entries. A few duplicate rows are printed to confirm.

# In[59]:


duplicate_apps_google = []
unique_apps_google = []

for app in google:
    name = app[0]
    if name in unique_apps_google:
        duplicate_apps_google.append(name)
    else:
        unique_apps_google.append(name)
        
print('Number of duplicate Google apps:', len(duplicate_apps_google))
print('\n')
print('Examples of duplicate Google apps:', duplicate_apps_google[:])


# Checking for duplicates for the App Store dataset.

# In[60]:


duplicate_apps_apple = []
unique_apps_apple = []

for app in apple:
    name = app[1]
    if name in unique_apps_apple:
        duplicate_apps_apple.append(name)
    else:
        unique_apps_apple.append(name)
        
print('Number of duplicate apps:', len(duplicate_apps_apple))
print('\n')
print('Examples of duplicate apps:', duplicate_apps_apple[:])


# The criterion used to remove duplicates will be to keep the most recent review with the highest number of reviews(number of reviews), and remove all previous duplicates for the Google Play and App Store. 

# In[61]:


reviews_max_google = {}

for app in google:
    name = app[0]
    n_reviews = float(app[3])
    
    if name in reviews_max_google and reviews_max_google[name] < n_reviews:
        reviews_max_google[name] = n_reviews
    elif name not in reviews_max_google:
        reviews_max_google[name] = n_reviews 

print('Expected length:', len(google) - len(duplicate_apps_google))
print('Actual length of reviews_max:', len(reviews_max_google))


# In[62]:


reviews_max_apple = {}

for app in apple:
    name = app[1]
    n_reviews = float(app[5])
    
    if name in reviews_max_apple and reviews_max_apple[name] < n_reviews:
        reviews_max_apple[name] = n_reviews
    elif name not in reviews_max_apple:
        reviews_max_apple[name] = n_reviews 

print('Expected length:', len(apple) - len(duplicate_apps_apple))
print('Actual length of reviews_max:', len(reviews_max_apple))


# Using the dictionary reviews_max that was created above by data cleaning and removing the duplicate rows.

# In[63]:


google_clean = []
already_added = []

for app in google:
    name = app[0]
    n_reviews = float(app[3])
    
    if (reviews_max_google[name] == n_reviews) and (name not in already_added):
            google_clean.append(app)
            already_added.append(name)
            
explore_data(google_clean, 0, 3, True)


# In[64]:


apple_clean = []
already_added_apple = []

for app in apple:
    name = app[1]
    n_reviews = float(app[5])
    
    if (reviews_max_apple[name] == n_reviews) and (name not in already_added_apple):
            apple_clean.append(app)
            already_added_apple.append(name)
            
explore_data(apple_clean, 0, 3, True)


# ## Removing Non-English Apps
# Creating a function that takes in a string and returns False if there's any character in the string that doesn't belong to the set of common English characters and True otherwise to remove any apps that are not English-based. The filter function that is used is that the app will be removed from the database, if the app has more than 3 emoji or special characters(this filter function is not completely perfect, but fairly effective).

# In[65]:


def is_english(string):
    sum = 0
    for character in string:
        if ord(character) > 127:
           sum += 1
    if sum > 3:
        return False
    else:
        return True        
        
print(is_english('Instagram'))
print(is_english('爱奇艺PPS -《欢乐颂2》电视剧热播'))
print(is_english('Docs To Go™ Free Office Suite'))
print(is_english('Instachat 😜'))


# Examining the App Store and the Google Play datasets, if an app is identified as English, append to English list and explore how many rows are remaining for each English dataset.

# In[66]:


google_english = []
apple_english = []
     
for app in google_clean:
    name = app[0]
    if is_english(name):
        google_english.append(app)

for app in apple_clean:
    name = app[1]
    if is_english(name):
        apple_english.append(app)
        
explore_data(google_english, 0, 3, True)
print('\n')
explore_data(apple_english, 0, 3, True)


# ## Isolating the Free Apps
# We only consider apps that are free to download and install, and our main source of revenue consists of in-app ads. Our datasets contain both free and non-free apps, we'll isolate only the free apps and then perform our analysis.

# In[67]:


apple_free = []
google_free = []

for app in apple_english:
    name = app[1]
    price = app[4]
    if (price == '0.0') and (name not in apple_free):
        apple_free.append(name)
        
print('The number of free apps in the App Store are:', len(apple_free))

for app in google_english:
    name = app[0]
    price = app[7]
    if (price == '0') and (name not in google_free):
        google_free.append(name)
        
print('The number of free apps in Google Play are:', len(google_free))
print('\nWe have 3220 Apple and 8064 Google apps, which should be enough to continue our analysis.')


# ## Most Common Apps by Genre
# Our goal is to determine the kinds of apps that are likely to attract more users because the number of people using our apps affect our revenue.
# 
# To minimize risks and overhead, our validation strategy for an app has the following three steps:
# 1. Build a minimal Android version of the app, and add it to Google Play.
# 2. If the app has a good response from users, we develop it further.
# 3. If the app is profitable after six months, we build an iOS version of the app and add it to the App Store.
# 
# Our end goal is to add the app on both Google Play and the App Store, and we need to find app profiles that are successful in both markets.
# 
# To begin our analysis, we determine the most common genres for each market by building frequency tables for our datasets and organizing the indexed column in descending order.

# In[68]:


apple_free_genres = []
google_free_genres = []

for app in apple_english:
    name = app[1]
    genre = app[11]
    if (genre not in apple_free_genres):
        apple_free_genres.append(genre)
        
print('The genres of free apps in the App Store are:', apple_free_genres)

for app in google_english:
    name = app[0]
    genre = app[9]
    if (genre not in google_free_genres):
        google_free_genres.append(genre)
        
print('\nThe genres of free apps in Google Play are:', google_free_genres)
print('\n')

def freq_table(dataset, index):
    table = {}
    total = 0
    
    for row in dataset:
        total += 1
        value = row[index]
        if value in table:
            table[value] += 1
        else:
            table[value] = 1
    
    table_percentages = {}
    for key in table:
        percentage = (table[key] / total) * 100
        table_percentages[key] = percentage 
    
    return table_percentages

def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)
        
    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])

print('A sorted frequency table for the columns prime_genre for the App Store.') 
display_table(apple_english, 11)
print('\nA sorted frequency table for the categories and genres of the apps in Google Play.')
display_table(google_english, 1)
print('\n')
display_table(google_english, 9)


# ## Analyzing the frequency table for the most common genres in the App Store and Google Play datasets

# Upon analyzing the sorted frequency table, the most common genre were games, entertainment, education, photo & video, and utilities for the App Store dataset. These 5 categories made up around 75% or most of all English free apps. When examining the top 10 frequent categories of free apps: 6 of 10 were for entertainment(games, entertainment, photo & video, music, social networking, and sports) comprising 73.56%, while the other 4 were for practical purposes(education, utilities, productivity, and health & fitness) making up approximately 15.47%. There were significantly more apps for entertainment than practical purposes, with games making up over half of all free apps available with 54.86%. It is noted that fun apps are the most numerous, however, they do not have the greatest number of users - the demand is not the same as the offerings.

# For the category column of the Google Play dataset, the top 5 categories were: family, games, tools, business, and medical, while the top 5 categories for genres were: tools, entertainment, education, business, and medical. This time the top 5 categories made up around 46% or nearly half of all English free apps and the top 5 genres made up only 28%. There were 11 categories with at least 3% usage for both the categories and genres. Of the top 10 apps used, there are not that many apps used for entertainment, and it seems more of the apps are designed for practical purposes(family, tools, business, lifestyle, productivity, etc.). Upon further investigation, the family category which accounts for almost 19% of the apps, is mainly games for kids.

# Even so, practical apps seem to have a better representation on Google Play compared to the App Store. The difference between the genres and the category columns is not quite clear, but the genres column is more granular(it has more categories). We are interested in the bigger picture at the moment, so we'll work with the category column for Google Play moving forward. 
# 
# At this point, we found that the App Store is mostly apps designed for fun, while Google Play shows a more balanced landscape of both practical and for-fun apps.

# ## Most popular apps on the App Store by average number of installs per app genre

# One way to find out which genres are the most popular(have the most users) is to calculate the average number of installs for each app genre. For the Google Play dataset, we can find this information in ths Installs column, but this information is missing for the App Store dataset. As a workaround, we'll take the total number of user ratings instead, which we can find in the rating_count_tot app.

# In[69]:


genres_apple = freq_table(apple_english, 11)

for genre in genres_apple:
    total = 0
    len_genre = 0
    for app in apple_english:
        genre_app = app[11]
        if genre_app == genre:            
            n_ratings = float(app[5])
            total += n_ratings
            len_genre += 1
    avg_n_ratings = total / len_genre
    print(genre, ':', avg_n_ratings)


# On average, navigation/reference apps have the highest number of user reviews, but this figure is heavily influenced by Waze and Google Maps, which have close to half a million reviews together. 

# In[70]:


for app in apple_english:
    if app[11] == 'Navigation':
        print(app[1], ':', app[5]) # print name and number of ratings


# The same pattern applies to social networking apps, where the average number is heavily influenced by a few giants like Facebook, Pinterest, Skype, etc. Same applies to music apps, where a few big players like Pandora, Spotify, and Shazam heavily influence the average number.
# 
# Our aim is to find popular genres, but navigation, social networking or music apps might seem more popular than they really are. The average number of ratings seem to be skewed by very few apps which have hundreds of thousands of user ratings, while the other apps may struggle to get past the 10,000 threshold. We could get a better picture by removing these extremely popular apps for each genre and then rework the averages.

# ## Most popular apps on Google Play by average number of installs per app genre

# In[71]:


categories_google = freq_table(google_english, 1)

for category in categories_google:
    total = 0
    len_category = 0
    for app in google_english:
        category_app = app[1]
        if category_app == category: 
            n_installs = app[5]
            n_installs = n_installs.replace(',','')
            n_installs = n_installs.replace('+','')
            total += float(n_installs)
            len_category += 1
    avg_n_installs = total / len_category
    print(category, ':', avg_n_installs)  


# On average, communication apps have the most installs with 35,153,714. This number is heavily skewed up by a few apps that have over one billion installations(WhatsApp, Facebook, Messenger, Skype, Google Chrome, Gmail, and Hangouts), and a few others with over 100 and 500 million installs. 

# In[72]:


for app in google_english:
    if app[1] == 'COMMUNICATION' and (app[5] == '1,000,000,000+'
                                      or app[5] == '500,000,000+'
                                      or app[5] == '100,000,000+'):
        print(app[0], ':', app[5])


# If we removed all the communication apps that have over 100 million installs, the average would be reduced roughly ten times from 35,135,714 to 3,269,220: 

# In[73]:


under100_m = []

for app in google_english:
    n_installs = app[5]
    n_installs = n_installs.replace(',', '')
    n_installs = n_installs.replace('+', '')
    if (app[1] == 'COMMUNICATION') and (float(n_installs) < 100000000):
        under100_m.append(float(n_installs))
        
sum(under100_m) / len(under100_m)


# We see the same pattern for the video players category, which is the runner-up with 24,727,872 installs. The market is dominated by apps like Youtube, Google Play Movies & TV, or MX Player. The pattern is repeated for social apps (where we have giants like Facebook, Instagram, Google+, etc.), photography apps (Google Photos and other popular photo editors), or productivity apps (Microsoft Word, Dropbox, Google Calendar, Evernote, etc.).
# 
# Again, the main concern is that these app genres might seem more popular than they really are. Moreover, these niches seem to be dominated by a few giants who are hard to compete against.
# 
# The game genre seems pretty popular, but previously we found out this part of the market seems a bit saturated, so we'd like to come up with a different app recommendation if possible.
# 
# The books and reference genre looks fairly popular as well, with an average number of installs of 8,767,811. It's interesting to explore this in more depth, since we found this genre has some potential to work well on the App Store, and our aim is to recommend an app genre that shows potential for being profitable on both the App Store and Google Play.
# 
# Let's take a look at some of the apps from this genre and their number of installs:

# In[74]:


for app in google_english:
    if app[1] == 'BOOKS_AND_REFERENCE':
        print(app[0], ':', app[5])


# The book and reference genre includes a variety of apps: software for processing and reading ebooks, various collections of libraries, dictionaries, tutorials on programming or languages, etc. It seems there's still a small number of extremely popular apps that skew the average:

# In[75]:


for app in google_english:
    if app[1] == 'BOOKS_AND_REFERENCE' and (app[5] == '1,000,000,000+'
                                            or app[5] == '500,000,000+'
                                            or app[5] == '100,000,000+'):
        print(app[0], ':', app[5])


# However, it looks like there are only a few very popular apps, so this market still shows potential. Let's try to get some app ideas based on the kind of apps that are somewhere in the middle in terms of popularity (between 1,000,000 and 100,000,000 downloads):

# In[76]:


for app in google_english:
    if app[1] == 'BOOKS_AND_REFERENCE' and (app[5] == '1,000,000+'
                                            or app[5] == '5,000,000+'
                                            or app[5] == '10,000,000+'
                                            or app[5] == '50,000,000+'):
        print(app[0], ':', app[5])


# This niche seems to be dominated by software for processing and reading ebooks, as well as various collections of libraries and dictionaries, so it's probably not a good idea to build similar apps since there'll be some significant competition.
# 
# We also notice there are quite a few apps built around the book Quran, which suggests that building an app around a popular book can be profitable. It seems that taking a popular book (perhaps a more recent book) and turning it into an app could be profitable for both the Google Play and the App Store markets.
# 
# However, it looks like the market is already full of libraries, so we need to add some special features besides the raw version of the book. This might include daily quotes from the book, an audio version of the book, quizzes on the book, a forum where people can discuss the book, etc.

# ## Conclusions
# In this project, we analyzed data about the App Store and Google Play mobile apps with the goal of recommending an app profile that can be profitable for both markets.
# 
# We concluded that taking a popular book (perhaps a more recent book) and turning it into an app could be profitable for both the Google Play and the App Store markets. The markets are already full of libraries, so we need to add some special features besides the raw version of the book. This might include daily quotes from the book, an audio version of the book, quizzes on the book, a forum where people can discuss the book, etc.

# In[ ]:




