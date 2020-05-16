# Alex Laughlin
# Chris Tucker
# CSCI 340 Project 2

import sys
import random

# The job class will be constructed with name as a parameter.
class job:

    def __init__(self, name):
        self.name = name
        self.runTime = 0
        self.memSize = 0
        self.done = False
        self.pagesNeeded = 0
        self.timeLeft = 0
        self.randomSeed = 0
        self.startTime = 0
        self.endTime = 0

    def setName(self, name):
        self.name = name

    def setRunTime(self, minJobRun, maxJobRun, randomSeed):
        self.runTime = random.randrange(minJobRun, maxJobRun)
        self.timeLeft = self.runTime
        self.randomSeed = randomSeed

    def setMemSize(self, minJobMem, maxJobMem, randomSeed):
        self.memSize = random.randrange(minJobMem, maxJobMem)
        self.randomSeed = randomSeed

    def setPagesNeeded(self, pageSize):
        if int(self.getMemSize() / pageSize) == 0:
            self.pagesNeeded = int(self.getMemSize() / pageSize)
        else:
            self.pagesNeeded = int(self.getMemSize() / pageSize) + 1

    def setStartTime(self, startTime):
        self.startTime = startTime

    def setEndTime(self, endTime):
        self.endTime = endTime

    def terminate(self):
        self.done = True

    def run(self, timeStep):
        self.timeLeft = self.timeLeft - timeStep
        if self.timeLeft == 0:
            self.terminate()

    def takesPage(self, pageSize):
        return (self.timeLeft >= pageSize)

    def getMemSize(self):
        return self.memSize

    def getRunTime(self):
        return self.runTime

    def getName(self):
        return self.name

    def getPagesNeeded(self):
        return self.pagesNeeded

    def getTimeLeft(self):
        return self.timeLeft

    def getStartTime(self):
        return self.startTime

    def getEndTime(self):
        return self.endTime

    def isDone(self):
        return self.done



# Build the queue
def buildQ(numJobs, minJobRun, maxJobRun, minJobMem, maxJobMem, pageSize, randomSeed):

    random.seed(randomSeed)

    # This loop will fill the queue with jobs
    queue = []
    for i in range(numJobs):
        queue.append(job(i))
        queue[i].setRunTime(minJobRun, maxJobRun, randomSeed)
        queue[i].setMemSize(minJobMem, maxJobMem, randomSeed)
        queue[i].setPagesNeeded(pageSize)
    return queue



def schedule(queue, memSize, pageSize):

    # This is the time slice that will be passed to the run() method for each job to indicate how long the job has
    # run on the CPU in the Round Robin scheduler. When the run() method is used, the time slice value will be
    # subtracted from the job's timeLeft variable, which is the amount of time remaining that the job needs to finish.
    timeSlice = 1

    # The timestep will start counting at 1
    count = 1

    # This while loop will continue while the queue has at least one job in it.
    # When a job is started, its start time will be recorded.
    # When a job is finished, its end time will be recorded and it will be removed from the queue
    while len(queue) != 0:

        # Space is how many pages are available
        space = int(memSize / pageSize)

        # dotsArray is an array of dots to help the user visualize the page usage of each job.
        # It will print out an array of dots that will change to the job number using it to represent
        # the job taking up pages.
        dotArray = []
        dots = int(memSize / pageSize)
        for d in range(dots):
            dotArray.append('.')

        # The list RR is the Round Robin scheduler
        RR = []
        print()

        # Print the current count value as the timestep
        print("Time Step " + str(count) + ": ")

        # Test to make sure the queue is rearranging
        # This loop will print the current queue of jobs to show that any previous jobs have been moved
        # to the back of the queue and the other jobs have moved up.
        print("Current Queue")
        for p in range(len(queue)):
            print("queue[" + str(p) + "] = Job " + str(queue[p].getName()))

        # This loop appends the Round Robin array with jobs as long as there is page space available
        print()
        for i in range(len(queue)):
            if space - queue[i].getPagesNeeded() > 0:
                RR.append(queue[i])
                space = space - queue[i].getPagesNeeded()
                print(("Job " + str(queue[i].getName()) + " added. Time remaining = " + str(queue[i].getTimeLeft()) + " Available pages remaining = " + str(space)))
        print("Unusued Page Space = " + str(space))

        # This first loop copies the job name into dotArray
        # The second loop formats and prints dotArray
        v = 0
        for x in range(len(RR)):
            for k in range(v, (v + RR[x].getPagesNeeded())):
                dotArray[k] = str(RR[x].getName())
            # v will be equal to the value of the job's pages needed so that the it can be added to itself
            # so that when the loop iterates, it starts at the correct index in dotArray instead of
            # continually restarting at index 0
            v = v + RR[x].getPagesNeeded()
        for z in range(len(dotArray)):
            if ((z % 4) == 0) and (z != 0): # every set of 4 dots will be separated by an additional space
                print(' ', end='')
            if ((z % 16) == 0) and (z != 0): # every set of 16 dots will be separated by a line break
                print()
            # This prints the array out
            print("{0:>3}".format(dotArray[z]), sep=' ', end='')

        print()
        print("Executing")
        print()

        # Round Robin Scheduler
        for j in range(len(RR)):
            if RR[j].startTime == 0:
                RR[j].setStartTime(count)

            # Run will be called with the timeslice.
            # Currently the time slice is set to 1
            RR[j].run(timeSlice)
            if RR[j].isDone() == True:
                RR[j].setEndTime(count)
                queue.remove(RR[j])
            else:
                queue.append(RR[j])
                queue.remove(RR[j])
        count = count + 1

    print("All jobs completed.")



