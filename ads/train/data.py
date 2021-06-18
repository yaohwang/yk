# encoding: utf-8

import traceback
import pandas as pd

from tqdm import tqdm
from pathlib import Path

from typing import (
    List,
    Union,
)


def load(path: Path, columns: Union[str, List[str]] = None) -> pd.DataFrame:
    
    if isinstance(columns, str):
        columns = [columns]
    elif (not isinstance(columns, List)) and columns is not None:
        raise ValueError(
            f"type of columns unknown: {type(columns)}. "
            f"Should be one of a str or list[str]."
        )  
        
    return _load(path, columns)


def _load(path: Path, columns: List[str]) -> pd.DataFrame:
    
    def load_dir(path: Path) -> pd.DataFrame:
        try:
            return pd.concat(load_file(p) for p in path.iterdir())
        except:
            # traceback.print_exc()
            pass
    
    def load_file(path: Path) -> pd.DataFrame:
        try:
            if path.name.startswith('chat_record'):
                return pd.read_csv(path, sep='\t', header=None)
        except:
            pass
    
    df = pd.concat(load_dir(p) for p in tqdm(list(path.iterdir())))
    
    if 13 == len(df.columns):
        df.columns = [
            '_id',
            'platform',
            'server_id',
            'role_uid',
            'name',
            'level',
            'vip',
            'target_uid',
            'channel',
            'msg_type',
            'is_audio',
            'chat_content',
            'time',
        ]
    elif 27 == len(df.columns):
        df.columns = [
            '_id',
            'platform',
            'server_id',
            'role_uid',
            'role_name',
            'role_level',
            'role_vip',
            
            'target_uid',
            'target_name',
            'target_level',
            'target_vip',
            
            'channel',
            'msg_type',
            'is_audio',
            'chat_content',
            'time',
            
            'role_is_ai',
            'target_is_ai',
            'role_corpus_id',
            'role_corpus_title',
            'role_country_id',
            'role_country_title',
            'target_corpus_id',
            'target_corpus_title',
            'target_country_id',
            'target_country_title',
            'charge',
        ]
    else:
        raise ValueError(f'Expected 13 or 27 fields, Now get {len(df.columns)} fields')
    
    df['chat_content'] = df['chat_content'].apply(lambda x: x[1:-1] if "'"==x[0] and "'"==x[-1] else x)
    
    return df if columns is None else df[columns]


if __name__ == '__main__':
    # path = Path('~/data/yk-zhanguo-chat/tw').expanduser()
    path = Path('~/data/yk-zhanguo-chat/dl').expanduser()
    path
    
    df = load(path, columns='chat_content')
    df.head(3)
