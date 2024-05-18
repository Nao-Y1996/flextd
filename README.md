# FlexTD

FlexTD (Flexible Torch Dataset) is a Python package that extends PyTorch's Dataset capabilities for computer vision
tasks, making it easier and more flexible to handle datasets.

## Overview

It provides the ability to generate new annotation files from existing annotation files, filtering the necessary
information by specifying categories and image files to be used in training and evaluating classification models.

In addition, a pytorch Dataset can be generated from the new annotation file.
Datasets for object detection, semantic segmentation, instance segmentation, and keypoint detection will be provided

## Usage

Here is an example of how to use the `FlexCocoDatasetBaseSS` class provided by FlexTDS:

```python
import os
from flextds.flexcoco.coco_semantic_segmentation import FlexCocoDatasetBaseSS
from torchvision import transforms
from torch.utils.data import DataLoader

# Define image and annotation directories
image_dir = 'path/to/your/images'
annotation_file = 'path/to/your/annotations.json'

# Define data transformations
data_transforms = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((768, 768)),
    transforms.ToTensor(),
])

# FlexCocoDataset for semantic segmentation
dataset = FlexCocoDatasetBaseSS(
    image_dir=image_dir,
    annotation_file=annotation_file,  # original annotation
    data_transforms=data_transforms,
    exclude_files=["image1.jpg", "image2.jpg"],  # ignore these two images
    exclude_categories=["person"]  # ignore 'person' category
)

# Create a DataLoader
data_loader = DataLoader(dataset, batch_size=5, shuffle=True)

# Iterate over the dataset
for img, target in data_loader:
    print(img.shape, target)
```

## Supported Feature

### Utils

- [x] Generation of annotation files filtered for required information

### Annotation Format

- [x] COCO
- [ ] VOC

### Dataset

- [ ] Object detection
- [x] Semantic Segmentation
- [ ] Instance Segmentation
- [ ] Key Point Detection

## Future Plans

Currently, FlexTD supports only the COCO format.
However, we plan to extend support to other dataset formats in the future.

## Contributing

Contributions are welcome!
If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request on GitHub.

### Running Tests

To run tests, you can use the following command:

```bash
poetry run pytest
```

Make sure you have the required test data in the `tests/data` directory.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
