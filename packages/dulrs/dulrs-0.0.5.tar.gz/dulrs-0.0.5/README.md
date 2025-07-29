# API

## Download 

Please download 'Template.zip'.

### Description of Folders

- **datasets**: This folder should hold the raw datasets used for the project. 
- **export**: This folder is for files that include models.
- **result**: This folder is for pretrained model parameters
- **mats**: This directory stores MATLAB-related files, such as `.mat` files or other results generated during computation.
- **your script**: Your script should be placed at the same level as 'export'

## Usage Guide for `dulrs` Package

The `dulrs` package provides tools to calculate and visualize some evaluation matrix (heatmap, low-rankness, sparsity)of our models on various scenarios from different datasets.

### Installation

First, install the package using `pip`:

```bash
pip install dulrs
```

### Importing the Package

Import the package in your Python script:

```python
from dulrs import dulrs_class
```

### Available Functions

The package includes the following functions:

0. `dulrs_class(model_name, model_path, use_cuda=True, num_stages=6)`
1. `dulrs_class.heatmap(img_path, data_name,output_mat,output_png)`
2. `dulrs_class.lowrank_cal(img_path, model_name, data_name, save_dir)`
3. `dulrs_class.lowrank_draw(model_name, data_name, mat_dir, save_dir)`
4. `dulrs_class.sparsity_cal(img_path, model_name, data_name, save_dir)`

### Function Descriptions and Examples

#### 0. `dulrs_class(model_name, model_path, use_cuda=True, num_stages=6)`
The `dulrs_class` in the `dulrs` package is used to initialize the models with pretrained parameters and including following fucntions.

#### 1. `dulrs_class.heatmap(img_path, data_name, output_mat, output_png)`

The `dulrs_class.heatmap` function in the `dulrs` package allows users to draw and save the heatmaps obtained from different stages.

#### 2. `dulrs_class.lowrank_cal(img_path, model_name, data_name, save_dir)`

The `dulrs_class.lowrank_cal` function in the `dulrs` package allows users to calculate and save the low-rankness data with mat format.

#### 3. `dulrs_class.lowrank_draw(model_name, data_name, mat_dir, save_dir)`

The `dulrs_class.lowrank_draw` function in the `dulrs` package allows users to draw the low-rankness figure based on the calculated low-rankess data and save with png format.

#### 4. `dulrs_class.sparsity_cal(img_path, model_name, data_name, save_dir)`

The `dulrs_class.sparsity_cal` function in the `dulrs` package allows users to calculate and save the sparsity data with mat format.


#### Function Parameters

The `dulrs_class` accepts the following parameters:
- `model_name`: refer to the model which is underestimated.
- `model_path`: the pretrained parameters pkl path.
- `use_cuda`: Determined whether use GPU for acceleration.
- `num_stages`: Determined the number of saving stages.

The `dulrs_class.heatmap` function accepts the following parameters:
- `img_path`: refer to the testing image.
- `data_name`: refer to the name of testing image.
- `output_mat`: save path for result with mat format.
- `output_png`: save path for result with png format.

The `dulrs_class.lowrank_cal` function accepts the following parameters:
- `img_path`: refer to the testing image set.
- `model_name`: refer to the model which is underestimated.
- `data_name`: refer to the name of testing image.
- `save_dir`: save path for low-rankness result with mat format.

The `dulrs_class.lowrank_draw` function accepts the following parameters:
- `model_name`: refer to the model which is underestimated.
- `data_name`: refer to the name of testing image.
- `mat_dir`: refer to the path for low-rankess result.
- `save_dir`: save path for low rankness result with png format.

The `dulrs_class.sparsity_cal` function accepts the following parameters:
- `img_path`: refer to the testing image set.
- `model_name`: refer to the model which is underestimated.
- `data_name`: refer to the name of testing image.
- `save_dir`: save path for sparsity result with mat format.

## Examples

1. Model: RPCANet_pp

Please follow the instructions below to set up the dataset and run the model:

### 📥 Download Dataset
Download the dataset from the following link:

[📎 Google Drive - IRSTD-1k Dataset](https://drive.google.com/file/d/1sLU4KFoYF5Sczo-Laf9B7AhN8ya3Oy-p/view?usp=drive_link)

### 📂 Directory Setup
After downloading:

1. Extract the contents of the archive.
2. Place the extracted dataset folder into the following path:
   ```
   ./datasets/
   ```

### 📜 Script Placement
Ensure that the main execution script is placed in the **same directory** as the `export` file.

> 📌 Example directory structure:
> ```
> .
> ├── export/
> ├── your_main_script.py
> └── datasets/
>     └── [IRSTD-1k]
> ```

### 📜 Script Example

   ```python
    from dulrs import dulrs_class
    import torch

    # Set CUDA as default device
    torch.set_default_tensor_type('torch.cuda.FloatTensor' if torch.cuda.is_available()     else 'torch.FloatTensor')

    dulrs = dulrs_class(
    model_name="rpcanet_pp",
    model_path="./result/ISTD/1K/s6_best.pkl",     # Path for pretrained parameters
    num_stages=6,
    use_cuda=True)

    # For heatmap generation
    heatmap = dulrs.heatmap(
        img_path="./datasets/IRSTD-1k/test/images/000009.png",
        data_name="IRSTD-1k_test_images_000009",
        output_mat="./heatmap/mat",  # If users want to save the data as mat format.    Default=None
        output_png="./heatmap/png"   # If users want to save the figure as png format.  Default=None
    )

    # For lowrank calculation
    lowrank_matrix = dulrs.lowrank_cal(
        img_path="./datasets/IRSTD-1k/test/images",
        model_name="rpcanet_pp",
        data_name="IRSTD-1k",
        save_dir= "./mats/lowrank"
    )

    # For lowrank paint based on calculation
    lowrank_matrix_draw = dulrs.lowrank_draw(
        model_name="rpcanet_pp",
        data_name="IRSTD-1k",
        mat_dir= './mats/lowrank',
        save_dir = './mats/lowrank/figure' # Save path for result with png format
    )

    # For sparsity calculation
    sparsity_matrix = dulrs.sparsity_cal(
        img_path="./datasets/IRSTD-1k/test/images",
        model_name="rpcanet_pp",
        data_name="IRSTD-1k",
        save_dir = './mats/sparsity'        # Save path for result with mat format
    )
   ```

