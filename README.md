# Contents
- [Introduction](#introduction)
- [Results](#results)
  - [Visual Results](#visual-results)
  - [Quantitative Results](#quantitative-results)
- [TL;DR](#tldr)
- [Installation](#installation)
- [Usage](#usage)
  * [Absolute VS relative paths](#absolute-vs-relative-paths)
  * [RCAN](#rcan)
    + [Single image](#single-image)
    + [Without CUDA](#without-cuda)
    + [Multiple images (wildcard)](#multiple-images-wildcard)
    + [Multiple images (explicit)](#multiple-images-explicit)
    + [Multiple images (combining all at once)](#multiple-images-combining-all-at-once)
    + [Changing the output directory...](#changing-the-output-directory)
    + [Using a different upscaling factor...](#using-a-different-upscaling-factor)
    + [Custom pre-trained files (advanced)](#custom-pre-trained-files-advanced)
    + [Example with absolute paths](#example-with-absolute-paths)
  * [RCAN+](#rcan-1)
  * [Sample full output](#sample-full-output)

# Introduction

See [TL;DR](#tldr) if you are in a hurry. Note: this is more of a
"one time" thing made for someone else, and I can't keep up with
upstream changes.

This repository is a fork of
[the original RCAN repository](https://github.com/yulunzhang/RCAN),
"Image Super-Resolution Using Very Deep Residual Channel Attention
Networks". It is intended to make it easier to install and use for end
users, ie. those who just want a (commandline) tool to upscale images.
The RCAN algorithm itself was not modified. What's provided:

- Included pre-trained models made by the authors of RCAN (grabbed
  [here](https://drive.google.com/file/d/10bEK-NxVtOS9-XSeyOZyaRmxUTX3iIRa/view?usp=sharing)
  to be precise).
- Installation script (+ requirements.txt).
- Faster execution by upgrading to (py)torch 1.1.x (instead of 0.4.x
  like the original code).
- Simplified commandline invocation.
  * Including passing a single or multiple images as positional argument(s)
  (instead of a dataset with specific directory structure and naming
  conventions).
- Some user friendly (common) errors (eg. image not found).
- Simplified project structure.
- Explicit MIT license (see
  [this](https://github.com/yulunzhang/RCAN/issues/92))

RCAN is a super-resolution algorithm introduced in the following paper
[Yulun Zhang](http://yulunzhang.com/),
[Kunpeng Li](https://kunpengli1994.github.io/),
[Kai Li](http://kailigo.github.io/),
[Lichen Wang](https://sites.google.com/site/lichenwang123/),
[Bineng Zhong](https://scholar.google.de/citations?user=hvRBydsAAAAJ&hl=en),
and [Yun Fu](http://www1.ece.neu.edu/~yunfu/), "Image Super-Resolution
Using Very Deep Residual Channel Attention Networks", ECCV 2018,
[[arXiv]](https://arxiv.org/abs/1807.02758)

# Results

## Visual Results

![Visual_PSNR_SSIM_BI](/data/figs/fig1_visual_bi_x4.PNG)
Visual results with Bicubic (BI) degradation (4×) on “img 074” from Urban100

![Visual_PSNR_SSIM_BI](/data/figs/fig5_visual_psnr_ssim_bi_x4.PNG)
![Visual_PSNR_SSIM_BI](/data/figs/supp_fig1_visual_psnr_ssim_bi_x4_1.PNG)
![Visual_PSNR_SSIM_BI](/data/figs/supp_fig1_visual_psnr_ssim_bi_x4_2.PNG)
![Visual_PSNR_SSIM_BI](/data/figs/supp_fig1_visual_psnr_ssim_bi_x4_3.PNG)
Visual comparison for 4× SR with BI model.

![Visual_PSNR_SSIM_BI](/data/figs/fig6_visual_psnr_ssim_bi_x8.PNG)
Visual comparison for 8× SR with BI model.

![Visual_PSNR_SSIM_BD](/data/figs/fig7_visual_psnr_ssim_bd_x3.PNG)
Visual comparison for 3× SR with BD model.

![Visual_Compare_GAN_PSNR_SSIM_BD](/data/figs/supp_fig1_visual_compare_gan_psnr_ssim_bi_x4_1.PNG)
&!los[Visual_Compare_GAN_PSNR_SSIM_BD](/data/figs/supp_fig1_visual_compare_gan_psnr_ssim_bi_x4_2.PNG)
![Visual_Compare_GAN_PSNR_SSIM_BD](/data/figs/supp_fig1_visual_compare_gan_psnr_ssim_bi_x4_3.PNG)

Visual comparison for 4× SR with BI model on Set14 and B100 datasets.
The best results are highlighted. SRResNet, SRResNet VGG22, SRGAN MSE,
SR- GAN VGG22, and SRGAN VGG54 are proposed in [CVPR2017SRGAN], ENet E
and ENet PAT are proposed in [ICCV2017EnhanceNet]. These comparisons
mainly show the effectiveness of RCAN against GAN based methods.

## Quantitative Results
![PSNR_SSIM_BI](/data/figs/psnr_bi_1.PNG)
![PSNR_SSIM_BI](/data/figs/psnr_bi_2.PNG)
![PSNR_SSIM_BI](/data/figs/psnr_bi_3.PNG)

Quantitative results with BI degradation model. Best and second best
results are highlighted and underlined.

For more results, please refer to the
[main paper](https://arxiv.org/abs/1807.02758) and the
[supplementary file](http://yulunzhang.com/papers/ECCV-2018-RCAN_supp.pdf).

# TL;DR

See [Installation](#installation) and [Usage](#usage) for a more
in-depth documentation.

###### Grab the source

```shell
cd /home/user/me/workspace # <- use whatever directory you want the source code to be in.
git clone https://github.com/Antoine-Patel/user-friendly-RCAN.git # Or download ZIP archive from github
```

###### Install CUDA 10.0 + cuDNN

Refer to NVIDIA website for guides on installing CUDA on your system.
Alternatively, skip this step, then use the --cpu option to invoke
RCAN without CUDA.

###### Install

```shell
cd /home/user/me/workspace/user-friendly-RCAN # For example
python install.py

```

Note: if CUDA is detected, it will at some point print
`Downloading https://download.pytorch.org/whl/cu100/[...]` instead
of `Downloading https://download.pytorch.org/whl/cpu/[...]`.

###### Test run on a small provided image

```shell
# Small image, fast even without CUDA. If the end of the installation
# script shows that you have CUDA enabled, remove '--cpu'.
target='./data/LR/LRBI/Set5/x2/bird_LRBI_x2.png'
result='/tmp/bird_LRBI_x2_RCAN_x2.png'

python run.py --chop --cpu --scale 2 --outdir /tmp "$target"
# Display the result.
display "$result" || xviewer "$result" # Or whatever is your image viewer, you get the idea.
```

###### Note

If you installed CUDA after running the install.py script, you need to
uninstall pytorch and torchvision inside the rcan-env/, then rerun the
install.py script.
See 
[Re-installing pytorch with CUDA support](#re-installing-pytorch-with-cuda-support).

# Installation

If you plan on using CUDA, install it first before the command
below:

```shell
# python <absolute>/<path>/<to>/user-friendly-RCAN/install.py
# Eg (if you installed into C:/Users/me/sr/user-friendly-RCAN):
python C:/Users/me/sr/user-friendly-RCAN/install.py

# If the working directory is the root of this repository, you can use
# a relative path:
# python install.py
```

Note: you can invoke this install script multiple times, it's "smart"
enough not to:
- break a previous successful install
- re-create the already existing python virtual environment
- re-download each dependencies thanks to pip's cache

Python 3.6 or later is recommended. Pip is also needed to install the
dependencies. Because this project was updated to work with pytorch
1.1, CUDA 10.0 or CUDA 9.0 are supported. Please check the matching
cuDNN version with the help of your favorite search engine.

This code was tested on python 3.6 and 3.7. It should be able to run
on python 3.4 and python 3.5, but no garantees here.

The provided installation script installs dependencies (pytorch,
matplotlib etc) into a "python virtual environment". If you are
unfamiliar with this concept, you can think of it has a self-contained
local installation; the opposite of a global, system-wide
installation. This allows multiple version of the same packages (eg.
pytorch) to cohexists on the same computer without issues.

This explains why pytorch may be re-installed, even if you already
have it globally on your system, or on another virtual environment.

The installation of CUDA + cuDNN is not part of the install
process, because:
- I don't have access to a computer with a NVIDIA graphic card.
- From my understanding, in order to download cuDNN, you must register
  for the NVIDIA Developer Program, wich would be quite hard to
  script / impossible ?
- Managing multiple CUDA versions on the same computer, if the need
  arises, sounds like a pain.

Thus, you should install those two **optional** dependencies yourself.
Please note that the quality of the upscaling is not affected at all
by having CUDA + cuDNN available or not, only speed (runtime).

If you have run the install.py script before installing CUDA, refer to
the next section to make RCAN aware of CUDA.

## Re-installing pytorch with CUDA support

###### Activate the virtual environment

`<venv>` below refers to the directory: 
`<absolute>/<path>/<to>/user-friendly-RCAN/rcan-env`.

| Platform | Shell | Command to activate virtual environment |
| -------- | ----- | --------------------------------------- |
| POSIX | bash/zsh | `$ source <venv>/bin/activate` |
| POSIX | fish | `$ . <venv>/bin/activate.fish` |
| POSIX | csh/tcsh | `$ source <venv>/bin/activate.csh` |
| POSIX | PowerShell Core | `<venv>/bin/Activate.ps1` |
| Windows | cmd.exe | `C:\> <venv>\Scripts\activate.bat` |
| Windows | PowerShell | `PS C:\> <venv>\Scripts\Activate.ps1` |

'(rcan-env)' should be mentionned in your terminal (before the prompt)
if the virtual environment was successfully activated.

###### Uninstall pytorch and torchvision

```shell
python -m pip uninstall torch torchvision
```

###### Rerun the install script

```shell
# Will only re-download and re-install torch and torchvision
python install.py
```

###### Deactivate the virtual environment

```shell
deactivate
```

# Usage

## Absolute VS relative paths

Let's say you downloaded and extracted (or cloned) this repository to
C:/Users/me/Documents/user-friendly-RCAN on your system. Then you can invoke
RCAN by specifying the full absolute path to "run.py", which will work
not matter the working directory:

```shell
python C:/Users/me/Documents/user-friendly-RCAN/run.py --help
```

Alternatively, you can change the working directory to the repository
root, and use a relative path:

```shell
cd C:/Users/me/Documents/user-friendly-RCAN
python run.py --help
```

Absolute paths are recommended for scripts, while relative paths are
more convenient during interactive sessions.

The next examples will assume the working directory is the repository
root unless specified.

## RCAN

### Single image

```shell
# Running RCAN on a single image (/home/user/me/pictures/bird.png):
# --scale: Upscale by a factor 2
# Result: /home/user/me/pictures/bird-RCAN-x2.png
# --chop: enable memory efficient forwarding. Recommended.
python run.py --chop --scale 2  /home/user/me/pictures/bird.png
```

### Without CUDA

Same, but do not (try to) use CUDA, only use a cpu (even if CUDA is
available on your system). Use this if you encounter the error 'Found
no NVIDIA driver on your system. [...]'.

```shell
python run.py --chop --cpu --scale 2  /home/user/me/pictures/bird.png
```

### Multiple images (wildcard)

Eg. process all .png and .jpg pictures inside directory
/home/user/me/pictures/:

```shell
# Note: use PowerShell (or something like "git bash") on windows if
# you want to use wildcards; doesn't work in cmd.exe.
# Results: /home/user/me/pictures/*-RCAN-x2.{png,jpg,jpeg}
python run.py --chop --scale 2 "/home/user/me/pictures/*.jpg" "/home/user/me/pictures/*.jpeg" "/home/user/me/pictures/*.png"
```

You may want to use the --ignore_invalid_files flag to prevent RCAN
from stopping as soon as an invalid image is encountered, especially
when using wildcards.

### Multiple images (explicit)

```shell
# Results: /home/user/me/pictures/bird-RCAN-x2.png, /home/user/me/pictures/2020/tree_small_RCAN_x2.png, 'tmp/birthday cake RCAN x2.png'
python run.py --chop --scale 2 /home/user/me/pictures/bird.png /home/user/me/pictures/2020/tree_small.png '/tmp/birthday cake.png'
```

Note how because "_" exists in "tree_small.png", it's reusing this
separator (instead of the default one: '-') to name the result
(tree_small_RCAN_x2.png). Same thing for ' '.

### Multiple images (combining all at once)

```shell
python run.py --chop --scale 2 /home/user/me/pictures/bird.png /tmp/baby.png /tmp/apple.jpg /media/me/hdd/pictures/small/*.jpg /media/me/hdd/pictures/small/holyday-summer-2020-*.png
```

### Changing the output directory...

... with --outdir:

```shell
# Results: /tmp/bird-RCAN-x2.png, /tmp/baby-RCAN-x2.png
python run.py --chop --scale 2 --outdir /tmp /home/user/me/pictures/bird.png ./baby.png

# To use the current directory (working directory):
# Results: ./bird-RCAN-x2.png, ./baby-RCAN-x2.png
python run.py --chop --scale 2 --outdir "." /home/user/me/pictures/bird.png ./baby.png

```

### Using a different upscaling factor

```shell
# Eg. upscale by a factor 4. Allowed values: 2, 3, 4, 8.
python run.py --chop --scale 4  --outdir /tmp /home/user/me/pictures/bird.png
```

Note: a pre-trained file is automatically choosen according to the
upscaling factor. Eg. if you choose --scale 4, a pre-trained file,
resulting from training RCAN to do upscaling by a factor of 4, is
loaded. The four allowed values correspond to the four pre-trained
files provided. See --pre_trained_file and --custom_scale for more
flexibility.

### Custom pre-trained files (advanced)

You can use a custom pre-trained file for the model, one that you
created yourself (see
[here](https://github.com/yulunzhang/RCAN#train)). Not required unless
you are unhappy with the provided pre-trained files, that can be found
in ./data/model/RCAN_*.pt. Use --custom_scale in this case.

```shell
python run.py --chop --custom_scale 6  --pre_trained_file /home/user/me/documents/RCAN_scale_by_6.pt /home/user/me/pictures/bird.png

```

Although not recommended, you can also use a pre-trained file
resulting from training the model to upscale by a factor different
than the value of --scale:

```shell
# Upscale by 2, but load a model created to upscale by 4.
python run.py --chop --custom_scale 2  --pre_trained_file ./data/model/RCAN_BIX4.pt /home/user/me/pictures/bird.png

```

### Example with absolute paths

Git Bash / Bash example:

```shell
python ~/workspace/user-friendly-RCAN/run.py --chop --scale 2 --outdir /tmp ~/workspace/user-friendly-RCAN/data/LR/LRBI/Set5/x2/bird_LRBI_x2.png
```

# RCAN+

Add the '--self_ensemble' flag to any of the previous examples in 
order to enable 'RCAN+', which yields slightly better results, but is
 slower (see [Quantitative Results](#quantitative-results)).

```shell
python run.py --self_ensemble --chop --scale 2  /home/user/me/pictures/bird.png
```

# Sample full output

```shell
user@user-laptop:~$ python ~/workspace/user-friendly-RCAN/run.py --chop --cpu --scale 2 --outdir /tmp ~/workspace/user-friendly-RCAN/data/LR/LRBI/Set5/x2/b*_x2.png
Loading model from /media/user/icybox_02/data/documents/workspace/user-friendly-RCAN/data/model/RCAN_BIX2.pt
100%|#############################################| 3/3 [04:22<00:00, 87.44s/it]
Saved results:
/tmp/baby_LRBI_x2_RCAN_x2.png
/tmp/bird_LRBI_x2_RCAN_x2.png
/tmp/butterfly_LRBI_x2_RCAN_x2.png

```
