# Fine-Tuning and Deploying Pre-trained Language Models

> Overview: this part introduces fine-tuning of pre-trained models
Want to improve a pre-trained model's performance on a given task? Let's pick a suitable pre-trained model, fine-tune it on a specific task, and deploy the fine-tuned model as an easy-to-use demo!
## Goals of this tutorial:
1. Get familiar with the Transformers toolkit
2. Master fine-tuning and inference of pre-trained models (decoupled customizable version & default integrated version)
3. Master deploying a demo with Gradio Spaces
4. Understand how to choose among different types of pre-trained models and their use cases
## Contents of this tutorial:
### 1. Preparation:
#### 1.1 Get to know the toolkit: Transformers
https://github.com/huggingface/transformers

> 🤗 Transformers provides APIs and tools to easily download and train state-of-the-art pre-trained models. Using pre-trained models reduces compute costs and carbon emissions, and saves the time and resources needed to train from scratch. These models support common tasks across different modality types, such as:
📝 Natural language processing (NLP): text classification, named entity recognition (NER), question answering, language modeling, summarization, translation, multiple choice, and text generation.
🖼️ Computer vision: image classification, object detection, and semantic segmentation.
🗣️ Audio: automatic speech recognition and audio classification.
🐙 Multimodal: table question answering, optical character recognition, information extraction from scanned documents, video classification, and visual question answering.

Detailed Chinese documentation: https://huggingface.co/docs/transformers/main/zh/index

![huggingface](./assets/huggingface.PNG)

#### 1.2 Environment setup: text classification (e.g., fake news detection) as the example
1. Go to the text classification examples, read the readme to learn the key arguments, and download requirements.txt and run_classification.py

https://github.com/huggingface/transformers/tree/main/examples/pytorch/text-classification

2. Set up the environment:
- 1. Create a new environment with conda: conda create -n llm python=3.9
- 2. Enter the virtual environment: conda activate llm
- 3. pip install transformers
- 4. Remove torch (which would be installed automatically) from requirements.txt, then pip install -r requirements.txt

> If downloads are slow, use a mirror inside mainland China: pip [Packages] -i https://pypi.tuna.tsinghua.edu.cn/simple

> If you install pytorch from a mirror inside mainland China, the cpu build of pytorch is picked automatically and cannot run on the gpu, so:

- 5. conda install pytorch

> If downloads are slow, configure conda mirrors by following this blog: https://blog.csdn.net/weixin_42797483/article/details/132048218

3. Prepare the data: we use the fake tweets dataset on Kaggle as the example: https://www.kaggle.com/c/nlp-getting-started/data

#### 1.3 Ready-made project packages (demo code and data)
(1) Decoupled customizable version (key modules are decoupled for easier understanding; you can customize data loading, model architecture, evaluation metrics, etc.)

