import sys
import os.path
from os import listdir
from omadb import Client

OUTPUT_PATH = './output'
DATABASES_PATH = './databases'
IDS_PATH = DATABASES_PATH + '/ids'
CGD_PATH = DATABASES_PATH + '/cgd'
OMA_PATH = DATABASES_PATH + '/oma'
STRING_PATH = DATABASES_PATH + '/string'
ORTHOLOGY_PATH = DATABASES_PATH + '/orthology'

EXTENSION = '.txt'
EXTENSION_INDEX = -1 * len(EXTENSION)

class Protein():
    def __init__(self, cgd_id, oma_id=None, string_id=None, name=None):
        self.cgd_id = cgd_id
        self.oma_id = oma_id
        self.string_id = string_id
        self.name = name
    def __str__(self):
        return '\t'.join([self.cgd_id, str(self.oma_id), str(self.string_id), str(self.name)])

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def list_files():
    filenames = listdir(CGD_PATH)
    for filename in filenames:
        if not filename.endswith(EXTENSION):
            filenames.remove(filename)
    return filenames

def choose_file(filenames):
    data = ""
    while (not data.isdigit() or int(data) >= len(filenames)):
        for i in range(0, len(filenames)):
            eprint(i, filenames[i][:EXTENSION_INDEX])
        eprint('Choose an organism: ', end='')
        data = input()
    return int(data)

def read_cgd(filename, proteins):
    pathname = CGD_PATH + '/' + filename
    file = open(pathname, 'r')
    data = file.read()
    data = data.split('\n')

    for i in range(1, len(data), 2):
        ids = data[i-1].split('|')
        cgd_id = ids[0][1:]
        sequence = data[i]
        proteins.append(Protein(cgd_id, sequence))
    return

def read_oma(filename, proteins):
    pathname = OMA_PATH + '/' + filename
    file = open(pathname, 'r')
    data = file.read()
    data = data.split('\n')

    i_data = 1
    i_proteins = 0
    while (i_data < len(data) and i_proteins < len(proteins)):
        line = data[i_data].split('\t')
        protein = proteins[i_proteins]

        if protein.cgd_id in line[0]:
            protein.oma_id = line[1]
            i_data += 1
        i_proteins += 1
    return

def read_string(filename, proteins):
    pathname = STRING_PATH + '/' + filename[:EXTENSION_INDEX] + '.tsv'
    eprint(pathname)
    file = open(pathname, 'r')
    data = file.read()
    data = data.split('\n')

    i_data = 1
    i_proteins = 0
    while (i_data < len(data) and i_proteins < len(proteins)):
        line = data[i_data].split('\t')
        protein = proteins[i_proteins]

        if protein.cgd_id in line[1]:
            protein.string_id = line[2]
            protein.name = line[5]
            i_data += 1
        i_proteins += 1
    return

def read_ids(filename):
    proteins = []

    # check if there is an ids file for the organism
    pathname = IDS_PATH + '/' + filename
    if os.path.isfile(pathname):
        file = open(pathname, 'r')
        for line in file:
            line = line.strip()
            line = line.split('\t')

            if len(line) < 4:
                eprint(line)
                continue

            proteins.append(Protein(line[0], oma_id=line[1], string_id=line[2], name=line[3]))
        file.close()

    # make the ids file for the organism
    else:
        read_cgd(filename, proteins)
        read_oma(filename, proteins)
        read_string(filename, proteins)
        
        proteins_str = []
        for protein in proteins:
            proteins_str.append(str(protein))
        
        file = open(pathname, 'w')
        file.write('\n'.join(proteins_str))
        file.close()
    return proteins

def read_orthology(filename1, filename2):
    filename = None
    filenames = listdir(ORTHOLOGY_PATH)
    filename1 = filename1[:EXTENSION_INDEX]
    filename2 = filename2[:EXTENSION_INDEX]

    for filename_i in filenames:
        if filename1 in filename_i and filename2 in filename_i:
            filename = filename_i
            break
        if filename1 in filename_i or filename2 in filename_i:
            eprint(filename_i)
    if filename is None:
        eprint('Could not find an orthology file for', filename1, 'and', filename2)
        return None

    pathname = ORTHOLOGY_PATH + '/' + filename
    file = open(pathname, 'r')

    orthology = {}
    for line in file:
        line = line.split('\t')
        if len(line) < 2:
            continue

        protein1 = line[0]
        protein2 = line[1]
        if protein1 not in orthology:
            orthology[protein1] = []
        if protein2 not in orthology:
            orthology[protein2] = []
        orthology[protein1].append(protein2)
        orthology[protein2].append(protein1)
    file.close()
    return orthology

def compare(proteins, orthology):
    pUnion = []
    pExcept = []

    for protein in proteins:
        oma_id = protein.oma_id
        if oma_id in orthology:
            protein.orthology = orthology[oma_id]
            pUnion.append(protein)
        else:
            pExcept.append(protein)

    return pUnion, pExcept

def output_compare(filename1, filename2, pUnion, pExcept):
    filename1 = filename1[:EXTENSION_INDEX]
    filename2 = filename2[:EXTENSION_INDEX]

    data = [filename1 + ' Union ' + filename2 + ': ' + str(len(pUnion))]
    for protein in pUnion:
        orthology_str = []
        for orthology in protein.orthology:
            orthology_str.append(str(orthology))
        data.append(str(protein.oma_id) + ': ' + ','.join(orthology))

    data.append(filename1 + ' Except ' + filename2 + ': ' + str(len(pExcept)))
    data.extend(pExcept)

    pathname = OUTPUT_PATH + '/' + filename1 + ' ' + filename2 + EXTENSION
    file = open(pathname, 'w')
    file.write('\n'.join(data))
    file.close()
    return

def main():
    filenames = list_files()
    file1 = choose_file(filenames)
    file2 = choose_file(filenames)
    while (file1 == file2):
        eprint('You selected the same organism twice.', file=sys.stderr)
        file1 = choose_file(filenames)
        file2 = choose_file(filenames)
    file1 = filenames[file1]
    file2 = filenames[file2]
    proteins1 = read_ids(file1)
    proteins2 = read_ids(file2)
    orthology = read_orthology(file1, file2)

    p1Union, p1Except = compare(proteins1, orthology)
    p2Union, p2Except = compare(proteins2, orthology)

    output_compare(file1, file2, p1Union, p1Except)

    eprint('Fin.')

if __name__ == '__main__':
    main()