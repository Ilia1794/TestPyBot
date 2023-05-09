# Dima_feeding_time
# FeedDimaBot
#
# Done! Congratulations on your new bot. You will find it at t.me/FeedDimaBot. You can now add a description, about section and profile picture for your bot, see /help for a list of commands. By the way, when you've finished creating your cool bot, ping our Bot Support if you want a better username for it. Just make sure the bot is fully operational before you do this.
#
# Use this token to access the HTTP API:
# 5777661926:AAHkGXN_McFo3L5bh2RmPBEiwQQkNvAJhSc
# Keep your token secure and store it safely, it can be used by anyone to control your bot.
#
# For a description of the Bot API, see this page: https://core.telegram.org/bots/api
import pandas as pd
import telebot
from Bot.resources.env_var import TOKEN
from telebot import types
from Bot.resources.check_dimension import Dimension
from Bot.resources.PlotStatistic import PlotStatistic


class FeedDimaBot:
    def __init__(self):
        self.bot = telebot.TeleBot(TOKEN)
        self.dem = Dimension()
        self.plot = PlotStatistic()
        self.btns = [
            types.KeyboardButton('Help'),
            types.KeyboardButton('Статистика за день'),
            types.KeyboardButton('Статистика за неделю'),
            types.KeyboardButton('Статистика за месяц'),
            types.KeyboardButton('Статистика за всё время'),
        ]

    def run(self):
        self.bot.message_handler(commands=['start'])(self.start)
        self.bot.message_handler(content_types=['text'])(self.get_text_messages)
        self.bot.polling(none_stop=True, interval=0)

    def start(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Покушали")
        btn2 = types.KeyboardButton('Help')
        markup.add(*self.btns)
        # self.bot.send_message(message.from_user.id, "Будем тут вести учет", reply_markup=markup)
        self.bot.send_message(message.chat.id, "Будем тут вести учет", reply_markup=markup)

    def get_text_messages(self, message):

        if message.text == '👋 Поздороваться':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
            markup.add(*self.btns)

            self.bot.send_message(message.chat.id, "Будем тут вести учет", reply_markup=markup)

        # elif message.text == 'Покушали':
        #     self.bot.send_message(message.from_user.id, 'Сколько мы скушали?', parse_mode='Markdown')
        elif message.text == 'Help':
            with open('./Bot/resources/help.txt', 'r', encoding='utf-8') as f:
                mess_help = f.read()
            self.bot.send_message(message.chat.id, mess_help, parse_mode='Markdown')

        elif self.dem.check_food_dimensional(message.text.lower()):
            volume = self.parse_volume_liq(message)
            mess_info = f"Записано {volume[0].time()}, {volume[1]} мл"
            self.bot.send_message(message.chat.id, mess_info, parse_mode='Markdown')
            self.__add_data(*volume)

        elif message.text =='Статистика за день':
            self.plot.plot_day_statistic()
            self.send_fig("./Bot/resources/images/day_statistic.png", message)

        elif message.text =='Статистика за неделю':
            self.plot.plot_week_statistic()
            self.send_fig("./Bot/resources/images/week_statistic.png", message)

        elif message.text =='Статистика за месяц':
            self.plot.plot_month_statistic()
            self.send_fig("./Bot/resources/images/month_statistic.png", message)

        elif message.text =='Статистика за всё время':
            self.plot.plot_all_statistic()
            self.send_fig("./Bot/resources/images/all_statistic.png", message)


    def send_fig(self, path, message):
        photo = open(path, 'rb')
        self.bot.send_photo(message.chat.id, photo)
        photo.close()

    def parse_volume_liq(self, message) -> tuple[pd.Timestamp, float]:
        mess = message.text.lower()
        _, base, mult = self.dem.get_food_dimens_mult(mess)
        date_mess = pd.to_datetime(message.date, unit='s') + pd.DateOffset(hours=3)
        mess = mess.replace(base, '')
        mess = mess.strip()
        mess = mess.replace(',', '.')

        if '-' in mess:
            date, val = mess.split('-')
            date = date.replace('-', '')
            date = date.strip()
            date = self.__parse_date(date, date_mess)
            val = val.replace('-', '')
            val = val.strip()
        elif '—' in mess:
            date, val = mess.split('—')
            date = date.replace('—', '')
            date = date.strip()
            date = self.__parse_date(date, date_mess)
            val = val.replace('—', '')
            val = val.strip()
        else:
            date = date_mess
            val = mess
        ret = self.__parse_volume(val)
        return (date, ret * mult)

    @staticmethod
    def __parse_volume(mess: str) -> float:
        try:
            ret = float(mess)
        except ValueError:

            ret = 0.
            print(f"Нипонял {mess=}")
        finally:
            return ret

    @staticmethod
    def __parse_date(date: str, date_mess: pd.Timestamp) -> pd.Timestamp:
        spl = ':' if ':' in date else (
            '.' if '.' in date else (
                ',' if ',' in date else (
                    ';' if ';' in date else (
                        '/' if '/' in date else '\\'
                    )
                )
            )
        )
        try:
            hour, minute, *_ = date.split(spl)
            return pd.Timestamp(
                year=date_mess.year,
                month=date_mess.month,
                day=date_mess.day,
                hour=int(hour),
                minute=int(minute)
            )
        except ValueError:
            return date_mess

    @staticmethod
    def __add_data(date: pd.Timestamp, value: float, type_data: str = "food"):
        df_write = pd.DataFrame({"date": [date], "value": [value]})
        try:
            df = pd.read_parquet(f"./Bot/resources/{type_data}.val")
            ret_df = pd.concat([df, df_write], ignore_index=False)
            ret_df.to_parquet(f"./Bot/resources/{type_data}.val")
        except FileNotFoundError:
            df_write.to_parquet(f"./Bot/resources/{type_data}.val")
