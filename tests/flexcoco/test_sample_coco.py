import json
import os

DATA_DIR = str(os.path.dirname(__file__).replace("flexcoco", "data"))


def test_sample_coco():
    annotation_file = str(os.path.join(DATA_DIR, "sample_coco.json"))
    with open(annotation_file, "r") as f:
        sample_coco = json.load(f)

    origin_info = sample_coco["info"]
    origin_licenses = sample_coco["licenses"]
    origin_images = sample_coco["images"]
    origin_annotations = sample_coco["annotations"]
    origin_categories = sample_coco["categories"]

    assert origin_info == {
        "year": 2024,
        "version": "1.0",
        "description": "sample annotation",
        "date_created": "2024",
    }
    assert origin_licenses == [{"id": 1, "name": "sample license", "url": ""}]

    assert origin_images == [
        {
            "date_captured": "2021",
            "file_name": "000000000001.jpg",
            "id": 1,
            "height": 480,
            "width": 640,
        },
        {
            "date_captured": "2021",
            "file_name": "000000000002.jpg",
            "id": 2,
            "height": 426,
            "width": 640,
        },
        {
            "date_captured": "2021",
            "file_name": "000000000003.jpg",
            "id": 3,
            "height": 428,
            "width": 640,
        },
    ]

    assert origin_annotations == [
        {
            "segmentation": [
                [
                    1.0799999999999272,
                    187.69008000000002,
                    612.66976,
                    187.69008000000002,
                    612.66976,
                    473.53008000000005,
                    1.0799999999999272,
                    473.53008000000005,
                ]
            ],
            "area": 174816.81699840003,
            "iscrowd": 0,
            "image_id": 1,
            "bbox": [
                1.0799999999999272,
                187.69008000000002,
                611.5897600000001,
                285.84000000000003,
            ],
            "category_id": 1,
            "id": 1,
        },
        {
            "segmentation": [
                [
                    311.73024,
                    4.310159999999996,
                    631.0102400000001,
                    4.310159999999996,
                    631.0102400000001,
                    232.99032,
                    311.73024,
                    232.99032,
                ]
            ],
            "area": 73013.00148480001,
            "iscrowd": 0,
            "image_id": 1,
            "bbox": [311.73024, 4.310159999999996, 319.28000000000003, 228.68016],
            "category_id": 2,
            "id": 2,
        },
        {
            "segmentation": [
                [
                    385.52992,
                    60.030002999999994,
                    600.50016,
                    60.030002999999994,
                    600.50016,
                    357.19013700000005,
                    385.52992,
                    357.19013700000005,
                ]
            ],
            "area": 63880.58532441216,
            "iscrowd": 0,
            "image_id": 2,
            "bbox": [385.52992, 60.030002999999994, 214.97024, 297.160134],
            "category_id": 3,
            "id": 9,
        },
        {
            "segmentation": [
                [
                    53.01024000000001,
                    356.49000599999994,
                    185.04032,
                    356.49000599999994,
                    185.04032,
                    411.6800099999999,
                    53.01024000000001,
                    411.6800099999999,
                ]
            ],
            "area": 7286.7406433203205,
            "iscrowd": 0,
            "image_id": 2,
            "bbox": [53.01024000000001, 356.49000599999994, 132.03008, 55.190004],
            "category_id": 4,
            "id": 10,
        },
        {
            "segmentation": [
                [
                    204.86016,
                    31.019728000000015,
                    459.74016,
                    31.019728000000015,
                    459.74016,
                    355.13984800000003,
                    204.86016,
                    355.13984800000003,
                ]
            ],
            "area": 82611.73618559999,
            "iscrowd": 0,
            "image_id": 3,
            "bbox": [204.86016, 31.019728000000015, 254.88, 324.12012],
            "category_id": 4,
            "id": 11,
        },
    ]

    assert origin_categories == [
        {"id": 1, "name": "label1", "supercategory": "_1"},
        {"id": 2, "name": "label2", "supercategory": "_2"},
        {"id": 3, "name": "label3", "supercategory": "_3"},
        {"id": 4, "name": "label4", "supercategory": "_4"},
    ]
