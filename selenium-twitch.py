import logging
import threading

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from tkinter import *
import easygui
from datetime import datetime as d
import time
import random

available = []


class SearchTwitch:
    def mainFunction(self, readfile, writefile):
        user_agents = ['Instagram 10.34.0 Android (18/4.3; 320dpi; 720x1280; Xiaomi; HM 1SW; armani; qcom; en_US)',
                       'Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 74.0.3729.169 Safari / 537.36'
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
                       'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
                       'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1'
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'
                       'Opera/9.80 (Windows NT 6.1; WOW64) Presto/2.12.388 Version/12.18'
                       'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36 OPR/43.0.2442.991'
                       'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36 OPR/36.0.2130.32'
                       ]
        ua = random.choice(user_agents)
        arg = "user-agent=[" + ua + "]"

        autoWriteFieName = 'TestOutputTUS_' + d.now().strftime('%Y_%m_%d_%H_%M%S') + '.txt'

        self.textfile = open(readfile, "r")
        #self.write_to_file = open(writefile, 'a+')
        self.write_to_file = open(autoWriteFieName, 'a+')
        self.handles = self.textfile.read().splitlines()

        # Uncomment below to open program in normal browser
        # browser = webdriver.Chrome(executable_path='chromedriver.exe')

        # Options for using headless browser
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument(
        #    "user-agent=[Instagram 10.34.0 Android (18/4.3; 320dpi; 720x1280; Xiaomi; HM 1SW; armani; qcom; en_US)]")
        chrome_options.add_argument(arg)

        self.browser = webdriver.Chrome(chrome_options=chrome_options,
                                        executable_path=r'C:\webdrivers\chromedriver.exe')

        self.browser.get("https://www.twitch.tv/signup")
        self.checkName()

    def checkName(self):
        # logger.info(len(browser.find_elements_by_css_selector(".tw-c-text-error")))
        elem = self.browser.find_element_by_css_selector("input[type='text']")
        for handle in self.handles:
            elem.send_keys(handle)
            time.sleep(3)
            err_message_count = len(
                # self.browser.find_elements_by_css_selector(".tw-c-text-error"))  # 1 if name available and 2/3 if taken
                self.browser.find_elements_by_css_selector(
                    ".tw-svg__asset--success"))  # 1 if name available and 2/3 if taken

            if err_message_count == 1:
                logger.info(handle + " is available")
                available.append(handle)
                self.write_to_file.write(handle + '\n')
                logger.info(available)
            else:
                logger.info(handle + " is not available")

            elem.send_keys(Keys.CONTROL + "a")
            elem.send_keys(Keys.DELETE)

        self.textfile.close()
        self.write_to_file.close()
        self.browser.quit()
        sys.exit()


# Creating and running GUI interface
window = Tk()

window.title("Twitch URL Search")
window.geometry('350x200')
lbl = Label(window, text="Twitch URL Search")
lbl.grid(column=0, row=0)


def clicked1():
    global readfile
    readfile = easygui.fileopenbox()


def clicked2():
    global writefile
    wf = easygui.enterbox(msg='Enter output file name(not including .txt)', title='', default='', strip=True)
    writefile = wf + '.txt'


def clicked3():
    if not readfile.strip():
        logger.info('Input file is null. Please enter real file.')
    if not writefile.strip():
        logger.info('Output file is null. Please enter correct values.')
    else:
        thread = threading.Thread(target=s.mainFunction(readfile, writefile))
        thread.start()
        # s.mainFunction(readfile, writefile)


logger = logging.getLogger('server_logger')
file_name = 'TUS_Logs_' + d.now().strftime('%Y_%m_%d_%H_%M%S') + '.log'
save_file = r"C:\Users\cag36\Desktop\GitHub Projects\_Completed and Working Projects\twitch-scraper-master\logs\\" + file_name
logger.setLevel(logging.INFO)
fh = logging.FileHandler(save_file, encoding="utf-8")
fh.setLevel(logging.INFO)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)

s = SearchTwitch()

btn_input_file = Button(window, text="Select input file:  ", command=clicked1, height=2, width=15)
btn_output_file = Button(window, text='Select output file: ', command=clicked2, height=2, width=15)
btn_run = Button(window, text='Run Program', command=clicked3, height=2, width=15)

btn_input_file.grid(column=1, row=0)
btn_output_file.grid(column=1, row=1)
btn_run.grid(column=1, row=2)
window.mainloop()
