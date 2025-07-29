from torchvision import transforms

grayscale = transforms.Compose(
    [transforms.Grayscale(num_output_channels=1), transforms.ToTensor()]
)
