import json
import os

import pytest

from flextd.flexcoco.utils import (
    filter_dicts_by_inclusion,
    filter_dicts_by_exclusion,
    filter_dataset,
)

DATA_DIR = os.path.dirname(__file__).replace("flexcoco", "data")
annotation_file = str(os.path.join(DATA_DIR, "sample_coco.json"))
with open(annotation_file, "r") as f:
    sample_coco = json.load(f)


def test_filter_dicts_by_inclusion():
    """
    Test that dictionaries with specified key having values in the value_list are included.
    """
    origins = [
        {"name": "apple", "color": "red"},
        {"name": "banana", "color": "yellow"},
        {"name": "grape", "color": "purple"},
    ]
    key = "name"
    value_list = ["apple", "banana"]
    result = filter_dicts_by_inclusion(origins, key, value_list)
    expected = [
        {"name": "apple", "color": "red"},
        {"name": "banana", "color": "yellow"},
    ]
    assert result == expected, f"Expected {expected}, but got {result}"


def test_filter_dicts_by_exclusion():
    """
    Test that dictionaries with specified key having values in the value_list are excluded.
    """
    origins = [
        {"name": "apple", "color": "red"},
        {"name": "banana", "color": "yellow"},
        {"name": "grape", "color": "purple"},
    ]
    key = "name"
    value_list = ["apple", "banana"]
    result = filter_dicts_by_exclusion(origins, key, value_list)
    expected = [
        {"name": "grape", "color": "purple"},
    ]
    assert result == expected, f"Expected {expected}, but got {result}"


def test_filter_dicts_by_inclusion_empty_origins():
    """
    Test that an empty list of dictionaries returns an empty list.
    """
    origins = []
    key = "name"
    value_list = ["apple", "banana"]
    result = filter_dicts_by_inclusion(origins, key, value_list)
    expected = []
    assert result == expected, f"Expected {expected}, but got {result}"


def test_filter_dicts_by_exclusion_empty_origins():
    """
    Test that an empty list of dictionaries returns an empty list.
    """
    origins = []
    key = "name"
    value_list = ["apple", "banana"]
    result = filter_dicts_by_exclusion(origins, key, value_list)
    expected = []
    assert result == expected, f"Expected {expected}, but got {result}"


def test_filter_dicts_by_inclusion_key_not_in_dicts():
    """
    Test that a KeyError is raised when the specified key is not in the dictionaries.
    """
    origins = [
        {"fruit": "apple", "color": "red"},
        {"fruit": "banana", "color": "yellow"},
    ]
    key = "name"
    value_list = ["apple", "banana"]
    with pytest.raises(KeyError):
        filter_dicts_by_inclusion(origins, key, value_list)


def test_filter_dicts_by_exclusion_key_not_in_dicts():
    """
    Test that a KeyError is raised when the specified key is not in the dictionaries.
    """
    origins = [
        {"fruit": "apple", "color": "red"},
        {"fruit": "banana", "color": "yellow"},
    ]
    key = "name"
    value_list = ["apple", "banana"]
    with pytest.raises(KeyError):
        filter_dicts_by_exclusion(origins, key, value_list)


def test_filter_dicts_by_inclusion_empty_value_list():
    """
    Test that an empty value list returns an empty list.
    """
    origins = [
        {"name": "apple", "color": "red"},
        {"name": "banana", "color": "yellow"},
    ]
    key = "name"
    value_list = []
    result = filter_dicts_by_inclusion(origins, key, value_list)
    expected = []
    assert result == expected, f"Expected {expected}, but got {result}"


def test_filter_dicts_by_exclusion_empty_value_list():
    """
    Test that an empty value list returns the original list.
    """
    origins = [
        {"name": "apple", "color": "red"},
        {"name": "banana", "color": "yellow"},
    ]
    key = "name"
    value_list = []
    result = filter_dicts_by_exclusion(origins, key, value_list)
    expected = origins
    assert result == expected, f"Expected {expected}, but got {result}"


