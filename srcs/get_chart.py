import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash import html

# Create the chart with the stock price. First, set the size of the chart depending
# on the screen size. Then, determine which lines have to be included in the chart
# and create the chart. Add additional lines / figures for indicators, which require
# some different design elements. Finally, set the design of the chart and remove the
# x-axis if a second chart is displayed below.
def create_chart(hist, indicator, include_indicator, date, width):
	if width >= 1200:
		height_large = 500
		height_small = 450
	else:
		height_large = max(100, width * 500 / 1200)
		height_small = max(100, width * 450 / 1200)
	
	displayed_lines = ['Close']
	no_line = ['Fibonacci levels', '21 day Bollinger bands', 'Parabolic SAR']
	if include_indicator  and not indicator in no_line:
		displayed_lines.append(indicator)

	fig, df = get_chart(hist, date, displayed_lines)

	if (indicator == 'Fibonacci levels'):	
		min_fib = min(df['Close'])
		max_fib = max(df['Close'])
		fig.add_hline(y = min_fib, line_width = 2, line_color = 'red')
		fig.add_hline(y = min_fib + (max_fib - min_fib) * 0.236, line_width = 2, line_color = 'red')
		fig.add_hline(y = min_fib + (max_fib - min_fib) * 0.382, line_width = 2, line_color = 'red')
		fig.add_hline(y = min_fib + (max_fib - min_fib) * 0.5, line_width = 2, line_color = 'red')
		fig.add_hline(y = min_fib + (max_fib - min_fib) * 0.618, line_width = 2, line_color = 'red')
		fig.add_hline(y = min_fib + (max_fib - min_fib) * 0.764, line_width = 2, line_color = 'red')
		fig.add_hline(y = max_fib, line_width = 2, line_color = 'red')

	elif indicator == '21 day Bollinger bands':
		fig2 = go.Figure()
		fig2.add_traces(go.Scatter(x = df['Date'], y = df[indicator + '_low'],
			line = dict(color = 'red')))

		fig2.add_traces(go.Scatter(x = df['Date'], y = df[indicator + '_high'],
			line = dict(color = 'red'),
			fill = 'tonexty', 
			fillcolor = 'rgba(255,0,0,0.5)'))

		fig.data[0].line.color = 'blue'
		fig2.add_traces(data = fig.data)
		fig = fig2

	elif indicator == 'Parabolic SAR':
		fig2 = px.scatter(x = df['Date'], y = df['PSAR'], color_discrete_sequence = ['red'])
		fig = go.Figure(data = fig.data+fig2.data)

	update_layout(fig, displayed_lines, indicator)

	if not include_indicator:
		fig.update_layout(
			xaxis = {
				'visible': False
			},
			height = height_small
		)
	else:
		fig.update_layout(
			height = height_large
		)

	return fig

# Create a chart that includes the indicator only. First, set the size of the chart
# depending on the screen size. Then, determine which lines have to be included in
# the chart and create and update the chart. 
def create_indicator_chart(hist, indicator, date, width):
	if width >= 1200:
		height = 240
	else:
		height = max(100, width * 240 / 1200)

	indicator_list = [indicator]
	if indicator == '12 / 26 day MACD':
		indicator_list.append(indicator+' moving average')
	if indicator == '25 day Aroon indicator':
		indicator_list = [indicator+' up', indicator+' down']
	if indicator == '14 day stochastic oscillator':
		indicator_list.append(indicator+' moving average')

	fig, df = get_chart(hist, date, indicator_list)
	update_layout(fig, indicator_list, indicator)

	fig.update_layout(
		height = height
	)

	return fig

# Create the chart that displays the included lines for the selected time period.
def get_chart(hist, date, displayed_lines):
	hist['Date'] = pd.to_datetime(hist['Date'], format = '%Y-%m-%d')
	df = hist.loc[(hist['Date'] >= date)]

	fig = px.line(
		df,
		x = 'Date',
		y = displayed_lines,
		title = '',
		labels = {
			'Date': '',
			'value': ''
		}
	)

	return fig, df

# Update the layout of the chart. 
def update_layout(fig, displayed_lines, indicator):
	fig.update_layout(
		showlegend = False,
		margin = dict(l = 75, r = 50, t = 10, b = 0),
		plot_bgcolor = 'rgba(0,0,0,0.85)'
	)

	fig.update_yaxes(gridcolor = 'grey', zeroline = False)
	fig.update_xaxes(showgrid = False)
	if not indicator == '21 day Bollinger bands':
		fig.data[0].line.color = 'blue'
		if len(displayed_lines) == 2:
			fig.data[1].line.color = 'red'

# Create the news feed for the stock. For each stock, up to 3 (latest) news items are includeed.
def news_feed(news):
	if len(news) > 3:
		num_news = 3
	else:
		num_news = len(news)
	news_list = []
	for i in range(num_news):
		news_item = html.Li(
			html.P([
				news[i]['title'],
				' (',
				html.I(news[i]['publisher']),
				') \U0001F449 ',
				html.A('read more', href = news[i]['link'], target = '_blank')
			], className = 'news-list')
		)
		news_list.append(news_item)
	news_feed = html.Div([
		html.Ul(news_list)
	])
	return news_feed
