from base.core_bot import CoreBot
import multiprocessing

def run_bot(div_name):
    bot = CoreBot(div_name)
    bot.start()

if __name__ == "__main__":
    p1 = multiprocessing.Process(target=run_bot, args=("em",))
    p2 = multiprocessing.Process(target=run_bot, args=("sp",))

    p1.start()
    p2.start()

    p1.join()
    p2.join()
