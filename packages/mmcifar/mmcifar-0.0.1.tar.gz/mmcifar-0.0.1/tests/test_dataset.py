import torch
import pytest
from cifar_rgb.datasets import RGBDataset, CIFARRGBData
from torch.utils.data import DataLoader
from torchvision import datasets as tv_datasets


class DummyDataset(torch.utils.data.Dataset):
    def __init__(
        self, length: int = 100, channels: int = 1, height: int = 32, width: int = 32
    ):
        self.data = torch.rand(length, channels, height, width)
        self.targets = torch.randint(0, 10, (length,))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx], int(self.targets[idx])


# ---------------------------------------------------------------------------
# RGBDataset tests
# ---------------------------------------------------------------------------


@pytest.fixture
def rgb_train_dataset():
    ds1 = DummyDataset(100)
    ds2 = DummyDataset(100)
    ds3 = DummyDataset(100)
    rgb_ds = RGBDataset(ds1, ds2, ds3, train=True, train_ratio=0.8, random_seed=123)
    return rgb_ds


def test_rgb_dataset_len(rgb_train_dataset):
    # 80 % of 100 samples should be in the training split → 80
    assert len(rgb_train_dataset) == 80


def test_rgb_dataset_item_shape_and_label(rgb_train_dataset):
    sample, label = rgb_train_dataset[0]
    assert sample.shape == (3, 32, 32)
    assert isinstance(label, int)


def test_rgb_dataset_reproducibility():
    ds1 = DummyDataset(50)
    ds2 = DummyDataset(50)
    ds3 = DummyDataset(50)
    ds_a = RGBDataset(ds1, ds2, ds3, train=True, train_ratio=0.6, random_seed=42)
    ds_b = RGBDataset(ds1, ds2, ds3, train=True, train_ratio=0.6, random_seed=42)
    for i in range(len(ds_a)):
        img_a, label_a = ds_a[i]
        img_b, label_b = ds_b[i]
        assert torch.equal(img_a, img_b)
        assert label_a == label_b


def test_rgb_dataset_mismatched_lengths():
    ds1 = DummyDataset(100)
    ds2 = DummyDataset(90)
    ds3 = DummyDataset(100)
    with pytest.raises(AssertionError):
        _ = RGBDataset(ds1, ds2, ds3)


def test_dataloader_batch(rgb_train_dataset):
    loader = DataLoader(rgb_train_dataset, batch_size=16, shuffle=False)
    images, labels = next(iter(loader))
    assert images.shape == (16, 3, 32, 32)
    assert labels.shape == (16,)


# ---------------------------------------------------------------------------
# CIFARRGBData tests
# ---------------------------------------------------------------------------


@pytest.fixture
def cifar_manager(monkeypatch):
    def _fake_cifar10(root, train=True, download=False, transform=None):  # noqa: D401
        return DummyDataset(length=120)

    monkeypatch.setattr(tv_datasets, "CIFAR10", _fake_cifar10)

    return CIFARRGBData(data_root="./dummy", train_ratio=0.75, random_seed=1)


def test_cifar_manager_splits(cifar_manager):
    train_ds, test_ds = cifar_manager.get_datasets(download=False)
    assert len(train_ds) == 90
    assert len(test_ds) == 30
    img, label = train_ds[0]
    assert img.shape == (3, 32, 32)
    assert isinstance(label, int)


def test_cifar_manager_loaders(cifar_manager):
    train_loader, test_loader = cifar_manager.get_loaders(
        batch_size=10,
        shuffle_train=False,
        shuffle_test=False,
        num_workers=0,
        download=False,
    )
    train_imgs, train_labels = next(iter(train_loader))
    test_imgs, test_labels = next(iter(test_loader))
    assert train_imgs.shape == (10, 3, 32, 32)
    assert test_imgs.shape == (10, 3, 32, 32)
    assert train_labels.shape == (10,)
    assert test_labels.shape == (10,)
