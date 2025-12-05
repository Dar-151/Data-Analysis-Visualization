#!/usr/bin/env python
# coding: utf-8

# # Data extracting/visualization

# ## Darian Kacanski

# # 11/11/2025

# ## Importing libraries

# In[1]:


import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
sns.set_theme(style="whitegrid")
fmt_billions = FuncFormatter(lambda x, pos: f'${x:,.0f}')


# ## grabbing first link

# In[2]:


url = "https://en.wikipedia.org/wiki/List_of_American_films_of_2020"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
status = response.status_code

if status == 200:
    page = response.text
    soup = bs(page, "html.parser")
    print(" Success! Page loaded.")
else:
    print(f" Oops! Received status code {status}")


# ## using beautiful soup to navigate HTML

# In[3]:


print(soup.prettify())
type(soup)


# ## getting the table from the URL

# ### I had to use much more code because wikipedia used rowspan which made it harder to grab the rows

# #### I had AI help me progress through this issue

# In[4]:


# making a empty list
movie_list = []
#finding class name named wikitable 
table = soup.find("table", class_="wikitable").tbody
#this is AI made but variables to help handle row span
carry_distributor = None
carry_left = 0
#loop through the table
for tr in table.find_all("tr"):
    tds = tr.find_all("td")
    # This is to handle the row spans
    if len(tds) < 3:        # skip non-data rows
        continue

    Rank  = tds[0].get_text(strip=True)
    Title = tds[1].get_text(strip=True)
    #this is to go through with normal rows without rowspan
    if len(tds) == 4:       # distributor cell present
        dist_td = tds[2]
        Distributor = dist_td.get_text(strip=True)
        Gross = tds[3].get_text(strip=True)

        # start/refresh carry if this cell has a rowspan
        if dist_td.has_attr("rowspan"):
            carry_left = int(dist_td["rowspan"]) - 1
            carry_distributor = Distributor
        else:
            carry_left = 0
            carry_distributor = None
    #If the row has 3 columns, that means it is shared
    else:                   # len(tds) == 3 -> distributor omitted due to rowspan
        Distributor = carry_distributor
        Gross = tds[2].get_text(strip=True)
        if carry_left >   0:
            carry_left -= 1
            if carry_left == 0:
                carry_distributor = None
    #make the information into a list
    movie_list.append({
        "Rank": Rank, "Title": Title,
        "Distributor": Distributor, "Domestic Gross": Gross
    })
#print list to make sure it worked
print(movie_list)

movie_df_2020 = pd.DataFrame(movie_list)


# ## what the data looks like in a dataframe

# In[5]:


movie_df_2020


# # Grabbing link 

# In[6]:


url = "https://en.wikipedia.org/wiki/List_of_American_films_of_2021"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
status = response.status_code

if status == 200:
    page = response.text
    soup = bs(page, "html.parser")
    print(" Success! Page loaded.")
else:
    print(f" Oops! Received status code {status}")


# # using pretty soup

# In[7]:


print(soup.prettify())
type(soup)


# ## scraping the data from URL 2021

# ### I having trouble grabbing the table because I was grabbing a different table so I had AI help.

# #### This was easier because no rowspans

# In[8]:


# Find the right table
tables = soup.find_all("table", class_="wikitable")
# to store the table
wikitable = None
# Used captions to find the title of table
for t in tables:
    cap = t.find("caption")
    if cap and "Highest-grossing films of 2021" in cap.get_text(strip=True):
        wikitable = t.tbody
        break
# if couldn't find the table I have this if
if not wikitable:
    raise ValueError("Could not find the Box Office table.")

# Extract rows, including the rank <th> and rowspan fix
movie_list = []
last_dist = None
# loop through the rows
for row in wikitable.find_all("tr"):
    cells = row.find_all(["th", "td"])
    # skip empty I only have this as a precaution becuase it was somehow grabbing a different table with my other code 
    if not cells:
        continue
    # Skip header row for rank and title
    if cells[0].name == "th" and cells[0].get_text(strip=True).lower() in {"rank", "title"}:
        continue
    #handling normal without rowspan
    if len(cells) >= 4:
        rank  = cells[0].get_text(strip=True)
        title = cells[1].get_text(strip=True)
        dist  = cells[2].get_text(strip=True)
        gross = cells[3].get_text(strip=True)
        last_dist = dist
        # handling rowspan
    elif len(cells) == 3:
        rank  = cells[0].get_text(strip=True)
        title = cells[1].get_text(strip=True)
        dist  = last_dist
        gross = cells[2].get_text(strip=True)
    else:
        continue
    #making a list 
    movie_list.append({
        "Rank": rank,
        "Title": title,
        "Distributor": dist,
        "Domestic Gross": gross
    })
