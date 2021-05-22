import pandas as pd
import requests 
import numpy as np
from bs4 import BeautifulSoup
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.plotting import figure, output_file, show
from bokeh.palettes import Spectral10

TOOLS = "hover,pan,wheel_zoom,box_zoom,reset,save,box_select"

req = requests.get('https://www.fundsexplorer.com.br/ranking')

if req.status_code == 200:
    print('Requisição bem sucedida!')
    content = req.content
    
soup = BeautifulSoup(content, 'html.parser')
table = soup.find(name='table')
table_str = str(table)
df = pd.read_html(table_str)[0]
new_dy = []
for i in df['DividendYield']:
    i = str(i)
    novo_dy = i.replace("%","").replace(",",".")
    new_dy.append(novo_dy)
new_dy =list(np.float_(new_dy))
new_dy = pd.Series(new_dy).fillna(0).tolist()

setores = pd.unique(df.Setor)
leg_cols = dict(zip(setores,Spectral10))
colors = [list(leg_cols.values())[i%10] for i in range(len(setores))]
region_cols = [leg_cols[j] for j in list(df['Setor'])]

location_source = ColumnDataSource(
    data = {
        "x": list(df['P/VPA']/100),
        "y": new_dy,
        "colors": region_cols,
        "fundo": list(df['Códigodo fundo']),
        "setores":list(df['Setor']),
        "Dividendo":list(df['Dividendo']),
        "Price":list(df['Preço Atual']),
    }
)

fig = figure(title="FII's Analysis",x_axis_location = "below", tools=TOOLS,
    x_axis_label="P/VPA", y_axis_label="Dividend Yield - DY(%)")
fig.plot_width  = 800
fig.plot_height = 800
fig.circle("x", "y", size=10, source=location_source, color="colors", 
           line_color = None,legend_field = "setores")
hover = fig.select(dict(type = HoverTool))
hover.tooltips = {
    "Sigla": "@fundo",
    "setor": "@setores",
    "Dividendo":"@Dividendo",
    "Preço Atual":"@Price",
    "P/VPA,Dy": "($x, $y)",
}

fig.legend.location = "top_right"
fig.legend.click_policy="hide"

output_file("FII's.html")

show(fig)
