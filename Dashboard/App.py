# dashboard/app.py
import os
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import base64
import io
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import shap
import matplotlib.pyplot as plt
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Intraday Trading Dashboard"

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

# Load all OrderDF.csv paths recursively
order_files = []
for root, _, files in os.walk(DATA_DIR):
    for file in files:
        if file == "OrderDF.csv":
            full_path = os.path.join(root, file)
            label = os.path.relpath(root, DATA_DIR)
            order_files.append({"label": label, "value": full_path})

app.layout = html.Div([
    html.H2("Intraday Strategy Analysis Dashboard"),
    html.Div([
        html.Div([
            html.Label("Select OrderDF File(s)", style={"fontWeight": "bold"}),
            dcc.Dropdown(
                id="file-selector",
                options=order_files,
                multi=True,
                placeholder="Select one or more OrderDF files...",
            )
        ], style={"flex": "2", "padding": "0 10px"}),

        html.Div([
            html.Label("Date Range (OrderStartTime)", style={"fontWeight": "bold"}),
            dcc.DatePickerRange(id='date-range', style={"width": "100%"})
        ], style={"flex": "1", "padding": "0 10px"}),

        html.Div([
            html.Label("Trade Status Filter", style={"fontWeight": "bold"}),
            dcc.Dropdown(id="status-filter", options=[], multi=True)
        ], style={"flex": "1", "padding": "0 10px"}),

        html.Div([
            html.Label("Strategy Filter", style={"fontWeight": "bold"}),
            dcc.Dropdown(id="strategy-filter", options=[], multi=True)
        ], style={"flex": "1", "padding": "0 10px"}),

    ], style={"display": "flex", "flexWrap": "wrap", "gap": "5px", "marginBottom": "10px"}),

    html.Div(id="stats-output", style={"display": "flex", "gap": "20px", "flexWrap": "wrap", "marginTop": "10px"}),
    html.Div([
        html.Button("Download Excel", id="download-button"),
        dcc.Download(id="download-dataframe-xlsx")
    ], style={"margin": "10px 0"}),
    dcc.Tabs(id="tabs", value="tab1", children=[
        dcc.Tab(label="PnL Summary", value="tab1"),
        dcc.Tab(label="Candle Chart", value="tab_candles"),
        dcc.Tab(label="Indicator Heatmap", value="tab2"),
        dcc.Tab(label="Hourly Performance", value="tab3"),
        dcc.Tab(label="Trade Type Breakdown", value="tab4"),
        dcc.Tab(label="Per-Trade Charts", value="tab5"),
        dcc.Tab(label="Time Interval Performance", value="tab6"),
        dcc.Tab(label="Session-wise Performance", value="tab7"),
        dcc.Tab(label="Indicator Distributions", value="tab8"),
        dcc.Tab(label="Cumulative PnL", value="tab9"),
        dcc.Tab(label="Win Rate by Indicator Bin", value="tab10"),
        dcc.Tab(label="Scatter Matrix", value="tab11"),
        dcc.Tab(label="Model Insights (SHAP)", value="tab12"),
        dcc.Tab(label="Near Success Alerts", value="tab13"),
    ]),
    html.Div(id="tab-content")
])

@app.callback(
    Output("status-filter", "options"),
    Output("strategy-filter", "options"),
    Input("file-selector", "value")
)
def update_filters(file_paths):
    if not file_paths: return [], []
    df = pd.concat([pd.read_csv(f) for f in file_paths])
    options_status = [{'label': s, 'value': s} for s in df["TradeStatusOnPnL"].dropna().unique()]
    options_strategy = [{'label': s, 'value': s} for s in df["Strategy"].dropna().unique()]
    return options_status, options_strategy

