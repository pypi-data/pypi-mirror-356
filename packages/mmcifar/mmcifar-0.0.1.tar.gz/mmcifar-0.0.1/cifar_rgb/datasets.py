import torch
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision import datasets


class RGBDataset(Dataset):
    def __init__(
        self,
        mode1_dataset,
        mode2_dataset,
        mode3_dataset,
        train=True,
        train_ratio=0.8,
        random_seed=42,
    ):
        assert len(mode1_dataset) == len(mode2_dataset) == len(mode3_dataset), (
            "All modes must have equal length"
        )

        self.train = train
        self.train_ratio = train_ratio
        self.random_seed = random_seed

        self.mode1_active, self.mode2_active, self.mode3_active = self._prepare_splits(
            [mode1_dataset, mode2_dataset, mode3_dataset]
        )

    def _prepare_splits(self, datasets):
        torch.manual_seed(self.random_seed)
        total_size = len(datasets[0])
        train_size = int(total_size * self.train_ratio)
        test_size = total_size - train_size

        active_datasets = []
        for dataset in datasets:
            train_split, test_split = random_split(dataset, [train_size, test_size])
            active_datasets.append(train_split if self.train else test_split)

        return active_datasets

    def __len__(self):
        return len(self.mode1_active)

    def __getitem__(self, idx):
        r = self.mode1_active[idx][0]
        g = self.mode2_active[idx][0]
        b = self.mode3_active[idx][0]
        rgb = torch.cat([r, g, b], dim=0)
        label = self.mode1_active[idx][1]
        return rgb, label


class CIFARRGBData:
    def __init__(
        self, data_root="./data", transform=None, train_ratio=0.8, random_seed=42
    ):
        self.data_root = data_root
        self.transform = transform
        self.train_ratio = train_ratio
        self.random_seed = random_seed
        self._datasets = {}

    def get_datasets(self, download=True):
        if not self._datasets:
            self._create_datasets(download)
        return self._datasets["train"], self._datasets["test"]

    def get_loaders(
        self,
        batch_size=32,
        shuffle_train=True,
        shuffle_test=False,
        num_workers=0,
        download=True,
    ):
        train_dataset, test_dataset = self.get_datasets(download)

        train_loader = DataLoader(
            train_dataset,
            batch_size=batch_size,
            shuffle=shuffle_train,
            num_workers=num_workers,
        )
        test_loader = DataLoader(
            test_dataset,
            batch_size=batch_size,
            shuffle=shuffle_test,
            num_workers=num_workers,
        )

        return train_loader, test_loader

    def _create_datasets(self, download):
        def load_cifar():
            return datasets.CIFAR10(
                root=self.data_root,
                train=True,
                download=download,
                transform=self.transform,
            )

        modes = [load_cifar() for _ in range(3)]

        self._datasets["train"] = RGBDataset(
            *modes,
            train=True,
            train_ratio=self.train_ratio,
            random_seed=self.random_seed,
        )
        self._datasets["test"] = RGBDataset(
            *modes,
            train=False,
            train_ratio=self.train_ratio,
            random_seed=self.random_seed,
        )


def create_cifar_rgb_datasets(
    data_root="./data", transform=None, train_ratio=0.8, random_seed=42, download=True
):
    manager = CIFARRGBData(data_root, transform, train_ratio, random_seed)
    return manager.get_datasets(download)


def create_cifar_rgb_loaders(
    batch_size=32,
    data_root="./data",
    transform=None,
    train_ratio=0.8,
    random_seed=42,
    shuffle_train=True,
    shuffle_test=False,
    num_workers=0,
    download=True,
):
    manager = CIFARRGBData(data_root, transform, train_ratio, random_seed)
    return manager.get_loaders(
        batch_size, shuffle_train, shuffle_test, num_workers, download
    )
