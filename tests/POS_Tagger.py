import sys
import os
path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, '..')
sys.path.insert(0, path)
from pytib import getSylComponents, Agreement, Segment
from pytib.common import open_file
import jsonpickle as jp
jp.set_encoder_options('simplejson', sort_keys=True, indent=4, ensure_ascii=False)
import re


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

equivalence_struct, monlam_map, soas_map = load_equivalence('../pytib/data/POS/Tagset/Equivalence_Table.csv', '../pytib/data/POS/Tagset/Monlam to UD.csv', '../pytib/data/POS/Tagset/SOAS to UD.csv')

monlam_pos = jp.decode(open_file('../pytib/data/POS/output/Monlam_POS.json'))

tsikchen_seg = Segment()
tsikchen_seg.include_user_vocab(['Nanhai_clean'])

to_tag_raw = open_file('to_tag.txt').strip()
to_tag_paragraphs = to_tag_raw.split('\n')
pos_tagged = []
par_tagged = []
for par in to_tag_paragraphs:
    if par_tagged != []:
        pos_tagged.append(par_tagged)
        par_tagged = []
    segmented = Segment().segment(par, reinsert_aa=True, distinguish_ra_sa=True, unknown=0)
    print(segmented)
    words = segmented.split(' ')
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

pos_tagged.append(par_tagged)

print('\n'.join([' '.join(a) for a in pos_tagged]))
