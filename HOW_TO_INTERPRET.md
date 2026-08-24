# Methodological Interpretation Guide

This document summarizes how the main outputs should be interpreted.

## Information-pressure time series

`figures/information_pressure_timeseries.png`

The time series shows the share of GDELT-monitored news coverage matching the project's digital-influence query.

The lagged rolling baseline represents the recent expected level of topic attention.

## Rolling z-score

`figures/rolling_zscore.png`

The rolling z-score measures how unusual the current observation is relative to the preceding baseline.

Approximate interpretation:

- `z ≈ 0` — typical
- `z ≈ 1` — elevated
- `z ≥ 2` — unusual spike
- `z ≥ 3` — highly unusual spike

The default analysis uses `z ≥ 2` as the spike threshold.

## Detected spikes

`results/spike_days.csv`

This file ranks periods with unusually high relative coverage.

These observations should not automatically be interpreted as evidence of coordinated influence activity. A separate event-level investigation would be required to identify the political or informational episode associated with each spike.

## Lagged OLS model

`results/model_summary.txt`

The `lag1_share` coefficient estimates whether information pressure in the previous period predicts information pressure in the current period.

A positive and statistically significant coefficient is consistent with temporal persistence.

This is an associative result and does not establish causality.

## Augmented Dickey-Fuller test

The ADF test evaluates whether the series is consistent with stationarity.

A common interpretation is:

- `p < 0.05` — evidence against a unit root
- `p ≥ 0.05` — insufficient evidence to reject a unit root

This diagnostic helps assess whether additional time-series transformations may be required before drawing stronger inferential conclusions.

## Substantive interpretation

The defensible interpretation of the project is:

> The analysis constructs a macro-level indicator of unusually high information pressure around digital influence and information-manipulation topics.

It should not be interpreted as direct evidence that individuals experienced cognitive overload.

A subsequent study could connect this environmental indicator to experimentally measured cognitive or political outcomes.
