# read result file
from collections import defaultdict
import numpy as np
import hicstraw
import pysam

def load_matrix_from_cool(clr, chrom1, chrom2):
    # load matrix from cool file
    chromsomes = clr.chromnames
    if chrom1 not in chromsomes or chrom2 not in chromsomes:
        raise ValueError(f"Chromosome number is invalidation.")
    if chrom1 == chrom2:
        M = clr.matrix(balance=False).fetch(chrom1)
    else:
        M = clr.matrix(balance=False).fetch(chrom1, chrom2)

    M[np.isnan(M)] = 0
    return M

def load_matrix_from_hic(hicfile, chrom1, chrom2, resolution):
    # load matrix from hic file
    hic = hicstraw.HiCFile(hicfile)
    result = hicstraw.straw('observed', 'NONE', hicfile, chrom1, chrom2, 'BP', resolution)
    # load chrom length
    chromosomes = hic.getChromosomes()
    chrom1_length = next(chrom.length for chrom in chromosomes if chrom.name == chrom1)
    chrom2_length = next(chrom.length for chrom in chromosomes if chrom.name == chrom2)
    size1 = chrom1_length // resolution + 1
    size2 = chrom2_length // resolution + 1
    # init matrix
    contact_matrix = np.zeros((size1, size2))
    for i in range(len(result)):
        row_idx = result[i].binX // resolution
        col_idx = result[i].binY // resolution
        contact_matrix[row_idx, col_idx] = result[i].counts
    if chrom1 == chrom2:
        contact_matrix += contact_matrix.T - np.diag(contact_matrix.diagonal())
    return contact_matrix

def group(data):
    '''
    # Merge consecutive identical values
    :param data: pos index
    :return: start and end of consecutive same values
    '''
    index = 10
    last = data[0]
    start = end = 0
    for n in data[1:]:
        if n - last <= index: # Part of the group, bump the end
            last = n
            end += 1
        else: # Not part of the group, yield current group and start a new
            yield range(data[start], data[end]+1)
            last = n
            start = end = end + 1
    # yield start, end
    yield range(data[start], data[end]+1)


def group_position(pos1list, pos2list):
    result = defaultdict(list)
    l1 = sorted(set(pos1list), key=pos1list.index)
    pos1group = list(group(l1))
    for i in range(len(pos1group)):
        start_pos = pos1list.index(pos1group[i][0])
        end_pos = len(pos1list) - 1 - pos1list[::-1].index(pos1group[i][-1])
        cur_pos2_list = pos2list[start_pos:end_pos + 1]
        cur_pos1_list = pos1list[start_pos:end_pos + 1]
        cur_pos2_list_sort = sorted(cur_pos2_list)
        l2 = sorted(set(cur_pos2_list_sort), key=cur_pos2_list_sort.index)
        pos2group = list(group(l2))
        if len(pos2group) > 1:
            for j in range(len(pos2group)):
                new_pos1 = []
                for k in range(len(pos2group[j])):
                    if pos2group[j][k] in cur_pos2_list:
                        pos = cur_pos2_list.index(pos2group[j][k])
                        new_pos1.append(cur_pos1_list[pos])

                new_pos1 = sorted(new_pos1)
                result['pos1_start'].append(new_pos1[0])
                result['pos1_end'].append(new_pos1[-1])
                result['pos2_start'].append(pos2group[j][0])
                result['pos2_end'].append(pos2group[j][-1])

        else:
            result['pos1_start'].append(pos1group[i][0])
            result['pos1_end'].append(pos1group[i][-1])
            result['pos2_start'].append(pos2group[0][0])
            result['pos2_end'].append(pos2group[0][-1])
    return result

