# pathway_comparer
Authors: Helen Dun, Austin Bassett

V-Nums: V00912482, V00


*Introduction*
This program was created to compare the proteins of cellular signalling pathways, specifically circadian rhythm pathways, between organisms. The comparison is output as text files, some for the comparison and others for an easy conversion to a graph for a visual representation. It operates in the following fashion:
1. Has user choose 2 different organisms to compare
2. Reads in the set of proteins for each organism and the orthologous mapping between the organisms
3. Compares the set of proteins using Union and Except operations
4. Outputs the results


*Running the Program*
To run the program, run the following command:
    python3 main.py

Note. I use a MacOS environment with Python version 3.8.2

The program will then prompt you to choose 2 organisms for comparison using listed index numbers. When done, the program will output how many proteins there are for each organism and in each set to the commandline. The comparison files will be output to the output directory.

There are 2 folders in the output directory: graphs and text. The graphs folder contains textfiles, each containing the STRING ids for a set of proteins. These are inputs to the STRING database to easily make STRING graphs. The text folder contains textfiles, each containing the OMA ids for a set of proteins. For each protein P in the Union textfiles, there should also be a correlating list of OMA ids and scores for the proteins orthologous to P. If an OMA id has an 'x' character at the beginning, this means the protein is part of both the Imperfect and Perfect sets. Otherwise, if there is no 'x' character, the protein is only part of the Imperfect set.


*Algorithm*
The program uses files from 3 different databases:
- Circadian Gene Database (CGD)
- Orthologous MAtrix Project (OMA)
- STRING Database

CGD is used to find the lists of circadian rhythm proteins. OMA is used to find orthology between the proteins of organisms. STRING is used to graph the output of the program for better visualization and analysis.

For the 2 organisms chosen, A and B, the program outputs 8 different sets as text files: Imperfect Union (A,B), Perfect Union (A,B), Imperfect Except (A,B), Perfect Except (A,B), Imperfect Union (B,A), Perfect Union (B,A), Imperfect Except (B,A) and Perfect Except (B,A).


**Why Order Matters**
Some proteins of organism A can be orthologous to many proteins in organism B and vice-versa. Therefore, for the union of orthologous proteins in A and B the program would have to create a node that combines all proteins orthologous with each other. This was infeasible as for the graph part STRING only takes a list of proteins so we would need to create or use some otther graphing software for the project. Simplifying the graph of the pathway may also be destructive to information about the proteins. Instead, Union (A,B) is the set of proteins in A that are orthologous to some protein in organism B and Union (B,A) is the set of proteins in B that are orthologous to some protein in organism A.


**Union and Except**
There are 2 set operations this program performs on the proteins of the 2 selected organisms: Union (U) and Except (-). As mentioned in the previous section, the Union operation is slightly different from the well-known set operation as it does not consolidate the 2 input sets. The Union operation takes the sets of proteins for 2 organisms, A and B, and the orthology between them and returns the subset of proteins of organism A that are orthologous to some protein of organism B. The Except operation takes the same input but does the opposite of the Union function: it returns the subset of proteins of organism A that are not orthologous to any protein of organism B.


**Perfect v. Imperfect**
Protein A from Organism X is orthologous to a set of proteins P of Organism Y. For some protein Q in P, Q may or may not be a protein of the cellular signalling pathway being studied in Organism Y. Suppose Q is not. Do we keep that A is orthologous to Q? The Imperfect set keeps the orthology between A and Q and the Perfect set does not.


*Adding an Organism*
1. Choose an organism. Make sure the organism is listed in all 3 databases.
2. Download the list of protein sequences for the organism from the CGD. Place the file in /databases/cgd
3. Fast map the list of protein sequences to OMA ids. Download and place the file in /databases/oma
4. Fast map the list of protein sequences to STRING ids. Download and place the file in /databases/string
5. Name all files to '<Name of the Organism>.txt'
6. Download the lists of proteins orthologous from the OMA for every possible pairing of the  new organism with all other organisms. Place the file in /databases/orthology and name each file '<Name of 1st Organism> <Name of 2nd Organism>.txt'
7. Done. Go ahead and run the program.



