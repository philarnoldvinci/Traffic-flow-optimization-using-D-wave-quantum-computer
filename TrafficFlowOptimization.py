from dwave_qbsolv import QBSolv
from dwave.system import DWaveSampler
import dimod
import hybrid
import time

token="Your Token"

class TrafficFlowOptimization:

    # get number of cars and routes
    def __init__(self, number: int, routes: list, streets: list):
        self.number_of_cars = number
        self.routes = routes
        self.streets = streets

    # Depending on the route of choice, consider each car as variable
    def make_cars_variables(self):
        cars_variables = []
        for i in range(1, self.number_of_cars + 1):
            for j in range(1, len(self.routes) + 1):
                cars_variables.append(f'q{i}{j}')
        return cars_variables

    def route_for_each_cars_variables(self, cars_variables: list, ):
        cars_routes = dict()
        counter = 0
        for i in range(len(cars_variables)):
            cars_routes[cars_variables[i]] = self.routes[counter]
            counter += 1
            if counter == len(self.routes):
                counter = 0
        return cars_routes

    # make qubo without any cost and penalty
    def make_qubo(self, cars_variables: list, ):
        qubo = dict()
        for i in range(len(cars_variables)):
            for j in range(i, len(cars_variables)):
                qubo[(cars_variables[i], cars_variables[j])] = 0
        return qubo

    # adding cost and penalty to the qubo
    def adding_cost_and_penalty(self, qubo, routes_cars):

        k = self.number_of_cars*35

        for item in qubo:

            # cost for existence of two cars in the same section
            for j in self.streets:
                if item[0][0:] != item[1][0:]:
                    if j in routes_cars[item[0]] and j in routes_cars[item[1]]:
                        qubo[item] += float(2)


            # penalty due to existence of one car in two sections at the same time1
            if item[0][0:] == item[1][0:]:
                x = int(item[0][-1])-1
                qubo[item] = len(self.routes[x]) - k

            elif (item[0][1:-1] == item[1][1:-1]) and (item[0][0:] != item[1][0:]):
                qubo[item] = qubo[item] + (2*k)

    # solve with D'Wave and find best Conditions with low energy
    def solve_with_Dwave(self, qubo, method="qbsolv"):

        if method == "qbsolv":
            limit = 30
            s = time.time()
            response = QBSolv().sample_qubo(qubo, solver_limit=limit,)
            e = time.time()
            print(e - s)

        elif method == "hybrid":
            bqm = dimod.BinaryQuadraticModel.from_qubo(qubo, 0)
            # z = dimod.BinaryQuadraticModel.to_qubo(bqm)

            workflow = hybrid.Loop(
                hybrid.Race(
                    hybrid.InterruptableTabuSampler(num_reads=10),
                    hybrid.EnergyImpactDecomposer(size=50, rolling=True, traversal='bfs', rolling_history=0.75)
                    | hybrid.QPUSubproblemAutoEmbeddingSampler(
                                                               qpu_sampler=DWaveSampler(token=token))
                    | hybrid.SplatComposer()) | hybrid.ArgMin(), convergence=3)

            start = time.time()

            response = hybrid.HybridSampler(workflow).sample(bqm)

            end = time.time()
            print(f"time :  {end - start}")

        for datum in response.data(['sample', 'energy', 'num_occurrences', ]):
            conter = 0
            for i in datum.sample:
                if datum.sample[i] == 1:
                    conter += 1
                    print(i, end=" ")
            print("Energy: ", datum.energy, "Occurrences: ", datum.num_occurrences)
            print(conter)


#num_reads=5000