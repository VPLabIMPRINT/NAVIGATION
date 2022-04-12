
# Navigation
(explanation needed)

For more details please refer to our [arxiv paper](https://arxiv.org/abs/2202.02567)




## Installation & Preparation

#### prerequisites
- Python 3.5
- Pytorch 1.5.1
- Cuda 9.2

#### Installation

Clone the repo and make new virtual enviornment by using [enviornment.yml](https://github.com/VPLabIMPRINT/NAVIGATION/blob/main/environment.yml)

``` bash
# Clone this repository
git clone https://github.com/VPLabIMPRINT/NAVIGATION.git  

# Go into the repository
cd NAVIGATION

# Deactivating previous enviornment
conda deactivate

# Creating enviornment from enviornment.yml file
conda env create --file enviornment.yml 

# Activating new enviornment
conda activate navigation_demo 
```




### Model weights
Download following model weights and place it into appropriate folder

- object detection model weights: 
Download weights from [here](https://drive.google.com/drive/folders/1D9_7jCFyLwS0EGy6VP7uXw-22EuhIMkZ?usp=sharing)
and place it into [this](https://github.com/VPLabIMPRINT/NAVIGATION/tree/main/pytorch-0.4-yolov3) folder.

- Depth estimation model weights:
Download weights from [here](https://drive.google.com/file/d/158txNr2sP90FaWkk1q1rBkEwaWNuZJuO/view?usp=sharing)
and place it into [this](https://github.com/VPLabIMPRINT/NAVIGATION/tree/main/Revisiting_Single_Depth_Estimation/pretrained_model)
folder.

- Encoder weights:
Download weights from [here](https://drive.google.com/drive/folders/1QHfpg4FmA5WFT--gGGVloFD7PvVkw-5_?usp=sharing)
and place it into [this](https://github.com/VPLabIMPRINT/NAVIGATION/tree/main/Revisiting_Single_Depth_Estimation/pretrained_model/encoder) folder

- Segmentation model weights:
Download weights from [here](https://drive.google.com/drive/folders/1--uvbvqUgwDilHU60ZuBn1-Jd1-fAxFn?usp=sharing) and place it into [this](https://github.com/VPLabIMPRINT/NAVIGATION/tree/main/semantic-segmentation-pytorch/ckpt/ade20k-mobilenetv2dilated-c1_deepsup_fnf_best) folder.




### Running GUI
``` bash
python fileExp.py
```

### Main results
