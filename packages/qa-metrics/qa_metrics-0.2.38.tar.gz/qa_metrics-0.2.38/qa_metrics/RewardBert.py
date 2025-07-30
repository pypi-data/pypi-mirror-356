# from transformers import AutoTokenizer, AutoModel, AutoConfig
# from huggingface_hub import hf_hub_download
# import torch
# import torch.nn as nn
# from safetensors.torch import load_file as load_safetensors
# import os


# os.environ["TOKENIZERS_PARALLELISM"] = "false"
# class BertAnswerScorer(nn.Module):
#     """
#     BERT-based regressor head identical to the one you trained.
#     """
#     def __init__(self, config):
#         super().__init__()
#         self.bert = AutoModel.from_config(config)
#         hidden_size = config.hidden_size

#         self.dropout = nn.Dropout(p=0.1)
#         self.regressor = nn.Linear(hidden_size, 1)

#     def forward(self, input_ids, attention_mask, token_type_ids=None):
#         if token_type_ids is not None and getattr(self.bert.config, "type_vocab_size", 1) > 1:
#             outputs = self.bert(
#                 input_ids=input_ids,
#                 attention_mask=attention_mask,
#                 token_type_ids=token_type_ids,
#             )
#         else:
#             outputs = self.bert(
#                 input_ids=input_ids,
#                 attention_mask=attention_mask,
#             )

#         pooled = (
#             outputs.pooler_output
#             if hasattr(outputs, "pooler_output") and outputs.pooler_output is not None
#             else outputs.last_hidden_state[:, 0, :]
#         )

#         x = self.dropout(pooled)
#         logits = self.regressor(x)
#         score = torch.sigmoid(logits).squeeze(-1)
#         return score

# def load_model_and_tokenizer_from_hub(
#     repo_id: str = "IntelligenceLab/RewardPreferenceBert",
#     device: torch.device = None,
# ):
#     # 1) device
#     if device is None:
#         device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

#     # 2) tokenizer + config
#     tokenizer = AutoTokenizer.from_pretrained(repo_id)
#     config = AutoConfig.from_pretrained(repo_id)

#     # 3) build your custom model
#     model = BertAnswerScorer(config)

#     # 4) download the safetensors weights from HF
#     weights_path = hf_hub_download(repo_id=repo_id, filename="pytorch_model.safetensors")

#     # 5) load and attach
#     state_dict = load_safetensors(weights_path)
#     model.load_state_dict(state_dict)
#     model.to(device)
#     model.eval()

#     return model, tokenizer

# def get_score(model, tokenizer, reference, generated_response, device=None):
#     MAX_LENGTH = 2048
#     # if no device passed, pick cuda if available else cpu
#     if device is None:
#         device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

#     combo = f"{reference} [SEP] {generated_response}"
#     enc = tokenizer(
#         combo,
#         return_tensors="pt",
#         padding="max_length",
#         truncation=True,
#         max_length=MAX_LENGTH,
#     )
#     enc = {k: v.to(device) for k, v in enc.items()}

#     with torch.no_grad():
#         norm_score = model(**enc).item()

#     final_score = 1.0 + 4.0 * norm_score
#     return norm_score, final_score


# class RewardBert:
#     def __init__(self, repo_id="IntelligenceLab/RewardPreferenceBert", device=None):
#         # 1) record the device choice
#         self.device = device
#         # 2) load model+tokenizer, passing that device along
#         self.model, self.tokenizer = load_model_and_tokenizer_from_hub(
#             repo_id,
#             device=self.device
#         )

#     def compute_score(self, extracted_answer, label):
#         return get_score(
#             self.model,
#             self.tokenizer,
#             label,
#             extracted_answer,
#             device=self.device
#         )


from transformers import AutoTokenizer, AutoModel, AutoConfig
from huggingface_hub import hf_hub_download
import torch
import torch.nn as nn
from safetensors.torch import load_file as load_safetensors
import os
from tqdm import tqdm
from typing import List, Tuple

# disable parallelism warnings
os.environ["TOKENIZERS_PARALLELISM"] = "false"


