### **`pip install sprite-pipeline`**

You download images to a folder

![image](https://github.com/user-attachments/assets/c9571d74-167c-444a-85c0-de09c9c78eb6)

⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️

`sp_group --style painting.png -H 100 downloaded/`

![image](https://github.com/user-attachments/assets/f78390a6-6737-4d33-bf24-3554721d5bdd)

⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️

You open output.psd, resize layers, fix perspective, patch.

⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️

`sp_pack`

![image](https://github.com/user-attachments/assets/8f7ed3f2-b918-4268-a123-a919f21e2485)
![image](https://github.com/user-attachments/assets/8a650d62-fa07-426c-a2fa-600af78e0420)

Congrats! You get packed spritesheet and UV coordinates in .txt

## Features

- Foreground extraction
- Light correction
- Style transfer
- PSD building
- Spritesheet packing

## CLI args

#### sp_group

`sp_group folder_name/ --style STYLE_IMAGE -W MAX_WIDTH -H MAX_HEIGHT -f STYLE_FORCE -o OUTPUT_PSD`

Creates PSD file containing group `folder_name` where each layer is a processed image with the specified maximum dimensions.

#### sp_pack

`sp_pack psd_file.psd -o OUTPUT_DIR --format SPRITESHEET_IMAGE_FORMAT`

For each group in PSD creates packed spritesheet image and UV coordinates file named group_name.fmt and group_name_uvs.txt.

## Details

1. [BiRefNet](https://huggingface.co/ZhengPeng7/BiRefNet) to extract foreground
2. [RetinexNet](https://github.com/weichen582/RetinexNet) to fix lights
3. [nst_vgg19](https://github.com/alexanderbrodko/nst_vgg19) for Neural Style Transfer
4. [RealESRGAN_MtG](https://huggingface.co/rullaf/RealESRGAN_MtG) to improve quality
5. OpenCV to other filters and algorithms


![output](https://github.com/user-attachments/assets/e10aedcc-0cd9-47e3-ac60-e1d426b30cc0)

