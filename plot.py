from webcam_motion_detector import df
import pandas
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models import HoverTool

df["NEW_Start"] = df["Start"].dt.strftime("%d-%m-%y %H:%M:%S")
df["NEW_End"] = df["End"].dt.strftime("%d-%m-%y %H:%M:%S")

cds = ColumnDataSource(df)

df["Start"] = pandas.to_datetime(df["Start"],format="%d/%m/%y %H:%M:%S")
df["End"] = pandas.to_datetime(df["End"],format="%d/%m/%y %H:%M:%S")

hover = HoverTool(tooltips=[("START","@NEW_Start"),("END","@NEW_End")])

p = figure(plot_height=400,plot_width=1200, x_axis_type="datetime",tools=[hover])
p.yaxis.minor_tick_line_color = "White"
p.ygrid[0].ticker.desired_num_ticks = 1

p.quad(top=1,bottom=0,left=df["Start"],right=df["End"], source = cds, color="Green", alpha = 0.5)

output_file("new.html")
show(p)
