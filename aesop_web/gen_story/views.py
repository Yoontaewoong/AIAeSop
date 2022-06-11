from django.shortcuts import render
from django.conf import settings
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response

# Create your views here.
import pandas as pd
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import numpy as np
import random
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import GPT2Tokenizer, GPT2LMHeadModel, AdamW, get_linear_schedule_with_warmup
from tqdm import tqdm, trange
import torch.nn.functional as F
import csv
import pickle
import re
import os
# # text = "In another moment down went Alice after it"
# def run(text):

#     # 토크나이저 불러오기
#     import pickle
#     import re
#     with open('tokenizer.pickle', 'rb') as handle:
#         tokenizer = pickle.load(handle)
#     # 모델 불러오기
#     model = torch.load('gpt_model2.pt')

#     def generate(model,tokenizer, prompt, entry_count=10, entry_length=50, top_p=0.8, temperature=1.,):
#         model.eval()
#         generated_num = 0
#         generated_list = []

#         filter_value = -float("Inf")

#         with torch.no_grad():

#             for entry_idx in trange(entry_count):

#                 entry_finished = False
#                 generated = torch.tensor(tokenizer.encode(prompt)).unsqueeze(0)

#                 for i in range(entry_length):
#                     outputs = model(generated, labels=generated)
#                     loss, logits = outputs[:2]
#                     logits = logits[:, -1, :] / (temperature if temperature > 0 else 1.0)

#                     sorted_logits, sorted_indices = torch.sort(logits, descending=True)
#                     cumulative_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)

#                     sorted_indices_to_remove = cumulative_probs > top_p
#                     sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[
#                         ..., :-1
#                     ].clone()
#                     sorted_indices_to_remove[..., 0] = 0

#                     indices_to_remove = sorted_indices[sorted_indices_to_remove]
#                     logits[:, indices_to_remove] = filter_value

#                     next_token = torch.multinomial(F.softmax(logits, dim=-1), num_samples=1)
#                     generated = torch.cat((generated, next_token), dim=1)

#                     if next_token in tokenizer.encode("<|endoftext|>"):
#                         entry_finished = True

#                     if entry_finished:

#                         generated_num = generated_num + 1

#                         output_list = list(generated.squeeze().numpy())
#                         output_text = tokenizer.decode(output_list)
#                         generated_list.append(output_text)
#                         break
                
#                 if not entry_finished:
#                     output_list = list(generated.squeeze().numpy())
#                     output_text = f"{tokenizer.decode(output_list)}<|endoftext|>" 
#                     generated_list.append(output_text)
                    
#         return generated_list

#     res = generate(model.to('cpu'), tokenizer, text, entry_count=1)[0]
#     to_remove = res.split('.')[-1]
#     output = res.replace(to_remove,'')
#     return output



# class Generate(views.APIView):
#     def post(self, request):
#         for a in request.data:
#             try :
#                 text = a.pop("text")
#             except Exception as err:
#                 return Response(str(err), status=status.HTTP_400_BAD_REQUEST)
#             return Response(text + "test test test", status = status.HTTP_200_OK)
        # return Response(request.query_params, status = status.HTTP_200_OK)

class Generate(views.APIView):
    def post(self, request):
        for a in request.data:
            text = a.pop("text")

        def run(text):
            # 토크나이저 불러오기
            import pickle
            import re
            path = os.path.join(settings.MODEL_ROOT, 'tokenizer.pickle')
            with open(path, 'rb') as handle:
                tokenizer = pickle.load(handle)
            # 모델 불러오기
            path = os.path.join(settings.MODEL_ROOT, 'gpt_model2.pt')
            device = torch.device('cpu')
            model = torch.load(path , map_location=device)

            def generate(model,tokenizer, prompt, entry_count=10, entry_length=50, top_p=0.8, temperature=1.,):
                model.eval()
                generated_num = 0
                generated_list = []

                filter_value = -float("Inf")

                with torch.no_grad():

                    for entry_idx in trange(entry_count):

                        entry_finished = False
                        generated = torch.tensor(tokenizer.encode(prompt)).unsqueeze(0)

                        for i in range(entry_length):
                            outputs = model(generated, labels=generated)
                            loss, logits = outputs[:2]
                            logits = logits[:, -1, :] / (temperature if temperature > 0 else 1.0)

                            sorted_logits, sorted_indices = torch.sort(logits, descending=True)
                            cumulative_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)

                            sorted_indices_to_remove = cumulative_probs > top_p
                            sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[
                                ..., :-1
                            ].clone()
                            sorted_indices_to_remove[..., 0] = 0

                            indices_to_remove = sorted_indices[sorted_indices_to_remove]
                            logits[:, indices_to_remove] = filter_value

                            next_token = torch.multinomial(F.softmax(logits, dim=-1), num_samples=1)
                            generated = torch.cat((generated, next_token), dim=1)

                            if next_token in tokenizer.encode("<|endoftext|>"):
                                entry_finished = True

                            if entry_finished:

                                generated_num = generated_num + 1

                                output_list = list(generated.squeeze().numpy())
                                output_text = tokenizer.decode(output_list)
                                generated_list.append(output_text)
                                break
                        
                        if not entry_finished:
                            output_list = list(generated.squeeze().numpy())
                            output_text = f"{tokenizer.decode(output_list)}<|endoftext|>" 
                            generated_list.append(output_text)
                            
                return generated_list

            res = generate(model.to('cpu'), tokenizer, text, entry_count=1)[0]
            to_remove = res.split('.')[-1]
            output = res.replace(to_remove,'')
            return output
        ans = run(text)
        return Response(ans, status = status.HTTP_200_OK)