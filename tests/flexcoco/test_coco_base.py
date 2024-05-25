import os
import pytest

from flextd.flexcoco.coco_base import FlexCocoDatasetBase


@pytest.fixture
def sample_dataset():
    class SampleDataset(FlexCocoDatasetBase):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def __getitem__(self, index):
            return None, None

        def __len__(self):
            return len(self.ids)

    file_path = os.path.dirname(__file__)
    return SampleDataset(
        image_dir="",
        annotation_file=os.path.join(file_path, "../data/sample_coco.json"),
        data_transforms=None,
        label_transforms=None,
    )


# テストケース
def test_len(sample_dataset):
    assert len(sample_dataset) == 3


def test_get_category_name(sample_dataset):
    assert sample_dataset.get_category_name(1) == "label1"
    assert sample_dataset.get_category_name(4) == "label4"


def test_get_categories(sample_dataset):
    expected_categories = ["label1", "label2", "label3", "label4"]
    assert sample_dataset.get_categories() == expected_categories


def test_get_statistics(sample_dataset):
    expected_statistics = {
        "label1": 1,
        "label2": 1,
        "label3": 1,
        "label4": 2,
    }
    assert sample_dataset.get_statistics() == expected_statistics
