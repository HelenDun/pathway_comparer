import sys
import os.path
from os import listdir

OUTPUT_PATH = './output'
TEXT_PATH = OUTPUT_PATH + '/text'
GRAPHS_PATH = OUTPUT_PATH + '/graphs'

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
        self.orthology_perfect = [] # [(protein_a, 56328), (protein_b, 58921), (protein_c, None)]
        self.orthology_imperfect = [] # [(protein_a, 56328), (protein_b, 58921), (protein_c, None)]
    
    def __eq__(self, other):
        is_self_none = self.oma_id is None
        is_other_none = other.oma_id is None
        is_both_none = is_self_none and is_other_none
        is_either_none = is_self_none or is_other_none
        return is_both_none or (not is_either_none and self.oma_id == other.oma_id)
    def __lt__(self, other):
        return self.oma_id is None or (other.oma_id is not None and self.oma_id < other.oma_id)
    def __gt__(self, other):
        return other.oma_id is None or (self.oma_id is not None and self.oma_id > other.oma_id)
    def __le__(self, other):
        return self < other or self == other
    def __ge__(self, other):
        return self > other or self == other
    def __ne__(self, other):
        return not self.oma_id == other.oma_id

    def __str__(self):
        return 'x' + self.oma_id
    
    def __hash__(self):
        return int(self.cgd_id[8:])

    def is_orthologous(self, is_imperfect):
        length = len(self.orthology_perfect)
        if is_imperfect:
            length += len(self.orthology_imperfect)
        return length > 0

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

def write_file(pathname, data):
    file = open(pathname, 'w')
    file.write(data)
    file.close()

def read_cgd(filename, proteins):
    pathname = CGD_PATH + '/' + filename + EXTENSION
    file = open(pathname, 'r')
    data = file.read()
    data = data.split('\n')

    for i in range(1, len(data), 2):
        ids = data[i-1].split('|')
        cgd_id = ids[0][1:]
        proteins.append(Protein(cgd_id))
    return

def read_oma(filename, proteins):
    pathname = OMA_PATH + '/' + filename + EXTENSION
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
    pathname = STRING_PATH + '/' + filename + EXTENSION
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
    # Note. delete all files in the ids folder when this is modified
    proteins = []

    # check if there is an ids file for the organism
    pathname = IDS_PATH + '/' + filename + EXTENSION
    if os.path.isfile(pathname):
        file = open(pathname, 'r')
        for line in file:
            line = line.strip()
            line = line.split('\t')

            oma_id = line[1]
            if oma_id == 'None':
                oma_id = None

            string_id = line[2]
            if string_id == 'None':
                string_id = None

            name = line[3]
            if name == 'None':
                name = None

            proteins.append(Protein(line[0], oma_id=oma_id, string_id=string_id, name=name))
        file.close()

    # make the ids file for the organism
    else:
        # read each database's ids for the organism
        read_cgd(filename, proteins)
        read_oma(filename, proteins)
        read_string(filename, proteins)
        
        # convert to string
        proteins_str = []
        for protein in proteins:
            proteins_str.append('\t'.join([protein.cgd_id, str(protein.oma_id), str(protein.string_id), str(protein.name)]))

        # write to file
        write_file(pathname, '\n'.join(proteins_str))

    proteins.sort()
    return proteins

def read_orthology(filename1, filename2):
    filename = None
    filenames = listdir(ORTHOLOGY_PATH)

    for filename_i in filenames:
        if filename1 in filename_i and filename2 in filename_i:
            filename = filename_i
            break
    if filename is None:
        eprint('Could not find an orthology file for', filename1, 'and', filename2)
        return None

    pathname = ORTHOLOGY_PATH + '/' + filename
    file = open(pathname, 'r')

    orthology = {}
    for line in file:
        line = line.strip()
        line = line.split('\t')
        if len(line) < 2:
            continue

        protein1 = line[0]
        protein2 = line[1]
        score = None
        if len(line) >= 4:
            score = int(line[3])

        if protein1 not in orthology:
            orthology[protein1] = []
        if protein2 not in orthology:
            orthology[protein2] = []
        orthology[protein1].append((protein2, score))
        orthology[protein2].append((protein1, score))

    file.close()
    return orthology

def find_protein(oma_id, proteins):
    assert oma_id is not None
    temp_protein = Protein('', oma_id=oma_id)
    start = 0
    end = len(proteins)
    while (start < end):
        middle = (start + end) // 2
        protein = proteins[middle]
        if (temp_protein == protein):
            return protein
        elif (temp_protein < protein):
            end = middle
        else:
            start = middle + 1
    return None

def compare(proteins1, proteins2, orthology):
    union_imperfect = []
    union_perfect = []
    except_imperfect = []
    except_perfect = []

    for protein1 in proteins1:
        oma_id = protein1.oma_id
        if oma_id is None or oma_id not in orthology:
            except_imperfect.append(protein1)
            except_perfect.append(protein1)
            continue

        pairs = orthology[oma_id]
        for pair in pairs:
            protein2 = find_protein(pair[0], proteins2)
            if protein2 is None:
                protein1.orthology_imperfect.append(pair)
            else:
                protein1.orthology_perfect.append((protein2, pair[1]))

        union_imperfect.append(protein1)
        if len(protein1.orthology_perfect) > 0:
            union_perfect.append(protein1)
        else:
            except_perfect.append(protein1)
    return union_imperfect, union_perfect, except_imperfect, except_perfect

