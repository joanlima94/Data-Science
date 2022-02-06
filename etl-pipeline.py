import pandas as pd
import requests
import matplotlib.pyplot as plt

movie_list = []

api_key = '<Your Api_key>'

#Etapa de extração.

for movie_id in range(1,5000):
    url = 'https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id,api_key)
    r = requests.get(url)
    movie_list.append(r.json())

#Etapa de transformação.

df = pd.DataFrame.from_dict(movie_list)

genres_list = df['genres'].to_list()


df['release_date'] = pd.to_datetime(df['release_date'])
df_sorted = df.sort_values('revenue',ascending = False)
df_10 = df_sorted.head(10)

#Etapa de carga e visualização

title = df_10['title'].dropna().to_list()
revenue = df_10['revenue'].dropna().to_list() 
plt.style.use('ggplot')
plt.barh(title,revenue)
plt.gca().invert_yaxis()
plt.title('Revenue by Title')
plt.ylabel('Title')
plt.xlabel('Revenue (USD)')
plt.savefig('Revenue_by_title_tmdb')
plt.show()




