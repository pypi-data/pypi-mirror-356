import torch
from torch import nn
import numpy as np
import pandas as pd
from pytorch_metric_learning.losses import ArcFaceLoss, ProxyAnchorLoss, ProxyNCALoss, NTXentLoss
from pytorch_metric_learning.losses import SelfSupervisedLoss
from torch.utils.data import DataLoader, TensorDataset
from sklearn.cluster import KMeans
from tqdm import tqdm
import torch.nn.functional as F
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import LabelEncoder
from collections import defaultdict

from ...utils.splitting import Split
from ...workflow import Step, Field



class MLPEmbedder(nn.Module):
    """
    Neural network encoder for transforming input records into embeddings.
    """

    def __init__(
            self,
            input_dim,
            embedding_dim=512,
            n_layers=4, 
            normalize: bool=True,
            bucket_name: str=None,
            blob_name: str=None,
            filepath: str=None,
            device: str="cpu",
            mode_eval: bool=False
        ):
        """
        Initialize the RecordEncoder.

        Parameters
        ----------
        input_dim : int
            Input dimension of the data
        embedding_dim : int, default=512 
            Output dimension of the embeddings
        n_layers : int, default=4
            Number of layers in the encoder network
        normalize : bool, default=True
            Whether to normalize the embeddings
        """
        super().__init__()

        self.normalize = normalize
        current_dim = input_dim
        layers = []

        while current_dim >= embedding_dim and len(layers) < n_layers:
            next_dim = max(current_dim // 2, embedding_dim)
            layers.append(nn.Linear(current_dim, next_dim))
            layers.append(nn.BatchNorm1d(next_dim))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(0.2))
            current_dim = next_dim

        if current_dim != embedding_dim:
            layers.append(nn.Linear(current_dim, embedding_dim))

        self.model = nn.Sequential(*layers)
        self.device = device
        if (bucket_name is not None) and (blob_name is not None):
            print(f"Loading weights from GCS for {self.__class__}.....")
            self.load_from_gcs(bucket_name, blob_name, device)
        elif filepath is not None:
            print(f"Loading weights from local for {self.__class__}.....")
            self.load_from_local(filepath, device)

        self.model.to(device)

    def forward(self, X: torch.Tensor) -> np.ndarray:
        """
        Forward pass of embedder.
        
        Parameters
        ----------
        x : torch.Tensor
            Input tensor
            
        Returns
        -------
        torch.Tensor
            Encoded embeddings, normalized if using cosine distance
        """
        return self.model(X)





def _avg_dist_to_nn(X, k=5):

    nbrs = NearestNeighbors(n_neighbors=k + 1, algorithm='auto').fit(X)
    distances, indices = nbrs.kneighbors(X)

    # distances[:, 0] is distance to self (0.0), so we exclude it
    avg_dist_to_knn = distances[:, 1:].mean()
    return avg_dist_to_knn


def average_intragroup_distance(X, group_ids):
    group_to_indices = defaultdict(list)
    for idx, gid in enumerate(group_ids):
        group_to_indices[gid].append(idx)
    
    dists = []
    for indices in group_to_indices.values():
        if len(indices) <= 1:
            continue  # Skip singleton groups
        group_X = X[indices]
        dist_matrix = pairwise_distances(group_X, metric='cosine')
        # Take upper triangle without diagonal
        triu = dist_matrix[np.triu_indices_from(dist_matrix, k=1)]
        dists.append(triu.mean())
    
    return np.mean(dists) if dists else np.nan


def train_step(self, X_labeled, y_labeled, X_unlabeled):
    """
    X_labeled: (B_l, C, H, W) or (B_l, D)
    y_labeled: (B_l,)
    X_unlabeled: (B_u, C, H, W) or (B_u, D)
    """

    # Forward pass
    z_labeled = self.model(X_labeled)    # (B_l, D)
    z_unlabeled = self.model(X_unlabeled)  # (B_u, D)

    # ProxyAnchor requires known num_classes, set dynamically
    if self.proxy_loss.num_classes is None:
        num_classes = len(torch.unique(y_labeled))
        self.proxy_loss = ProxyAnchorLoss(num_classes=num_classes, embedding_size=self.embedding_dim, margin=0.1, alpha=32)

    # Supervised loss on labeled
    loss_supervised = self.proxy_loss(z_labeled, y_labeled)

    # Unsupervised contrastive loss (can also include labeled here)
    z_all = torch.cat([z_labeled, z_unlabeled], dim=0)
    labels_fake = torch.arange(z_all.size(0), device=z_all.device)
    loss_unsupervised = self.contrastive_loss(z_all, labels_fake)

    # Combine losses
    total_loss = loss_supervised + self.lambda_unsup * loss_unsupervised
    return total_loss




