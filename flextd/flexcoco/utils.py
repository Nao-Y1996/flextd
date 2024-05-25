import json


def filter_dicts_by_inclusion(
    origins: list[dict], key: str, value_list: list[str]
) -> list[dict]:
    """
    Filter a list of dictionaries to include only those with a specified key having any value in a given list.

    Parameters
    ----------
    origins : list of dict
        A list of dictionaries to be filtered.
    key : str
        The key in each dictionary to be checked against the value_list.
    value_list : list of str
        A list of acceptable values for the specified key.

    Returns
    -------
    list of dict
        A list of dictionaries where the value associated with the specified key is in the value_list.

    Examples
    --------
    >>> origins = [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}, {'name': 'Charlie', 'age': 35}]
    >>> key = 'name'
    >>> value_list = ['Alice', 'Charlie']
    >>> filter_dicts_by_inclusion(origins, key, value_list)
    [{'name': 'Alice', 'age': 30}, {'name': 'Charlie', 'age': 35}]
    """
    new_list = []
    for origin in origins:
        if origin[key] in value_list:
            new_list.append(origin)
    return new_list


def filter_dicts_by_exclusion(
    origins: list[dict], key: str, value_list: list[str]
) -> list[dict]:
    """
    Filter a list of dictionaries to exclude those with a specified key having any value in a given list.

    Parameters
    ----------
    origins : list of dict
        A list of dictionaries to be filtered.
    key : str
        The key in each dictionary to be checked against the value_list.
    value_list : list of str
        A list of values to be excluded for the specified key.

    Returns
    -------
    list of dict
        A list of dictionaries where the value associated with the specified key is not in the value_list.

    Examples
    --------
    >>> origins = [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}, {'name': 'Charlie', 'age': 35}]
    >>> key = 'name'
    >>> value_list = ['Alice', 'Charlie']
    >>> filter_dicts_by_exclusion(origins, key, value_list)
    [{'name': 'Bob', 'age': 25}]
    """
    new_list = []
    for origin in origins:
        if origin[key] not in value_list:
            new_list.append(origin)
    return new_list


def filter_dataset(
    annotation_file: str,
    include_files: list[str] = None,
    exclude_files: list[str] = None,
    include_categories: list[str] = None,
    exclude_categories: list[str] = None,
) -> dict | None:
    """
    filter dataset by file names and category names.

    Parameters
    ----------
    annotation_file: str
        path to the annotation file
    include_files: list[str]
        list of file names to include
    exclude_files: list[str]
        list of file names to exclude
    include_categories: list[str]
        list of category names to include
    exclude_categories: list[str]
        list of category names to exclude

    Returns
    -------
    annotation_dict: dict | None
        filtered annotation dictionary or None if no filter is applied
    """

    if (
        (include_files is None)
        and (exclude_files is None)
        and (include_categories is None)
        and (exclude_categories is None)
    ):
        return None

    with open(annotation_file) as f:
        annotation_dict = json.load(f)

    # filter by file names
    if include_files is not None or exclude_files is not None:
        # fix image list
        new_images = annotation_dict["images"]
        if include_files is not None:
            new_images = filter_dicts_by_inclusion(
                new_images, key="file_name", value_list=include_files
            )
        if exclude_files is not None:
            new_images = filter_dicts_by_exclusion(
                new_images, key="file_name", value_list=exclude_files
            )
        # fix annotation list
        new_image_ids = [image["id"] for image in new_images]
        new_annotations = filter_dicts_by_inclusion(
            annotation_dict["annotations"], key="image_id", value_list=new_image_ids
        )

        # fix annotation dictionary
        annotation_dict["images"] = new_images
        annotation_dict["annotations"] = new_annotations

    # filter by category names
    if include_categories is not None or exclude_categories is not None:

        # fix category list
        new_categories = annotation_dict["categories"]
        if include_categories is not None:
            new_categories = filter_dicts_by_inclusion(
                new_categories, key="name", value_list=include_categories
            )
        if exclude_categories is not None:
            new_categories = filter_dicts_by_exclusion(
                new_categories, key="name", value_list=exclude_categories
            )

        # fix annotation list
        new_category_ids = [category["id"] for category in new_categories]
        new_annotations = filter_dicts_by_inclusion(
            annotation_dict["annotations"],
            key="category_id",
            value_list=new_category_ids,
        )

        # fix image list
        new_image_ids = [annotation["image_id"] for annotation in new_annotations]
        new_images = filter_dicts_by_inclusion(
            annotation_dict["images"], key="id", value_list=new_image_ids
        )

        # fix annotation dictionary
        annotation_dict["images"] = new_images
        annotation_dict["annotations"] = new_annotations
        annotation_dict["categories"] = new_categories

    return annotation_dict


def create_filtered_annotation_file(
    annotation_file: str,
    new_annotation_file: str = None,
    include_files: list[str] = None,
    exclude_files: list[str] = None,
    include_categories: list[str] = None,
    exclude_categories: list[str] = None,
) -> str:
    """
    create a filtered annotation file by file names and category names.

    Parameters
    ----------
    annotation_file: str
        path to the annotation file
    new_annotation_file: str
        path to the new annotation file
    include_files: list[str]
        list of file names to include
    exclude_files: list[str]
        list of file names to exclude
    include_categories: list[str]
        list of category names to include
    exclude_categories: list[str]
        list of category names to exclude

    Returns
    -------
    output_file: str
        path to the annotation file
    """

    annotation_dict = filter_dataset(
        annotation_file=annotation_file,
        include_files=include_files,
        exclude_files=exclude_files,
        include_categories=include_categories,
        exclude_categories=exclude_categories,
    )

    if annotation_dict is not None:
        if new_annotation_file is None:
            new_annotation_file = annotation_file.replace(".json", "_filtered.json")
        with open(new_annotation_file, "w") as f:
            json.dump(annotation_dict, f)
        return new_annotation_file
    else:
        return annotation_file
