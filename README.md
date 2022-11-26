# Traffic flow optimization using D-Wave quantum computer

The objective of the project is to optimize traffic flow by reducing the amount of time it takes for a group of automobiles to travel between their separate origins and destinations by minimizing total congestion on all route segments. To achieve this, we limit traffic flow by rerouting a subset of vehicles to other routes so as to reduce the number of road segments that overlap. Consequently, it is vital to optimize autos concurrently. In other words, any transfer of autos that alleviates the initial congestion should not result in traffic congestion elsewhere on the map. An individual segment's congestion may be calculated using a quadratic function of the number of vehicles transiting it during a certain time frame. We use a quantum-classical hybrid strategy to overcome this challenge.

## Workflow:
**1-  Classical:** create a random graph of the specified size using the networkx module.

![Screenshot 2022-11-26 190419](https://user-images.githubusercontent.com/51785162/204097491-b92995cb-6581-4cbe-a99e-f149c1006fe4.jpg)

**2- Classical:** add a weight to each edge (links) of this graph (for the instance speed limit, length of the edges, traffic weight). By having this information, we could calculate travel time on this edge.

![Screenshot 2022-11-26 193542](https://user-images.githubusercontent.com/51785162/204097957-6d589513-ebf3-4897-83cb-f7b8f2389aba.jpg)

**3- Classical:** find 3 different routes from the origin node to the destination node with the lowest travel time.

![Screenshot 2022-11-26 193912](https://user-images.githubusercontent.com/51785162/204098066-c02a3eeb-5fe9-4c06-94fd-b1df65c6b3c7.jpg)

**4- Classical:** in order to minimize congestion in road segments on overlapping routes, we formulate it as a QUBO 

**5- Hybrid Quantum/Classical:** Find a solution that decreases congestion in three selected routes.

**6- Classical:** the cars are distributed based on the results in these 3 routes.

![Screenshot 2022-11-26 194236](https://user-images.githubusercontent.com/51785162/204098185-e590cb7c-6c5c-4297-84e3-3e8e503626e5.jpg)

## Advantages of resolving the traffic issue using quantum computers as opposed to conventional navigational software:

As is well knowledge, a subset of these applications uses mean-field theory to tackle the traffic problem, although they do not exactly address the issue. Assume that many trip requests are delivered concurrently to the application. In order to provide the optimal route for all requests, they rely only on traffic data, which, when combined with machine learning techniques, allows them to minimize trip time. Due to the comparable routes that the algorithm may propose for certain requests, they do not, however, account for the likely traffic that each vehicle would generate after traversing.



Quantum annealing technologies, such as quantum processing units (QPUs), are utilized by D-Wave Systems to solve complex combinatorial optimization problems. As an example of time-sensitive optimization tasks, we can demonstrate that the continuous redistribution of position data for cars in dense road graphs is an ideal candidate for quantum computing. It is crucial to note that Volkswagen and D-Wave Systems were responsible for this project and that we had just created a rudimentary prototype.

## Setup and usage

Enter your D-Wave token in the TrafficFlowOptimization.py file and then run main.py file.

```bash
python main.py
```
## 🔗 References
[Neukart, F.; Compostella, G.; Seidel, C.; Von Dollen, D.; Yarkoni, S.; Parney, B., Traffic flow optimization using a quantum annealer. Frontiers in ICT 2017, 4, 29.](https://www.frontiersin.org/articles/10.3389/fict.2017.00029/full)
