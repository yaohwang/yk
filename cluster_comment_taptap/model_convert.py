# encoding: utf-8

import os
import torch

# print(os.getcwd())
# import sys
# print(sys.path)

from model import BERTClass

# import torch
# import transformers


# class BERTClass(torch.nn.Module):
# 
#     def __init__(self):
#         super(BERTClass, self).__init__()
#         self.l1 = transformers.BertModel.from_pretrained(model_name)
#         self.l2 = torch.nn.Dropout(0.3)
#         self.l3 = torch.nn.Linear(768, len(mlb.classes_))
# 
# 
#     def forward(self, ids, mask, token_type_ids):
#         output_1 = self.l1(ids, attention_mask = mask, token_type_ids = token_type_ids)
#         output_2 = self.l2(output_1.pooler_output)
#         output = self.l3(output_2)
#         return output


path = os.path.dirname(__file__)

model_file = os.path.join(path, 'model/chinese-bert-wwm-ext-4.bin')
model = torch.load(model_file)
model.to('cpu')


# output_model_file = model_file.rstrip('.bin') + '-cpu.bin'
# torch.save(model, output_model_file)

output_model_file = model_file.rstrip('.bin') + '-cpu.sd'
torch.save(model.state_dict(), output_model_file)

print('saved')
