from dash import Dash, html, dcc
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime, time, timedelta


def read_data():
    return pd.read_csv("data.csv", parse_dates=["date"])


def get_last_data():
    df = read_data()
    df = df.iloc[-1]
    return df['temperature'], df['humidity']


def get_data_by_day(date):
    df = read_data()
    start = datetime.combine(date, time.min)
    end = datetime.combine(date, time.max)
    return df.loc[(df['date'] >= start) & (df['date'] <= end)]


def get_data_for_current_day():
    date_now = datetime.now().date()
    return get_data_by_day(date_now)


def data_component(icon_src, data, component_name, dash_app):
    return html.Div(className="data-component", children=[
        html.Div(
            className="data-container",
            children=[html.Div(children=[html.Img(className="data-icon", src=dash_app.get_asset_url(icon_src))]),
                      html.Div(children=[html.Span(children=data)], className="data-text")]
        ),
        html.H2(children=component_name, className="data-title")
    ])


def combined_data_component():
    temp, hum = get_last_data()
    if temp < 20:
        icon = "cold.png"
    else:
        icon = "hot.png"
    return html.Div(children=[data_component(icon, f"{temp:.1f}\u00b0", "Temperature", app),
                              data_component("humidity.png", f"{hum}%", "Humidity", app)],
                    className="combined-data-container")


def day_chart():
    data = get_data_for_current_day()

    data['temp_color'] = data.apply(lambda row: "royalblue" if row['temperature'] <= 19 else "orange" if 19 <= row[
        'temperature'] <= 22 else "crimson", axis=1)
    data['hum_color'] = data.apply(lambda row: "lightskyblue" if row['humidity'] <= 40 else "dodgerblue" if 40 <= row[
        'humidity'] <= 55 else "darkblue", axis=1)

    fig_temp = go.Figure(go.Bar(x=data['date'], y=data['temperature'], marker={"color": data['temp_color']}))
    fig_temp.update_layout(xaxis={"tickformat": '%H:%M', "dtick": 7200000.0,
                                 "tick0": data.iloc[0]['date'].strftime("%H:%M")})
    fig_hum = go.Figure(go.Bar(x=data['date'], y=data['humidity'], marker={"color": data['hum_color']}))
    fig_hum.update_layout(xaxis={"tickformat": '%H:%M', "dtick": 7200000.0,
                                 "tick0": data.iloc[0]['date'].strftime("%H:%M")})
    return fig_temp, fig_hum


def daily_chart_component(fig, fig_id):
    return html.Div(children=dcc.Graph(id=fig_id, figure=fig))


def combined_daily_chart(fig_temp, fig_hum):
    return html.Div(children=[daily_chart_component(fig_temp, 'temp_fig'), daily_chart_component(fig_hum, 'hum_fig')])


app = Dash(__name__)

temp_fig, humidity_fig = day_chart()
app.layout = html.Div(children=[combined_data_component(), combined_daily_chart(temp_fig, humidity_fig)])

app.run_server(port=8080)
