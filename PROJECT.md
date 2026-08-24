# 60-second project explanation

I built this project to operationalize one dimension of information overload as **information pressure**.

Using the GDELT DOC 2.0 API, I retrieve a time series of news coverage related to disinformation and digital influence operations. I normalize matched coverage by the total volume of news monitored by GDELT, then construct a lagged rolling baseline and identify statistically unusual spikes using z-scores.

I also estimate a lag-1 OLS model to examine whether elevated information pressure persists from one period to the next, and I use an Augmented Dickey-Fuller test to assess stationarity.

I am careful not to claim that media volume itself proves cognitive overload. Instead, this creates a reproducible macro-level exposure indicator that could later be combined with experiments or survey data to test whether information pressure affects recall, trust, heuristic processing, or susceptibility to manipulation.
