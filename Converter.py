"""
Description of file

@author: Thomas Pugh
@date:   2018-01-04
"""

import sys
import Tkinter as tk
import tkFileDialog
import ttk
import os
import time
import subprocess

WINDOW_TITLE = "VIDEO EZY 2: Electric Boogaloo"

class Application(tk.Frame):

	DEBUG = False

	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.pack()
		self.create_widgets(master)

		self.list_of_files = []


	def create_widgets(self, master):
		# box listing selected files
		self.selected_files_string = tk.StringVar()
		self.selectedTxt = tk.Entry(self, textvariable = self.selected_files_string, width=50)

		# button for browsing for files
		self.browseBtn = tk.Button(self, text="Browse...", command=self.pick_files)

		# checkbox for if keep the old files or not
		self.keep_old = tk.IntVar()
		self.keep_old.set(1)
		self.keepChk = tk.Checkbutton(self, text="Keep old files", variable=self.keep_old)

		# convert button
		self.convertBtn = tk.Button(self, text="CONVERT!", command=self.start)

		# progress label
		self.progress = ttk.Progressbar(self, orient="horizontal", mode="determinate")

		# placing all the items
		self.selectedTxt.grid(row=0, column=0, columnspan=5)
		self.browseBtn  .grid(row=0, column=5, columnspan=1)
		self.keepChk    .grid(row=1, column=0, columnspan=1)
		self.convertBtn .grid(row=1, column=1, columnspan=5, sticky=tk.W+tk.E)
		self.progress   .grid(row=2, column=0, columnspan=6, sticky=tk.W+tk.E)


	def pick_files(self):
		# ask for files
		selected_files = tkFileDialog.askopenfilenames(parent=self, title="Choose a file")
		
		# turn the list of files into a string
		string_of_files = ", ".join([str(file).replace("/","\\") for file in selected_files if str(file) != ""])
		
		# set the text in the selected_files text box
		self.selected_files_string.set(string_of_files)

		self.progress["value"] = 0


	def start(self):
		if self.selected_files_string.get() == "":
			print("No files selected")
			return

		# disable the buttons and checkbox so you cant change anything
		self.selectedTxt.configure(state=tk.DISABLED)
		self.browseBtn.configure(state=tk.DISABLED)
		self.keepChk.configure(state=tk.DISABLED)
		self.convertBtn.configure(state=tk.DISABLED)
		

		# what number are we up to?
		self.count = 0

		# all the files to convert
		self.list_of_files = self.selected_files_string.get().split(", ")

		self.progress["value"] = 0
		self.file_count = len(self.list_of_files)
		self.progress["maximum"] = len(self.list_of_files)

		root.title(WINDOW_TITLE + " [{}/{}]".format(self.count, self.file_count))

		self.after(100, self.convert)


	def convert(self):
		filename = self.list_of_files.pop(0)

		path, f = filename.rsplit("\\", 1)
		filename_new = os.path.join(path, "small-") + f.rsplit(".", 1)[0]+".mp4"

		self.execute('ffmpeg -y -i "{}" -strict -2 -vf scale=-1:720 "{}"'.format(filename, filename_new))

		if self.keep_old.get() == 0:
			self.execute('del "{}"'.format(filename))

		self.count += 1
		self.progress["value"] = self.count

		root.title(WINDOW_TITLE + " [{}/{}]".format(self.count, self.file_count))

		if self.count < self.file_count:
			self.after(100, self.convert)

		else:
			# after completion
			self.selected_files_string.set("")
			self.selectedTxt.configure(state=tk.NORMAL)
			self.browseBtn.configure(state=tk.NORMAL)
			self.keepChk.configure(state=tk.NORMAL)
			self.convertBtn.configure(state=tk.NORMAL)
			root.title(WINDOW_TITLE)


	def execute(self, command):
		if self.DEBUG:
			print(command)
		else:
			CREATE_NO_WINDOW = 0x08000000
			DETACHED_PROCESS = 0x00000008

			#os.system(command)
			output = subprocess.call(command, creationflags=CREATE_NO_WINDOW, shell=True)


# create root and configure
root = tk.Tk()
root.title(WINDOW_TITLE)
root.resizable(0,0)

# start up the application
app = Application(master=root)
app.mainloop()