#printing the table
import pandas as pd
movie_df_2021 = pd.DataFrame(movie_list)
movie_df_2021


# ## This is to grab the code for 2022

# In[9]:


url = "https://en.wikipedia.org/wiki/List_of_American_films_of_2022"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
status = response.status_code

if status == 200:
    page = response.text
    soup = bs(page, "html.parser")
    print(" Success! Page loaded.")
else:
    print(f" Oops! Received status code {status}")


# ## using pretty soup

# In[10]:


print(soup.prettify())
type(soup)


# ## This code was same as 2020 but just reformatted code

# In[11]:


# empty String
movie_list = []
table = soup.find("table", class_="wikitable").tbody
#variables
carry_distributor = None
carry_left = 0
#for loop to get data
for tr in table.find_all("tr"):
    cells = tr.find_all(["th","td"])
    if len(tds) < 3:        # skip non-data rows
        continue

    Rank  = cells[0].get_text(strip=True)
    Title = cells[1].get_text(strip=True)
    # to handle cells
    if len(cells) >= 4:       # distributor cell present
        dist_td = cells[2]
        Distributor = dist_td.get_text(strip=True)
        Gross = cells[3].get_text(strip=True)

        # start/refresh carry if this cell has a rowspan
        if dist_td.has_attr("rowspan"):
            carry_left = int(dist_td["rowspan"]) - 1
            carry_distributor = Distributor
        else:
            carry_left = 0
            carry_distributor = None

    else:                   # len(tds) == 3 -> distributor omitted due to rowspan
        Distributor = carry_distributor
        Gross = cells[2].get_text(strip=True)
        if carry_left >   0:
            carry_left -= 1
            if carry_left == 0:
                carry_distributor = None

    movie_list.append({
        "Rank": Rank, "Title": Title,
        "Distributor": Distributor, "Domestic Gross": Gross
    })

print(movie_list)


# ## put dataframe into movie variable to use later to combine

# ### I got the headers but I will fix when I do the cleaning 

# In[12]:


movie_df_2022 = pd.DataFrame(movie_list)
movie_df_2022


# ## Getting the link and doing beautiful soup in same step

# In[13]:


url = "https://en.wikipedia.org/wiki/List_of_American_films_of_2023"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
status = response.status_code

if status == 200:
    page = response.text
    soup = bs(page, "html.parser")
    print(" Success! Page loaded.")
else:
    print(f" Oops! Received status code {status}")
print(soup.prettify())
type(soup)


# # this is the same as 2021 I just reformatted for 2023 because tables were the same

# In[14]:


# Find the right table
tables = soup.find_all("table", class_="wikitable")
# variable for wikitable
wikitable = None
# this is to get the table title
for t in tables:
    cap = t.find("caption")
    if cap and "Highest-grossing films of 2023" in cap.get_text(strip=True):
        wikitable = t.tbody
        break
# if couldn't get it have a fallback
if not wikitable:
    raise ValueError("Could not find the Box Office table.")

# Extract rows, including the rank <th> and rowspan fix
movie_list = []
last_dist = None
#grab the data from the table
for row in wikitable.find_all("tr"):
    cells = row.find_all(["th", "td"])
    if not cells:
        continue
    if cells[0].name == "th" and cells[0].get_text(strip=True).lower() in {"rank", "title"}:
        continue

    if len(cells) >= 4:
        rank  = cells[0].get_text(strip=True)
        title = cells[1].get_text(strip=True)
        dist  = cells[2].get_text(strip=True)
        gross = cells[3].get_text(strip=True)
        last_dist = dist
    elif len(cells) == 3:
        rank  = cells[0].get_text(strip=True)
        title = cells[1].get_text(strip=True)
        dist  = last_dist
        gross = cells[2].get_text(strip=True)
    else:
        continue

    movie_list.append({
        "Rank": rank,
        "Title": title,
        "Distributor": dist,
        "Domestic Gross": gross
    })

import pandas as pd
movie_df_2023 = pd.DataFrame(movie_list)
movie_df_2023


# ##  getting link for 2024 and using beautiful soup   

# In[15]:


url = "https://en.wikipedia.org/wiki/List_of_American_films_of_2024"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
status = response.status_code

