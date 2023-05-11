
from Bot.feed_dima_bot import FeedDimaBot
from threading import Thread


def main():
    bot_obj = FeedDimaBot()
    bot_obj.run()

if __name__ == "__main__":
    th = Thread(target=main, name="BotForDima")
    # main()
    th.start()
