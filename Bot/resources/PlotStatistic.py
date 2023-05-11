import plotly.express as px
from telebot import TeleBot
import pandas as pd
import os
import plotly.io as pio


class PlotStatistic:
    def __init__(self,
                 name_statistic: str = "food"):
        self.addr = f"./Bot/resources/{name_statistic}.val"
        self.save_path = os.path.abspath(os.path.dirname(__file__) + os.sep + "images")

    def plot_day_statistic(self, name: str = "Димочка скушал"):
        df = self.__group_by_days(0)
        fig = self.__create_fig(df, name + " за день")
        self.__save_fig(fig, "day_statistic.png")

    def plot_week_statistic(self, name: str = "Димочка скушал"):
        df = self.__group_by_days(7)
        fig = self.__create_fig(df, name + " за неделю")
        self.__save_fig(fig, "week_statistic.png")

    def plot_month_statistic(self, name: str = "Димочка скушал"):
        df = self.__group_by_days(30)
        fig = self.__create_fig(df, name + " за месяц")
        self.__save_fig(fig, "month_statistic.png")

    def plot_all_statistic(self, name: str = "Димочка скушал"):
        df = self.__group_by_days(3000)
        fig = self.__create_fig(df, name + " за всё время")
        self.__save_fig(fig, "all_statistic.png")

    def __group_by_days(self, days: int = 0):
        df = pd.read_parquet(self.addr)
        df = df.query("value != 0")
        if days > 0:
            begin_date = pd.Timestamp.now() - pd.DateOffset(days=days)
            df = df.query('date >= @begin_date')
            df['just_date'] = df["date"].values.astype(dtype='datetime64[D]')
            ddf = df.groupby('just_date')['value'].sum()
            ddf = ddf.reset_index()
            ddf.rename(columns={"just_date": "date"}, inplace=True)
            return ddf
        else:
            begin_date = pd.Timestamp.now() - pd.DateOffset(hours=24)
            df = df.query('date >= @begin_date')
            return df

    @staticmethod
    def __create_fig(df: pd.DataFrame, name):
        return px.bar(
            df,
            x="date",
            y='value',
            title=name + f" {df['value'].values.sum()} мл",
            labels={
                "date": "Время",
                "value": "Выпито, мл"
            },
            text="value",
            width=1200, height=900
        )

    def __save_fig(self, fig, name):
        if not os.path.exists(self.save_path):
            os.mkdir(self.save_path)
        save_path = self.save_path + os.sep + name
        fig.write_image(save_path, scale=2)


if __name__ == "__main__":
    ps = PlotStatistic()
    ps.addr = os.path.abspath('food.val')
    ps.plot_day_statistic()