if status == 200:
    page = response.text
    soup = bs(page, "html.parser")
    print(" Success! Page loaded.")
else:
    print(f" Oops! Received status code {status}")
print(soup.prettify())
type(soup)


# ## Same code for table 2020 to handle rowspan

# In[16]:


#empty list
movie_list = []
# this it help find the table
table = soup.find("table", class_="wikitable").tbody
#variables for to help handle rowspan
carry_distributor = None
carry_left = 0
# this is to get the data
for tr in table.find_all("tr"):
    cells = tr.find_all(["th","td"])
    if len(tds) < 3:        # skip non-data rows
        continue

    Rank  = cells[0].get_text(strip=True)
    Title = cells[1].get_text(strip=True)

    if len(cells) >= 4:       # distributor cell present
        dist_td = cells[2]
        Distributor = dist_td.get_text(strip=True)
        Gross = cells[3].get_text(strip=True)

        # start/refresh carry if this cell has a rowspan
        if dist_td.has_attr("rowspan"):
            carry_left = int(dist_td["rowspan"]) - 1
            carry_distributor = Distributor
        else:
            carry_left = 0
            carry_distributor = None

    else:                   # len(tds) == 3 -> distributor omitted due to rowspan
        Distributor = carry_distributor
        Gross = cells[2].get_text(strip=True)
        if carry_left >   0:
            carry_left -= 1
            if carry_left == 0:
                carry_distributor = None

    movie_list.append({
        "Rank": Rank, "Title": Title,
        "Distributor": Distributor, "Domestic Gross": Gross
    })
print(movie_list)


# # this is it in a dataframe is also got the heading I can clean after I scrape all the websites

# In[17]:


movie_df_2024 = pd.DataFrame(movie_list)
movie_df_2024


# ## This is to grab the url for 2025 and using beautiful soup

# In[18]:


url = "https://en.wikipedia.org/wiki/List_of_American_films_of_2025"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
status = response.status_code

if status == 200:
    page = response.text
    soup = bs(page, "html.parser")
    print(" Success! Page loaded.")
else:
    print(f" Oops! Received status code {status}")
print(soup.prettify())
type(soup)


# ## this is similar to what I did for 2021 but couldn't grab the title because they didn't add a title to the table

# ### I needed help from AI to handle that because the other options I tried it grabbed the wrong table

# In[19]:


# Find the right table
tables = soup.find_all("table", class_="wikitable")
wikitable = None

wanted = {"rank", "title", "distributor", "domestic gross"}   # lowercased

for t in tables:
    # collect all header texts from this table
    ths = [th.get_text(strip=True).lower() for th in t.find_all("th")]
    if wanted.issubset(set(ths)):
        wikitable = t.tbody
        break

if not wikitable:
    raise ValueError("Could not find a table with Rank/Title/Distributor/Domestic gross headers.")



# Extract rows, including the rank <th> and rowspan fix
movie_list = []
last_dist = None

for row in wikitable.find_all("tr"):
    cells = row.find_all(["th", "td"])
    if not cells:
        continue
    if cells[0].name == "th" and cells[0].get_text(strip=True).lower() in {"rank", "title"}:
        continue

    if len(cells) >= 4:
        rank  = cells[0].get_text(strip=True)
        title = cells[1].get_text(strip=True)
        dist  = cells[2].get_text(strip=True)
        gross = cells[3].get_text(strip=True)
        last_dist = dist
    elif len(cells) == 3:
        rank  = cells[0].get_text(strip=True)
        title = cells[1].get_text(strip=True)
        dist  = last_dist
        gross = cells[2].get_text(strip=True)
    else:
        continue

    movie_list.append({
        "Rank": rank,
        "Title": title,
        "Distributor": dist,
        "Domestic Gross": gross
    })

import pandas as pd
movie_df_2025 = pd.DataFrame(movie_list)
movie_df_2025


# ## making the columns match

# In[20]:



for df in [movie_df_2020, movie_df_2021, movie_df_2022, movie_df_2024, movie_df_2025]:
    df.rename(columns={"Domestic gross": "Domestic Gross"}, inplace=True)
    # drop any header rows that slipped in
    df.drop(df.index[df["Rank"] == "Rank"], inplace=True)


# ## add the year column so I can do better analysis

# In[21]:


movie_df_2020["Year"] = 2020
movie_df_2021["Year"] = 2021
movie_df_2022["Year"] = 2022
movie_df_2024["Year"] = 2024
movie_df_2025["Year"] = 2025


