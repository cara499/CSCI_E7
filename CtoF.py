#title           :CtoF.py
#description     :GUI application to convert temperature in Celsius to Fahrenheit.
#author          :Caroline Smith
#date            :04/17/16
#python_version  :3.5.1 
#notes           :none
#==============================================================================
from tkinter import *

class Convert_temp(Frame):
	def __init__(self):
		Frame.__init__(self)
		self.master.title("Celsius to Fahrenheit Converter")
		self.grid()
		
		# Label and field for temp in celcius
		self._cLabel = Label(self, text="Celcius")
		self._cLabel.grid(row=0,column=0)
		self._cVar = DoubleVar()
		self._cEntry = Entry(self,
							 textvariable = self._cVar)
		self._cEntry.grid(row=0,column=1)

		# Label and field for temp in fahrenheit
		self._fLabel = Label(self, text="Fahrenheit")
		self._fLabel.grid(row=1,column=0)
		self._fVar = DoubleVar()
		self._fEntry = Entry(self,
							textvariable = self._fVar)
		self._fEntry.grid(row=1,column=1)

		# Convert button
		self._button = Button(self,
							  text = "Convert",
							  command = self._convertC)
		self._button.grid(row=2,column=0, columnspan=2) 

	def _convertC(self):
		"""Event handler for convert button."""
		try:
			tempC = self._cVar.get()
			tempF = tempC* 9/5 + 32
			self._fVar.set(tempF)
		except ValueError:
			tkinter.messagebox.showerror(message = "Error: Bad Format",
				                         parent = self)

def main():
	Convert_temp().mainloop()

main()
		