def main():

    # The user will provide 8 arguments: computer memory size, page size, the number of jobs, the minimum job run time,
    # the maximum job run time, the minimum job memory, the maximum job memory, and a random seed
    # The length is set to 9 instead of 8 because the 0th index will be the name of the file.
    #print('Number of arguments:', len(sys.argv), 'arguments.')
    # If the user doesn't provide the correct amount of parameters
    print()
    if len(sys.argv) != 9:
        print("Error. Incorrect amount of parameters. Please indicate the values for each variable.")
        memSize = int(input("Please input the value for computer memory size: "))
        pageSize = int(input("Please input the value for the page size: "))
        numJobs = int(input("Please input the value for the number of jobs: "))
        minJobRun = int(input("Please input the value for the minimum job run time: "))
        maxJobRun = int(input("Please input the value for the maximum job run time: "))
        minJobMem = int(input("Please input the value for the minimum job memory: "))
        maxJobMem = int(input("Please input the value for the maximum job memory: "))
        randomSeed = int(input("Please input the value for the random seed: "))
        print("Simulation Parameters:")
        print(" Memory Size: " + str(memSize))
        print(" Page Size: " + str(pageSize))
        print(" Random Seed: " + str(randomSeed))
        print(" Number of jobs: " + str(numJobs))
        print(" Runtime (min-max) timesteps: " + str(minJobRun) + "-" + str(maxJobRun))
        print(" Memory (min-max): " + str(minJobMem) + "-" + str(maxJobMem))

    else:
        memSize = int(sys.argv[1])
        pageSize = int(sys.argv[2])
        numJobs = int(sys.argv[3])
        minJobRun = int(sys.argv[4])
        maxJobRun = int(sys.argv[5])
        minJobMem = int(sys.argv[6])
        maxJobMem = int(sys.argv[7])
        randomSeed = int(sys.argv[8])
        print("Simulation Parameters:")
        print(" Memory Size: " + str(memSize))
        print(" Page Size: " + str(pageSize))
        print(" Random Seed: " + str(randomSeed))
        print(" Number of jobs: " + str(numJobs))
        print(" Runtime (min-max) timesteps: " + str(minJobRun) + "-" + str(maxJobRun))
        print(" Memory (min-max): " + str(minJobMem) + "-" + str(maxJobMem))

    print()

    # Build the queue by making a list of jobs
    queue = buildQ(numJobs, minJobRun, maxJobRun, minJobMem, maxJobMem, pageSize, randomSeed)
    q = list(queue)

    # This loop prints the header at the start of the program and displays the current queue, each job's runtime, memory
    # and the number of pages that each job requires
    print("Job Queue:")
    print("{0:>6}{1:>10}{2:>10}{3:>10}".format("Job #", "Runtime", "Memory", "Pages"))
    for i in range(len(queue)):
        print("{0:>6}{1:>10}{2:>10}{3:>10}".format(str(queue[i].getName()), str(queue[i].getRunTime()), str(queue[i].getMemSize()), str(queue[i].getPagesNeeded())))

    print()
    print("Simulator Starting:")

    # This method calls the Round Robin scheduler
    schedule(queue, memSize, pageSize)

    # This loop prints at the end of the program and displays each job number, its start time, and its end time
    print("{0:>6}{1:>13}{2:>11}".format("Job #", "Start Time", "End Time"))
    for j in range(len(q)):
        print("{0:>6}{1:>13}{2:>11}".format(str(q[j].getName()), str(q[j].getStartTime()), str(q[j].getEndTime())))

main()