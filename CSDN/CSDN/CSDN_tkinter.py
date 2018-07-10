# -*- coding: utf-8 -*-
import os
from time import sleep
from tkinter import *
import win32clipboard as w
import win32con
from selenium import webdriver

class ResultList(object):
    def __init__(self):
        self.top = Tk()
        self.top.title('Search From CSDN')
        # 显示居中
        ws = self.top.winfo_screenwidth()
        hs = self.top.winfo_screenheight() - 100
        w, h = 750, 550
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.top.geometry('%dx%d+%d+%d' % (w, h, x, y))

        # Title label
        self.title_label = Label(self.top, fg='blue', font=('Helvetica', 12, 'bold'))
        self.title_label.pack(fill=X, pady=10)

        self.cwd = StringVar(self.top)
        self.variable = StringVar(self.top)

        # Search module
        self.search_module = Frame(self.top)
        self.textbox = Entry(self.search_module, textvariable=self.cwd)
        self.textbox.bind('<Return>', self.do_search)
        self.textbox.pack(fill=X, expand=1, side=LEFT, padx=60)

        self.clear_button = Button(self.search_module, text='Clear', command=self.clear_text, activeforeground='white', activebackground='blue')
        self.search_button = Button(self.search_module, text='Search', command=self.do_search, activeforeground='white', activebackground='blue')
        self.clear_button.pack(side=RIGHT, padx=10)
        self.search_button.pack(side=RIGHT)

        self.search_module.pack(fill=X)

        # Search label
        self.search_label = Label(self.top, fg='red', font=('Helvetica', 9, 'bold'))
        self.search_label.pack(fill=X)

        # Body
        self.body = Frame(self.top)
        self.drop_down = Scrollbar(self.body)
        self.drop_down.pack(side=RIGHT, fill=Y)
        self.results = Listbox(self.body, height=15, width=50, yscrollcommand=self.drop_down.set)
        self.drop_down.config(command=self.results.yview)
        self.results.bind('<Button-3>', self.popupmenu)
        self.results.bind('<Double-Button-1>', self.get_url)
        self.results.pack(side=LEFT, fill=BOTH, expand=1)
        self.body.pack(fill=BOTH, expand=1, padx=20)

        # option
        self.menu = Menu(self.top, tearoff=0)
        self.menu.add_command(label="Copy url", command=self.copy_url)
        self.menu.add_command(label="Open in Chrome", command=self.open_url)

    def clear_text(self, ev=None):
        self.cwd.set('')
        self.results.delete(0, END)

    def popupmenu(self, event):
        self.menu.post(event.x_root, event.y_root)

    def get_url(self, ev=None):
        index = self.results.curselection()[0]
        self.url = self.results.get(index).strip().split(' ')[-1]

    def copy_url(self):
        # write to Paste board
        w.OpenClipboard()
        w.EmptyClipboard()
        w.SetClipboardData(win32con.CF_UNICODETEXT, self.url)
        w.CloseClipboard()
        # read from Paste board
        w.OpenClipboard()
        d = w.GetClipboardData(win32con.CF_UNICODETEXT)
        w.CloseClipboard()
        return d

    def open_url(self):
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.set_page_load_timeout(10)
        driver.get(self.url)

    def do_search(self, ev=None):
        search_text = self.cwd.get()
        if not search_text:
            self.search_label.config(text='Please input word')
            self.top.update()
            sleep(3)
            self.search_label.config(text='')
            self.top.update()
            return
        else:
            self.search_label.config(text='Searching...')
            self.top.update()
            command = "scrapy crawl csdn -a search=%s" % '+'.join(search_text.strip().split(' '))
            os.system(command)
            self.title_label.config(text='Get Info By Search     %s' % search_text)
            self.results.delete(0, END)
            with open('./result.txt', 'r', encoding='utf-8') as f:
                for info in f.readlines():
                    self.results.insert(END, info)
            f.close()
            self.search_label.config(text='')
            self.top.update()


def main():
    d = ResultList()
    mainloop()


if __name__ == '__main__':
    main()
