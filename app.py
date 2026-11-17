"""Lebanon winter rainfall: interactive Streamlit app (Plotly charts with hover tooltips).

Run locally:   pip install -r requirements.txt   then   streamlit run app.py
Show one chart only (for embedding):  ?chart=winters  or  ?chart=cumulative
"""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

INK, MUTED, GREY, RULE, ORANGE = "#111827", "#4B5563", "#9CA3AF", "#E5E7EB", "#C2410C"
st.set_page_config(page_title="Lebanon Winter Rain", layout="centered")

winters = pd.read_csv("winter_totals.csv")
cum = pd.read_csv("cumulative_rain.csv")
HIGHLIGHT = ("2024-2025", "2025-2026")
MONTHS = {0: "Oct", 3: "Nov", 6: "Dec", 9: "Jan", 12: "Feb", 15: "Mar", 18: "Apr"}


def winters_chart():
    fig = go.Figure()
    for _, r in winters.iterrows():
        hl = r["winter"] in HIGHLIGHT
        fig.add_trace(go.Bar(
            x=[r["winter"].replace("-", "/")], y=[r["pct_of_normal"]], width=0.62,
            marker=dict(color=ORANGE if hl else GREY),
            text=[f"<b>{r['pct_of_normal']:.0f}%</b>"], textposition="inside", insidetextanchor="start",
            textfont=dict(size=26 if hl else 20, color="white"),
            customdata=[[r["rain_mm"], r["normal_mm"], r["oct_dec_pct"], r["jan_apr_pct"]]],
            hovertemplate="<b>Winter %{x}</b><br>%{y:.1f}% of normal (%{customdata[0]:.0f} mm vs %{customdata[1]:.0f} mm)"
                          "<br>Oct to Dec: %{customdata[2]:.0f}% of normal<br>Jan to Apr: %{customdata[3]:.0f}% of normal<extra></extra>",
            showlegend=False))
    fig.add_hline(y=100, line=dict(color=INK, width=2.5, dash="dash"))
    fig.add_annotation(x=0, xref="paper", y=106, yref="y", xanchor="left", showarrow=False,
                       text="<b>Normal = 100%</b>", font=dict(size=15, color=INK))
    fig.update_yaxes(range=[0, 135], visible=False, fixedrange=True)
    fig.update_xaxes(tickfont=dict(size=16, color=INK), fixedrange=True)
    fig.update_layout(height=470, margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor="white",
                      paper_bgcolor="white", bargap=0.3, hoverlabel=dict(font_size=14))
    return fig


def cumulative_chart():
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
                           text=f"<b>{name}<br>{df.cum.iloc[-1]:.0f} mm</b>", font=dict(size=15, color=color if color == ORANGE else MUTED))
    fig.add_annotation(x=a.dek.iloc[-1], y=a.cum_avg.iloc[-1], xanchor="left", xshift=8, showarrow=False,
                       text=f"<b>Normal<br>{a.cum_avg.iloc[-1]:.0f} mm</b>", font=dict(size=15, color=INK))
    fig.update_xaxes(tickvals=list(MONTHS), ticktext=list(MONTHS.values()), range=[0, 24],
                     tickfont=dict(size=15, color=INK), fixedrange=True, showgrid=False)
    fig.update_yaxes(title="Rain since 1 October (mm)", range=[0, 900], gridcolor=RULE, fixedrange=True,
                     tickfont=dict(size=13, color=MUTED))
    fig.update_layout(height=470, margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor="white",
                      paper_bgcolor="white", hovermode="x unified", hoverlabel=dict(font_size=14))
    return fig


which = st.query_params.get("chart", "both")

if which in ("both", "winters"):
    st.subheader("Lebanon's winter rain swung from 79% to 121% of normal in one year")
    st.plotly_chart(winters_chart(), use_container_width=True, config={"displayModeBar": False})
    st.caption("Winter = October to April. National figure: average of the 7 governorates, weighted by satellite "
               "pixel count. Satellite-estimated rainfall. Hover a bar for the early and late winter split.")

if which in ("both", "cumulative"):
    st.subheader("One winter ran dry from January, the next poured")
    st.plotly_chart(cumulative_chart(), use_container_width=True, config={"displayModeBar": False})
    st.caption("Cumulative rain since 1 October, in 10-day steps, against the long-term average in the data. "
               "Source: Lebanon subnational rainfall indicators (10-day, by governorate).")
