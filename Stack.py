#title           :Stack.py
#description     :Part 1: Write an implementation of the abstract data type stack.
#                :Part 2: Write a class RPN that implements the interface of RPN calculator only.
#author          :Caroline Smith
#date            :04/10/16
#python_version  :3.5.1 
#notes           :none
#==============================================================================

# Part 1
class Stack:
	"""Abstract data type stack."""
	def __init__(self):
		self._elements = []

	def push(self, element):
		self._elements.append(element)

	def pop(self):
		try:
			return self._elements.pop()
		except IndexError:
			return "Stack is empty: cannot remove element"

	def isEmpty(self):
		if not self._elements:
			return True
		else:
			return False

# Part 2
class RPN(Stack):
	"""Implements the interface of RPN calculator."""

	def add(self):
		new = self.pop() + self.pop()
		self.push(new)

	def sub(self):
		y = self.pop()
		x = self.pop()
		new = x - y
		self.push(new)

	def mul(self):
		new = self.pop() * self.pop()
		self.push(new)

	def div(self):
		y = self.pop()
		x = self.pop()
		new = x / y
		self.push(new)

