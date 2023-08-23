from bciplugin.Core.Datasets.base import BaseConcatDataset, fetch_data_description, RawDataset


class CustomDataset(BaseConcatDataset):
    """
    A custom dataset class that creates a dataset using a loading script.

    This class inherits from BaseConcatDataset and allows for the creation of a custom dataset by
    loading data using a provided loading script.

    Args:
        **kwargs (dict): Keyword arguments for configuring the custom dataset.
            loading_script (str): The path to the loading script file.

    Attributes:
        classes_codes (dict): A dictionary containing class codes loaded from the loading script.

    Methods:
        __init__(self, **kwargs): Constructor method for initializing the CustomDataset.
    """

    def __init__(self, **kwargs):
        """
        Initialize the CustomDataset.

        Loads data and class codes using the provided loading script and constructs a custom dataset.

        Args:
            **kwargs (dict): Keyword arguments for configuring the custom dataset.
                loading_script (str): The path to the loading script file.
        """
        if (len(kwargs) == 1) and 'loading_script' in kwargs:
            loading_script = kwargs['loading_script']
            local_env = {}
            exec(open(loading_script, 'r', encoding='UTF-8').read(), local_env)
            data = local_env['data']
            self.classes_codes = local_env['classes_codes']

            all_base_ds = []
            raws, description = fetch_data_description(data)
            for raw, (_, row) in zip(raws, description.iterrows()):
                all_base_ds.append(RawDataset(raw, row))
            BaseConcatDataset.__init__(self, all_base_ds)
