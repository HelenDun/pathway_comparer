# pathway_comparer
Authors: Helen Dun, Austin Bassett

V-Nums: V00912482, V00


*Introduction*

This program was created to compare the proteins of cellular signalling pathways, specifically circadian rhythm pathways, between organisms. The comparison is output as both a text file and a graph for a visual representation. It operates in the following fashion:
1. Has user choose 2 different organisms to compare
2. Reads in the set of proteins for each organism and the orthologous mapping between the organisms
3. Compares the set of proteins using Union and Except operations
4. Outputs the results


*Databases*

The program uses files from 3 different databases:
- Circadian Gene Database (CGD)
- Orthologous MAtrix Project (OMA)
- STRING Database

The CGD is used for getting the list of proteins in the circadian rhythm pathway for organisms. The OMA is used for getting the lists of proteins orthologous to one-another between 2 organisms. The STRING is used for getting the protein-protein interactions of a pathway for an organism. 


**Adding an Organism**
1. Choose an organism. Make sure the organism is listed in all 3 databases.
2. Download the list of protein sequences for the organism from the CGD. Place the file in /databases/cgd
3. Fast map the list of protein sequences to OMA ids. Download and place the file in /databases/oma
4. Fast map the list of protein sequences to STRING ids. Download and place the file in /databases/string
5. Name all files to '<Name of the Organism>.txt'
6. Download the lists of proteins orthologous from the OMA for every possible pairing of organisms. Place the file in /databases/orthology and name each file '<Name of 1st Organism> <Name of 2nd Organism>.txt'
7. Done. Go ahead and run the program.


**Perfect v. Imperfect**

