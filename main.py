import os,glob
os.environ['TRANSFORMERS_OFFLINE'] = '1'
from tqdm import tqdm
from g2pw import G2PWConverter


def chai_p(char , clean_num = True):
    ALL_SHENMU = ['zh', 'ch', 'sh', 'b', 'p', 'm', 'f', 'd', 
                  't', 'n', 'l', 'g', 'k', 'h', 'j',
                  'q', 'x', 'r', 'z', 'c', 's', 'y', 'w']
    if char[-1] in {'1','2','3','4','5'}:
        if clean_num:
            char = char[:-1]
            _char = char
        else:
            _char = char
    else:
        _char = char
    res = []
    if char[:2] in ALL_SHENMU:
        res.append( char[:2] )
        char = char[2:]
    else:
        res.append( char[:1] )
        char = char[1:]
    if len(char) > 0:
        res.append(char)
    if res[-1] in {'1','2','3','4','5'}:
        _op = ''.join(res)
    else:
        _op = ' '.join(res)
    return _char , _op

if __name__ == '__main__':
    import  yaml,argparse
    # from pypinyin.style._utils import get_initials,get_finals
    # chai_p('an1',True)
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_path", default='./config.yaml', type=str)
    args = parser.parse_args()
    config = yaml.safe_load(open(args.config_path))    
    paths = glob.glob( config['data_path_txt'] )

    zh_char_pin = G2PWConverter(style='pinyin', 
        model_dir='./G2PWModel',
        model_source = './g2p_token/',
        enable_non_tradional_chinese=True,device= config['device'] )
    dic_word_pp = {}
    for path in tqdm(paths):
        save_path = path.replace('.txt','.lab')
        if os.path.isfile(save_path):
            continue
        with open(path) as file:
            txt = file.read().split('\n')[0]#[:-1]
        res = []
        pinyins = zh_char_pin(txt)[0]
        _so_b_ = ( len(pinyins) == len(txt) )
        if  not _so_b_:
            print ('bbb {}'.format(txt))
        for ind , pinyin in enumerate(pinyins):
            if pinyin is None  :
                if _so_b_:
                    res.append( txt[ind] )
                    dic_word_pp[txt[ind]] = txt[ind]
                continue
            _0 , _1 = chai_p(pinyin,clean_num=config['clean_num'] ) 
            res.append(_0)
            dic_word_pp[_0] = _1
        with open(save_path , 'w') as file:
            file.write(' '.join(res))
    with open( config['save_dic_path'],'w') as file:
        res_0 = [ '{}\t{}'.format(key , oo)  for key ,oo in dic_word_pp.items()]
        res_0.sort()
        file.write('\n'.join( res_0 ))