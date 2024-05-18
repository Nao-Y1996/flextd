from pycocotools.coco import COCO
from torch.utils.data import Dataset

from utils import create_filtered_annotation_file


class FlexCocoDatasetBase(Dataset):
    """
    Custom Dataset class for COCO dataset.

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

    def __init__(self, image_dir: str,
                 annotation_file: str,
                 data_transforms=None,
                 label_transforms=None,
                 include_files: list[str] = None,
                 exclude_files: list[str] = None,
                 include_categories: list[str] = None,
                 exclude_categories: list[str] = None, ):
        """
        constructor of CustomCocoDataset.
        When include_files is given, only the images with the file names in the list are used.
        When exclude_files is given, the images with the file names in the list are excluded.
        When given include_categories, only the images with the category names in the list used.
        If include_files and exclude_files both contain the same file name, that file will be excluded from the dataset.

        Parameters`
        ----------
        image_dir: str
            path to the image directory
        annotation_file: str
            path to the annotation json file
        data_transforms:
            transform to be applied to the image
        label_transforms:
            transform to be applied to the mask
        include_files: list[str]
            list of file names to include
        exclude_files: list[str]
            list of file names to exclude
        include_categories: list[str]
            list of category names to include
        exclude_categories: list[str]
            list of category names to exclude
        """

        annotation_file = create_filtered_annotation_file(annotation_file=annotation_file,
                                                          include_files=include_files,
                                                          exclude_files=exclude_files,
                                                          include_categories=include_categories,
                                                          exclude_categories=exclude_categories)
        self.coco = COCO(str(annotation_file))
        self.image_dir = image_dir
        self.data_transforms = data_transforms
        self.label_transforms = label_transforms
        self.ids = list(self.coco.imgs.keys())

    def __getitem__(self, index: int):
        raise NotImplementedError("This method should be implemented in the subclass.")

    def __len__(self) -> int:
        raise NotImplementedError("This method should be implemented in the subclass.")

    def get_category_name(self, category_id: int) -> str:
        """
        get category name by category id.
        :param category_id:
        :return: category name
        """
        categories = self.coco.loadCats(category_id)
        return categories[0]['name']

    def get_categories(self) -> list[str]:
        """
        get all category names.
        """
        categories = self.coco.loadCats(self.coco.getCatIds())
        return [category['name'] for category in categories]