[TextClassificationCustom download link](https://pan.quark.cn/s/00dae5c2b128)

(2) Default integrated version (richer, more complex code, usually driven directly through hyperparameters; a slightly higher bar for development)

[TextClassification download link](https://pan.quark.cn/s/9d0510f1c98d)


### 2. Custom development on the decoupled version (minimum viable product, MVP)
Three main files in total: main.py, the main program; utils_data.py, data loading and processing; modeling_bert.py, the model architecture

![project structure](./assets/0.png)

#### 2.1 Understand the key modules
1. Load and process data (utils_data.py)
![utils_data.py](./assets/1.png)

2. Load the model (modeling_bert.py)

![modeling_bert_1.py](./assets/2.png)

![modeling_bert_2.py](./assets/3.png)


3. Train/validate/predict (main.py)

![main.py](./assets/4.png)

#### 2.2 Run training, validation and prediction end to end
```shell
python main.py
```

### 3. Fine-tuning on the integrated version (Optional, based on run_classification.py)

#### 3.1 Understand the key modules:
1. Load the data (csv or json format)
![load data](./assets/5.png)

2. Process the data
![process data](./assets/6.png)

3. Load the model
![load model](./assets/7.png)

4. Train/validate/predict
![train dev predict](./assets/8.png)

#### 3.2 Train the model
Train while validating on the development set and predicting on the test set; run the script below:

```shell
python run_classification.py \
    --model_name_or_path  bert-base-uncased \
    --train_file data/train.csv \
    --validation_file data/val.csv \
    --test_file data/test.csv \
    --shuffle_train_dataset \
    --metric_name accuracy \
    --text_column_name "text" \
    --text_column_delimiter "\n" \
    --label_column_name "target" \
    --do_train \
    --do_eval \
    --do_predict \
    --max_seq_length 512 \
    --per_device_train_batch_size 32 \
    --learning_rate 2e-5 \
    --num_train_epochs 1 \
    --output_dir experiments/
```

If you get an error or it hangs, it is usually a network problem:

1. <u>If downloading the model shows “Network is unreachable”, download the model manually to your machine: https://huggingface.co/google-bert/bert-base-uncased</u>
2. <u>If it hangs after the data is loaded, and after you stop it with CTRL+C it shows it was stuck at “connection”, the cause is a failed network connection while the evaluate package was loading the evaluation metric.</u>

![bug](./assets/9.png)

In that case, download the whole package from the evaluate GitHub repository: https://github.com/huggingface/evaluate/tree/main, then in the hyperparameters change the --metric_name path to the local metric path, i.e.:

```shell
python run_classification.py \
    --model_name_or_path  bert-base-uncased \
    --train_file data/train.csv \
    --validation_file data/val.csv \
    --test_file data/test.csv \
    --shuffle_train_dataset \
    --metric_name evaluate/metrics/accuracy/accuracy.py \
    --text_column_name "text" \
    --text_column_delimiter "\n" \
    --label_column_name "target" \
    --do_train \
    --do_eval \
    --do_predict \
    --max_seq_length 512 \
    --per_device_train_batch_size 32 \
    --learning_rate 2e-5 \
    --num_train_epochs 1 \
    --output_dir experiments/
```

![reference result](./assets/10.png)


### 4. Deploy the model: once training is done, we can build online demos on Gradio Spaces
#### 4.1 Gradio Spaces tutorial
https://huggingface.co/docs/hub/en/spaces-sdks-gradio
#### 4.2 Create a Space
1. https://huggingface.co/new-space?sdk=gradio
2. Note: if it does not open, try a VPN or proxy (needed from mainland China)

![Gradio Spaces](./assets/gradio.png)

#### 4.3 Key inference code
See app.py in the project package for details

![app.py](./assets/11.png)

#### 4.4 Upload app.py, the environment configuration file and the model to Gradio Spaces
1. Configuration file (requirements.txt)
```
transformers==4.30.2
torch==2.0.0
```

2. File overview

![file overview](./assets/12.png)


3. Demo result
A successfully deployed example for reference: https://huggingface.co/spaces/cooelf/text-classification
The source code is visible under the “Files” tab in the top right.

![Files](./assets/13.png)


4. Easter egg (bonus tip): the Spaces platform shows the trending Demos every week, and you can search for large models and Demos that interest you and try them out
![Spaces](./assets/14.png)


### 5. Further exercises
1. Try other classification/regression tasks, such as sentiment classification, news classification, vulnerability classification, etc.
2. Try other types of models, such as T5, ELECTRA, etc.
### 6. Other commonly used models
1. Question answering models: https://github.com/huggingface/transformers/tree/main/examples/pytorch/question-answering
2. Text summarization: https://github.com/huggingface/transformers/tree/main/examples/pytorch/summarization
3. Running inference with Llama2: https://huggingface.co/docs/transformers/en/model_doc/llama2
4. Parameter-efficient fine-tuning (lightweight fine-tuning) of Llama2 (LoRA):  https://github.com/peremartra/Large-Language-Model-Notebooks-Course/blob/main/5-Fine%20Tuning/LoRA_Tuning_PEFT.ipynb


### 7. Further reading
1. A 43-page [survey](https://mp.weixin.qq.com/s?__biz=Mzk0MTYzMzMxMA==&mid=2247484539&idx=1&sn=6ee42baab4ad792e74ac6a89d7dd87d9) with a comprehensive, in-depth analysis of large language models (LLMs) (by the author of Word2Vec)
   
    Paper title: Large Language Models: A Survey

    Paper link: https://arxiv.org/pdf/2402.06196.pdf

2. [GPT, GPT-2, GPT-3 Paper Close Reading (Paper Close Reading)](https://www.bilibili.com/video/BV1AF411b7xQ?t=0.0)

3. [InstructGPT Paper Close Reading (Paper Close Reading · 48)](https://www.bilibili.com/video/BV1hd4y187CR?t=0.4)
