# Energy Efficiency and Neighborhood Wealth in NYC

An exploratory data science project examining the relationship between neighborhood socioeconomic conditions and building-level energy efficiency across New York City.

## Motivation

New York City's Local Law 84 (LL84) requires large buildings to annually benchmark their energy and water usage. When combined with census-level income and wealth data, this data makes it possible to ask: **do wealthier neighborhoods have more energy-efficient buildings?**

I was interested by the complexity of the factors effecting energy usage. Particularly in NYC building energy use as a potential case study of the environmental Kuznet's curve. Wealthier areas may have newer, better-maintained buildings with efficient systems, but could also just have the resources to use more resources. Lower-income neighborhoods may have underinvested buildings running inefficient equipment, or smaller footprints with lower usage. There are many logical ways to come to completely different assumptions about the relationship between energy efficiency and wealth in NYC. This project aims to explore the public data to learn more about this relationship. 

## Data Sources

| Dataset | Source | Description |
|---|---|---|
| **NYC LL84 Benchmarking** | [NYC Open Data](https://data.cityofnewyork.us/Environment/NYC-Building-Energy-and-Water-Data-Disclosure-for-/5zyy-y8am/about_data) | Annual building-level energy use intensity (EUI) |
| **American Community Survey (ACS)** | [U.S. Census Bureau](https://www.census.gov/data/developers/data-sets/acs-5year.html) | Median household income at the census tract level |
| **MapPLUTO** | [NYC Department of City Planning](https://www.nyc.gov/content/planning/pages/resources?search=pluto#datasets) | Parcel-level data used to crosswalk BBL (Borough-Block-Lot) identifiers to census tracts |

## Methodology

Buildings in the LL84 dataset are identified by **BBL** (Borough-Block-Lot). Census income data lives at the **census tract** level. Bridging these requires using MapPLUTO as a crosswalk — each parcel's BBL maps to a census tract, which then joins to ACS data.

The core pipeline:

1. **Ingest** — Pull LL84 benchmarking data and PLUTO crosswalk data via the Socrata API and pull ACS data via the Census API
2. **Normalize** — Clean and process data in pandas, including standardizing messy BBL formats across datasets for easy joining
3. **Crosswalk** — Join LL84 → PLUTO on BBL to get census tract; join to ACS on tract ID
4. **Store** — Load the merged dataset into a local SQLite database (`energy_efficiency_and_wealth.db`)
5. **Analyze** — Explore correlations between neighborhood income and building Energy Use Intensity (EUI)

## Repo Structure

```
energy-efficiency-and-wealth/
├── data/                  # Raw and intermediate data files
├── scripts/               # Python scripts for ingestion, cleaning, and crosswalking
├── sql/                   # SQL queries for exploration and analysis
├── energy_efficiency_and_wealth.db   # SQLite database (merged dataset)
├── requirements.txt
└── README.md
```

## Getting Started

**Prerequisites:** I'm on Python 3.13.7

```bash
git clone https://github.com/liam-py/energy-efficiency-and-wealth.git
cd energy-efficiency-and-wealth
pip install -r requirements.txt
```

You'll need an API keys to reproduce the data ingestion from scratch:

- **Socrata app token** — for the NYC Open Data API ([register here](https://data.cityofnewyork.us/profile/app_tokens))

Set this in a .env file before running the ingestion scripts:

```.env
export socrata_application_token=your_token_here
```

If you just want to explore the data without re-ingesting, the SQLite database is already included in the repo.

## Key Variables

| Variable | Description |
|---|---|
| `site_eui` | Site Energy Use Intensity (kBtu/ft²) — primary efficiency metric |
| `median_household_income` | ACS median HH income for the building's census tract |

## Notes and Caveats

- **LL84 coverage**: Only buildings over 25,000 sq ft are required to benchmark, so this dataset skews toward larger commercial and residential buildings. Small residential buildings are underrepresented.
- **ACS income cap**: Median household incomes cap out at 250,001, highest income tracts are actually a mixed group of varying wealth levels.
- **Self-reported data**: Energy benchmarking data is submitted by building owners and subject to reporting errors.
- **ACS margins of error**: Tract-level income estimates carry uncertainty, especially in lower-population tracts.
- **Causality**: Any correlations observed are descriptive, not causal. Confounders like building age, use type, and size are important to control for in any deeper analysis.

## Tools Used

- Python (pandas, requests, sqlite3)
- SQLite
- Jupyter Notebooks
- NYC Open Data Socrata API
- U.S. Census Bureau API

## Looking Forward

I have finished ingesting, processing, and combining the data into a sql table with average eui and average household income as the two main data points for each tract. I am now moving out of the data science section and into the data analysis section of this project. I plan to calculate a wider variety of metrics and display my findings visually using libraries like matplotlib. I am also aiming to build a simple frontend to display these graphs and some short notes about my findings.

## Author

Liam — [github.com/liam-py](https://github.com/liam-py)
