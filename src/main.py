import sys

sys.path.insert(0, "/Users/mikebrgs/CurrentWork/tecnico/iasd/proj3/data")
sys.path.insert(1, "/Users/mikebrgs/CurrentWork/tecnico/iasd/proj3/ext/aima-python")

import probability

from probability import BayesNode, BayesNet, elimination_ask

class Problem:

    def __init__(self, fh):
        self.BNet = BayesNet()
        self.connections = dict()
        self.sensors = dict()
        self.measures = list()
        for line in fh:
            line = line.replace("\n","").split(" ")
            if line[0] == "R":
                self.rooms = list()
                for room in line[1:]:
                    room = room
                    self.rooms.append(room)
                    self.connections[room] = list()
                    self.sensors[room] = list()
            elif line[0] == "C":
                # self.connections = list()
                for connection in line[1:]:
                    sconnection = connection.split(",")
                    self.connections[sconnection[0]].append(sconnection[1])
                    self.connections[sconnection[1]].append(sconnection[2])
                    # self.connections.append((sconnection[0],sconnection[1]))
            elif line[0] == "S":
                for sensor in line[1:]:
                    ssensor = sensor.split(":")
                    self.sensors[ssensor[1]].append((ssensor[0],float(ssensor[2]),float(ssensor[3])))
            elif line[0] == "P":
                self.PropagationLaw = float(line[1])
            elif line[0] == "M":
                self.measures.append(list())
                for measure in line[1:]:
                    smeasure = measure.split(":")
                    if smeasure[1] == "T":
                        self.measures[-1].append((smeasure[0],True))
                    elif smeasure[1] == "F":
                        self.measures[-1].append((smeasure[0],False))
        instant = 0
        for measure_instant in self.measures:
            instant += 1
            node = None
            if measure_instant == self.measures[0]:
                # Iterate every room
                for room in self.rooms:
                    node = BayesNode(room + "_" + str(instant), "", 1)
                    self.BNet.add(node)
                    # Add all sensors
                    for sensor, sensor_data in self.sensors[room].items():
                        sensor_dict = dict()
                        sensor_dict[True] = sensor_data[1]
                        sensor_dict[False] = sensor_data[2]
                        node = BayesNode(sensor + "_" + str(instant), room + "_" + str(instant), sensor_dict)
                        self.BNet.add(node)
            else:
                # Iterate every room
                for room in self.rooms:
                    parents = room + "_" + str(instant)
                    probabilities = dict()
                    for neighbour in self.connections[room]:
                        parents += " " + neighbour + "_" + str(instant - 1)
                    for counter in range(0, 2**(len(self.connections) + 1)):
                        bin_counter = format(counter,'0' + str(len(self.connections) + 1) + 'b')
                        domain = tuple()
                        for index in range(0, len(self.connections) + 1):
                            if bin_counter[index] == 0:
                                domain += False
                            else:
                                domain += True
                        if domain[0] == True:
                            probabilities[domain] = 1
                        elif True in domain:
                            probabilities[domain] = self.PropagationLaw
                        else:
                            probabilities[domain] = 0
                    node = BayesNode(room + "_" + str(instant), parents, probabilities)
                    self.BNet.add(node)
                    # Add all sensors
                    for sensor, sensor_data in self.sensors[room].items():
                        sensor_dict = dict()
                        sensor_dict[True] = sensor_data[1]
                        sensor_dict[False] = sensor_data[2]
                        node = BayesNode(sensor + "_" + str(instant), room + "_" + str(instant), sensor_dict)
                        self.BNet.add(node)
        # Place here your code to load problem from opened file object fh
        # and use probability.BayesNet() to create the Bayesian network
        pass

    def solve(self):
        instant = 0
        e = dict()
        p_max = 0
        r_max = None
        for measure_instant in self.measures:
            instant += 1
            for measure in measure_instant:
                e[measure[0] + "_" + str(instant)] = measure[1]
        for room in self.rooms:
            p = elimination_ask(room + "_" + len(self.measures),e,self.BNet)
            if p >= p_max:
                p_max = p
                r_max = room
        # Place here your code to determine the maximum likelihood solution
        # returning the solution room name and likelihood
        # use probability.elimination_ask() to perform probabilistic inference
        return (r_max, p_max)

def solver(input_file):
    return Problem(input_file).solve()

fp = open("/Users/mikebrgs/CurrentWork/tecnico/iasd/proj3/data/data1.txt","r")
Problem(fp)