def test_filter_dataset__include_images():
    origin_info = sample_coco["info"]
    origin_licenses = sample_coco["licenses"]
    origin_images = sample_coco["images"]
    origin_annotations = sample_coco["annotations"]
    origin_categories = sample_coco["categories"]

    include_files = ["000000000001.jpg", "000000000002.jpg"]
    # exclude_files = ["000000000003.jpg"]
    # include_categories = ["label1", "label2", "label3"]
    # exclude_categories = ["label3"]

    filtered_ann = filter_dataset(annotation_file, include_files=include_files)

    # info, licenses and categories should not be changed
    assert filtered_ann["info"] == origin_info
    assert filtered_ann["licenses"] == origin_licenses
    assert filtered_ann["categories"] == origin_categories

    # images should be filtered by include_files
    filtered_images = filter_dicts_by_inclusion(
        origin_images, "file_name", include_files
    )
    assert filtered_ann["images"] == filtered_images

    # annotations should be filtered by image_id
    filtered_image_ids = [image["id"] for image in filtered_images]
    filtered_annotations = filter_dicts_by_inclusion(
        origin_annotations, "image_id", filtered_image_ids
    )
    assert filtered_ann["annotations"] == filtered_annotations


def test_filter_dataset__exclude_images():
    origin_info = sample_coco["info"]
    origin_licenses = sample_coco["licenses"]
    origin_images = sample_coco["images"]
    origin_annotations = sample_coco["annotations"]
    origin_categories = sample_coco["categories"]

    # include_files = ["000000000001.jpg", "000000000002.jpg"]
    exclude_files = ["000000000003.jpg"]
    # include_categories = ["label1", "label2", "label3"]
    # exclude_categories = ["label3"]

    filtered_ann = filter_dataset(annotation_file, exclude_files=exclude_files)

    # info, licenses and categories should not be changed
    assert filtered_ann["info"] == origin_info
    assert filtered_ann["licenses"] == origin_licenses
    assert filtered_ann["categories"] == origin_categories

    # images should be filtered by exclude_files
    filtered_images = filter_dicts_by_exclusion(
        origin_images, "file_name", exclude_files
    )
    assert filtered_ann["images"] == filtered_images

    # annotations should be filtered by image_id
    filtered_image_ids = [image["id"] for image in filtered_images]
    filtered_annotations = filter_dicts_by_inclusion(
        origin_annotations, "image_id", filtered_image_ids
    )
    assert filtered_ann["annotations"] == filtered_annotations


def test_filter_dataset__include_exclude_images():
    origin_info = sample_coco["info"]
    origin_licenses = sample_coco["licenses"]
    origin_images = sample_coco["images"]
    origin_annotations = sample_coco["annotations"]
    origin_categories = sample_coco["categories"]

    include_files = ["000000000001.jpg", "000000000002.jpg"]
    exclude_files = ["000000000003.jpg"]
    # include_categories = ["label1", "label2", "label3"]
    # exclude_categories = ["label3"]

    filtered_ann = filter_dataset(
        annotation_file, include_files=include_files, exclude_files=exclude_files
    )

    # info, licenses and categories should not be changed
    assert filtered_ann["info"] == origin_info
    assert filtered_ann["licenses"] == origin_licenses
    assert filtered_ann["categories"] == origin_categories

    # images should be filtered by exclude_files
    filtered_image = filter_dicts_by_inclusion(
        origin_images, "file_name", include_files
    )
    filtered_images = filter_dicts_by_exclusion(
        filtered_image, "file_name", exclude_files
    )
    assert filtered_ann["images"] == filtered_images

    # annotations should be filtered by image_id
    filtered_image_ids = [image["id"] for image in filtered_images]
    filtered_annotations = filter_dicts_by_inclusion(
        origin_annotations, "image_id", filtered_image_ids
    )
    assert filtered_ann["annotations"] == filtered_annotations


