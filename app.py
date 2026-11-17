"""Lebanon winter rainfall, 1981/82 to 2025/26: one interactive Streamlit + Plotly chart.

Run locally:   pip install -r requirements.txt   then   streamlit run app.py
Embed (no page chrome):  ?embed=true
"""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

INK, MUTED, GREY, ORANGE, BAND = "#111827", "#4B5563", "#9CA3AF", "#C2410C", "#F3F4F6"
st.set_page_config(page_title="Lebanon Winter Rain", layout="centered")

w = pd.read_csv("winters_1981_2025.csv")
n_near = int(w["near_normal"].sum())
n = len(w)


def chart():
    fig = go.Figure()
    fig.add_hrect(y0=90, y1=110, fillcolor=BAND, line_width=0, layer="below")
    fig.add_hline(y=100, line=dict(color=INK, width=2, dash="dash"))
    fig.add_trace(go.Bar(
        x=w["winter"], y=w["pct_of_normal"],
        marker=dict(color=[GREY if v else ORANGE for v in w["near_normal"]]),
        customdata=w[["rain_mm", "normal_mm"]].values,
        hovertemplate="<b>Winter %{x}</b><br>%{y:.0f}% of normal (%{customdata[0]:.0f} mm vs %{customdata[1]:.0f} mm)<extra></extra>",
        showlegend=False))
    for yr, lab in [("2024/2025", "79%"), ("2025/2026", "121%")]:
        v = float(w.loc[w["winter"] == yr, "pct_of_normal"].iloc[0])
        fig.add_annotation(x=yr, y=v, text=f"<b>{lab}</b>", showarrow=False, yshift=14 if v > 100 else -14,
                           font=dict(size=14, color=ORANGE))
    fig.add_annotation(x=1, xref="paper", y=100, yref="y", xanchor="right", yanchor="bottom", showarrow=False,
                       text="<b>Normal ±10%</b>", font=dict(size=13, color=MUTED), yshift=18)
    fig.update_yaxes(range=[60, 170], ticksuffix="%", tickvals=[60, 80, 100, 120, 140, 160], gridcolor="white",
                     tickfont=dict(size=13, color=MUTED), fixedrange=True)
    fig.update_xaxes(tickvals=list(w["winter"][4::10]), tickfont=dict(size=13, color=INK), fixedrange=True)
    fig.update_layout(height=480, margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor="white", paper_bgcolor="white",
                      bargap=0.25, hoverlabel=dict(font_size=14))
    return fig


st.subheader(f"Only {n_near} of {n} Lebanese winters brought near-normal rain")
st.plotly_chart(chart(), use_container_width=True, config={"displayModeBar": False})
st.caption(f"Winter rain as a share of the long-term average, 1981/82 to 2025/26. Orange = missed normal by more than "
           f"10% ({n - n_near} winters). Winter = October to April. National figure: 7 governorates weighted by satellite "
           "pixel count; satellite-estimated rainfall. Source: Lebanon subnational rainfall indicators (10-day).")
