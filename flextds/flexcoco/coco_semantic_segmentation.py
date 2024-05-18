import os

import numpy as np
from pycocotools.coco import COCO
import torch
from torchvision.io import read_image

from coco_base import FlexCocoDatasetBase


class FlexCocoDatasetBaseSS(FlexCocoDatasetBase):
    """
        Custom Dataset class for COCO dataset for semantic segmentation.

        Attributes
        ----------
        image_dir: str
            path to the image directory
        coco: COCO
            COCO object
        data_transforms:
            transform to be applied to the image
        label_transforms:
            transform to be applied to the label such as mask, bounding box, etc.
        ids: list[int]
            list of image ids
        """

    def __init__(self, image_dir: str, annotation_file: str, *args, **kwargs):
        super().__init__(image_dir, annotation_file, *args, **kwargs)

    def __getitem__(self, index: int) -> tuple[torch.Tensor, dict]:
        """
        Parameters
        ----------
        index: int
            index of the image

        Returns
        -------
        img: torch.Tensor
            image tensor
        target: dict
            dictionary containing masks, origin_height, origin_width
            mask is a tensor of shape (n_batches, n_classes, height, width)
        """
        # 画像IDを取得
        img_id = self.ids[index]
        height = self.coco.loadImgs(img_id)[0]["height"]
        width = self.coco.loadImgs(img_id)[0]["width"]
        file_name = self.coco.loadImgs(img_id)[0]['file_name']
        # 画像IDに対応するアノテーションID一覧を取得（1枚の画像に複数のアノテーションがある）
        ann_ids = self.coco.getAnnIds(imgIds=img_id)
        # アノテーションID一覧から画像に紐ずくアノテーション一覧を取得
        coco_anns = self.coco.loadAnns(ann_ids)

        category_ids = self.coco.getCatIds()

        self.cat_id2idx = {}
        self.cat_name2idx = {}
        for idx, category in enumerate(self.coco.loadCats(category_ids)):
            self.cat_id2idx[category["id"]] = idx
            self.cat_name2idx[category["name"]] = idx

        # masks: (num_of_category_mask, height, width)
        masks = np.zeros(shape=(len(category_ids), height, width), dtype=bool)
        # アノテーションをカテゴリごとに結合してカテゴリマスクを作成
        for ann in coco_anns:
            category_id: int = int(ann['category_id'])
            index_of_cat = self.cat_id2idx[category_id]
            category_mask = masks[index_of_cat]  # get category mask
            category_mask = np.logical_or(category_mask, self.coco.annToMask(ann))  # update category mask
            masks[index_of_cat] = category_mask  # put category mask back
        masks = torch.Tensor(masks.astype(np.float32))

        img: torch.Tensor = read_image(os.path.join(self.image_dir, file_name))

        if self.data_transforms is not None:
            img = self.data_transforms(img)
        if self.label_transforms is not None:
            masks = self.label_transforms(masks)

        target = {
            "masks": masks,
            "file_name": file_name,
            "origin_height": height,
            "origin_width": width
        }

        return img, target

    def __len__(self) -> int:
        return len(self.ids)
