# Methodological Interpretation Guide

This document explains how the main outputs of the project should be interpreted.

## Political event-pressure time series

`figures/event_pressure_timeseries.png`

The time series shows the daily share of GDELT events classified as conflict-coded using negative Goldstein Scale values.

The 7-day lagged rolling baseline represents the recent expected level of conflict-event pressure.

## Rolling z-score

`figures/rolling_zscore.png`

The rolling z-score measures how unusual the current conflict-event share is relative to the preceding baseline.

Approximate interpretation:

- `z ≈ 0` — typical
- `z ≈ 1` — elevated
- `z ≥ 2` — unusual spike
- `z ≥ 3` — highly unusual spike

The analysis uses `z ≥ 2` as the spike threshold.

## Detected spikes

`results/spike_days.csv`

This file identifies periods in which conflict-event pressure was unusually high relative to the recent baseline.

These observations should not automatically be interpreted as evidence of a single geopolitical event or coordinated influence operation. Event-level contextual analysis is required to interpret the substantive meaning of each spike.

## Actor-country contributors

`results/spike_contributors_2024-02-03.csv`

This file summarizes the most frequently represented identifiable actor-country codes among conflict-coded events during the strongest detected spike.

The shares refer to actor-country appearances, not unique countries or causal responsibility.

## Lagged OLS model

`results/model_summary.txt`

The `lag1_share` coefficient estimates whether the conflict-event share on the previous day predicts the conflict-event share on the current day.

A positive and statistically significant coefficient is consistent with short-term temporal persistence.

This is an associative result and does not establish causality.

## Augmented Dickey-Fuller test

The Augmented Dickey-Fuller test evaluates whether the conflict-event share series is consistent with stationarity.

A common interpretation is:

- `p < 0.05` — evidence against a unit root
- `p ≥ 0.05` — insufficient evidence to reject a unit root

The result should be treated as an exploratory diagnostic rather than definitive evidence about the full time-series structure.

## Substantive interpretation

The defensible interpretation of the project is:

> The analysis constructs a macro-level indicator of political event pressure based on the relative concentration of conflict-coded GDELT events and examines whether unusually elevated periods can be detected and whether event pressure persists over short time intervals.

The project should not be interpreted as direct evidence that individuals experienced cognitive overload or that information pressure caused political effects.

A stronger follow-up design could combine this environmental indicator with individual-level experimental or survey measures such as attention, recall, trust, decision confidence, heuristic reasoning, and misinformation susceptibility.