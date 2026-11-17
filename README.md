# Lebanon winter rainfall: two interactive charts

Streamlit + Plotly app for an AUB MSBA 325 data story. Chart 1: every winter (October to April) from 1981/82 to 2025/26 as a share of
the long-term average; orange marks winters that missed normal by more than 10%. Chart 2: cumulative rain in the last two winters against normal.

Data: Lebanon subnational rainfall indicators (10-day rainfall and long-term average, by governorate), aggregated to a
national figure weighted by satellite pixel count. Run: `pip install -r requirements.txt` then `streamlit run app.py`.