*References*

**Circadian Gene Database (CGD)**
Shujing Li, Ke Shui, Ying Zhang, Yongqiang Lv, Wankun Deng, Shahid Ullah, Luoying Zhang, Yu Xue, CGDB: a database of circadian genes in eukaryotes, Nucleic Acids Research, Volume 45, Issue D1, January 2017, Pages D397–D403, https://doi.org/10.1093/nar/gkw1028

**STRING Database**
Szklarczyk D, Gable AL, Nastou KC, Lyon D, Kirsch R, Pyysalo S, Doncheva NT, Legeay M, Fang T, Bork P, Jensen LJ, von Mering C. The STRING database in 2021: customizable protein-protein networks, and functional characterization of user-uploaded gene/measurement sets. Nucleic Acids Res. 2021 Jan 8;49(D1):D605-D612. doi: 10.1093/nar/gkaa1074. Erratum in: Nucleic Acids Res. 2021 Oct 11;49(18):10800. PMID: 33237311; PMCID: PMC7779004.

Szklarczyk D, Gable AL, Lyon D, Junge A, Wyder S, Huerta-Cepas J, Simonovic M, Doncheva NT, Morris JH, Bork P, Jensen LJ, Mering CV. STRING v11: protein-protein association networks with increased coverage, supporting functional discovery in genome-wide experimental datasets. Nucleic Acids Res. 2019 Jan 8;47(D1):D607-D613. doi: 10.1093/nar/gky1131. PMID: 30476243; PMCID: PMC6323986.

Szklarczyk D, Morris JH, Cook H, Kuhn M, Wyder S, Simonovic M, Santos A, Doncheva NT, Roth A, Bork P, Jensen LJ, von Mering C. The STRING database in 2017: quality-controlled protein-protein association networks, made broadly accessible. Nucleic Acids Res. 2017 Jan 4;45(D1):D362-D368. doi: 10.1093/nar/gkw937. Epub 2016 Oct 18. PMID: 27924014; PMCID: PMC5210637.

Szklarczyk D, Franceschini A, Wyder S, Forslund K, Heller D, Huerta-Cepas J, Simonovic M, Roth A, Santos A, Tsafou KP, Kuhn M, Bork P, Jensen LJ, von Mering C. STRING v10: protein-protein interaction networks, integrated over the tree of life. Nucleic Acids Res. 2015 Jan;43(Database issue):D447-52. doi: 10.1093/nar/gku1003. Epub 2014 Oct 28. PMID: 25352553; PMCID: PMC4383874.

Franceschini A, Lin J, von Mering C, Jensen LJ. SVD-phy: improved prediction of protein functional associations through singular value decomposition of phylogenetic profiles. Bioinformatics. 2016 Apr 1;32(7):1085-7. doi: 10.1093/bioinformatics/btv696. Epub 2015 Nov 26. PMID: 26614125; PMCID: PMC4896368.

Franceschini A, Szklarczyk D, Frankild S, Kuhn M, Simonovic M, Roth A, Lin J, Minguez P, Bork P, von Mering C, Jensen LJ. STRING v9.1: protein-protein interaction networks, with increased coverage and integration. Nucleic Acids Res. 2013 Jan;41(Database issue):D808-15. doi: 10.1093/nar/gks1094. Epub 2012 Nov 29. PMID: 23203871; PMCID: PMC3531103.

Szklarczyk D, Franceschini A, Kuhn M, Simonovic M, Roth A, Minguez P, Doerks T, Stark M, Muller J, Bork P, Jensen LJ, von Mering C. The STRING database in 2011: functional interaction networks of proteins, globally integrated and scored. Nucleic Acids Res. 2011 Jan;39(Database issue):D561-8. doi: 10.1093/nar/gkq973. Epub 2010 Nov 2. PMID: 21045058; PMCID: PMC3013807.

