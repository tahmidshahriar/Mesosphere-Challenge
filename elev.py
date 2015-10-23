# Create an elevator class to hold all my elevators
# Elevator contains id, goals (floors it must reach),
# current floor, direction it is moving. Additionally,
# it contains future pickup and future goals. These two
# values are added as goals to elevator when it tries to 
# change direction (More explanation below)

# Elev number is used to simply mention number of elevators
elevNumber = 16;
class elevator:
	myID = 0;
	goals = [];
	direction = 0;
	currentFloor = 0;
	futurePickup = -1;
	futureGoal = -1;

	# Initialize elevator
	def __init__(self, setID):
		self.myID = setID;
		self.goals = [];
		self.direction = 0;
		self.currentFloor = 0;
	
	# Going Up
	def setUp(self):
		self.direction = 1;

	# Going down
	def setDown(self):
		self.direction = -1;

	# Add goal to elevator 
	def addGoal(self, add):
		if not (add in self.goals):
			self.goals.append(add);
			# Going up
			if (self.direction == 1):
				self.goals.sort(reverse = True);
			# Going down
			else:
				self.goals.sort();

	# Time step
	def step(self):
		# Simply add floors according to direction
		if (self.direction == 1):
			self.currentFloor = self.currentFloor+1;
		elif (self.direction == -1):
			self.currentFloor = self.currentFloor-1;

        # If floor visited is part of goals, let user know
		if (self.currentFloor in self.goals):
			self.goals.remove(self.currentFloor);
			print("Elevator #" + str(self.myID) + " is stopping on " +
			 str(self.currentFloor));
			if (len(self.goals) == 0):
				# This is where we set the future pickup and future goals
				# to goals. If the current floor is same as future pickup
				# then we do not add that. Explanation of how future pickup
				# works is below.
				if (self.futurePickup != -1):
					if (self.currentFloor != self.futurePickup):
						self.goals.append(self.futurePickup);
					self.goals.append(self.futureGoal);
					if (self.futurePickup > self.futureGoal):
						self.setDown();
					else:
						self.setUp();
					self.futureGoal = -1;
					self.futurePickup = -1;
				else:
					self.direction = 0;

	# Gives status update on all the elevators
	def status(self):
		if (self.direction == 1):
			print("Elevator #" + str(self.myID) + " is currently on " +
			 str(self.currentFloor) + ", headed up towards " + str(self.goals[0]));
		elif (self.direction == -1):
			print("Elevator #" + str(self.myID) + " is currently on " +
			 str(self.currentFloor) + ", headed down towards " + str(self.goals[len(self.goals) - 1]));
		else:
			print("Elevator #" + str(self.myID) + " is currently waiting on " +
			 str(self.currentFloor));
		

# This function is called when a request is made to go upwards
def pickupUp (myElevs, wordList, myUnprocessed):
	# simple checks if task is done
	done = False;
	# closest keeps track of closest elevator to make it faster
	closest = -1;

	# First find any elevator not running. We want to maximize number
	# of elevators running to reduce time wasted
	for i in range(0, elevNumber):
		if (myElevs[i].direction == 0):
			if (closest != -1):
				if (abs(myElevs[closest].currentFloor - wordList[1]) > abs(myElevs[i].currentFloor - wordList[1])):
					closest = i;
			else:
				closest = i;
				done = True;

	# If empty elevators are found
	if (done):	
		# This is the simplest case:
		# Elevator needs to go up to pick up user
		# Goal is also up
		# so elevator simply goes up
		if (myElevs[closest].currentFloor < wordList[1]):
			myElevs[closest].addGoal(wordList[1]);
			myElevs[closest].addGoal(wordList[2]);
			myElevs[closest].setUp();
		# This case is simple as well:
		# Elevator is on pick up floor
		# Elevator needs to go up, direction is up as well
		elif (myElevs[closest].currentFloor == wordList[1]):
			myElevs[closest].addGoal(wordList[2]);
			myElevs[closest].setUp();
		# This case is hardest:
		# Elevator needs to go down to pick up user
		# User wishes to go up
		# So, we use futurepickup and future goals.
		# We set the elevator to go down and give as the goal the
		# pickup floor. This way, the elevator will also process 
		# requests as it travels down. It will keep serving as a 
		# downwards elevator until it has no job left for downwards.
		# At this time, it will process the future requests and start
		# moving upwards. This will minimize overall wait time, even 
		# if it increases wait time in specific cases
		else:
			myElevs[closest].futurePickup = wordList[1];
			myElevs[closest].futureGoal = wordList[2];
			myElevs[closest].addGoal(wordList[1]);
			myElevs[closest].setDown();
		return done;
	# All elevator have jobs, so find same way (going up) and in the way (current <= pickup)
	if not (done):
		for i in range(0, elevNumber):
			if (myElevs[i].direction == 1 and (myElevs[i].currentFloor <= wordList[1])):
				if (closest == -1):
					closest = i;
					done = True;
				else:
					if (abs(myElevs[closest].currentFloor - wordList[1]) > abs(myElevs[i].currentFloor - wordList[1])):
						closest = i;

	if (done):
		if (myElevs[closest].currentFloor < wordList[1]):
			myElevs[closest].addGoal(wordList[1]);
			myElevs[closest].addGoal(wordList[2]);
		else:
			myElevs[closest].addGoal(wordList[2]);

	# If request has been added to an elevator, returns true.
	return done;



