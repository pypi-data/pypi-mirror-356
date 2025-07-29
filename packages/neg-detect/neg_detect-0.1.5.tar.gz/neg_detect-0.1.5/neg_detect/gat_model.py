import torch
import torch.nn as nn
from torch_geometric.nn import GATv2Conv
from torch_geometric.utils import degree
from transformers import AutoModel, BertConfig, AutoConfig
from torch_geometric.data import Data
from torch.nn import functional as F
from typing import Optional, List, Union, Tuple
from transformers.modeling_outputs import TokenClassifierOutput


class ContextGatedFusion(nn.Module):
    def __init__(self, embed_dim):
        super(ContextGatedFusion, self).__init__()
        self.query_proj = nn.Linear(embed_dim, embed_dim)
        self.ctx1_proj = nn.Linear(embed_dim, embed_dim)
        self.ctx2_proj = nn.Linear(embed_dim, embed_dim)

    def forward(self, E_main, E_ctx1, E_ctx2):
        """
        E_main:  (batch_size, embed_dim)
        E_ctx1:  (batch_size, embed_dim)
        E_ctx2:  (batch_size, embed_dim)
        """
        q = self.query_proj(E_main)  # (batch_size, embed_dim)
        k1 = self.ctx1_proj(E_ctx1)
        k2 = self.ctx2_proj(E_ctx2)
        # Dot product attention gates (sigmoid for gating)
        g1 = torch.sigmoid(q * k1)  # (batch_size, 1)
        g2 = torch.sigmoid(q * k2)  # (batch_size, 1)
        # Gated context features
        gated_ctx1 = g1 * E_ctx1
        gated_ctx2 = g2 * E_ctx2
        # Combine all
        fused = E_main + gated_ctx1 + gated_ctx2
        return fused