@app.callback(
    Output("stats-output", "children"),
    Output("tab-content", "children"),
    Input("file-selector", "value"),
    Input("status-filter", "value"),
    Input("strategy-filter", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
    Input("tabs", "value")
)
def render_dashboard(file_paths, status_filter, strategy_filter, start_date, end_date, tab):
    if not file_paths:
        return html.Div(), html.Div()
    df = pd.concat([pd.read_csv(f) for f in file_paths])
    if 'OrderStartTime' in df.columns:
        df['OrderStartTime'] = pd.to_datetime(df['OrderStartTime'], errors='coerce')
    if status_filter:
        df = df[df["TradeStatusOnPnL"].isin(status_filter)]
    if strategy_filter:
        df = df[df["Strategy"].isin(strategy_filter)]
    if start_date and end_date:
        df = df[(df['OrderStartTime'].dt.date >= pd.to_datetime(start_date).date()) &
                (df['OrderStartTime'].dt.date <= pd.to_datetime(end_date).date())]

    total_trades = len(df)
    wins = df[df.TradeStatusOnPnL == "Success"].shape[0]
    pnl = df.PLStatus.sum()
    win_rate = (wins / total_trades * 100) if total_trades else 0
    stats = [
        html.Div([html.P("Total Trades:"), html.H4(total_trades)]),
        html.Div([html.P("Successes:"), html.H4(wins)]),
        html.Div([html.P("Total PnL:"), html.H4(f"₹{pnl:.2f}")]),
        html.Div([html.P("Win Rate:"), html.H4(f"{win_rate:.1f}%")])
    ]

    if tab == "tab1":
        fig = px.histogram(df, x="PLStatus", color="TradeStatusOnPnL", nbins=50, title="PnL Distribution")
        return stats, dcc.Graph(figure=fig)

    if tab == "tab2":
        corr = df.select_dtypes(include='number').corr()
        fig = px.imshow(corr, text_auto=True, title="Indicator Correlation Heatmap")
        return stats, dcc.Graph(figure=fig)

    if tab == "tab3":
        df["Hour"] = df["OrderStartTime"].dt.hour
        hourly = df.groupby("Hour")["PLStatus"].sum().reset_index()
        fig = px.bar(hourly, x="Hour", y="PLStatus", title="Hourly PnL")
        return stats, dcc.Graph(figure=fig)

    if tab == "tab4":
        strat = df.groupby("Strategy")["PLStatus"].sum().reset_index()
        fig = px.bar(strat, x="Strategy", y="PLStatus", title="PnL by Strategy")
        return stats, dcc.Graph(figure=fig)

    if tab == "tab5":
        fig = px.scatter(df, x="OrderStartTime", y="PLStatus", color="TradeStatusOnPnL", hover_data=["OrderID"], title="Per-Trade PnL")
        return stats, dcc.Graph(figure=fig)

    if tab == "tab6":
        df["Minute"] = df["OrderStartTime"].dt.minute
        interval_bins = pd.cut(df["Minute"], bins=[0, 15, 30, 45, 60], right=False, labels=["00-15", "15-30", "30-45", "45-60"])
        grouped = df.groupby(interval_bins)["PLStatus"].sum().reset_index()
        fig = px.bar(grouped, x="Minute", y="PLStatus", title="15-Minute Interval Performance")
        return stats, dcc.Graph(figure=fig)

    if tab == "tab7":
        df["Session"] = df["OrderStartTime"].dt.hour
        bins = [9, 10, 11, 12, 13, 14, 15, 16]
        labels = ["09-10", "10-11", "11-12", "12-13", "13-14", "14-15", "15-16"]
        df["SessionBin"] = pd.cut(df["Session"], bins=bins, labels=labels, right=False)
        session_perf = df.groupby("SessionBin")["PLStatus"].sum().reset_index()
        fig = px.bar(session_perf, x="SessionBin", y="PLStatus", title="Session-wise PnL")
        return stats, dcc.Graph(figure=fig)

    if tab == "tab8":
        num_cols = [col for col in df.columns if ("IN" in col or "OUT" in col) and df[col].dtype != "O"]
        melted = df.melt(id_vars=["TradeStatusOnPnL"], value_vars=num_cols)
        fig = px.violin(melted, y="value", x="variable", color="TradeStatusOnPnL", box=True, points="all")
        return stats, dcc.Graph(figure=fig)

    if tab == "tab9":
        df = df.sort_values("OrderStartTime")
        df["CumulativePnL"] = df["PLStatus"].cumsum()
        fig = px.line(df, x="OrderStartTime", y="CumulativePnL", title="Cumulative PnL Over Time")
        return stats, dcc.Graph(figure=fig)

    if tab == "tab10":
        if "RSID1IN" in df.columns:
            df["RSI_BIN"] = pd.cut(df["RSID1IN"], bins=5)
            r = df.groupby("RSI_BIN")["TradeStatusOnPnL"].apply(lambda x: (x == "Success").mean()).reset_index()
            fig = px.bar(r, x="RSI_BIN", y="TradeStatusOnPnL", title="Win Rate by RSI_BIN")
            return stats, dcc.Graph(figure=fig)
        return stats, html.P("RSID1IN column not found.")

    if tab == "tab11":
        subset = df[["PLStatus"] + [c for c in df.columns if "IN" in c and df[c].dtype != "O"]].dropna()
        fig = px.scatter_matrix(subset, dimensions=subset.columns[1:], color="PLStatus", title="Scatter Matrix of IN Indicators")
        return stats, dcc.Graph(figure=fig)

    if tab == "tab12":
        try:
            indicators = [col for col in df.columns if "IN" in col and df[col].dtype != "O"]
            df = df.dropna(subset=indicators + ["PLStatus"])
            df["Success"] = (df["TradeStatusOnPnL"] == "Success").astype(int)
            X = df[indicators]
            y = df["Success"]
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            explainer = shap.Explainer(model, X_train)
            shap_values = explainer(X_test[:100])
            shap.summary_plot(shap_values, X_test[:100], show=False)
            buf = io.BytesIO()
            plt.savefig(buf, format="png")
            plt.close()
            encoded = base64.b64encode(buf.getvalue()).decode()
            return stats, html.Img(src="data:image/png;base64," + encoded, style={"width": "100%"})
        except Exception as e:
            return stats, html.Pre(str(e))

    if tab == "tab13":
        if "TargetPrice" not in df.columns or "FinalExecutedPrice" not in df.columns:
            return stats, html.Div("Missing TargetPrice or FinalExecutedPrice columns")
        df_alerts = df[(df["TradeStatusOnPnL"] == "Failure") &
                       (df["FinalExecutedPrice"] >= 0.9 * df["TargetPrice"])]
        if df_alerts.empty:
            return stats, html.Div("No trades near success threshold.")
        fig = px.scatter(df_alerts, x="OrderStartTime", y="FinalExecutedPrice",
                         color="SYMBOL" if "SYMBOL" in df_alerts.columns else None,
                         hover_data=["TargetPrice", "PLStatus", "Strategy"])
        fig.update_layout(title="Near-Success Failed Trades")
        return stats, dcc.Graph(figure=fig)

    if tab == "tab_candles":
        candle_df = None
        for order_path in file_paths:
            candle_path = os.path.join(os.path.dirname(order_path), "candles.csv")
            if os.path.exists(candle_path):
                candle_df = pd.read_csv(candle_path)
                break
        if candle_df is None:
            return stats, html.P("No candles.csv file found in selected folders.")

        required_cols = {"timestamp", "open", "high", "low", "close"}
        if not required_cols.issubset(set(candle_df.columns)):
            return stats, html.P("Candlestick data is missing required columns.")

        candle_df["timestamp"] = pd.to_datetime(candle_df["timestamp"], errors="coerce")
        candle_df = candle_df.sort_values("timestamp")

        fig = go.Figure()

        # Add candlestick chart
        fig.add_trace(go.Candlestick(
            x=candle_df['timestamp'],
            open=candle_df['open'],
            high=candle_df['high'],
            low=candle_df['low'],
            close=candle_df['close'],
            increasing_line_color='green',
            decreasing_line_color='red',
            name='Price'
        ))

        # Overlay trade orders if available
        if 'OrderStartTime' in df.columns and 'OrderPrice' in df.columns:
            df['OrderStartTime'] = pd.to_datetime(df['OrderStartTime'], errors='coerce')
            df = df.dropna(subset=["OrderStartTime", "OrderPrice"])

            buy_orders = df[df["OrderDirection"] == "BUY"]
            sell_orders = df[df["OrderDirection"] == "SELL"]

            fig.add_trace(go.Scatter(
                x=buy_orders["OrderStartTime"],
                y=buy_orders["OrderPrice"],
                mode="markers",
                name="BUY Orders",
                marker=dict(color="blue", symbol="triangle-up", size=10)
            ))

            fig.add_trace(go.Scatter(
                x=sell_orders["OrderStartTime"],
                y=sell_orders["OrderPrice"],
                mode="markers",
                name="SELL Orders",
                marker=dict(color="orange", symbol="triangle-down", size=10)
            ))

        fig.update_layout(title="Candlestick Chart with Orders", xaxis_title="Time", yaxis_title="Price")
        return stats, dcc.Graph(figure=fig)

    

    
    return stats, html.Div("Tab not implemented")

@app.callback(
    Output("download-dataframe-xlsx", "data"),
    Input("download-button", "n_clicks"),
    State("file-selector", "value"),
    prevent_initial_call=True
)
def download_excel(n_clicks, file_paths):
    if not file_paths: return
    df = pd.concat([pd.read_csv(f) for f in file_paths])
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name="Orders")
    output.seek(0)
    return dcc.send_bytes(output.read(), filename="OrderDF.xlsx")

if __name__ == '__main__':
    app.run(debug=True)