def output_union(filename1, filename2, union_set, is_imperfect):
    str_perfect = 'Perfect'
    if is_imperfect:
        str_perfect = 'Imperfect'
    operation = ' ' + str_perfect + ' Union '

    data = [filename1 + operation + filename2 + ': ' + str(len(union_set))]
    eprint(data[0])

    for protein in union_set:
        orthology_str = []

        orthology = protein.orthology_perfect
        for pair in orthology:
            orthology_str.append('(' + str(pair[0]) + ',' + str(pair[1]) + ')')

        if is_imperfect:
            orthology = protein.orthology_imperfect
            for pair in orthology:
                orthology_str.append('(' + str(pair[0]) + ',' + str(pair[1]) + ')')

        data.append(str(protein.oma_id) + ': [' + ', '.join(orthology_str) + ']')

    pathname = TEXT_PATH + '/' + filename1 + operation + filename2 + EXTENSION
    write_file(pathname, '\n'.join(data))
    return

def output_except(filename1, filename2, except_set, is_imperfect):
    str_perfect = 'Perfect'
    if is_imperfect:
        str_perfect = 'Imperfect'
    operation = ' ' + str_perfect + ' Except '

    data = [filename1 + operation + filename2 + ': ' + str(len(except_set))]
    eprint(data[0])

    for protein in except_set:
        assert len(protein.orthology_perfect) == 0
        assert not is_imperfect or len(protein.orthology_imperfect) == 0
        data.append(protein.cgd_id + '\t' + str(protein.oma_id))
        
    pathname = TEXT_PATH + '/' + filename1 + operation + filename2 + EXTENSION
    write_file(pathname, '\n'.join(data))
    return

def output_string(filename1, filename2, proteins, is_imperfect, is_union):
    data = []
    for protein in proteins:
        if protein.string_id is not None:
            data.append(protein.string_id)

    filename = [filename1, 'Perfect', 'Except', filename2]
    if is_imperfect:
        filename[1] = 'Imperfect'
    if is_union:
        filename[2] = 'Union'
    
    pathname = GRAPHS_PATH + '/' + ' '.join(filename) + EXTENSION
    write_file(pathname, '\n'.join(data))
    return

def output_string_full(filename, proteins):
    data = []
    for protein in proteins:
        if protein.string_id is not None:
            data.append(protein.string_id)
    
    pathname = GRAPHS_PATH + '/' + filename + EXTENSION
    write_file(pathname, '\n'.join(data))
    return

def main():
    # user chooses 2 different organisms
    filenames = list_files()
    file1 = choose_file(filenames)
    file2 = choose_file(filenames)
    while (file1 == file2):
        eprint('You selected the same organism twice.', file=sys.stderr)
        file1 = choose_file(filenames)
        file2 = choose_file(filenames)
    file1 = filenames[file1][:EXTENSION_INDEX]
    file2 = filenames[file2][:EXTENSION_INDEX]

    # read the ids of the proteins of the selected organisms
    proteins1 = read_ids(file1)
    proteins2 = read_ids(file2)
    assert len(proteins1) == len(set(proteins1))
    assert len(proteins2) == len(set(proteins2))

    # read the orthology between the selected organisms
    orthology = read_orthology(file1, file2)

    # compare the organisms
    # union_imperfect, union_perfect, except_imperfect, except_perfect
    union_imperfect1, union_perfect1, except_imperfect1, except_perfect1 = compare(proteins1, proteins2, orthology)
    union_imperfect2, union_perfect2, except_imperfect2, except_perfect2 = compare(proteins2, proteins1, orthology)

    eprint()
    eprint(file1, len(proteins1))
    eprint(file2, len(proteins2))

    # output what proteins are union to txt file
    output_union(file1, file2, union_imperfect1, True)
    output_union(file1, file2, union_perfect1, False)
    output_union(file2, file1, union_imperfect2, True)
    output_union(file2, file1, union_perfect2, False)

    # output what proteins are except to txt file
    output_except(file1, file2, except_imperfect1, True)
    output_except(file1, file2, except_perfect1, False)
    output_except(file2, file1, except_imperfect2, True)
    output_except(file2, file1, except_perfect2, False)

    # output proteins as STRING ids for creating STRING database maps
    output_string_full(file1, proteins1)
    output_string_full(file2, proteins2)

    output_string(file1, file2, union_imperfect1, True, True)
    output_string(file1, file2, union_perfect1, False, True)
    output_string(file2, file1, union_imperfect2, True, True)
    output_string(file2, file1, union_perfect2, False, True)

    output_string(file1, file2, except_imperfect1, True, False)
    output_string(file1, file2, except_perfect1, False, False)
    output_string(file2, file1, except_imperfect2, True, False)
    output_string(file2, file1, except_perfect2, False, False)
    return

if __name__ == '__main__':
    main()