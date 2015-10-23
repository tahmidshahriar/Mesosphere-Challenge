# Start work at 3:45 pm

How to start:

Simple start the application using python 2.7:
python elev.py



Known bugs:

I could not figure out how to simulate an elevator such that you can request your 
goal AFTER you are in the elevator. Thus, I decided to take in pickup floor and goal
floor at the same time. If I had more time, I would spend it trying to figure out 
how to avoid doing this.

I may have overcomplicated the problem by taking goal floor into account- the
solution would have been much simpler had I simply considered the goal floors to
be the pickup floors only and not taken into account the floors users might be going
towards.


How application works:

elev.py is an elevator control system built using 16 elevators.
This system is able to provide status updates on all elevators, update on a specific
elevator, time step forward or take in pickup requests. 

The elevator works by trying to minimize time an user has to wait and maximizing
the numbers of elevators running.

When a pickup request comes in, the application first tries to locate elevators 
that are currently not in use. If it locates any, it then tries to figure out which 
amongst these free elevators are the closest and gives the task to the closest one.

If the pickup location and the goal location is in the same direction for the
elevator, it simply adds both to the goal and moves forward.

If the pickup location requires the elevator to move in one direction (ex: up) and 
switch to a different direction afterwards (ex: down), it stores the pickup and 
goal floors and simply behaves like a normal elevator with one goal : the pickup 
floor. Thus, it takes other users headed same way. As soon as it is done working 
towards the direction the pickup called for, it switches direction.

To make the above simpler to understand, an exapmple:
Elevator is currently in 5th floor. A request is received to go from 1st to 2nd.
The elevator starts going down towards 1st. It will process requests such as 5th
to 4th, or 4th to 2nd or even 1st to 0th as it behaves like a standard elevator 
going down. However, soon as it is done moving downwards, it readds floor 1 and 2
and starts moving upwards.

Another scenario is all elevators are busy.

If such is the case, we look for two cases.

First case is if the running elevators have elevators that are moving in the 
same direction as pickup location and will reach it on its way (elevator going down 
from 7 will easily process a call from 5 going to 3).

Second case is every other case (elevator is at 7, going to 3 and we get request 
for 5 to 7 or 9 to 10). If such is the case, we leave the request be and process it only after we free up an elevator.



How to use:

Pickup: command is -> pickup a b
	pickup user from a and drop him off at b

Status: command is -> status

Step: command is -> step

Update: command is -> update a
	updates the user on info about elevator number a

Exit: command is -> exit
