from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import scipy.special
#import matplotlib.mlab as mlab
#import matplotlib.pyplot as plt
from bokeh.embed import components
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file, ColumnDataSource
from bokeh.models import HoverTool
#import csv
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral3
from bokeh.layouts import widgetbox
import os


app = Flask(__name__)
filename1 = "heading.csv"

fn1 = os.path.join(os.path.dirname(__file__), filename1)

with open(fn1) as f:
    lines = f.readlines()

XL1  = list(map(lambda x:x.strip(),lines))

#print(XL2)
feature_names = (XL1)

filename2 = "Deaths_by_year_male"

fn2 = os.path.join(os.path.dirname(__file__), filename2)
with open(fn2) as g:
    lines1 = g.readlines()

XL2  = list(map(lambda x:x.strip(),lines1))


B = []

for i in XL2:
    if len(i)==0:
        B.append([])
    else:
        B.append([float(j) for j in i.split(',')])





def create_figure(current_feature_name,bins):
    current_feature_position = feature_names.index(current_feature_name)
    x = B[current_feature_position]

    lst = B[current_feature_position]
    Sums = sum(B[current_feature_position])
    counts = len(B[current_feature_position])
    Avg = Sums/(max(counts,1))
    Avg = round(float(Avg),1)
    counts = int(counts)
    counts1 = ("{:,}".format(counts))
    Barray = np.asarray(lst)
    Std_Dev = (sum((Barray - Avg)**2)/(max(counts,1)))**.5
    Std_Dev = round(float(Std_Dev),1)

    hover = HoverTool(
        tooltips=[
            ("Age", "$x{int}"),
            ("# Deaths","$y{'0,0'}")
            ]
        )

    p1 = figure(title="Distribution of Deaths",tools=[hover],
            background_fill_color="#E8DDCB",x_axis_label='Age at Death',
            y_axis_label = 'Number of Deaths')

    hist, edges = np.histogram(x, range= (0,115),density=False, bins=115)

    p1.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
        fill_color="#036564", line_color="#033649")

    #p1.rect(x=hist,y= edges, width=0.2, height=40, color="#CAB2D6",
    #        height_units="screen")



    return gridplot(p1, ncols=2, plot_width=400, plot_height=400, toolbar_location=None), Avg, Std_Dev, counts1


# Index page
@app.route('/')
def index():
  # Determine the selected feature
 	current_feature_name = request.args.get("feature_name")
 	if current_feature_name == None:
 		 current_feature_name = "Male"

    # Create the plot
 	plot, Avg, Std_Dev, counts1 = create_figure(current_feature_name,115)

    # Embed plot into HTML via Flask Render
 	script, div = components(plot)
 	return render_template("deaths_male.html",  counts1= counts1, Avg = Avg,
         Std_Dev = Std_Dev, script=script, div=div, feature_names= feature_names, current_feature_name=current_feature_name)


# With debug=True, Flask server will auto-reload
# when there are code changes
if __name__ == '__main__':
	app.run(debug=True)
