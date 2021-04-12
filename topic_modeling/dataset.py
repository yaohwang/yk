# encoding: utf-8

import torch

from torch.utils.data import Dataset


class CustomDataset(Dataset):

    def __init__(self, texts, tokenizer, max_len):
        self.tokenizer = tokenizer
        self.max_len = max_len
        self.texts = texts    # X
        

    def __len__(self):
        return len(self.texts)
    

    def __getitem__(self, index):
        texts = str(self.texts[index])
        texts = " ".join(texts.split())

        inputs = self.tokenizer.encode_plus(
            texts,
            None,
            add_special_tokens=True,
            max_length=self.max_len,
            padding='max_length',
            truncation=True,
            return_token_type_ids=True
        )
        
        ids = inputs['input_ids']
        mask = inputs['attention_mask']
        token_type_ids = inputs["token_type_ids"]

        return {
            'ids': torch.tensor(ids, dtype=torch.long),
            'mask': torch.tensor(mask, dtype=torch.long),
            'token_type_ids': torch.tensor(token_type_ids, dtype=torch.long),
        }
