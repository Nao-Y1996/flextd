# FlexTD

FlexTD (Flexible Torch Dataset) is a Python package that extends PyTorch's Dataset capabilities for computer vision
tasks, making it easier and more flexible to handle datasets.

## Overview

It provides the ability to generate new annotation files from existing annotation files, filtering the necessary
information by specifying categories and image files to be used in training and evaluating classification models.
You can check sample codes in the `notebooks/sample.ipynb`.

In addition, a pytorch Dataset can be generated from the new annotation file.
Datasets for object detection, semantic segmentation, instance segmentation, and keypoint detection will be provided

## Installation

You can install FlexTD using poetry:

```bash
git clone https://github.com/Nao-Y1996/flextd.git
cd flextd
poetry install
```

## Supported Feature

### Utils

- [x] Generation of annotation files filtered for required information
- [ ] Create new files for tran and val from one annotation file

### Supported Annotation Format

- [x] COCO
- [ ] VOC

### Template class of PyTorch Dataset

- [ ] Object detection
- [x] Semantic Segmentation
- [ ] Instance Segmentation
- [ ] Key Point Detection

## Usage

Using flextd, you can generate Pytorch dataset classes that use only specific files or specific classes.
The following code is an example of using the template classes provided by flextd.

```python
import os
from flextd.flexcoco.coco_semantic_segmentation import FlexCocoDatasetBaseSS
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
    exclude_files=["image1.jpg", "image2.jpg"],  # these two images are ignored
    include_categories=["person"]  # only 'person' category is used
)


# Create a DataLoader
data_loader = DataLoader(dataset, batch_size=5, shuffle=True)

# Iterate over the dataset
for img, target in data_loader:
    print(img.shape, target)
```

You can also specify images that you want to use and categories that you want to ignore.
```python
dataset = FlexCocoDatasetBaseSS(
    image_dir=image_dir,
    annotation_file=annotation_file,  # original annotation
    data_transforms=data_transforms,
    include_files=["image1.jpg", "image2.jpg"],  # only these two images are used
    exclude_categories=["person"]  # ignore 'person' category
)
```

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

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