def test_filter_dataset__include_categories():
    origin_info = sample_coco["info"]
    origin_licenses = sample_coco["licenses"]
    origin_images = sample_coco["images"]
    origin_annotations = sample_coco["annotations"]
    origin_categories = sample_coco["categories"]

    # include_files = ["000000000001.jpg", "000000000002.jpg"]
    # exclude_files = ["000000000003.jpg"]
    include_categories = ["label1", "label2", "label3"]
    # exclude_categories = ["label3"]

    filtered_ann = filter_dataset(
        annotation_file, include_categories=include_categories
    )

    # info and licenses should not be changed
    assert filtered_ann["info"] == origin_info
    assert filtered_ann["licenses"] == origin_licenses

    # categories should be filtered by include_categories
    filtered_categories = filter_dicts_by_inclusion(
        origin_categories, "name", include_categories
    )
    assert filtered_ann["categories"] == filtered_categories

    # annotations should be filtered by category_id
    filtered_category_ids = [category["id"] for category in filtered_categories]
    filtered_annotations = filter_dicts_by_inclusion(
        origin_annotations, "category_id", filtered_category_ids
    )
    assert filtered_ann["annotations"] == filtered_annotations

    # images should be filtered by image_id
    filtered_image_ids = [annotation["image_id"] for annotation in filtered_annotations]
    filtered_images = filter_dicts_by_inclusion(origin_images, "id", filtered_image_ids)
    assert filtered_ann["images"] == filtered_images


def test_filter_dataset__exclude_categories():
    origin_info = sample_coco["info"]
    origin_licenses = sample_coco["licenses"]
    origin_images = sample_coco["images"]
    origin_annotations = sample_coco["annotations"]
    origin_categories = sample_coco["categories"]

    # include_files = ["000000000001.jpg", "000000000002.jpg"]
    # exclude_files = ["000000000003.jpg"]
    # include_categories = ["label1", "label2", "label3"]
    exclude_categories = ["label3"]

    filtered_ann = filter_dataset(
        annotation_file, exclude_categories=exclude_categories
    )

    # info and licenses should not be changed
    assert filtered_ann["info"] == origin_info
    assert filtered_ann["licenses"] == origin_licenses

    # categories should be filtered by exclude_categories
    filtered_categories = filter_dicts_by_exclusion(
        origin_categories, "name", exclude_categories
    )
    assert filtered_ann["categories"] == filtered_categories

    # annotations should be filtered by category_id
    filtered_category_ids = [category["id"] for category in filtered_categories]
    filtered_annotations = filter_dicts_by_inclusion(
        origin_annotations, "category_id", filtered_category_ids
    )
    assert filtered_ann["annotations"] == filtered_annotations

    # images should be filtered by image_id
    filtered_image_ids = [annotation["image_id"] for annotation in filtered_annotations]
    filtered_images = filter_dicts_by_inclusion(origin_images, "id", filtered_image_ids)
    assert filtered_ann["images"] == filtered_images


def test_filter_dataset__include_exclude_categories():
    origin_info = sample_coco["info"]
    origin_licenses = sample_coco["licenses"]
    origin_images = sample_coco["images"]
    origin_annotations = sample_coco["annotations"]
    origin_categories = sample_coco["categories"]

    # include_files = ["000000000001.jpg", "000000000002.jpg"]
    # exclude_files = ["000000000003.jpg"]
    include_categories = ["label1", "label2", "label3"]
    exclude_categories = ["label3"]

    filtered_ann = filter_dataset(
        annotation_file,
        include_categories=include_categories,
        exclude_categories=exclude_categories,
    )
    # info and licenses should not be changed
    assert filtered_ann["info"] == origin_info
    assert filtered_ann["licenses"] == origin_licenses

    # categories should be filtered by include_categories
    filtered_categories = filter_dicts_by_inclusion(
        origin_categories, "name", include_categories
    )
    filtered_categories = filter_dicts_by_exclusion(
        filtered_categories, "name", exclude_categories
    )
    assert filtered_ann["categories"] == filtered_categories

    # annotations should be filtered by category_id
    filtered_category_ids = [category["id"] for category in filtered_categories]
    filtered_annotations = filter_dicts_by_inclusion(
        origin_annotations, "category_id", filtered_category_ids
    )
    assert filtered_ann["annotations"] == filtered_annotations

    # images should be filtered by image_id
    filtered_image_ids = [annotation["image_id"] for annotation in filtered_annotations]
    filtered_images = filter_dicts_by_inclusion(origin_images, "id", filtered_image_ids)
    assert filtered_ann["images"] == filtered_images