# # Combining the dataframes

# ### I did use a AI I wasn't familiar with the concat function

# In[22]:


# this combines all of dataframes and makes the index match with the combining
all_movies = pd.concat(
    [movie_df_2020, movie_df_2021, movie_df_2022, movie_df_2024, movie_df_2025],
    ignore_index=True
)


# # cleaning the data

# In[33]:


# Take out $ signs and commas so we can turn it into numbers
all_movies["Domestic Gross"] = (
    all_movies["Domestic Gross"]
    .astype(str)                 # make sure everything is a string first
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
)

# turn Rank and Domestic Gross into numeric values (so we can do math later)
all_movies["Rank"] = all_movies["Rank"].astype(int)
all_movies["Domestic Gross"] = all_movies["Domestic Gross"].astype(float)

all_movies


# # Which year from 2020-25 had the highest box office?

# ## becuase I am looking across mutiple years had to use a groupby and I learned it from AI

# In[28]:


# making the data group by years
yearly_totals = (all_movies
                 .groupby("Year", as_index=False)["Domestic Gross"].sum())

ax = sns.barplot(data=yearly_totals, x="Year", y="Domestic Gross")
# making the y axis show billions because otherwise the decimals are hard to tell 
ax.yaxis.set_major_formatter(fmt_billions)
ax.bar_label(ax.containers[0], fmt='%.0f')
plt.title("Total Domestic Gross (Top-10) by Year")
plt.ylabel("Domestic Gross")
plt.xlabel("Year")


# # How  did the top gross change from each year?

# ## I chose a line plot because it shows the best trends over time

# In[29]:


# groups each year
yearly_top = (all_movies
              .groupby("Year", as_index=False)["Domestic Gross"].max())

ax = sns.lineplot(data=yearly_top, x="Year", y="Domestic Gross", marker="o")
# same this shows the billions
ax.yaxis.set_major_formatter(fmt_billions)
plt.title("Highest Single-Film Gross by Year")
plt.ylabel("Domestic Gross")
plt.xlabel("Year")


# # Which studio appeared in the top 10 across 6 years?

# ## Made the numbers on the bottom to make easier to read

# In[34]:


studio_counts = (all_movies["Distributor"]
                 # counting the values 
                 .value_counts()
                 .head(10)
                 #the distributor names were dissappear so running this fixes it
                 .reset_index()
                 # renamed to make it clearer
                 .rename(columns={"index":"Distributor", "Distributor":"Count"}))

ax = sns.barplot(data=studio_counts, y="Distributor", x="Count")
ax.bar_label(ax.containers[0], padding=3)
plt.title("Top Distributors by # of Top-10 Appearances (2020–2025)")
plt.xlabel("Appearances")
plt.ylabel("")


# # Which film had the highest gross of all?

# ## I saw instead of finding the max I could nlargest so I decided to do that instead because I was interested on how it worked/ it is more effiecent

# ## The x axis was cluttered so I made the plot bigger

# In[31]:


#this grabs the top 10 from the gross column
top_overall = all_movies.nlargest(10, "Domestic Gross")  # change 10→1 to show only winner
# makes it bigger
fig, ax = plt.subplots(figsize=(11,6))
sns.barplot(data=top_overall, y="Title", x="Domestic Gross", ax=ax)
# helps with the x axis formatting
ax.yaxis.set_tick_params(labelsize=9)
ax.xaxis.set_major_formatter(fmt_billions)
ax.bar_label(ax.containers[0], fmt='%.0f', padding=3)
plt.title("Top Domestic Grossing Films (Overall)")
plt.xlabel("Domestic Gross")
plt.ylabel("")
plt.tight_layout()




# # Which percentage of the top 10 films each year were released by Disney?

# In[32]:


per_disney = (all_movies.assign(is_disney = all_movies["Distributor"]
                                #makes a true false for if it was made by disney
                                .str.contains("Disney", case=False, na=False))
                         .groupby("Year")["is_disney"]
                         .mean()
                         .mul(100)
                         .reset_index()
                         .rename(columns={"is_disney":"Percent"}))

ax = sns.barplot(data=per_disney, x="Year", y="Percent")
ax.bar_label(ax.containers[0], fmt='%.0f%%')
plt.ylim(0, 100)
plt.title("Share of Top-10 Films Distributed by Disney")
plt.ylabel("Percent of Top-10")
plt.xlabel("Year")


# In[ ]:




