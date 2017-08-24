# Text guessing with Genetic algorithm 
>> Example of genetic algorithm used to guess text

>> Genetic algorithms are inspired by Darwin's theory of evolution. Solution to a problem solved by genetic algorithms is evolved.

The algorithm is started with a set of solutions (represented by chromosomes) called population. Solutions from one population are taken and used to form a new population. This is motivated by a hope, that the new population will be better than the old one. Solutions which are selected to form new solutions (offspring) are selected according to their fitness - the more suitable they are the more chances they have to reproduce.

## Genetic algorithm
1. [Start] Generate random population of n chromosomes (suitable solutions for the problem)
2. [Fitness] Evaluate the fitness f(x) of each chromosome x in the population
3. [New population] Create a new population by repeating following steps until the new population is complete
3-1. [Selection] Select two parent chromosomes from a population according to their fitness (the better fitness, the bigger chance to be selected)
3-2. [Crossover] With a crossover probability cross over the parents to form a new offspring (children). If no crossover was performed, offspring is an exact copy of parents.
3-3. [Mutation] With a mutation probability mutates new offspring at each locus (position on a chromosome).
3-4. [Accepting] Place new offspring in a new population
4. [Replace] Use newly generated population for a further run of algorithm
5. [Test] If the end condition is satisfied, stop, and return the best solution in current population
6. [Loop] Go to step 2

## Text representation 
The text is represented as numbers by asci table and every individual in a population is the same length as target text. 


## Dependencies
1. python3 
    ```bash 
    sudo apt-get install python3
    ```
    ```bash 
    sudo apt-get install python3-pip
    ```
2. matplotlib
    ```bash 
    sudo apt-get install python3-pip
    ```
    ```bash 
    pip3 install matplotlib
    ```
    
## Run 
python3 main.py "text to be guessed" 