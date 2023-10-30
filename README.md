# BioSim Project

by Nida Groenbekk and Yuliia Dzihora

## Results of the project:

We created a working simulation of an island with 2 species, that are introduced subsequently. 
While running the simulation the screen with graphical plots appear. We store the dataframe of the
parameters per year of the simulation: seed, year of simulation, number of animals of each
species and total number of animals. After the simulation, we store it as a csv file that can be 
accessed later. In the simulation we display the map of the  island,  dynamic plot for the number of
animals per species, age/weight/fitness distribution as well as heatmaps for the distribution of 
animals over the island map.

We developed test files for all the files in the biosim package with overall test coverage over 93%.

As examples of simulations, we made files additionally to the Example_try.
Example_random_simulation: simulation of the absolutely random island and animals
Example_massacre: simulation of the island with animals, where one species suppresses another and 
goes in decline after that.

## Possible developments and further improvements of the project.

   ### Code
1. Combine some functions and re-structure the code.
2. Find ways to optimise the code. For instance, skip iterations for those cells of the island
that do not contain the animals in them.
3. Consider using parallel processes instead of iterations over the island. So for instance, 
fodder regrowth could happen simultaneously instead of cell by cell.
4. Analyse the most time-consuming functions and optimise those.
   
   ### Graphics:
5. Add legend for the island.
6. Interactive GUI implementation, ability to stop and continue the simulation.  
   
   ### Tests:
7. Check all the tests: some might be redundant.
8. Is it possible to get 100% coverage and whether it is needed?

    



