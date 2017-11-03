## Simulated annealing for weighted directed graph assignment problem

### Problem statement
The assignment problem is commonly explained with an example -
as a problem of finding optimal allocation of n workers over m jobs.
Among various goals minimal total cost or maximal profit could be searched for.
Depending on the cardinality of both sets different models can be considered:
* if n >= m - no. of workers exceeds no. of jobs
* if n <= m - no. of workers is under no. of jobs

### Goals
* Design input and solution data models.
* Design and implement a program solving the problem.
* Test various temperature ranges.
* Test different temperature cooling schedules:
    * exponential: `T(t) = T_0 * a ^ t`
    * linear: `T(t) = T_0 + a * t`
    * logarithmic: `T(t) = c / log(t + d)`
* Test graphs of different sizes and structures,
* Visualize learning performance.

### Solution concept

### References
http://www.fys.ku.dk/~andresen/BAhome/ownpapers/permanents/annealSched.pdf
http://zzsw.zut.edu.pl/download/AB/5%20problemy%20przydzialu.pdf

