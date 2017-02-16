# hello_evolution
## Simple genetic algorithm for finding user's string

You choose target string, and genetic algorithm steadily crawls to find your string.

Sample input:
```
startEvolution(targetString = "Hello-Evolution", totalPopulation = 1000, mutationRate = 0.05)
```
Sample output:
```
Generation | Fitness | Phenotype       | MutationRate
-----------------------------------------------------
         0 |    0.13 | JGH;ofe;@|$~NB, |         0.05
         1 |    0.33 | x.$loeevg7%nimF |         0.05
         2 |     0.6 | H.~lo-ev.N:tton |         0.05
         3 |    0.67 | H.~lo-ev.l\tton |         0.05
         4 |     0.8 | Hellovevol\tiAn |         0.05
         5 |    0.87 | Hello-evglutiom |         0.05
         6 |    0.93 | Hello-evglution |         0.05
         7 |     1.0 | Hello-evolution |         0.12
I found best solution in  7 generations !
Solution has been found in  1.17 sec
```
Additional to target string you can specify how big will be total population and what is minimal probability of mutation at each crossover.


To run on your machine:
Run script on your machine
Use startevolution function to start evolving



How it works ?
0. Algorithms generates ```totalPopulation``` number of string of length equal to ```targetString```.

1. Based on fitness function (expressed as proportion of correct letters in correct position to total length of string), best 20% of population is selected

2. In some places mutation occurs (swapping random position in string with randomed letter). Rate of mutation occurance is based on homogenity of population ( ```1 - (unique chromosomes \ total number of chromosomes)``` )










NOTE:
Idea of algorithm taken from github user /thegrymek/ (https://github.com/thegrymek/python-hello-evolution)