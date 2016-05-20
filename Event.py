#title           :Event.py
#description     :Event-driven simulation of average ATM wait time.
#author          :Caroline Smith
#date            :05/11/16
#python_version  :3.5.1 
#notes           :none
#==============================================================================
from statistics import mean

class Event(object):
	"""Hold event information."""
	def __init__(self, time, typ, service=None, atm=None):
		self.time = time
		self.typ = typ
		self.service = service
		self.atm = atm

	def __eq__(self, other):
		if isinstance(other, Event):
			return self.time == other.time

	def __lt__(self, other):
		if isinstance(other, Event):
			return self.time < other.time

	def __gt__(self, other):
		if isinstance(other, Event): 
			return self.time > other.time

class Person(object):
	"""Hold information while the person is waiting in the queue."""
	def __init__(self, time, service):
		self.time = time
		self.service = service

def main():
	"""Run the Event-driven simulation."""
	# Instantiate the event queue
	event_queue = []

	# Instantiate the queue(s) for people waiting for the access to an ATM
	wait_list = []

	# Instantiate the ATM status list (0=available 1=unavailable)
	ATM_list = [0,0,0,0]

	# Instantiate an empty vector of waiting times
	wait_times = []

	# For each line in arrivals.txt, instantiate an arrival event
	# using the specified arrival time and service time 
	# Put all those events into the event queue
	arrivals = open("arrivals.txt", "r")
	for line in arrivals:
		arvl = line.split()	
		e = Event(int(arvl[0]), "A", service=int(arvl[1]))
		event_queue.append(e)
	arrivals.close()
	event_queue.sort()

	# Process the event queue 
	while event_queue:
		# get the next event E from the event list and remove it
		E = event_queue.pop(0)
		# set the current wall clock time Tc to the time of the event
		Tc = E.time

		# Arrival event
		if E.typ == "A":
			S = E.service
			# The waiting line is empty and there is an ATM available:
			if not wait_list and 0 in ATM_list:
				K = ATM_list.index(0)
				ATM_list[K] = 1
				# create a new departure event at time Tc+S for ATM machine K
				# and add to event queue
				d_time = Tc + S
				d = Event(d_time, "D", atm=K)
				event_queue.append(d)
				event_queue.sort()
				# append waiting time 0 to the list of waiting times (this person did not wait)
				wait_times.append(0)

			# There is a line or all ATMs are still taken
			else:
				# create new Person object that will remember the arrival time Tc and required service time S 
	            # and add this person to the end of the waiting line
				p = Person(time=Tc,service=S)
				wait_list.append(p)
				
		# Departure event		
		else:
			atm_id = E.atm
			# if waiting line is empty: change the status of ATM K to "available"
			if not wait_list:
				ATM_list[atm_id] = 0

	        # people are waiting
			else:
				# pop the next person from the waiting line
	        	# get that person's arrival time Ta and the required service time S
				next = wait_list.pop(0)
				Ta = next.time
				S = next.service
				# send person to the atm that just became avaiable
				K = atm_id
				d_time = Ta + S
				d = Event(d_time, "D", atm=K)
				event_queue.append(d)
				event_queue.sort()
				# calculate wait time
				Tw = Tc - Ta
				wait_times.append(Tw)

	# calculate the average wait time using the list of wait times
	avg_wait = mean(wait_times)
	print(avg_wait)

main()