class BERTResidualGATv2ContextGatedFusion(nn.Module):
    def __init__(self,
                 bert_id: str,
                 id2label,
                 label2id,
                 num_labels: int = 2,
                 pos_vocab_size=None,
                 dep_vocab_size=None,
                 hidden_size: int = 128
                 ):
        super().__init__()
        # Load configuration from model repository
        config = AutoConfig.from_pretrained(bert_id, trust_remote_code=True)
        self.hidden_size = hidden_size
        config.label2id = label2id
        config.id2label = id2label
        # Set the num_labels (if provided)
        if num_labels is not None:
            config.num_labels = num_labels

        self.num_labels = config.num_labels
        self.bert = AutoModel.from_pretrained(bert_id, config=config, trust_remote_code=True)
        self.bert_reduction = torch.nn.Linear(config.hidden_size, hidden_size)
        self.relu = torch.nn.ReLU()  # Added activation as discussed previously
        self.gelu = torch.nn.GELU()

        # POS and Dependency embeddings
        self.pos_emb = torch.nn.Embedding(pos_vocab_size, hidden_size)
        self.dep_emb = torch.nn.Embedding(dep_vocab_size, hidden_size)

        # gated cross attention mechanism
        self.context_gated_fusion = ContextGatedFusion(hidden_size)

        # Layer normalization and reduction layers
        self.ln_pre_gcn = torch.nn.LayerNorm(hidden_size, eps=1e-5)

        self.cat_norm = torch.nn.LayerNorm(hidden_size, eps=1e-5)
        self.ln_gcn = torch.nn.LayerNorm(hidden_size, eps=1e-5)

        # GATv2 Layer
        self.gcn = GATv2Conv(
            in_channels=hidden_size,
            out_channels=hidden_size,
            add_self_loops=True,
            heads=4,  # Multi-head attention
            dropout=0.1,  # Attention dropout
            concat=False,
            residual=True  # Concatenate heads
        )

        # Dropout layer
        """try:
            if config.classifier_dropout is None:
                raise Exception
            # Dropout layer
            classifier_dropout = (
                config.classifier_dropout if config.classifier_dropout is not None else config.hidden_dropout_prob
            )
        except:
            classifier_dropout = (
                config.hidden_dropout_prob if config.hidden_dropout_prob is not None else 0.1
            )"""
        if "classifier_dropout" in config:
            classifier_dropout = config.classifier_dropout
        elif "hidden_dropout_prob" in config:
            classifier_dropout = config.hidden_dropout_prob
        elif "hidden_dropout" in config:
            classifier_dropout = config.hidden_dropout
        else:
            classifier_dropout = 0.1
        if classifier_dropout is None:
            classifier_dropout = 0.1

        self.dropout = torch.nn.Dropout(classifier_dropout)

        # Classifier layer
        self.classifier = torch.nn.Linear(hidden_size, config.num_labels)

        # Initialize model weights
        self._init_weights()
        self.config = config

    def _init_weights(self):
        # Xavier initialization for weights
        torch.nn.init.xavier_uniform_(self.classifier.weight)
        torch.nn.init.zeros_(self.classifier.bias)
        torch.nn.init.xavier_uniform_(self.pos_emb.weight, gain=0.01)
        torch.nn.init.xavier_uniform_(self.dep_emb.weight, gain=0.01)

        # GCN weights initialization
        for name, param in self.gcn.named_parameters():
            if 'weight' in name:
                torch.nn.init.xavier_uniform_(param)
            elif 'bias' in name:
                torch.nn.init.zeros_(param)

        # GCN weights initialization
        for name, param in self.context_gated_fusion.named_parameters():
            if 'weight' in name:
                torch.nn.init.xavier_uniform_(param)
            elif 'bias' in name:
                torch.nn.init.zeros_(param)

    def forward(
            self,
            input_ids: Optional[torch.Tensor] = None,
            attention_mask: Optional[torch.Tensor] = None,
            pos_ids: Optional[torch.Tensor] = None,
            dep_ids: Optional[torch.Tensor] = None,
            edge_index: Optional[List[torch.Tensor]] = None,
            word_ids: Optional[List[List[int]]] = None,  # list of lists
            labels: Optional[torch.Tensor] = None,  # flattened labels (total_words)
            word_count: Optional[List[int]] = None,  # list of num_words per sentence
            token_type_ids: Optional[torch.Tensor] = None,
            position_ids: Optional[torch.Tensor] = None,
            head_mask: Optional[torch.Tensor] = None,
            inputs_embeds: Optional[torch.Tensor] = None,
            output_attentions: Optional[bool] = None,
            output_hidden_states: Optional[bool] = None,
            return_dict: Optional[bool] = None,
            **kwargs
    ) -> Union[Tuple[torch.Tensor], TokenClassifierOutput]:
        return_dict = return_dict if return_dict is not None else self.config.use_return_dict

        if word_ids is None or word_count is None or edge_index is None:
            raise ValueError("word_ids, word_count, and edge_index are required inputs.")

        # Get BERT output
        outputs = self.bert(
            input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids,
            position_ids=position_ids,
            # head_mask=head_mask,
            inputs_embeds=inputs_embeds,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
        )

        sequence_output = outputs.last_hidden_state if return_dict else outputs[0]
        sequence_output = self.bert_reduction(sequence_output)
        # Get POS and Dependency embeddings
        pos_embed = self.pos_emb(pos_ids)  # Shape: (batch_size, max_seq_length, 50)
        dep_embed = self.dep_emb(dep_ids)  # Shape: (batch_size, max_seq_length, 50)

        sequence_output = self.context_gated_fusion(sequence_output, pos_embed, dep_embed) + sequence_output

        sequence_output = self.ln_pre_gcn(sequence_output)
        sequence_output = self.relu(sequence_output)

        batch_size, seq_length, hidden_size = sequence_output.shape
        batch_word_embeddings = []

        # Handle word embeddings based on word_count and word_ids
        for i in range(batch_size):
            word_embeddings_list = []
            for j in range(word_count[i]):
                if j in word_ids[i]:
                    word_embeddings_list.append(sequence_output[i][word_ids[i].index(j)])
                else:
                    word_embeddings_list.append(sequence_output[i][0])

            batch_word_embeddings.append(torch.stack(word_embeddings_list))

        # Prepare graph data for GCN
        offset = 0
        edge_indices = [[], []]
        for i in range(batch_size):
            # ERROR HERE: RUN ONLY ON ONE GPU WITH HF TRAINER!!!!!!!!!!!!!!!!!!
            edge_indices[0].extend(edge_index[i][0] + offset)
            edge_indices[1].extend(edge_index[i][1] + offset)
            offset += batch_word_embeddings[i].size(0)


        gcn_in = torch.cat(batch_word_embeddings, dim=0)
        edge_index = torch.tensor(edge_indices, device=gcn_in.device, dtype=torch.int64)

        gcn_in = self.cat_norm(gcn_in)

        # Check for NaNs in word embeddings
        if torch.isnan(gcn_in).any():
            print("NaNs found in word embeddings after scatter/LayerNorm:", gcn_in)
            raise RuntimeError("NaNs found in word embeddings after scatter/LayerNorm")

        # GCN forward pass
        if edge_index.numel() != 0:
            num_nodes = gcn_in.size(0)
            if edge_index.min() < 0 or edge_index.max() >= num_nodes:
                raise ValueError(
                    f"edge_index contains out-of-bounds node indices: min={edge_index.min()}, max={edge_index.max()}, num_nodes={num_nodes}")
            edge_index = torch.unique(edge_index, dim=1)

        gcn_out = self.relu(self.gcn(gcn_in, edge_index))

        # Check for NaNs and Infs in GCN output
        if torch.isnan(gcn_out).any() or torch.isinf(gcn_out).any():
            print("NaNs or Infs found in GCN output after LayerNorm:", gcn_out)
            raise RuntimeError("NaNs found in GCN output after LayerNorm")

        gcn_out = self.ln_gcn(gcn_out)
        gcn_out = self.dropout(gcn_out)

        # Classifier layer
        logits = self.classifier(gcn_out)

        # Check for NaNs in logits
        if torch.isnan(logits).any():
            print("NaNs found in logits:", logits)
            raise RuntimeError("NaNs found in GCN output after logits")

        # Compute loss if labels are provided
        loss = None
        if labels is not None:
            loss_fct = torch.nn.CrossEntropyLoss()
            loss = loss_fct(logits.view(-1, self.num_labels), labels.view(-1))
            if torch.isnan(loss).any() or torch.isinf(loss).any():
                print(logits.view(-1, self.num_labels), labels.view(-1))
                print(loss)
                raise RuntimeError("NaNs or Infs found in Loss")

        return TokenClassifierOutput(
            loss=loss,
            logits=logits,
            hidden_states=outputs.hidden_states,
            attentions=outputs.attentions,
        )