class BertAnswerScorer(nn.Module):
    """
    BERT-based regressor head identical to the one you trained.
    """
    def __init__(self, config):
        super().__init__()
        self.bert = AutoModel.from_config(config)
        hidden_size = config.hidden_size

        self.dropout = nn.Dropout(p=0.1)
        self.regressor = nn.Linear(hidden_size, 1)

    def forward(self, input_ids, attention_mask, token_type_ids=None):
        if token_type_ids is not None and getattr(self.bert.config, "type_vocab_size", 1) > 1:
            outputs = self.bert(
                input_ids=input_ids,
                attention_mask=attention_mask,
                token_type_ids=token_type_ids,
            )
        else:
            outputs = self.bert(
                input_ids=input_ids,
                attention_mask=attention_mask,
            )

        pooled = (
            outputs.pooler_output
            if hasattr(outputs, "pooler_output") and outputs.pooler_output is not None
            else outputs.last_hidden_state[:, 0, :]
        )

        x = self.dropout(pooled)
        logits = self.regressor(x)
        score = torch.sigmoid(logits).squeeze(-1)
        return score


def load_model_and_tokenizer_from_hub(
    repo_id: str = "IntelligenceLab/RewardPreferenceBert",
    device: torch.device = None,
):
    # 1) device
    if device is None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # 2) tokenizer + config
    tokenizer = AutoTokenizer.from_pretrained(repo_id)
    config = AutoConfig.from_pretrained(repo_id)

    # 3) build your custom model
    model = BertAnswerScorer(config)

    # 4) download the safetensors weights from HF
    weights_path = hf_hub_download(repo_id=repo_id, filename="pytorch_model.safetensors")

    # 5) load and attach
    state_dict = load_safetensors(weights_path)
    model.load_state_dict(state_dict)
    model.to(device)
    model.eval()

    return model, tokenizer


def get_score(model, tokenizer, reference, generated_response, device=None, max_length: int = 2048):
    MAX_LENGTH = max_length
    if device is None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    combo = f"{reference} [SEP] {generated_response}"
    enc = tokenizer(
        combo,
        return_tensors="pt",
        padding="max_length",
        truncation=True,
        max_length=MAX_LENGTH,
    )
    enc = {k: v.to(device) for k, v in enc.items()}

    with torch.no_grad():
        norm_score = model(**enc).item()

    final_score = 1.0 + 4.0 * norm_score
    return norm_score, final_score


class RewardBert:
    def __init__(self, repo_id: str = "IntelligenceLab/RewardPreferenceBert", device: torch.device = None, max_length: int=2048):
        # 1) record the device choice
        self.device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # 2) load model+tokenizer, passing that device along
        self.max_len = max_length
        self.model, self.tokenizer = load_model_and_tokenizer_from_hub(repo_id, device=self.device)

    def compute_score(self, extracted_answer: str, label: str) -> Tuple[float, float]:
        return get_score(
            self.model,
            self.tokenizer,
            label,
            extracted_answer,
            device=self.device,
            max_length=self.max_len
        )

    def compute_batch_scores(
        self,
        extracted_answers: List[str],
        labels: List[str],
        batch_size: int = 1
    ) -> Tuple[List[float], List[float]]:
        """
        Batch compute normalized and final scores for lists of extracted_answers and labels.
        Returns two lists: (norm_scores, final_scores).
        """
        norm_scores = []
        final_scores = []
        self.model.eval()
        MAX_LENGTH = self.max_len

        for start in tqdm(range(0, len(extracted_answers), batch_size)):
            batch_ans = extracted_answers[start:start + batch_size]
            batch_lbl = labels[start:start + batch_size]
            combos = [f"{lbl} [SEP] {ans}" for lbl, ans in zip(batch_lbl, batch_ans)]

            enc = self.tokenizer(
                combos,
                return_tensors="pt",
                padding="max_length",
                truncation=True,
                max_length=MAX_LENGTH,
            )
            enc = {k: v.to(self.device) for k, v in enc.items()}

            with torch.no_grad():
                batch_norm = self.model(**enc)  # Tensor of shape (batch,)

            # move back to CPU and to plain floats
            batch_norm_list = batch_norm.cpu().tolist()
            batch_final_list = [1.0 + 4.0 * x for x in batch_norm_list]

            norm_scores.extend(batch_norm_list)
            final_scores.extend(batch_final_list)

        return norm_scores, final_scores


# if __name__ == "__main__":
#     # force CPU
#     rb_cpu = RewardBert(device=torch.device("cpu"))
#     print("CPU:", rb_cpu.compute_score("gen", "ref"))

#     # let it pick GPU if available
#     rb_auto = RewardBert()
#     print("auto:", rb_auto.compute_score("gen", "ref"))