# Function very similar to pickupUp
def pickupDown (myElevs, wordList, myUnprocessed):
	done = False;
	closest = -1;
	for i in range(0, elevNumber):
		if (myElevs[i].direction == 0):
			if (closest != -1):
				if (abs(myElevs[closest].currentFloor - wordList[1]) > abs(myElevs[i].currentFloor - wordList[1])):
					closest = i;
			else:
				closest = i;
				done = True;

	if (done):	
		if (myElevs[closest].currentFloor > wordList[1]):
			myElevs[closest].addGoal(wordList[1]);
			myElevs[closest].addGoal(wordList[2]);
			myElevs[closest].setDown();
		elif (myElevs[closest].currentFloor == wordList[1]):
			print("Elevator #" + str(myElevs[closest].myID) + " is currently waiting on " +
			 str(wordList[1]));
			myElevs[closest].addGoal(wordList[2]);
			myElevs[closest].setDown();
		else:
			myElevs[closest].futurePickup = wordList[1];
			myElevs[closest].futureGoal = wordList[2];
			myElevs[closest].addGoal(wordList[1]);
			myElevs[closest].setUp();
		return done;
			
	if not (done):
		for i in range(0, elevNumber):
			if (myElevs[i].direction == -1 and (myElevs[i].currentFloor >= wordList[1])):
				if (closest == -1):
					closest = i;
					done = True;
				else:
					if (abs(myElevs[closest].currentFloor - wordList[1]) > abs(myElevs[i].currentFloor - wordList[1])):
						closest = i;

	if (done):
		if (myElevs[closest].currentFloor > wordList[1]):
			myElevs[closest].addGoal(wordList[1]);
			myElevs[closest].addGoal(wordList[2]);
		else:
			print("Elevator #" + str(myElevs[closest].myID) + " is currently waiting on " +
			 str(wordList[1]));
			myElevs[closest].addGoal(wordList[2]);

	return done;




def main():
	# Initialize my elevators
	myElevs = [];
	myUnprocessed = [];
	for i in range(0, elevNumber):
		myElevs.append(elevator(i));
	
	while (True):
		user_input = raw_input("Some input please: ")
		wordList = user_input.split(' ');

		if (wordList[0] == "status"):
			for i in range(0, elevNumber):
				myElevs[i].status();

		# Change interface such that you put in 
		# arguments 2, pickup floor and goal floor. 
		elif (wordList[0] == "pickup"):
			if (len(wordList) == 3):
				wordList[1] = int(wordList[1]);
				wordList[2] = int(wordList[2]);
				# Pickup floor is lower
				if (wordList[2] > wordList[1]):
					if not (pickupUp(myElevs, wordList, myUnprocessed)):
						# If pickup was not done before, we add it to a list
						# of unprocessed requests
						# These requests are evaluated to see if it matches a
						# case during step
						myUnprocessed.append(wordList);


				# Pickup floor is higher
				elif (wordList[2] < wordList[1]): 
					if not (pickupDown(myElevs, wordList, myUnprocessed)):
						myUnprocessed.append(wordList);

				else:
					print "Pickup and goal floor are the same"

			else:
				print "Command not valid"

		elif (wordList[0] == "step"):
			# Deal with unprocessed requests
			for i in range(0, len(myUnprocessed)):
				if (myUnprocessed[i][2] > myUnprocessed[i][1]):
					if (pickupUp(myElevs, myUnprocessed[i], myUnprocessed)):
						myUnprocessed.remove(myUnprocessed[i]);

				elif (myUnprocessed[i][2] < myUnprocessed[i][1]):
					if (pickupDown(myElevs, myUnprocessed[i], myUnprocessed)):
						myUnprocessed.remove(myUnprocessed[i]);

			# Step forward all elevators
			for i in range(0, elevNumber):
				myElevs[i].step();

		elif (wordList[0] == "update"):
			if (len(wordList) < 2):
				print "Command not valid"
			try:
				elev = int(wordList[1]);
				if (elev < 16):
					myElevs[elev].status();
				else:
					print "Elevator number not valid"
			except ValueError:
				print "Elevator number not valid"

		elif (wordList[0] == "exit"):
			return;
		else:
			print "Command not valid"



if  __name__ =='__main__':
    main()






