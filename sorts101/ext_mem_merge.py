import string
import tqdm
import os
import shutil
import numpy as np


ABC = list(string.ascii_letters)
CHUNK_SIZE = 10000000
BLOCK_SIZE = 1000000


def recursive_mkdir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def merge(block1, block2):
    """
    :param block1: sorted list
    :param block2: sorted list
    :return: merged sorted list
    """
    res_block = []
    ptr1, ptr2 = 0, 0

    while len(res_block) < len(block1) + len(block2):
        if ptr1 < len(block1) and ptr2 < len(block2):
            if block1[ptr1] < block2[ptr2]:
                res_block.append(block1[ptr1])
                ptr1 += 1
            else:
                res_block.append(block2[ptr2])
                ptr2 += 1

        elif ptr1 == len(block1):
            res_block.append(block2[ptr2])
            ptr2 += 1
        else:
            res_block.append(block1[ptr1])
            ptr1 += 1
    return res_block


def merge_files(file1, file2, step, block):
    recursive_mkdir('step{}'.format(step))
    res_block, file = [], open('step{}/{}'.format(step, block), 'w')
    ptr1, ptr2 = 0, 0

    loader1 = load_strings(file1, BLOCK_SIZE)
    loader2 = load_strings(file2, BLOCK_SIZE)

    block1 = loader1.__next__()
    block2 = loader2.__next__()

    while ptr1 + ptr2 < len(block1) + len(block2):
        if ptr1 < len(block1) and ptr2 < len(block2):
            if block1[ptr1] < block2[ptr2]:
                res_block.append(block1[ptr1])
                ptr1 += 1
            else:
                res_block.append(block2[ptr2])
                ptr2 += 1
        elif ptr1 == len(block1):
            res_block.append(block2[ptr2])
            ptr2 += 1
        elif ptr2 == len(block2):
            res_block.append(block1[ptr1])
            ptr1 += 1

        if ptr1 == len(block1):
            ptr1 = 0
            try:
                block1 = loader1.__next__()
            except StopIteration:
                block1 = []

        if ptr2 == len(block2):
            ptr2 = 0
            try:
                block2 = loader2.__next__()
            except StopIteration:
                block2 = []

        if len(res_block) > BLOCK_SIZE:
            file.write('\n'.join(res_block) + '\n')
            res_block = []

    if len(res_block):
        file.write('\n'.join(res_block) + '\n')
    file.close()


def generate_big_file(file_path, string_len=100, num_lines=1000):
    num_chars = string_len * num_lines
    num_chunks = num_chars // CHUNK_SIZE + 1

    f = open(file_path, 'w')
    for _ in tqdm.tqdm(range(num_chunks)):
        s_list = []
        for _ in range(num_lines // num_chunks):
            s_list.append('{}'.format("".join(np.random.choice(ABC, string_len))))

        f.write('\n'.join(s_list))
        f.write('\n')
    f.close()


def load_strings(file_path, num_bytes):
    lines = []
    num_bytes_left = num_bytes
    with open(file_path) as f:
        line = f.readline().strip()
        while line != '':
            num_bytes_left -= len(line)
            lines.append(line)
            if num_bytes_left <= 0:
                yield lines
                lines = []
                num_bytes_left = num_bytes
            line = f.readline().strip()

    if len(lines):
        yield lines


def sort_step(step, num_blocks):
    save_step, num = step + 1, 0

    blocks = [(2 * i, 2 * i + 1) for i in range(num_blocks // 2)]
    if num_blocks % 2 == 1:
        blocks += [(num_blocks - 1,)]

    for num, block in enumerate(blocks):
        if len(block) == 2:
            print('merging blocks {} on step {}'.format(block, step))
            merge_files('step{}/{}'.format(step, block[0]),
                        'step{}/{}'.format(step, block[1]),
                        step=save_step, block=num)
        else:
            shutil.copy('step{}/{}'.format(step, block[0]), 'step{}/{}'.format(save_step, num))

    return save_step, num + 1


def sort_big_file(file_path):
    num_blocks = generate_sorted_blocks(file_path)
    step = 1

    while num_blocks > 1:
        step, num_blocks = sort_step(step, num_blocks)


def write_string_list(string_list, path):
    with open(path, 'w') as f:
        f.write('\n'.join(string_list))


def generate_sorted_blocks(file_path):
    string_loader, num = load_strings(file_path, CHUNK_SIZE), 0
    recursive_mkdir('step1')
    for num, s_list in enumerate(string_loader):
        s_list.sort()
        write_string_list(s_list, os.path.join('step1', '{}'.format(num)))

    return num + 1
