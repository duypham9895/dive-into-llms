# 动手学大模型 (Dive into LLMs): Multimodal Large Language Models

Overview: this part introduces the common architectures of multimodal large language models and how to build them

> The arrival of large language models (LLMs) has shown everyone that high-level intelligence is fully expressed in the language modality. As models that can simulate the real world more fully, how do multimodal large language models achieve stronger multimodal understanding and generation? Can multimodal large language models help achieve AGI?


## Goals of this tutorial

1. Get familiar with the types of multimodal large language models
2. Master the general technical framework of multimodal large language models
3. Master building, training and running inference with multimodal large language models



## 1. Theory primer



### 1.1 Understanding the types of multimodal large language models

- Classification of existing multimodal large language models by function and modality support


> Before building multimodal large language models (MLLMs), researchers in the field reached a consensus, which is also a key premise: thanks to scaling laws and emergent phenomena, today's language-based LLMs already have strong semantic understanding, which means language has become the key modality that carries intelligence, so language intelligence is seen as the hub of multimodal intelligence. Therefore, almost all MLLMs are built on top of language-based LLMs, with the LLM as the core decision-making module, similar to a brain or a central processing unit. In other words, by adding extra external modules or encoders for non-text modalities, the LLM is given multimodal perception/action capabilities.

We divide existing MLLMs into different types according to their modality support and function support.

![mllm](assets/MLLM-summary.png)