def train_embedding_model(X, y, split, embedding_size, loss_type="proxynca", epochs=100, batch_size=256):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    input_dim = X.shape[1]
    y = LabelEncoder().fit_transform(y)
    num_classes = len(np.unique(y))

    train_mask, val_mask = np.isin(np.array(split), [Split.TRAIN]), np.isin(split, Split.VAL)
    out_mask = np.isin(np.array(split), [Split.TEST, Split.VAL])
    X_train, y_train_ = X[train_mask], y[train_mask]
    X_val, y_val = X[val_mask], y[val_mask]
    X_out, y_out_ = X[out_mask], y[out_mask]

    print('Before:', _avg_dist_to_nn(X_train), _avg_dist_to_nn(X_out))
    print('Before:', average_intragroup_distance(X_train, y_train_), average_intragroup_distance(X_out, y_out_))

    # n_new_proxies = int(num_classes - np.unique(y_train_).shape[0])
    # print(X_out.shape, n_new_proxies)
    # kmeans = KMeans(n_clusters=n_new_proxies).fit(X_out)
    # X_out = kmeans.cluster_centers_
    # y_out = kmeans.labels_ + np.max(y) + 1
    # y_out = np.arange(np.max(y) + 1, np.max(y) + 1 + n_new_proxies)

    #X_train = np.vstack([X_train, X_out])
    #y_train = np.hstack([y_train_, y_out])
    y_train = y_train_

    # Model setup
    # encoder = RecordEncoder(input_dim, embedding_dim=embedding_size).to(device)
    encoder = MLPEmbedder(input_dim, embedding_dim=embedding_size).to(device)
    if loss_type == "arcface":
        loss_func = ArcFaceLoss(num_classes=num_classes, embedding_size=embedding_size).to(device)
    elif loss_type == "proxyanchor":
        loss_func = ProxyAnchorLoss(num_classes=num_classes, embedding_size=embedding_size, margin=2., alpha=256).to(device)
    elif loss_type == "proxynca":
        loss_func = ProxyNCALoss(num_classes=num_classes, embedding_size=embedding_size).to(device)
    else:
        raise ValueError("Unsupported loss type")

    optimizer = torch.optim.AdamW(list(encoder.parameters()) + list(loss_func.parameters()), lr=1e-3)

    # Dataloaders
    train_ds = TensorDataset(torch.tensor(X_train, dtype=torch.float32), torch.tensor(y_train, dtype=torch.long))
    unlabeled_ds = TensorDataset(torch.tensor(X_out, dtype=torch.float32))
    unlabeled_val_ds = TensorDataset(torch.tensor(X_val, dtype=torch.float32))
    val_ds = TensorDataset(torch.tensor(X_val, dtype=torch.float32), torch.tensor(y_val, dtype=torch.long))

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    unlabeled_loader = DataLoader(unlabeled_ds, batch_size=batch_size, shuffle=True)
    unlabeled_val_loader = DataLoader(unlabeled_ds, batch_size=batch_size, shuffle=False)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False)

    best_loss = float("inf")
    best_encoder_state = None

    # --- Setup losses ---
    proxy_loss_fn = ProxyAnchorLoss(num_classes=num_classes, embedding_size=embedding_size, margin=0.1, alpha=32)
    proxy_loss_fn = ProxyNCALoss(num_classes=num_classes, embedding_size=embedding_size).to(device)
    contrastive_loss_fn = NTXentLoss(temperature=0.1)
    lambda_unsup = .2  # weight for unsupervised contrastive loss

    best_loss = float('inf')
    best_encoder_state = None

    for epoch in range(epochs):
        encoder.train()
        total_proxy_loss = 0.0
        total_contrastive_loss = 0.0
        total_combined_loss = 0.0

        for (batch_X, batch_y), (unlabeled_X,) in tqdm(zip(train_loader, unlabeled_loader), desc=f"[semi-proxy] Epoch {epoch+1} - Train", total=len(train_loader)):
            batch_X, batch_y = batch_X.to(device), batch_y.to(device)
            unlabeled_X = unlabeled_X.to(device)

            emb_labeled = encoder(batch_X)
            emb_unlabeled = encoder(unlabeled_X)

            loss_proxy = proxy_loss_fn(emb_labeled, batch_y)

            emb_all = torch.cat([emb_labeled, emb_unlabeled], dim=0)
            labels_fake = torch.arange(emb_all.size(0), device=emb_all.device)
            loss_contrastive = contrastive_loss_fn(emb_all, labels_fake)

            loss = loss_proxy + lambda_unsup * loss_contrastive
            # loss = loss_proxy

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_proxy_loss += loss_proxy.item()
            total_contrastive_loss += loss_contrastive.item()
            total_combined_loss += loss.item()

        encoder.eval()
        val_proxy_loss = 0.0
        val_contrastive_loss = 0.0
        val_combined_loss = 0.0
        with torch.no_grad():
            for (batch_X, batch_y), (unlabeled_X,) in zip(val_loader, unlabeled_val_loader):
                batch_X, batch_y = batch_X.to(device), batch_y.to(device)
                unlabeled_X = unlabeled_X.to(device)

                emb_labeled = encoder(batch_X)
                emb_unlabeled = encoder(unlabeled_X)

                loss_proxy = proxy_loss_fn(emb_labeled, batch_y)

                emb_all = torch.cat([emb_labeled, emb_unlabeled], dim=0)
                labels_fake = torch.arange(emb_all.size(0), device=emb_all.device)
                loss_contrastive = contrastive_loss_fn(emb_all, labels_fake)

                loss = loss_proxy + lambda_unsup * loss_contrastive

                val_proxy_loss += loss_proxy.item()
                val_contrastive_loss += loss_contrastive.item()
                val_combined_loss += loss.item()

        n_train = len(train_loader)
        n_val = len(val_loader)
        print(f"[semi-proxy] Epoch {epoch+1} | "
            f"Train Loss: {total_combined_loss / n_train:.4f} "
            f"(Proxy: {total_proxy_loss / n_train:.4f}, Contrastive: {total_contrastive_loss / n_train:.4f}) | "
            f"Val Loss: {val_combined_loss / n_val:.4f} "
            f"(Proxy: {val_proxy_loss / n_val:.4f}, Contrastive: {val_contrastive_loss / n_val:.4f})")

        if val_combined_loss < best_loss:
            best_loss = val_combined_loss
            best_encoder_state = encoder.state_dict()

    # --- Restore best encoder ---
    if best_encoder_state is not None:
        encoder.load_state_dict(best_encoder_state)
    encoder.eval()


    X_enc = encoder.forward(torch.tensor(X, dtype=torch.float32))
    X_enc = X_enc.detach().numpy()

    print('After:', _avg_dist_to_nn(X_enc[train_mask]), _avg_dist_to_nn(X_enc[out_mask]))
    print('After:', average_intragroup_distance(X_enc[train_mask], y_train_), average_intragroup_distance(X_enc[out_mask], y_out_))


    return encoder


class MetricRefiner(Step):
    name = 'metric-refiner'

    inputs = [
        Field('X', 'Embedded input features'),
        Field('y', 'Group identifiers indicating which samples refer to the same entity'),
        Field('splits', 'Masks for train, validation, and test sets'),
    ]

    outputs = [
        Field('X', 'Refined embeddings with improved metric structure for entity resolution'),
    ]

    def _execute(self, inputs):
        X, y, splits = inputs['X'], inputs['y'], inputs['splits']
        encoder = train_embedding_model(X.values, y, splits[0], embedding_size=8)
        X_enc = encoder.forward(torch.tensor(X.values, dtype=torch.float32))
        X_enc = X_enc.detach().numpy()
        X = pd.DataFrame(X_enc, index=X.index)
        self.output('X', X)