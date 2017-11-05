## Simulated annealing for weighted directed graph assignment problem

### Problem statement
The assignment problem is commonly explained with an example -
as a problem of finding optimal allocation of *n* workers over *m* jobs.
Two different workers cannot be allocated over the same job and one worker cannot be do more than one job.
Each assignment of a worker to a job has defined its cost / profit *c*.
The goal of the task is to minimize the total cost or maximize the total profit *U*.
Depending on the cardinality of both sets, different models can be considered:

* if n >= m - no. of workers exceeds no. of jobs:
    - ![U(x) = \sum_{i=1}^{m}\sum_{j=1}^{n}c_{ij}x_{ij} \to min|max](http://latex.codecogs.com/gif.latex?%5Cinline%20U%28x%29%20%3D%20%5Csum_%7Bi%3D1%7D%5E%7Bm%7D%5Csum_%7Bj%3D1%7D%5E%7Bn%7Dc_%7Bij%7Dx_%7Bij%7D%20%5Cto%20min%7Cmax)
    - ![\sum_{i=1}^{n}x_{ij} = 1, i = 1,2,...m](http://latex.codecogs.com/gif.latex?%5Cinline%20%5Csum_%7Bi%3D1%7D%5E%7Bn%7Dx_%7Bij%7D%20%3D%201%2C%20i%20%3D%201%2C2%2C...m)
    - ![\sum_{i=1}^{m}x_{ij} \le 1, j = 1,2...n](http://latex.codecogs.com/gif.latex?%5Cinline%20%5Csum_%7Bi%3D1%7D%5E%7Bm%7Dx_%7Bij%7D%20%5Cle%201%2C%20j%20%3D%201%2C2...n)
    - ![x_{ij} \in \{1, 2\}, i = 1,2...n, j = 1,2...m](http://latex.codecogs.com/gif.latex?%5Cinline%20x_%7Bij%7D%20%5Cin%20%5C%7B1%2C%202%5C%7D%2C%20i%20%3D%201%2C2...n%2C%20j%20%3D%201%2C2...m)
* if n < m - no. of workers is under no. of jobs
    - ![U(x) = \sum_{i=1}^{m}\sum_{j=1}^{n}c_{ij}x_{ij} \to min|max](http://latex.codecogs.com/gif.latex?%5Cinline%20U%28x%29%20%3D%20%5Csum_%7Bi%3D1%7D%5E%7Bm%7D%5Csum_%7Bj%3D1%7D%5E%7Bn%7Dc_%7Bij%7Dx_%7Bij%7D%20%5Cto%20min%7Cmax)
    - ![\sum_{i=1}^{n}x_{ij} \le 1, i = 1,2,...m](http://latex.codecogs.com/gif.latex?%5Cinline%20%5Csum_%7Bi%3D1%7D%5E%7Bn%7Dx_%7Bij%7D%20%5Cle%201%2C%20i%20%3D%201%2C2%2C...m)
    - ![\sum_{i=1}^{m}x_{ij} = 1, j = 1,2...n](http://latex.codecogs.com/gif.latex?%5Cinline%20%5Csum_%7Bi%3D1%7D%5E%7Bm%7Dx_%7Bij%7D%20%3D%201%2C%20j%20%3D%201%2C2...n)
    - ![x_{ij} \in \{1, 2\}, i = 1,2...n, j = 1,2...m](http://latex.codecogs.com/gif.latex?%5Cinline%20x_%7Bij%7D%20%5Cin%20%5C%7B1%2C%202%5C%7D%2C%20i%20%3D%201%2C2...n%2C%20j%20%3D%201%2C2...m)

The problem can be presented graphically as follows:

![Workers - jobs allocation](docs/workers_jobs.png)

### Goals
* Design and implement a program solving simulated anneling algorithm,
* Test various temperature ranges,
* Test different temperature cooling schedules:
    * exponential: ![T(t) = T_0 * a ^ t$](http://latex.codecogs.com/gif.latex?%5Cinline%20T%28t%29%20%3D%20T_0%20*%20a%20%5E%20t%24)
    * linear: ![T(t) = T_0 + a * t](http://latex.codecogs.com/gif.latex?%5Cinline%20T%28t%29%20%3D%20T_0%20&plus;%20a%20*%20t)
    * logarithmic: ![T(t) = \frac{c}{log(t + d)}](http://latex.codecogs.com/gif.latex?%5Cinline%20T%28t%29%20%3D%20%5Cfrac%7Bc%7D%7Blog%28t%20&plus;%20d%29%7D)
* Test graphs of different sizes and structures: ![n > m, n = m, n < m](http://latex.codecogs.com/gif.latex?%5Cinline%20n%20%3E%20m%2C%20n%20%3D%20m%2C%20n%20%3C%20m),
* Visualize learning performance.

### Solution concept
#### Assumptions
* Edge costs are held in two dimensional table, where the first dimension denotes vertex indices from bipartite graph part with lower cardinality *LP* and the second indices from part of higher cardinality *HP*.
* The graph is a complete bipartite one. Edges missing in input file are replaced with *+inf* weights (for minimization problem, *-inf* weights in case of maximization).
* *x* is represented by a permutation of vertex indices ![\in HP](http://latex.codecogs.com/gif.latex?%5Cinline%20%5Cin%20HP):

        Let:          |LP| = 4, |HP| = 6

        Solution:     [ 1 4 2 5 ]
        Remaining:    { 3, 6 }
* Neighbour *x* is computed by choosing a random index from solution ![\in HP](http://latex.codecogs.com/gif.latex?%5Cinline%20%5Cin%20HP) and replacing it by other random index ![\in HP](http://latex.codecogs.com/gif.latex?%5Cinline%20%5Cin%20HP). No matter if it is in the solution or in the remaining set.

#### Algorithm
1. ![t = t_{max}](http://latex.codecogs.com/gif.latex?%5Cinline%20t%20%3D%20t_%7Bmax%7D)<br />
   choose random ![x_{current}](http://latex.codecogs.com/gif.latex?%5Cinline%20x_%7Bcurrent%7D)
2. choose ![x_{next}](http://latex.codecogs.com/gif.latex?%5Cinline%20x_%7Bnext%7D) from ![x_{current}](http://latex.codecogs.com/gif.latex?%5Cinline%20x_%7Bcurrent%7D) neighbourhood<br />
   if ![U(x_{next})](http://latex.codecogs.com/gif.latex?%5Cinline%20U%28x_%7Bnext%7D%29) is better than ![U(x_{current})](http://latex.codecogs.com/gif.latex?%5Cinline%20U%28x_%7Bcurrent%7D%29) than ![x_{current}:=x_{next}](http://latex.codecogs.com/gif.latex?%5Cinline%20x_%7Bcurrent%7D%3A%3Dx_%7Bnext%7D)<br />
   else if ![rand(0,1) > e^{-\delta U/t}](http://latex.codecogs.com/gif.latex?%5Cinline%20rand%280%2C1%29%20%3E%20e%5E%7B-%5Cdelta%20U/t%7D) than ![x_{current}:=x_{next}](http://latex.codecogs.com/gif.latex?%5Cinline%20x_%7Bcurrent%7D%3A%3Dx_%7Bnext%7D)<br />
   repeat step 2. ![k_t](http://latex.codecogs.com/gif.latex?%5Cinline%20k_t) times
3. ![t = T(t)](http://latex.codecogs.com/gif.latex?%5Cinline%20t%20%3D%20T%28t%29)<br />
   if ![t \gt t_{min}](http://latex.codecogs.com/gif.latex?%5Cinline%20t%20%3E%20t_%7Bmin%7D) then goto step 2.<br />
   else goto step 1.

### References
* http://www.fys.ku.dk/~andresen/BAhome/ownpapers/permanents/annealSched.pdf
* http://zzsw.zut.edu.pl/download/AB/5%20problemy%20przydzialu.pdf
* http://www.mini.pw.edu.pl/~januszwa/zad5.pdf
