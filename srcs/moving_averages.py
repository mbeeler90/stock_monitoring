# Calculating Bollinger bands with the upper / lower band 2 standard deviations
# away from the average of the true price.
def bollinger_bands(hist, indicator, look_back):      
	hist['TP'] = (hist['High'] + hist['Low'] + hist['Close']) / 3 
	hist[indicator] = hist['TP'].rolling(look_back).mean()
	hist[indicator + '_std'] = hist['TP'].rolling(look_back).std() 
	hist[indicator + '_low'] = hist[indicator] - 2 * hist[indicator + '_std'] 
	hist[indicator + '_high'] = hist[indicator] + 2 * hist[indicator + '_std']

# Calculation of double exponential moving average. Adds the exponential moving average
# to the exponential moving average and gives more weight to recent days.
def double_exponential_moving_average(hist, indicator, look_back, price = 'Close'):
	if not str(look_back) + ' day EMA' in hist.columns:
		exponential_moving_average(hist, str(look_back) + ' day EMA', look_back, price)
	multiplier = 2 / (1 + look_back) 
	for i in hist.index:
		if i < look_back - 1:
			continue
		elif i == look_back - 1:
			hist.loc[i, 'EMA_sqrt_' + str(look_back)] = hist.loc[i, str(look_back) + ' day EMA']
		else:
			hist.loc[i, 'EMA_sqrt_' + str(look_back)] = hist.loc[i, str(look_back) + ' day EMA'] * multiplier + hist.loc[i - 1, 'EMA_sqrt_' + str(look_back)] * (1 - multiplier)
	hist[indicator] = 2 * hist[str(look_back) + ' day EMA'] - hist['EMA_sqrt_' + str(look_back)]

# Calculation of exponential moving average. Calculates an average where recent periods is given
# a higher weight.
def exponential_moving_average(hist, indicator, look_back, price = 'Close'):
	if not str(look_back) + ' day simple MA' in hist.columns:
		moving_average(hist, str(look_back) + ' day simple MA', look_back, price)
	multiplier = 2 / (1 + look_back) 
	for i in hist.index:
		if i < look_back - 1:
			continue
		elif i == look_back - 1:
			hist.loc[i, indicator] = hist.loc[i, str(look_back) + ' day simple MA']
		else:
			hist.loc[i, indicator] = hist.loc[i, price] * multiplier + hist.loc[i - 1, indicator] * (1 - multiplier)

# Add all values from 0 to n.
def calculate_sum(n):
    my_sum = 0
    control=0
    while control <= n:
        my_sum += control
        control+= 1
    return my_sum

# Calculate linearly weighted moving average. The last period is multiplied by the look_back
# period. Each prior period is multiplied by n - 1, where the initial n = look_back period.
# All values are added up and devided by the sum of range(look_back) to get the average price.
def linear_weighted_moving_average(hist, indicator, look_back, price = 'Close'):        
	if not str(look_back) + ' day simple MA' in hist.columns:
		moving_average(hist, str(look_back) + ' day simple MA', look_back, price)
	for i in hist.index:
		if i >= look_back - 1:
			sum_prices = 0
			for number in range(look_back):
				sum_prices += hist.loc[i - number, price] * (look_back - number)
			hist.loc[i, indicator] = sum_prices / calculate_sum(look_back)

# Calculation of simple moving average.
def moving_average(hist, indicator, look_back, price = 'Close'):
	hist[indicator] = hist[price].rolling(look_back).mean()

# Calculation of moving average conversion devergence. Calculation of two exponential moving
# averages. The longer exponential moving average substracted from the longer to get the
# MACD. Finally, the simple moving average of the MACD is calculated.
def MACD(hist, indicator, low_avg, high_avg, look_back, price = 'Close'):
	for days in [low_avg, high_avg]:
		if not str(days) + ' day EMA' in hist.columns:
			exponential_moving_average(hist, str(days) + ' day EMA', days, price)
	hist[indicator] = hist[str(low_avg) + ' day EMA'] - hist[str(high_avg) + ' day EMA']
	hist[indicator + ' moving average'] = hist[indicator].rolling(look_back).mean()
