import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.dates import DateFormatter
from datetime import datetime
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import shap

class BTPlotter:
    def __init__(self, OrderDF: pd.DataFrame, output_dir: str, symbol: str):
        self.OrderDF = OrderDF.copy()

        # Normalize indicator column names
        rename_map = {
            "RSID1IN": "RSI_IN", "RSID1OUT": "RSI_OUT", "RSID2IN": "RSI_PREV", "RSID2OUT": "RSI_PREV_OUT",
            "MACD1IN": "MACD_IN", "MACD1OUT": "MACD_OUT",
            "SK1IN": "SK_IN", "SK1OUT": "SK_OUT", "SK2IN": "SK_PREV", "SK2OUT": "SK_PREV_OUT",
            "SM501IN": "SM50_IN", "SM501OUT": "SM50_OUT", "SM502IN": "SM50_PREV", "SM502OUT": "SM50_PREV_OUT",
            "SM211IN": "SM20_IN", "SM211OUT": "SM20_OUT", "SM212IN": "SM20_PREV", "SM212OUT": "SM20_PREV_OUT",
            "VWAP1": "VWAP_IN", "VWAP2": "VWAP_OUT",
            "BBU1": "BBUPPER_IN", "BBU2": "BBUPPER_OUT"
        }
        self.OrderDF.rename(columns=rename_map, inplace=True)

        # Detect trend
        def detect_trend(curr, prev):
            if pd.isna(curr) or pd.isna(prev): return "NA"
            return "Up" if curr > prev else ("Down" if curr < prev else "Flat")

        # Entry trend
        self.OrderDF["RSI_TREND"] = self.OrderDF.apply(lambda row: detect_trend(row.get("RSI_IN"), row.get("RSI_PREV")), axis=1)
        self.OrderDF["SM20_TREND"] = self.OrderDF.apply(lambda row: detect_trend(row.get("SM20_IN"), row.get("SM20_PREV")), axis=1)
        self.OrderDF["SM50_TREND"] = self.OrderDF.apply(lambda row: detect_trend(row.get("SM50_IN"), row.get("SM50_PREV")), axis=1)
        self.OrderDF["SK_TREND"] = self.OrderDF.apply(lambda row: detect_trend(row.get("SK_IN"), row.get("SK_PREV")), axis=1)

        # Exit trend
        self.OrderDF["RSI_TREND_OUT"] = self.OrderDF.apply(lambda row: detect_trend(row.get("RSI_OUT"), row.get("RSI_PREV_OUT")), axis=1)
        self.OrderDF["SM20_TREND_OUT"] = self.OrderDF.apply(lambda row: detect_trend(row.get("SM20_OUT"), row.get("SM20_PREV_OUT")), axis=1)
        self.OrderDF["SM50_TREND_OUT"] = self.OrderDF.apply(lambda row: detect_trend(row.get("SM50_OUT"), row.get("SM50_PREV_OUT")), axis=1)
        self.OrderDF["SK_TREND_OUT"] = self.OrderDF.apply(lambda row: detect_trend(row.get("SK_OUT"), row.get("SK_PREV_OUT")), axis=1)

        # Identify near-miss trades
        def is_near_miss(row):
            if row.get("TradeStatusOnPnL") == "Failure":
                try:
                    tgt = row.get("TargetPrice")
                    exec_price = row.get("FinalExecutedPrice")
                    if pd.notna(tgt) and pd.notna(exec_price):
                        if abs(tgt - exec_price) / tgt <= 0.002:
                            if row.get("RSI_TREND") == "Up" or row.get("MACD_IN", 0) > 0:
                                return True
                except:
                    pass
            return False

        self.OrderDF["NearMissCandidate"] = self.OrderDF.apply(is_near_miss, axis=1)

        # Time features
        self.OrderDF['Date'] = pd.to_datetime(self.OrderDF['Date'])
        self.OrderDF['Hour'] = pd.to_datetime(self.OrderDF['OrderStartTime'], format="%H:%M:%S", errors='coerce').dt.hour
        self.OrderDF['Month'] = self.OrderDF['Date'].dt.to_period('M').astype(str)
        self.OrderDF['Weekday'] = self.OrderDF['Date'].dt.day_name()

        self.symbol = symbol
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.sheet_prefix = f"{self.symbol}_{self.timestamp}"
        self.output_dir = os.path.join(output_dir, self.sheet_prefix)
        os.makedirs(self.output_dir, exist_ok=True)
        self.excel_path = os.path.join(self.output_dir, f"{self.sheet_prefix}_Analysis.xlsx")

        # Export full dataframe to Excel
        with pd.ExcelWriter(self.excel_path, engine="openpyxl") as writer:
            self.OrderDF.to_excel(writer, index=False, sheet_name="FullData")
            self.OrderDF[self.OrderDF["NearMissCandidate"]].to_excel(writer, index=False, sheet_name="NearMisses")

        # Trend plots
        trend_cols = [
            "RSI_TREND", "SM20_TREND", "SM50_TREND", "SK_TREND",
            "RSI_TREND_OUT", "SM20_TREND_OUT", "SM50_TREND_OUT", "SK_TREND_OUT"
        ]

        for col in trend_cols:
            if col in self.OrderDF.columns:
                plt.figure(figsize=(6, 4))
                sns.barplot(x=col, y="PLStatus", data=self.OrderDF, estimator=sum, ci=None)
                plt.title(f"Total PnL by {col}")
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.savefig(os.path.join(self.output_dir, f"pnl_by_{col}.png"))
                plt.close()

                plt.figure(figsize=(6, 4))
                sns.countplot(x=col, hue="TradeStatusOnPnL", data=self.OrderDF)
                plt.title(f"Trade Outcomes by {col}")
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.savefig(os.path.join(self.output_dir, f"success_rate_by_{col}.png"))
                plt.close()

        # Correlation heatmap
        numeric_df = self.OrderDF.select_dtypes(include=[np.number])
        if not numeric_df.empty:
            corr = numeric_df.corr()
            plt.figure(figsize=(12, 10))
            sns.heatmap(corr, cmap="coolwarm", annot=False)
            plt.title("Correlation Heatmap of Indicators")
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, "correlation_heatmap.png"))
            plt.close()

        # SHAP feature importance
        feature_cols = [col for col in numeric_df.columns if col not in ["PLStatus"] and numeric_df[col].notna().all()]
        if len(feature_cols) > 1 and "TradeStatusOnPnL" in self.OrderDF.columns:
            y = self.OrderDF["TradeStatusOnPnL"].apply(lambda x: 1 if x == "Success" else 0)
            X = self.OrderDF[feature_cols]
            if not X.empty and y.nunique() == 2:
                model = RandomForestClassifier(n_estimators=100)
                model.fit(X, y)
                explainer = shap.TreeExplainer(model)
                shap_values = explainer.shap_values(X)
                plt.figure()
                shap.summary_plot(shap_values, X, show=False)
                plt.tight_layout()
                plt.savefig(os.path.join(self.output_dir, "shap_summary.png"))
                plt.close()

        # Time-series grouping (hourly)
        hourly_group = self.OrderDF.groupby("Hour")["PLStatus"].sum()
        plt.figure(figsize=(8, 4))
        hourly_group.plot(kind="bar")
        plt.title("Hourly PnL")
        plt.xlabel("Hour")
        plt.ylabel("Total PnL")
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, "hourly_pnl.png"))
        plt.close()

        # TradeType/Strategy-specific slicing (if present)
        for col in ["Strategy", "TradeType"]:
            if col in self.OrderDF.columns:
                grouped = self.OrderDF.groupby(col)["PLStatus"].sum()
                plt.figure(figsize=(6, 4))
                grouped.plot(kind="bar")
                plt.title(f"PnL by {col}")
                plt.ylabel("Total PnL")
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.savefig(os.path.join(self.output_dir, f"pnl_by_{col}.png"))
                plt.close()


    def _save_plot(self, fig, name):
        fig.tight_layout()
        fig.savefig(os.path.join(self.output_dir, f"{name}.png"))
        plt.close(fig)

    def plot_daily_pnl(self):
        daily = self.OrderDF.groupby(self.OrderDF['Date'].dt.date)['PLStatus'].sum()
        fig, ax = plt.subplots(figsize=(10, 4))
        daily.plot(kind='bar', ax=ax)
        ax.set_title('Daily Net PnL')
        ax.set_ylabel('PnL')
        ax.set_xlabel('Date')
        self._save_plot(fig, 'Daily_PnL')

    def plot_cumulative_pnl(self):
        self.OrderDF.sort_values('Date', inplace=True)
        cumulative = self.OrderDF.groupby('Date')['PLStatus'].sum().cumsum()
        fig, ax = plt.subplots(figsize=(10, 4))
        cumulative.plot(ax=ax)
        ax.set_title('Cumulative PnL Over Time')
        ax.set_ylabel('Cumulative PnL')
        ax.set_xlabel('Date')
        self._save_plot(fig, 'Cumulative_PnL')

    def plot_hourly_pnl(self):
        hourly = self.OrderDF.groupby('Hour')['PLStatus'].sum()
        fig, ax = plt.subplots(figsize=(10, 4))
        hourly.plot(kind='bar', ax=ax)
        ax.set_title('Hourly PnL')
        ax.set_xlabel('Hour of Day')
        ax.set_ylabel('PnL')
        self._save_plot(fig, 'Hourly_PnL')

    def plot_monthly_pnl(self):
        monthly = self.OrderDF.groupby('Month')['PLStatus'].sum()
        fig, ax = plt.subplots(figsize=(10, 4))
        monthly.plot(kind='bar', ax=ax)
        ax.set_title('Monthly PnL')
        ax.set_xlabel('Month')
        ax.set_ylabel('PnL')
        self._save_plot(fig, 'Monthly_PnL')

    def plot_15min_interval(self):
        self.OrderDF['Interval'] = pd.to_datetime(self.OrderDF['OrderStartTime'], format="%H:%M:%S").dt.floor("15min").dt.strftime("%H:%M")
        interval = self.OrderDF.groupby('Interval')['PLStatus'].sum().sort_index()
        fig, ax = plt.subplots(figsize=(12, 4))
        interval.plot(kind='bar', ax=ax)
        ax.set_title('15-Minute Interval PnL')
        ax.set_xlabel('Time Interval')
        ax.set_ylabel('PnL')
        self._save_plot(fig, '15min_PnL')

    def plot_success_failure_by_hour(self):
        success_fail = self.OrderDF.copy()
        success_fail['Result'] = success_fail['TradeStatusOnPnL'].fillna('Unknown')
        pivot = pd.pivot_table(success_fail, values='OrderID', index='Hour', columns='Result', aggfunc='count', fill_value=0)
        fig, ax = plt.subplots(figsize=(10, 4))
        pivot.plot(kind='bar', stacked=True, ax=ax)
        ax.set_title('Trade Outcomes by Hour')
        ax.set_ylabel('Number of Trades')
        self._save_plot(fig, 'Hourly_Success_Failure')

    def plot_all(self):
        self.plot_daily_pnl()
        self.plot_cumulative_pnl()
        self.plot_hourly_pnl()
        self.plot_monthly_pnl()
        self.plot_15min_interval()
        self.plot_success_failure_by_hour()
