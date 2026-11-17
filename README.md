# Lebanon winter rainfall: interactive charts

Streamlit + Plotly app for an AUB MSBA 325 data story. Two charts: winter rain as a share of normal (2022/23 to 2025/26),
and cumulative rain across the 2024/25 and 2025/26 winters against the long-term average.

Data: Lebanon subnational rainfall indicators (10-day rainfall and long-term average, by governorate), aggregated to
a national figure weighted by satellite pixel count. Winter = October to April.

Run: `pip install -r requirements.txt` then `streamlit run app.py`.
Embed one chart: add `?embed=true&chart=winters` or `?embed=true&chart=cumulative`.
