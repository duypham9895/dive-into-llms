# 动手学大模型 (Dive into LLMs): Knowledge Editing for Large Models
Overview: editing methods and tools for language models
> Want to control what a language model remembers about a given piece of knowledge? Pick a suitable editing method, edit that specific knowledge, and then verify the edited model!

## 1. Goals of this tutorial:

- Get familiar with the EasyEdit toolkit
- Master editing methods for language models (the simplest version)
- Understand how to choose among different types of editing methods and where each applies

## 2. Preparation:
### 2.1 Getting to know EasyEdit

https://github.com/zjunlp/EasyEdit

EasyEdit is a Python package for editing language models such as GPT-J, Llama, GPT-NEO, GPT2, T5, etc. Its goal is to change a language model's behavior on a specific piece of knowledge effectively, without hurting its performance on other inputs, while being easy to use and easy to extend.

EasyEdit integrates the popular existing editing methods:
![](./assets/1.png)

### 2.2 Main framework

![](./assets/2.png)
EasyEdit contains a unified framework of Editor, Method and Evaluate, which represent the editing scenario, the editing technique and the evaluation method, respectively.
- Editor: describes the working scenario, including the model to edit, the knowledge to edit, and other necessary hyperparameters.
- Method: the specific knowledge editing method used (e.g., ROME, MEND, etc.).
- Evaluate: the metrics that evaluate knowledge editing performance, covering Reliability, Generalization, Locality and Portability.
- Trainer: some editing methods need a certain amount of training, which the Trainer module implements.
## 3. Environment setup:
```
git clone https://github.com/zjunlp/EasyEdit.git
(Optional) conda create -n EasyEdit python=3.9.7
cd EasyEdit
pip install -r requirements.txt
```
## 4. Editing example
> Goal: edit what GPT-2-XL remembers so that Lionel Messi's profession changes from football to basketball (football->basketball).
Steps:
- Choose an editing method and prepare the parameters
- Prepare the knowledge editing data
- Instantiate the Editor
- Run!
Below we use the ROME method as a detailed example:
### 4.1 ROME
Jupiter Notebook: [https://colab.research.google.com/drive/1KkyWqyV3BjXCWfdrrgbR-QS3AAokVZbr?usp=sharing#scrollTo=zWfGkNb9FBJQ] 
- Choose an editing method and prepare the parameters
  - Choose ROME as the editing method, and prepare the parameters that ROME and GPT2-XL need.
  - For example: alg_name: "ROME", model_name: "./hugging_cache/gpt2-xl" or the local path to this model, "device": the index of the GPU to use
  - The remaining parameters can stay at their defaults
![](./assets/3.png)
- Prepare the knowledge editing data
    ```
    prompts = ['Question:What sport does Lionel Messi play? Answer:'] # x_e
    ground_truth = ['football'] # y
    target_new = ['basketball'] # y_e
    subject = ['Lionel Messi'] 
    ```
- Instantiate the Editor: pass the prepared parameters into the BaseEditor class to instantiate it and get a customized Editor instance.
    ```
    hparams = ROMEHyperParams.from_hparams('./hparams/ROME/gpt2-xl.yaml')
    editor=BaseEditor.from_hparams(hparams)
    ```
- Run! Call the editor's edit method:
    ```
    metrics, edited_model, _ = editor.edit(
        prompts=prompts,
        ground_truth=ground_truth,
        target_new=target_new,
        subject=subject,
        keep_original_weight=False
    )
    ```
![](./assets/4.png)
> Note: the first time you edit a given model, the Wiki corpus is downloaded, and the states of each layer are computed for that model (stats_dir: "./data/stats") and saved, to be reused in every later edit. The first edit therefore takes a while; make sure the network connection is stable and wait patiently.
### 4.2 Verification and evaluation
editor.edit returns metrics (computed by EasyEdit's Evaluate module), in this form:
![](./assets/5.png)
To get the Generalization, Locality and Portability values, you need to pass evaluation data into the edit method.

Taking Locality as an example, this makes the edit method compute the Locality metric, i.e., the accuracy of the model's answers on locality_inputs.
```
locality_inputs = {
    'neighborhood':{
        'prompt': ['Joseph Fischhof, the', 'Larry Bird is a professional', 'In Forssa, they understand'],
        'ground_truth': ['piano', 'basketball', 'Finnish']
    }
}
metrics, edited_model, _ = editor.edit(
    prompts=prompts,
    ground_truth=ground_truth,
    target_new=target_new,
    locality_inputs=locality_inputs,
    keep_original_weight=False
)
```
Or directly compare the generte behavior of the model before and after editing.
```
generation_prompts = [
    "Lionel Messi, the",
    "The law in Ikaalinen declares the language"
]

model = GPT2LMHeadModel.from_pretrained('./hugging_cache/gpt2').to('cuda')
batch = tokenizer(generation_prompts, return_tensors='pt', padding=True, max_length=30)

pre_edit_outputs = model.generate(
    input_ids=batch['input_ids'].to('cuda'),
    attention_mask=batch['attention_mask'].to('cuda'),
    max_new_tokens=3
)
post_edit_outputs = edited_model.generate(
    input_ids=batch['input_ids'].to('cuda'),
    attention_mask=batch['attention_mask'].to('cuda'),
    max_new_tokens=3)
```
## 5. Editing at scale (optional)
### 5.1 Batch edit
Multiple data items can be formed into parallel lists and passed into the edit method together for a batch edit; MEMIT is the best method in this case. (https://colab.research.google.com/drive/1P1lVklP8bTyh8uxxSuHnHwB91i-1LW6Z)
```
prompts = ['Question:What sport does Lionel Messi play? Answer:',
            'The law in Ikaalinen declares the language']
ground_truth = ['football', 'Finnish']
target_new = ['basketball', 'Swedish']
subject = ['Lionel Messi', 'Ikaalinen']
```
### 5.2 Testing on Benchmarks
- Counterfact
- ZsRE
```
{
    "case_id": 4402,
    "pararel_idx": 11185,
    "requested_rewrite": {
      "prompt": "{} debuted on",
      "relation_id": "P449",
      "target_new": {
        "str": "CBS",
        "id": "Q43380"
      },
      "target_true": {
        "str": "MTV",
        "id": "Q43359"
      },
      "subject": "Singled Out"
    },
    "paraphrase_prompts": [
      "No one on the ground was injured.  v",
      "The sex ratio was 1063. Singled Out is to debut on"
    ],
    "neighborhood_prompts": [
      "Daria premieres on",
      "Teen Wolf was originally aired on",
      "Spider-Man: The New Animated Series was originally aired on",
      "Celebrity Deathmatch premiered on",
      "\u00c6on Flux premiered on",
      "My Super Psycho Sweet 16 premieres on",
      "Daria was released on",
      "Jersey Shore premiered on",
      "Skins was originally aired on",
      "All You've Got premiered on"
    ]
  }
  ```
https://github.com/zjunlp/EasyEdit/blob/main/examples/run_zsre_llama2.py 
