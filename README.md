# Political Information Pressure

A reproducible computational social-science project examining temporal spikes and persistence in news coverage related to digital influence, misinformation, and information manipulation.

## Research question

**When coverage of digital influence and information manipulation increases sharply, how abnormal and persistent are those information-volume spikes relative to the recent information environment?**

## Motivation

Research on misinformation often focuses on the accuracy or persuasive effect of individual messages. This project explores a complementary dimension: whether the **volume, velocity, and temporal concentration of information** can be measured as an environmental condition relevant to political communication and information overload.

The project operationalizes one macro-level component of information overload as **information pressure**.

It does not treat news volume as direct evidence of cognitive overload. Instead, it constructs a reproducible environmental indicator that could later be paired with individual-level experimental or survey outcomes.

A possible theoretical pathway is:

**information pressure → cognitive load → heuristic processing → political effects**

## Data

The analysis uses the **GDELT DOC 2.0 API** to retrieve time-series data for coverage involving:

- disinformation
- misinformation
- influence operations
- fake accounts
- bot networks

The analysis uses both matched article volume and total monitored article volume so that topic attention can be normalized.

## Methods

The workflow demonstrates:

- REST API retrieval
- JSON parsing
- pandas data cleaning
- normalized time-series construction
- rolling means and standard deviations
- z-score spike detection
- lagged OLS regression
- Augmented Dickey-Fuller stationarity testing
- matplotlib visualization
- reproducible project organization

## Main measure

### Coverage share

The main information-pressure measure is:

```text
matched articles about the topic
--------------------------------
all articles monitored by GDELT
```

This avoids interpreting raw publication volume alone as heightened attention.

## Spike detection

Each observation is compared with a lagged rolling baseline.

Approximate interpretation of the rolling z-score:

- `z ≈ 0` — typical relative to the recent baseline
- `z ≈ 1` — elevated
- `z ≥ 2` — unusually high
- `z ≥ 3` — highly unusual

The default project threshold classifies `z ≥ 2` as an information-pressure spike.

## Results

The final analysis covered **180 daily observations** and identified **15 periods of unusually elevated political event pressure** using a rolling z-score threshold of `z >= 2`.

A lagged OLS model showed substantial short-term persistence in conflict-event pressure:

- Lag-1 coefficient: **β = 0.692**
- p-value: **p < 0.001**
- Augmented Dickey-Fuller p-value: **0.0418**

The ADF result rejects a unit-root null at the 5% level, providing support for stationarity in this exploratory specification.

The highest-pressure periods included several major geopolitical episodes. Actor-country decomposition of the leading spike showed the largest identifiable shares associated with:

- USA: **22.8%**
- Israel: **12.9%**
- Palestine: **7.8%**
- Iran: **4.6%**
- Russia: **4.5%**

These results suggest that political event pressure exhibits meaningful short-term persistence and that unusually high-pressure periods can be detected computationally.

The results should not be interpreted as evidence that event volume itself causes cognitive overload. The project instead constructs a macro-level indicator of political information pressure that could later be paired with individual-level measures of attention, recall, trust, heuristic reasoning, or misinformation susceptibility.

### 180-day event-pressure timeline

![Political Event Pressure](figures/political_event_pressure_180d_annotated.png)

## Temporal persistence

A lagged OLS model estimates:

```text
information pressure today
=
constant
+ β × information pressure in the previous period
+ error
```

A positive and statistically significant lag coefficient suggests that elevated information pressure tends to persist across adjacent periods.

## Stationarity

An Augmented Dickey-Fuller test is included as a diagnostic for whether the series behaves as a stationary process.

This is relevant because regression relationships in trending time series can otherwise be misleading.

## Project structure

```text
political-information-pressure/
├── README.md
├── HOW_TO_INTERPRET.md
├── requirements.txt
├── config.json
├── src/
│   └── analysis.py
├── data/
├── results/
└── figures/
```

## Reproducibility

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

macOS/Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

Run the analysis:

```bash
python src/analysis.py
```

On Windows without PowerShell script activation:

```bash
.venv\Scripts\python.exe src\analysis.py
```

## Outputs

The script produces:

- `data/gdelt_timeline.csv`
- `results/processed_information_pressure.csv`
- `results/spike_days.csv`
- `results/model_summary.txt`
- `figures/information_pressure_timeseries.png`
- `figures/rolling_zscore.png`
- `figures/lag_persistence.png`

## Limitations

This project is exploratory and observational.

It does not establish that information pressure causes cognitive overload or political effects. News volume is only one dimension of the broader information environment, and keyword-based retrieval can contain both false positives and false negatives.

A stronger follow-up design could combine environmental information-pressure measures with individual-level outcomes such as:

- recall
- political trust
- misinformation recognition
- decision confidence
- response time
- heuristic reasoning
- political attitudes

## Research relevance

The project is designed as a small computational extension of broader research on:

- digital influence operations
- political communication
- information overload
- political cognition
- misinformation
- cognitive resilience
- computational social science
