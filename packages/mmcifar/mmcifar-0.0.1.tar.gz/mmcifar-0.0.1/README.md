# Multimodal CIFAR Dataset

## Quick Start

```python
from cifar_rgb.datasets import create_cifar_rgb_loaders
from cifar_rgb.transforms import grayscale

train_loader, test_loader = create_cifar_rgb_loaders(
    batch_size=32,
    transform=grayscale,
    train_ratio=0.8,
    random_seed=42
)

for data, target in train_loader:
    pass  # data shape: (32, 3, 32, 32), target shape: (32,)
```

## Visualization

```python
import matplotlib.pyplot as plt
from cifar_rgb.datasets import create_cifar_rgb_loaders
from cifar_rgb.transforms import grayscale

train_loader, _ = create_cifar_rgb_loaders(
    batch_size=4,
    transform=grayscale,
    train_ratio=0.8,
    random_seed=42
)

img_rgb, label = next(iter(train_loader))[0][0], next(iter(train_loader))[1][0].item()

plt.figure(figsize=(10, 3))
plt.subplot(1, 4, 1)
plt.imshow(img_rgb.permute(1, 2, 0).numpy())
plt.title(f"RGB (Label: {label})")
plt.axis('off')

for i, (channel, title) in enumerate(zip(img_rgb, ["R/Mode 1", "G/Mode 2", "B/Mode 3"]), start=2):
    plt.subplot(1, 4, i)
    plt.imshow(channel.numpy(), cmap='gray')
    plt.title(title)
    plt.axis('off')

plt.tight_layout()
plt.show()
```

## API Reference

### RGBDataset

Wraps three grayscale datasets as RGB.

```python
from cifar_rgb.datasets import RGBDataset

dataset = RGBDataset(
    mode1_dataset,
    mode2_dataset,
    mode3_dataset,
    train=True,
    train_ratio=0.8,
    random_seed=42
)
```

### CIFARRGBData

High-level manager for CIFAR RGB datasets.

```python
from cifar_rgb.datasets import CIFARRGBData

manager = CIFARRGBData(
    data_root='./data',
    transform=grayscale,
    train_ratio=0.8,
    random_seed=42
)

train_dataset, test_dataset = manager.get_datasets()
train_loader, test_loader = manager.get_loaders(
    batch_size=32,
    shuffle_train=True,
    shuffle_test=False,
    num_workers=0
)
```

### Helper Functions

```python
from cifar_rgb.datasets import create_cifar_rgb_datasets, create_cifar_rgb_loaders

# Datasets
train_dataset, test_dataset = create_cifar_rgb_datasets(
    data_root='./data',
    transform=grayscale,
    train_ratio=0.8,
    random_seed=42,
    download=True
)

# Loaders
train_loader, test_loader = create_cifar_rgb_loaders(
    batch_size=32,
    data_root='./data',
    transform=grayscale,
    train_ratio=0.8,
    random_seed=42,
    shuffle_train=True,
    shuffle_test=False,
    num_workers=0,
    download=True
)
```

### Transforms

```python
from cifar_rgb.transforms import grayscale
# grayscale = Compose([Grayscale(num_output_channels=1), ToTensor()])
```

## Data Format

- **Input**: Three grayscale datasets
- **Output**: RGB images with:
  - Red = mode1
  - Green = mode2
  - Blue = mode3
- **Shape**: (3, 32, 32)
- **Labels**: Taken from original datasets

## Dependencies

- PyTorch
- torchvision
- matplotlib
- pytest (for tests)

## Testing

```bash
pytest tests/
```

## Examples

See `examples/visualize.py` for RGB channel visualization.
