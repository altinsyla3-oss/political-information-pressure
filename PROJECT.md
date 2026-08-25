# 60-second project explanation

I built this project to examine whether global conflict-event activity shows statistically unusual spikes and short-term temporal persistence.

Using 180 consecutive days of GDELT Event Database files, I construct a daily measure of political event pressure based on the share of all recorded events with negative Goldstein Scale values.

I then use a lagged rolling baseline to identify anomalous periods with z-scores, estimate a lag-1 OLS model to test whether elevated event pressure persists from one day to the next, and use an Augmented Dickey-Fuller test to assess stationarity.

The final analysis identified 15 unusually high-pressure periods and substantial short-term persistence in conflict-event pressure.

I treat this as an exploratory computational social-science project rather than evidence that event volume itself causes cognitive overload. Its purpose is to demonstrate how structured event data can be used to operationalize and test temporal patterns in political information environments.
