#https://colab.research.google.com/github/dsbook/dsbook/blob/master/bert_example_based_finetuning.ipynb#scrollTo=Tj2ATbHmt9Wp
# from transformers.modeling_bert import BertForSequenceClassification
# from transformers.tokenization_bert import BertTokenizer
from transformers import AutoModel, AutoTokenizer
import torch
import torch.nn.functional as F


class BertEvaluator:
    def __init__(self):
        # self.tokenizer = BertTokenizer.from_pretrained("bert-base-multilingual-cased", do_lower_case=False)
        # self.model = BertForSequenceClassification.from_pretrained("bert-base-multilingual-cased", num_labels=2)
        #self.model.load_state_dict(torch.load("./bert_evaluator.bin", map_location='cpu'))

        self.model = AutoModel.from_pretrained("model/",force_download=True)  
        self.tokenizer = AutoTokenizer.from_pretrained("cl-tohoku/bert-base-japanese-whole-word-masking")
        #self.model.load_state_dict(torch.load("./bert_evaluator.bin", map_location='cpu'))

    def __convert_sequences_to_features(self, user_input, candidate):
        # トークンを格納するリスト
        user_candidate_tokens = []
        # 1文目のトークンの場合は0, 2文目の場合は1を格納するリスト
        user_candidate_input_type_ids = []
        
        # 先頭に[CLS]トークンを追加
        user_candidate_tokens.append("[CLS]")
        # [CLS]トークンは0とする
        user_candidate_input_type_ids.append(0)
        
        # 1文目をトークン化
        tokens_a = self.tokenizer.tokenize(user_input)
        for token in tokens_a:
            # トークンを先頭から順に格納
            user_candidate_tokens.append(token)
            # 1文目なので0を格納
            user_candidate_input_type_ids.append(0)
        # 1文目の最後に[SEP]トークンを格納
        user_candidate_tokens.append("[SEP]")
        # ここまで1文目とする
        user_candidate_input_type_ids.append(0)
        
        # 2文目をトークン化
        tokens_b = self.tokenizer.tokenize(candidate)
        for token in tokens_b:
            user_candidate_tokens.append(token)
            # 2文目なので1を格納
            user_candidate_input_type_ids.append(1)
        # 2文目の最後に[SEP]トークンを格納
        user_candidate_tokens.append("[SEP]")
        user_candidate_input_type_ids.append(1)
        
        # トークンをすべてIDに変換
        input_ids = self.tokenizer.convert_tokens_to_ids(user_candidate_tokens)

        return [input_ids], [user_candidate_input_type_ids]

    def evaluate(self, user_input, candidate):
        with torch.no_grad():
            ids_list, type_ids_list = self.__convert_sequences_to_features(user_input, candidate)
            result = self.model.forward(torch.tensor(ids_list).to("cpu"))#,token_type_ids=torch.tensor(type_ids_list).to("cpu"))
            result = F.softmax(result[0], dim=1).cpu().numpy().tolist()
            return result[0][1]
            