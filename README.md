[work in progress]

# Image Super-Resolution Using Very Deep Residual Channel Attention Networks
This repository is a fork of [the original RCAN repository](https://github.com/yulunzhang/RCAN). It is intended to make it easier to install and use for end users, ie. those who just want a (commandline) tool to upscale images. The RCAN algorithm itself was not modified. What's provided:

- Included pre-trained models made by the authors of RCAN (grabbed [here](https://drive.google.com/file/d/10bEK-NxVtOS9-XSeyOZyaRmxUTX3iIRa/view?usp=sharing) to be precise).
- [TODO] Simplified commandline interface.
- [TODO] Works for single or multiple images (not a dataset with specific naming conventions).
- [WIP] Installation script + requirements.txt.
- [WIP] simplified project structure.

RCAN is a super-resolution algorithm introduced in the following paper
[Yulun Zhang](http://yulunzhang.com/), [Kunpeng Li](https://kunpengli1994.github.io/), [Kai Li](http://kailigo.github.io/), [Lichen Wang](https://sites.google.com/site/lichenwang123/), [Bineng Zhong](https://scholar.google.de/citations?user=hvRBydsAAAAJ&hl=en), and [Yun Fu](http://www1.ece.neu.edu/~yunfu/), "Image Super-Resolution Using Very Deep Residual Channel Attention Networks", ECCV 2018, [[arXiv]](https://arxiv.org/abs/1807.02758)

## Results
![Visual_PSNR_SSIM_BI](/data/figs/fig1_visual_bi_x4.PNG)
Visual results with Bicubic (BI) degradation (4×) on “img 074” from Urban100


![Visual_PSNR_SSIM_BI](/data/figs/fig5_visual_psnr_ssim_bi_x4.PNG)
![Visual_PSNR_SSIM_BI](/data/figs/supp_fig1_visual_psnr_ssim_bi_x4_1.PNG)
![Visual_PSNR_SSIM_BI](/data/figs/supp_fig1_visual_psnr_ssim_bi_x4_2.PNG)
![Visual_PSNR_SSIM_BI](/data/figs/supp_fig1_visual_psnr_ssim_bi_x4_3.PNG)
Visual comparison for 4× SR with BI model

![Visual_PSNR_SSIM_BI](/data/figs/fig6_visual_psnr_ssim_bi_x8.PNG)
Visual comparison for 8× SR with BI model

![Visual_PSNR_SSIM_BD](/data/figs/fig7_visual_psnr_ssim_bd_x3.PNG)
Visual comparison for 3× SR with BD model

![Visual_Compare_GAN_PSNR_SSIM_BD](/data/figs/supp_fig1_visual_compare_gan_psnr_ssim_bi_x4_1.PNG)
&!los[Visual_Compare_GAN_PSNR_SSIM_BD](/data/figs/supp_fig1_visual_compare_gan_psnr_ssim_bi_x4_2.PNG)
![Visual_Compare_GAN_PSNR_SSIM_BD](/data/figs/supp_fig1_visual_compare_gan_psnr_ssim_bi_x4_3.PNG)
Visual comparison for 4× SR with BI model on Set14 and B100 datasets.
The best results are highlighted. SRResNet, SRResNet VGG22, SRGAN MSE, SR-
GAN VGG22, and SRGAN VGG54 are proposed in [CVPR2017SRGAN], ENet E and ENet PAT are
proposed in [ICCV2017EnhanceNet]. These comparisons mainly show the eﬀectiveness of our proposed
RCAN against GAN based methods