- Read the full tutorial: [[Slides](https://github.com/Lordog/dive-into-llms/blob/main/documents/chapter6/mllms.pdf)]


- More related surveys
    - [A Survey on Multimodal Large Language Models, https://github.com/BradyFU/Awesome-Multimodal-Large-Language-Models, 2023](https://github.com/BradyFU/Awesome-Multimodal-Large-Language-Models)
    - [MM-LLMs: Recent Advances in MultiModal Large Language Models, 2023](https://arxiv.org/pdf/2401.13601)


### 1.2 Understanding the general technical framework of multimodal large language models


- Architecture 1: LLM as Task Scheduler

> There are currently two common MLLM architectures in the community.
The first is the “LLM as discrete scheduler/controller” architecture. As shown in the figure below, the LLM's role is to receive text signals and issue text commands to downstream modules. All message passing inside the system is mediated by plain-text commands output by the LLM. There is no interaction between the different functional modules.


![Architecture1](assets/Architecture1.png)

- Architecture 2: LLM as Joint Part of System

> The second architecture is the encoder-LLM-decoder framework.
This is also the most popular architecture today. In it, the LLM's role is to perceive multimodal information and respond and act on its own within an encoder-LLM-decoder structure. The key difference between this architecture and the first one is therefore that the LLM, as a key joint part of the system, receives multimodal information directly from outside and delegates instructions to the decoder/generator more smoothly. In the encoder-LLM-decoder framework, as shown in the figure below, the encoder processes encoded signals from more than one modality, the LLM acts as the core decision-maker, and the decoder manages the multimodal output.

![Architecture2](assets/Architecture2.png)





## 2. Hands-on with general-purpose multimodal large language models

> Practice building a general-purpose “any-modality-to-any-modality” multimodal large language model


### 2.1 A general, unified “any-to-any modality” multimodal large language model: NExT-GPT

> Future MLLM research will surely move toward ever more general, generalist models, and will therefore cover as many modalities and functions as possible. NExT-GPT is currently one of the most pioneering works in this field: it was the first to introduce the concept of an “any-to-any modality” MLLM. This architecture achieves powerful capabilities and lays the foundation for future research directions in multimodal large language models.

![NExT-GPT](assets/NExT-GPT-screen.png)


> The hands-on coding part of this lesson on multimodal large language models takes the NExT-GPT code as its target, analyzing and practicing with it in an accessible yet in-depth way.

[NExT-GPT Project](https://next-gpt.github.io/)

[NExT-GPT GitHub code repository](https://github.com/NExT-GPT/NExT-GPT)




### 2.2 Code structure overview


```
├── figures
├── data
│   ├── T-X_pair_data  
│   │   ├── audiocap                      # text-autio pairs data
│   │   │   ├── audios                    # audio files
│   │   │   └── audiocap.json             # the audio captions
│   │   ├── cc3m                          # text-image paris data
│   │   │   ├── images                    # image files
│   │   │   └── cc3m.json                 # the image captions
│   │   └── webvid                        # text-video pairs data
│   │   │   ├── videos                    # video files
│   │   │   └── webvid.json               # the video captions
│   ├── IT_data                           # instruction data
│   │   ├── T+X-T_data                    # text+[image/audio/video] to text instruction data
│   │   │   ├── alpaca                    # textual instruction data
│   │   │   ├── llava                     # visual instruction data
│   │   ├── T-T+X                         # synthesized text to text+[image/audio/video] instruction data
│   │   └── MosIT                         # Modality-switching Instruction Tuning instruction data
├── code
│   ├── config
│   │   ├── base.yaml                     # the model configuration 
│   │   ├── stage_1.yaml                  # enc-side alignment training configuration
│   │   ├── stage_2.yaml                  # dec-side alignment training configuration
│   │   └── stage_3.yaml                  # instruction-tuning configuration
│   ├── dsconfig
│   │   ├── stage_1.json                  # deepspeed configuration for enc-side alignment training
│   │   ├── stage_2.json                  # deepspeed configuration for dec-side alignment training
│   │   └── stage_3.json                  # deepspeed configuration for instruction-tuning training
│   ├── datast
│   │   ├── base_dataset.py
│   │   ├── catalog.py                    # the catalog information of the dataset
│   │   ├── cc3m_datast.py                # process and load text-image pair dataset
│   │   ├── audiocap_datast.py            # process and load text-audio pair dataset
│   │   ├── webvid_dataset.py             # process and load text-video pair dataset
│   │   ├── T+X-T_instruction_dataset.py  # process and load text+x-to-text instruction dataset
│   │   ├── T-T+X_instruction_dataset.py  # process and load text-to-text+x instruction dataset
│   │   └── concat_dataset.py             # process and load multiple dataset
│   ├── model                     
│   │   ├── ImageBind                     # the code from ImageBind Model
│   │   ├── common
│   │   ├── anyToImageVideoAudio.py       # the main model file
│   │   ├── agent.py
│   │   ├── modeling_llama.py
│   │   ├── custom_ad.py                  # the audio diffusion 
│   │   ├── custom_sd.py                  # the image diffusion
│   │   ├── custom_vd.py                  # the video diffusion
│   │   ├── layers.py                     # the output projection layers
│   │   └── ...  
│   ├── scripts
│   │   ├── train.sh                      # training NExT-GPT script
│   │   └── app.sh                        # deploying demo script
│   ├── header.py
│   ├── process_embeddings.py             # precompute the captions embeddings
│   ├── train.py                          # training
│   ├── inference.py                      # inference
│   ├── demo_app.py                       # deploy Gradio demonstration 
│   └── ...
├── ckpt                           
│   ├── delta_ckpt                        # tunable NExT-GPT params
│   │   ├── nextgpt         
│   │   │   ├── 7b_tiva_v0                # the directory to save the log file
│   │   │   │   ├── log                   # the logs
│   └── ...       
│   ├── pretrained_ckpt                   # frozen params of pretrained modules
│   │   ├── imagebind_ckpt
│   │   │   ├──huge                       # version
│   │   │   │   └──imagebind_huge.pth
│   │   ├── vicuna_ckpt
│   │   │   ├── 7b_v0                     # version
│   │   │   │   ├── config.json
│   │   │   │   ├── pytorch_model-00001-of-00002.bin
│   │   │   │   ├── tokenizer.model
│   │   │   │   └── ...
├── LICENCE.md
├── README.md
└── requirements.txt
```


### 2.3 Environment setup

First clone the repository and install the required environment; you can set up the environment by running the following commands:

```
conda env create -n nextgpt python=3.8

conda activate nextgpt

# CUDA 11.6
conda install pytorch==1.13.1 torchvision==0.14.1 torchaudio==0.13.1 pytorch-cuda=11.6 -c pytorch -c nvidia

git clone https://github.com/NExT-GPT/NExT-GPT.git
cd NExT-GPT

pip install -r requirements.txt
```




### 2.4 Getting started with system inference


#### 2.4.1 Loading the NExT-GPT model checkpoint from pre-training

- **Step 1**: load the `frozen parameters`. [NExT-GPT](https://github.com/NExT-GPT/NExT-GPT) is trained on top of the following existing models or modules; prepare the checkpoints as described below.
    - `ImageBind` is the unified image/video/audio encoder. You can download the pre-training checkpoint from [here](https://dl.fbaipublicfiles.com/imagebind/imagebind_huge.pth), version `huge`. Then place the `imagebind_huge.pth` file in [[./ckpt/pretrained_ckpt/imagebind_ckpt/huge]](ckpt/pretrained_ckpt/imagebind_ckpt/).
    - `Vicuna`: first prepare LLaMA following the instructions [[here]](ckpt/pretrained_ckpt/prepare_vicuna.md). Then place the pre-trained model in [[./ckpt/pretrained_ckpt/vicuna_ckpt/]](ckpt/pretrained_ckpt/vicuna_ckpt/).
    - `Image Diffusion` is used to generate images. NExT-GPT uses version `v1-5` of [Stable Diffusion](https://huggingface.co/runwayml/stable-diffusion-v1-5). (_downloaded automatically by the code_)
    - `Audio Diffusion` is used to generate audio content. NExT-GPT uses version `l-full` of [AudioLDM](https://github.com/haoheliu/AudioLDM). (_downloaded automatically by the code_)
    - `Video Diffusion` is used to generate video. We use version `v2_576w` of [ZeroScope](https://huggingface.co/cerspense/zeroscope_v2_576w). (_downloaded automatically by the code_)

- **Step 2**: load the `trainable parameters`.

Place the NExT-GPT system in [[./ckpt/delta_ckpt/nextgpt/7b_tiva_v0]](./ckpt/delta_ckpt/nextgpt/7b_tiva_v0). You can either 1) use parameters you trained yourself, or 2) download a checkpoint that has completed pre-training from [Huggingface](https://huggingface.co/ChocoWu/nextgpt_7b_tiva_v0).


#### 2.4.2 Deploying the Gradio demo

Once the checkpoints are loaded, you can run the demo locally as follows:
```angular2html
cd ./code
bash scripts/app.sh
```
The key arguments to specify are:
- `--nextgpt_ckpt_path`: path to the NExT-GPT parameters from pre-training.



#### 2.4.3 Trying out test examples

The current version supports input in any combination of four modality types (text, image, video and audio), and output in any combination of modalities.
It also supports multi-turn interaction with context.

Run it yourself to see the results.

- **Case-1**: input T+I, output T+A

![case1](assets/T+I-T+A.png)


- **Case-2**: input T+V, output T+A

![case2](assets/T+V-T+A.png)


- **Case-3**: input T+I, output T+I+V

![case3](assets/T+I-T+I+V.png)


- **Case-4**: input T, output T+I+V+A

![case4](assets/T-T+I+V+A.png)







### 2.5 System training process


#### 2.5.1 Data preparation

Download the following datasets for model training:

A) T-X pair data
  - `CC3M` data of ***text-image*** pairs: follow these instructions [[here]](./data/T-X_pair_data/cc3m/prepare.md). Then place the data in [[./data/T-X_pair_data/cc3m]](./data/T-X_pair_data/cc3m).
  - `WebVid` data of ***text-video*** pairs: see the [[instruction]](./data/T-X_pair_data/webvid/prepare.md). Save the files in [[./data/T-X_pair_data/webvid]](./data/T-X_pair_data/webvid).
  - `AudioCap` data of ***text-audio*** pairs: see the [[instruction]](./data/T-X_pair_data/audiocap/prepare.md). Save the data in [[./data/T-X_pair_data/audiocap]](./data/T-X_pair_data/audiocap).

B) Instruction tuning data
  - T+X-T
    - ***Visual instruction data*** (from `LLaVA`): download it from [here](https://github.com/haotian-liu/LLaVA/blob/main/docs/Data.md) and place it in [[./data/IT_data/T+X-T_data/llava]](./data/IT_data/T+X-T_data/llava/).
    - ***Textual instruction data*** (from `Alpaca`): download it from [here](https://github.com/tatsu-lab/stanford_alpaca) and place it in [[./data/IT_data/T+X-T_data/alpaca/]](data/IT_data/T+X-T_data/alpaca/).
    - ***Video instruction data*** (from `VideoChat`): download it from [here](https://github.com/OpenGVLab/InternVideo/tree/main/Data/instruction_data) and place it in [[./data/IT_data/T+X-T_data/videochat/]](data/IT_data/T+X-T_data/videochat/).

    Note: after downloading the datasets, run `preprocess_dataset.py` to preprocess them into a unified format.
  - T-X+T (T2M)
    - The `T-X+T` instruction dataset (T2M) is stored in [[./data/IT_data/T-T+X_data]](./data/IT_data/T-T+X_data).
   
  - MosIT
    - Get the instructions for downloading the data [here](./data/IT_data/MosIT_data/). Finally, place the data in [[./data/IT_data/MosIT_data/]](./data/IT_data/MosIT_data/).




#### 2.5.2 Embedding preparation

In the decoder-side alignment training of NExT-GPT, we minimize the distance between the representations of the Signal Token and the captions. To keep the system efficient and save time and memory, we use the text encoder of each diffusion model to precompute the text embeddings of the image, audio and video captions.

Before training NExT-GPT, run the following command; the generated `embedding` files will be saved in [[./data/embed]](./data/embed).
```
cd ./code/
python process_embeddings.py ../data/T-X_pair_data/cc3m/cc3m.json image ../data/embed/ runwayml/stable-diffusion-v1-5
```


Arguments:
- args[1]: path to the caption file;
- args[2]: modality, one of `image`, `video` and `audio`;
- args[3]: path where the embedding files are saved;
- args[4]: name of the corresponding diffusion model from pre-training.




#### 2.5.3 Three-stage training


First, see the base configuration file [[./code/config/base.yaml]](./code/config/base.yaml) for the basic system settings of the whole module.

Then run the following script to start training NExT-GPT:
```
cd ./code
bash scripts/train.sh
```

The specific command is:
```
deepspeed --include localhost:0 --master_addr 127.0.0.1 --master_port 28459 train.py \
    --model nextgpt \
    --stage 1\
    --save_path  ../ckpt/delta_ckpt/nextgpt/7b_tiva_v0/\
    --log_path ../ckpt/delta_ckpt/nextgpt/7b_tiva_v0/log/
```
Key arguments:
- `--include`: `localhost:0` means CUDA device `0` used by DeepSpeed (translator's note: the source says “GPT cuda”).
- `--stage`: the training stage.
- `--save_path`: directory where the trained delta weights are stored. This directory is created automatically.
- `--log_path`: directory where the log files are stored.



NExT-GPT's training is divided into 3 steps:

- **Step 1**: encoder-side, LLM-centric multimodal alignment. This stage trains the ***input projection layer*** while freezing ImageBind, the LLM and the output projection layer.
  
  Simply run the `train.sh` script above with: `--stage 1`
  
  Also see the run configuration file [[./code/config/stage_1.yaml]](./code/config/stage_1.yaml) and the DeepSpeed configuration file [[./code/dsconfig/stage_1.yaml]](./code/dsconfig/stage_1.yaml) for more step-by-step configuration details.

  Note that the datasets used in this step are listed in `dataset_name_list`, and the dataset names must exactly match the definitions in [[./code/dataset/catalog.py]](./code/dataset/catalog.py).



- **Step 2**: decoder-side instruction-following alignment. This stage trains the ***output projection layer*** while freezing ImageBind, the LLM and the input projection layer.

  Simply run the `train.sh` script above with: `--stage 2`

  Also see the run configuration file [[./code/config/stage_2.yaml]](./code/config/stage_2.yaml) and the DeepSpeed configuration file [[./code/dsconfig/stage_2.yaml]](./code/dsconfig/stage_2.yaml) for more step-by-step configuration details.



- **Step 3**: instruction tuning. This stage tunes the following on the instruction dataset: 1) the ***LLM*** via LoRA, 2) the ***input projection layer***, and 3) the ***output projection layer***.

  Simply run the `train.sh` script above with: `--stage 3`

  Also see the run configuration file [[./code/config/stage_3.yaml]](./code/config/stage_3.yaml) and the DeepSpeed configuration file [[./code/dsconfig/stage_3.yaml]](./code/dsconfig/stage_3.yaml) for more step-by-step configuration details.
