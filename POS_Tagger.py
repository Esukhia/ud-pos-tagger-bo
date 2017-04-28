import re
import os
from dependencies.pytib import Segment
from dependencies.pytib.common import open_file, write_file
import json

def load_equivalence(Table, Monlam, SOAS):
    # parse Equivalence Table
    equivalence = open_file(Table).strip().split('\n')
    structure = {}
    UD_general = equivalence[0].split(',')[1:]
    for tag in UD_general:
        structure[tag] = {}

    for line in equivalence:
        parts = line.split(',')
        Type = parts[0]
        for idx in range(len(UD_general)):
            UD = UD_general[idx]
            new_tag = parts[idx+1]
            structure[UD][Type] = new_tag

    # parse Monlam to UD
    monlam = open_file(Monlam).strip().split('\n')
    monlam_map = {}
    for line in monlam[1:]:
        m_parts = line.split(',')
        for idx in range(len(UD_general)):
            m_UD = UD_general[idx]
            m_new_tag = m_parts[idx]
            if m_new_tag != '':
                monlam_map[m_new_tag] = m_UD

    # parse SOAS to UD
    soas = open_file(SOAS).strip().split('\n')
    soas_map = {}
    for line in soas[1:]:
        s_parts = line.split(',')
        for idx in range(len(UD_general)):
            s_UD = UD_general[idx]
            s_new_tag = s_parts[idx]
            if s_new_tag != '':
                soas_map[s_new_tag] = s_UD
    return structure, monlam_map, soas_map

# load the data for the POS tagger
equivalence_struct, monlam_map, soas_map = load_equivalence('data/Tagset/Equivalence_Table.csv', 'data/Tagset/Monlam to UD.csv', 'data/Tagset/SOAS to UD.csv')
monlam_pos = json.loads(open_file('data/Monlam_POS.json'))

# load the pytib and the data we want
nanhai_seg = Segment()
nanhai_seg.include_user_vocab(['Nanhai_clean'])
nanhai_seg.include_user_vocab(local_vocab=['ཐོགས་མེད་'])  # add custom words missing in the vocabs

# POS Tagging
print('Processing:')
in_path = 'input'
out_path = 'output'
for f in os.listdir(in_path):
    print('\t'+f)
    f_name = f.replace('.txt', '')
    to_tag_raw = open_file('{}/{}'.format(in_path, f)).strip()
    to_tag_paragraphs = to_tag_raw.split('\n')
    pos_tagged = []
    par_tagged = []
    for par in to_tag_paragraphs:
        if par_tagged != []:
            pos_tagged.append(par_tagged)
            par_tagged = []
        # segment the paragraph (the current line)
        segmented = nanhai_seg.segment(par, reinsert_aa=True, distinguish_ra_sa=True, unknown=0)
        words = segmented.split(' ')
        # actual POS Tagging
        for word in words:
            word_to_match = word.strip('་')
            if word_to_match in monlam_pos or word_to_match.replace('%', 'འ') in monlam_pos:
                m_pos = monlam_pos[word_to_match.replace('%', 'འ')][0]
                m_UD = monlam_map[m_pos]
                tib_pos = equivalence_struct[m_UD]['UD General']
                par_tagged.append('{}/{}'.format(word.replace('%', ''), tib_pos))
            elif re.match(r'(་?[༄༅༆༇༈།༎༏༐༑༔\s]+་?)', word):
                par_tagged.append(word + '/PUNCT')
            else:
                par_tagged.append(word.replace('@', '')+'/X')

    # add the last paragraph
    pos_tagged.append(par_tagged)

    # generate the string to write
    output = '\n'.join([' '.join(a) for a in pos_tagged])

    write_file('{}/{}_POS.txt'.format(out_path, f_name), output)
