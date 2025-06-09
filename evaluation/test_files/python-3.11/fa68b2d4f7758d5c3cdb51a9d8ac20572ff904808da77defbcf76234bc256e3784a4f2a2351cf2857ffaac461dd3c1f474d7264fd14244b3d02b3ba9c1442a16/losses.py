"""
This code is copied from ATLOP algorithm (https://github.com/wzhouad/ATLOP/blob/main/losses.py)
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor

class ATLoss(nn.Module):

    def __init__(self):
        super().__init__()

    def forward(self, logits: Tensor, labels: Tensor) -> float:
        """
        Args:
            logits: predicted probabilities (shape: batch size x num classes)
            labels: one-hot encoded true labels (shape: batch size x num classes)
        """
        th_label = torch.zeros_like(labels, dtype=torch.float).to(labels)
        th_label[:, 0] = 1.0
        labels[:, 0] = 0.0
        p_mask = labels + th_label
        n_mask = 1 - labels
        logit1 = logits - (1 - p_mask) * 1e+30
        loss1 = -(F.log_softmax(logit1, dim=-1) * labels).sum(1)
        logit2 = logits - (1 - n_mask) * 1e+30
        loss2 = -(F.log_softmax(logit2, dim=-1) * th_label).sum(1)
        loss = loss1 + loss2
        loss = loss.mean()
        return loss

    def get_label(self, logits: Tensor, num_labels: int=-1, threshold: float=None) -> Tensor:
        """ Calculated the labels """
        if threshold:
            th_logit = torch.full((len(logits), 1), threshold)
        else:
            th_logit = logits[:, 0].unsqueeze(1)
        output = torch.zeros_like(logits).to(logits)
        mask = logits > th_logit
        if num_labels > 0:
            top_v, _ = torch.topk(logits, num_labels, dim=1)
            top_v = top_v[:, -1]
            mask = (logits >= top_v.unsqueeze(1)) & mask
        output[mask] = 1.0
        output[:, 0] = (output.sum(1) == 0.0).to(logits)
        return output