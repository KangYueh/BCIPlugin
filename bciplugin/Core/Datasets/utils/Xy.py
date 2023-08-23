import torch
from torch.utils.data import DataLoader

from bciplugin.Core.Datasets.base import RawDataset, BaseConcatDataset

def x_y_from_dataset(dataset, shuffle=False):
    """
    Extract input data and target labels from a dataset.

    Parameters:
        dataset (RawDataset):
            The dataset containing data and labels.
        shuffle (bool):
            Whether to shuffle the data when loading.

    Returns:
        torch.Tensor, torch.Tensor:
            Input data and target labels.
    """
    Data = next(iter(DataLoader(dataset, batch_size=len(dataset), shuffle=shuffle)))
    try:
        return Data[0].to(dtype=torch.float32), Data[1].long()
    except:
        return Data[0], Data[1]


def x_from_dataset(dataset, shuffle=False):
    """
    Extract input data from a dataset.

    Parameters:
        dataset (RawDataset):
            The dataset containing data.
        shuffle (bool):
            Whether to shuffle the data when loading.

    Returns:
        torch.Tensor:
            Input data.
    """
    Data = next(iter(DataLoader(dataset, batch_size=len(dataset), shuffle=shuffle)))
    try:
        return Data[0].to(dtype=torch.float32)
    except:
        return Data[0]


def x_y_embedding_from_dataset(dataset, shuffle=False):
    """
    Extract input data, target labels, and embedding data from a dataset.

    Parameters:
        dataset (RawDataset):
            The dataset containing data, labels, and embeddings.
        shuffle (bool):
            Whether to shuffle the data when loading.

    Returns:
        torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor:
            Input data, target labels, embedding data, and additional information.
    """
    Data = next(iter(DataLoader(dataset, batch_size=len(dataset), shuffle=shuffle)))
    try:
        return Data[0].to(dtype=torch.float32), Data[1].long(), Data[2], Data[3]
    except:
        return Data[0], Data[1], Data[2], Data[3]


def x_y_id_from_dataset(dataset, shuffle=False):
    """
    Extract input data, target labels, and ID information from a dataset.

    Parameters:
        dataset (RawDataset):
            The dataset containing data, labels, and IDs.
        shuffle (bool):
            Whether to shuffle the data when loading.
    Returns:
        torch.Tensor, torch.Tensor, torch.Tensor:
            Input data, target labels, and ID information.
    """
    Data = next(iter(DataLoader(dataset, batch_size=len(dataset), shuffle=shuffle)))
    try:
        return Data[0].to(dtype=torch.float32), Data[1].long(), Data[2]
    except:
        return Data[0], Data[1], Data[2]
