import catbot
import discordrooms
import threading

catThread = threading.Thread(target=catbot.catbot)
roomThread = threading.Thread(target=discordrooms.roombot)


catThread.start()
roomThread.start()
catThread.join()
roomThread.join()