Jensen LJ, Kuhn M, Stark M, Chaffron S, Creevey C, Muller J, Doerks T, Julien P, Roth A, Simonovic M, Bork P, von Mering C. STRING 8--a global view on proteins and their functional interactions in 630 organisms. Nucleic Acids Res. 2009 Jan;37(Database issue):D412-6. doi: 10.1093/nar/gkn760. Epub 2008 Oct 21. PMID: 18940858; PMCID: PMC2686466.

von Mering C, Jensen LJ, Kuhn M, Chaffron S, Doerks T, Krüger B, Snel B, Bork P. STRING 7--recent developments in the integration and prediction of protein interactions. Nucleic Acids Res. 2007 Jan;35(Database issue):D358-62. doi: 10.1093/nar/gkl825. Epub 2006 Nov 10. PMID: 17098935; PMCID: PMC1669762.

von Mering C, Jensen LJ, Snel B, Hooper SD, Krupp M, Foglierini M, Jouffre N, Huynen MA, Bork P. STRING: known and predicted protein-protein associations, integrated and transferred across organisms. Nucleic Acids Res. 2005 Jan 1;33(Database issue):D433-7. doi: 10.1093/nar/gki005. PMID: 15608232; PMCID: PMC539959.

von Mering C, Huynen M, Jaeggi D, Schmidt S, Bork P, Snel B. STRING: a database of predicted functional associations between proteins. Nucleic Acids Res. 2003 Jan 1;31(1):258-61. doi: 10.1093/nar/gkg034. PMID: 12519996; PMCID: PMC165481.

Snel B, Lehmann G, Bork P, Huynen MA. STRING: a web-server to retrieve and display the repeatedly occurring neighbourhood of a gene. Nucleic Acids Res. 2000 Sep 15;28(18):3442-4. doi: 10.1093/nar/28.18.3442. PMID: 10982861; PMCID: PMC110752.

**Orthologous MAtrix Project (OMA)**
Adrian M Altenhoff, Clément-Marie Train, Kimberly J Gilbert, Ishita Mediratta, Tarcisio Mendes de Farias, David Moi, Yannis Nevers, Hale-Seda Radoykova, Victor Rossier, Alex Warwick Vesztrocy, Natasha M Glover, Christophe Dessimoz, OMA orthology in 2021: website overhaul, conserved isoforms, ancestral gene order and more, Nucleic Acids Research, Volume 49, Issue D1, 8 January 2021, Pages D373–D379, https://doi.org/10.1093/nar/gkaa1007

Adrian M Altenhoff, Natasha M Glover, Clément-Marie Train, Klara Kaleb, Alex Warwick Vesztrocy, David Dylus, Tarcisio M de Farias, Karina Zile, Charles Stevenson, Jiao Long, Henning Redestig, Gaston H Gonnet, Christophe Dessimoz, The OMA orthology database in 2018: retrieving evolutionary relationships among all domains of life through richer web and programmatic interfaces, Nucleic Acids Research, Volume 46, Issue D1, 4 January 2018, Pages D477–D485, https://doi.org/10.1093/nar/gkx1019

Adrian M. Altenhoff, Nives Škunca, Natasha Glover, Clément-Marie Train, Anna Sueki, Ivana Piližota, Kevin Gori, Bartlomiej Tomiczek, Steven Müller, Henning Redestig, Gaston H. Gonnet, Christophe Dessimoz, The OMA orthology database in 2015: function predictions, better plant support, synteny view and other improvements, Nucleic Acids Research, Volume 43, Issue D1, 28 January 2015, Pages D240–D249, https://doi.org/10.1093/nar/gku1158

Adrian M. Altenhoff, Adrian Schneider, Gaston H. Gonnet, Christophe Dessimoz, OMA 2011: orthology inference among 1000 complete genomes, Nucleic Acids Research, Volume 39, Issue suppl_1, 1 January 2011, Pages D289–D294, https://doi.org/10.1093/nar/gkq1238

Adrian Schneider, Christophe Dessimoz, Gaston H. Gonnet, OMA Browser—Exploring orthologous relations across 352 complete genomes, Bioinformatics, Volume 23, Issue 16, 15 August 2007, Pages 2180–2182, https://doi.org/10.1093/bioinformatics/btm295

