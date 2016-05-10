#title           :week12_2.py
#description     :GUI to query Google API for the distance and the travel time between two locations.
#author          :Caroline Smith
#date            :04/24/16
#python_version  :3.5.1 
#notes           :none
#==============================================================================
from tkinter import *
import tkinter.messagebox
import urllib.parse
import urllib.request
import json

class Distance(Frame):
	def __init__(self):
		Frame.__init__(self)
		self.master.title("Google Distance")
		self.grid()

		# Create the data pane
		self._dataPane = Frame(self)
		self._dataPane.grid(row=0,column=0)

		# Label and field for origin
		self._oLabel = Label(self._dataPane, text="Origin")
		self._oLabel.grid(row=0,column=0)
		self._oVar = StringVar()
		self._oEntry = Entry(self._dataPane,
							 textvariable = self._oVar)
		self._oEntry.grid(row=0,column=1)

		# Label and field for destination
		self._dLabel = Label(self._dataPane, text="Destination")
		self._dLabel.grid(row=1,column=0)
		self._dVar = StringVar()
		self._dEntry = Entry(self._dataPane,
							textvariable = self._dVar)
		self._dEntry.grid(row=1,column=1)

		# Label and field for distance 
		self._disLabel = Label(self._dataPane, text="Distance")
		self._disLabel.grid(row=2,column=0)
		self._disVar = StringVar()
		self._disEntry = Entry(self._dataPane,
							textvariable = self._disVar, state='readonly')
		self._disEntry.grid(row=2,column=1)

		# Label and field for travel time
		self._ttLabel = Label(self._dataPane, text="Travel Time")
		self._ttLabel.grid(row=3,column=0)
		self._ttVar = StringVar()
		self._ttEntry = Entry(self._dataPane,
							textvariable = self._ttVar, state='readonly')
		self._ttEntry.grid(row=3,column=1)
	
		# Create transport frame
		self._rbPane = Frame(self)
		self._rbPane.grid(row=0,column=1, rowspan=4, columnspan=2, padx=20)

		# Radiobutton for transport mode
		self._rbLabel = Label(self._rbPane, text="Transportation Mode")
		self._rbLabel.grid(row=0,column=0)
		Modes = ['driving', 'walking', 'biking']
		self._mode = StringVar()
		self._mode.set('driving') # initialize
		
		r=1 #set initial row
		for m in Modes:
			self._rb = Radiobutton(self._rbPane, text=m,
                        variable=self._mode, value=m)
			self._rb.grid(row=r, column=0, sticky=W)
			r+=1
			
		# Submit button
		self._button = Button(self,
							  text = "Submit",
							  command = self._GetDistance)
		self._button.grid(row=4,column=0) 

	def _GetDistance(self):
		"""Query Google API for the distance and the travel time between two locations."""
		# Set up query
		url = 'http://maps.googleapis.com/maps/api/distancematrix/json'
		values = {}
		values['origins'] = self._oVar.get()
		values['destinations'] = self._dVar.get()
		values['mode'] = self._mode
		data = urllib.parse.urlencode(values)
		full_url = url + '?' + data
		# Send HTTP request
		response = urllib.request.urlopen(full_url) 
		the_page = response.read()
		response.close()
		# Parse json data
		json_str = the_page.decode()
		parsed_data = json.loads(json_str)
		status = parsed_data['rows'][0]['elements'][0]['status']

		if status == "OK":
			distance = parsed_data['rows'][0]['elements'][0]['distance']['text']
			travel_time = parsed_data['rows'][0]['elements'][0]['duration']['text']
			self._disVar.set(distance)
			self._ttVar.set(travel_time)
		elif status == "NOT_FOUND":
			tkinter.messagebox.showerror(message = "The origin and/or destination could not be found.",
				                         parent = self)
		elif status == "ZERO_RESULTS":
			tkinter.messagebox.showerror(message = "The distance could not be calculated.",
				                         parent = self)

def main():
	Distance().mainloop()

main()
		