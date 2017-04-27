from utils import *
import jsonpickle as jp
jp.set_encoder_options('simplejson', sort_keys=True, indent=4, ensure_ascii=False)

content = open_file('third_party/monlam1_pos.txt')
lines = content.strip().split('\n')

structure = {}
for line in lines:
    ## ཀ་མིག—འཇལ་ཚིག: རྒྱུན་སྤྱོད། / མིང་ཚིག:
    entry, defi = line.split('—')
    structure[entry] = []
    meanings = defi.split('/')
    for meaning in meanings:
        pos, others = meaning.split(':')
        # features = list(set(others.split('_')))
        structure[entry].append(pos)  # for the time being, I only take the POS

write_file('output/Monlam_POS.json', jp.encode(structure))
print('ok')