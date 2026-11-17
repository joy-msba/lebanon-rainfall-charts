"""Lebanon winter rainfall, 1981/82 to 2025/26: two interactive Streamlit + Plotly charts.

Run locally:   pip install -r requirements.txt   then   streamlit run app.py
Embed one chart:  ?embed=true&chart=winters  or  ?embed=true&chart=recent
"""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

INK, MUTED, GREY, ORANGE, BAND, RULE = "#111827", "#4B5563", "#9CA3AF", "#C2410C", "#F3F4F6", "#E5E7EB"
MONTHS = {0: "Oct", 3: "Nov", 6: "Dec", 9: "Jan", 12: "Feb", 15: "Mar", 18: "Apr"}
st.set_page_config(page_title="Lebanon Winter Rain", layout="centered")

w = pd.read_csv("winters_1981_2025.csv")
cum = pd.read_csv("cumulative_rain.csv")
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
    for yr in ("2024/2025", "2025/2026"):
        v = float(w.loc[w["winter"] == yr, "pct_of_normal"].iloc[0])
        fig.add_annotation(x=yr, y=62, yanchor="bottom", text=f"<b>{v:.0f}%</b>", showarrow=False, textangle=-90,
                           font=dict(size=12, color="white"))
    fig.update_yaxes(range=[60, 170], ticksuffix="%", tickvals=[60, 80, 100, 120, 140, 160], gridcolor="white",
                     tickfont=dict(size=13, color=MUTED), fixedrange=True)
    fig.update_xaxes(tickvals=list(w["winter"][4::10]), tickfont=dict(size=13, color=INK), fixedrange=True)
    fig.update_layout(height=480, margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor="white", paper_bgcolor="white",
                      bargap=0.25, hoverlabel=dict(font_size=14))
    return fig


def recent_chart():
    a = cum[cum.winter == "2024-2025"].sort_values("dek")
    b = cum[cum.winter == "2025-2026"].sort_values("dek")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=a.dek, y=a.cum_avg, mode="lines", line=dict(color=INK, width=3, dash="dash"),
                             hovertemplate="Normal: %{y:.0f} mm so far<extra></extra>", showlegend=False))
    for df, name, color, width in [(a, "2024/25", GREY, 4), (b, "2025/26", ORANGE, 5)]:
        fig.add_trace(go.Scatter(x=df.dek, y=df.cum, mode="lines", line=dict(color=color, width=width),
                                 customdata=df[["cum_avg"]].values,
                                 hovertemplate=name + ": %{y:.0f} mm so far (normal %{customdata[0]:.0f} mm)<extra></extra>",
                                 showlegend=False))
        fig.add_annotation(x=df.dek.iloc[-1], y=df.cum.iloc[-1], xanchor="left", xshift=8, showarrow=False,
                           text=f"<b>{name}<br>{df.cum.iloc[-1]:.0f} mm</b>", font=dict(size=14, color=color if color == ORANGE else MUTED))
    fig.add_annotation(x=a.dek.iloc[-1], y=a.cum_avg.iloc[-1], xanchor="left", xshift=8, showarrow=False,
                       text=f"<b>Normal<br>{a.cum_avg.iloc[-1]:.0f} mm</b>", font=dict(size=14, color=INK))
    fig.update_xaxes(tickvals=list(MONTHS), ticktext=list(MONTHS.values()), range=[0, 25],
                     tickfont=dict(size=14, color=INK), fixedrange=True, showgrid=False)
    fig.update_yaxes(title="Rain since 1 October (mm)", range=[0, 900], gridcolor=RULE, fixedrange=True,
                     tickfont=dict(size=12, color=MUTED))
    fig.update_layout(height=460, margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor="white",
                      paper_bgcolor="white", hovermode="x unified", hoverlabel=dict(font_size=14))
    return fig


which = st.query_params.get("chart", "both")

if which in ("both", "winters"):
    st.subheader(f"Only {n_near} of {n} Lebanese winters brought near-normal rain")
    st.plotly_chart(chart(), use_container_width=True, config={"displayModeBar": False})
    st.caption(f"Winter rain as a share of the long-term average. Grey band = within 10% of normal. Orange = missed normal "
               f"by more than 10% ({n - n_near} winters). Winter = October to April. National figure: 7 governorates "
               "weighted by satellite pixel count; satellite-estimated rainfall. Source: Lebanon subnational rainfall indicators.")

if which in ("both", "recent"):
    st.subheader("The last two winters: one ran dry from January, the next poured")
    st.plotly_chart(recent_chart(), use_container_width=True, config={"displayModeBar": False})
    st.caption("Cumulative rain since 1 October, in 10-day steps, against the long-term average in the data. "
               "Source: Lebanon subnational rainfall indicators (10-day, by governorate).")