Glover NM, Altenhoff A, Dessimoz C. 2019. Assigning confidence scores to homoeologs using fuzzy logic. PeerJ 6:e6231 https://doi.org/10.7717/peerj.6231

Clément-Marie Train, Natasha M Glover, Gaston H Gonnet, Adrian M Altenhoff, Christophe Dessimoz, Orthologous Matrix (OMA) algorithm 2.0: more robust to asymmetric evolutionary rates and more scalable hierarchical orthologous group inference, Bioinformatics, Volume 33, Issue 14, 15 July 2017, Pages i75–i82, https://doi.org/10.1093/bioinformatics/btx229

Altenhoff AM, Gil M, Gonnet GH, Dessimoz C (2013) Inferring Hierarchical Orthologous Groups from Orthologous Gene Pairs. PLoS ONE 8(1): e53786. https://doi.org/10.1371/journal.pone.0053786

Roth, A.C., Gonnet, G.H. & Dessimoz, C. Algorithm of OMA for large-scale orthology inference. BMC Bioinformatics 9, 518 (2008). https://doi.org/10.1186/1471-2105-9-518

Christophe Dessimoz, Brigitte Boeckmann, Alexander C. J. Roth, Gaston H. Gonnet, Detecting non-orthology in the COGs database and other approaches grouping orthologs using genome-specific best hits, Nucleic Acids Research, Volume 34, Issue 11, 1 June 2006, Pages 3309–3316, https://doi.org/10.1093/nar/gkl433

Dessimoz C. et al. (2005) OMA, A Comprehensive, Automated Project for the Identification of Orthologs from Complete Genome Data: Introduction and First Achievements. In: McLysaght A., Huson D.H. (eds) Comparative Genomics. RCG 2005. Lecture Notes in Computer Science, vol 3678. Springer, Berlin, Heidelberg. https://doi.org/10.1007/11554714_6

Altenhoff, A., Boeckmann, B., Capella-Gutierrez, S. et al. Standardized benchmarking in the quest for orthologs. Nat Methods 13, 425–430 (2016). https://doi.org/10.1038/nmeth.3830

Dalquen DA, Altenhoff AM, Gonnet GH, Dessimoz C (2013) The Impact of Gene Duplication, Insertion, Deletion, Lateral Gene Transfer and Sequencing Error on Orthology Inference: A Simulation Study. PLoS ONE 8(2): e56925. https://doi.org/10.1371/journal.pone.0056925

Brigitte Boeckmann, Marc Robinson-Rechavi, Ioannis Xenarios, Christophe Dessimoz, Conceptual framework and pilot study to benchmark phylogenomic databases based on reference gene trees, Briefings in Bioinformatics, Volume 12, Issue 5, September 2011, Pages 423–435, https://doi.org/10.1093/bib/bbr034

Altenhoff AM, Dessimoz C (2009) Phylogenetic and Functional Assessment of Orthologs Inference Projects and Methods. PLoS Comput Biol 5(1): e1000262. https://doi.org/10.1371/journal.pcbi.1000262

Brigitte Boeckmann, Marc Robinson-Rechavi, Ioannis Xenarios, Christophe Dessimoz, Conceptual framework and pilot study to benchmark phylogenomic databases based on reference gene trees, Briefings in Bioinformatics, Volume 12, Issue 5, September 2011, Pages 423–435, https://doi.org/10.1093/bib/bbr034

Altenhoff AM, Dessimoz C (2009) Phylogenetic and Functional Assessment of Orthologs Inference Projects and Methods. PLoS Comput Biol 5(1): e1000262. https://doi.org/10.1371/journal.pcbi.1000262

Altenhoff A.M., Dessimoz C. (2012) Inferring Orthology and Paralogy. In: Anisimova M. (eds) Evolutionary Genomics. Methods in Molecular Biology (Methods and Protocols), vol 855. Humana Press, Totowa, NJ. https://doi.org/10.1007/978-1-61779-582-4_9