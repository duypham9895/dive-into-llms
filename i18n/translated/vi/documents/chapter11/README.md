# Dive into LLMs: RLHF (học tăng cường từ phản hồi của con người)

> Sổ tay thực hành này dịch và tổng hợp từ tài liệu trên mạng [blog](https://newfacade.github.io/notes-on-reinforcement-learning/17-ppo-trl.html) & [trl examples](https://github.com/huggingface/trl/blob/main/examples/notebooks/gpt2-sentiment.ipynb)

Cấu hình khi tái lập thí nghiệm: một GPU NVDIA A800-SXM4-80GB, chiếm 10097MiB bộ nhớ GPU, thời gian huấn luyện 35min19s.

Bài hướng dẫn: [slide](./RLHF.pdf)

Notebook: [notebook](./RLHF.ipynb)

## PPO hoạt động thế nào
1. Rollout: mô hình ngôn ngữ sinh câu trả lời dựa trên query (câu truy vấn đầu vào).
2. Evaluation: query và câu trả lời được đánh giá bằng một hàm, một mô hình, phản hồi của con người, hoặc một tổ hợp nào đó của chúng. Bước này phải tạo ra một **giá trị vô hướng** cho mỗi cặp query/câu trả lời.
3. Optimization: ở bước tối ưu hóa, các cặp query/câu trả lời được dùng để tính log-probability (logarit của xác suất mô hình gán cho token) của từng token (đơn vị văn bản nhỏ nhất mà mô hình đọc và sinh) trong chuỗi. Việc này được thực hiện bằng mô hình đang huấn luyện và mô hình tham chiếu. KL divergence (độ đo khác biệt giữa hai phân phối xác suất) giữa hai đầu ra được dùng làm tín hiệu reward (điểm thưởng cho một hành động/câu trả lời) bổ sung, để đảm bảo câu trả lời được sinh ra không đi quá xa mô hình ngôn ngữ tham chiếu. Sau đó, mô hình ngôn ngữ chính (mô hình đang được huấn luyện) được huấn luyện bằng PPO (Proximal Policy Optimization: thuật toán RL giới hạn mỗi bước cập nhật policy để huấn luyện ổn định).
<div style="text-align: center">
<img src='figs/trl1.png' width='600'>
<p style="text-align: center;"> <b>Hình:</b> Sơ đồ quy trình PPO </p>
</div>

# Fine-tuning GPT-2 để sinh bài đánh giá phim tích cực  
> Tối ưu hóa GPT-2 để sinh các bài đánh giá phim IMDB tích cực, dùng bộ phân loại cảm xúc BERT làm reward function (hàm tính reward cho mỗi bước).

<div style="text-align: center">
<img src='figs/gpt2_bert_training.png' width='600'>
<p style="text-align: center;"> <b>Hình:</b> Thiết lập thí nghiệm fine-tuning GPT-2</p>
</div>

Chúng ta thực hiện fine-tuning (tinh chỉnh một mô hình đã huấn luyện trên dữ liệu của một nhiệm vụ cụ thể) cho GPT-2 để sinh các bài đánh giá phim tích cực dựa trên tập dữ liệu IMDB. Mô hình nhận phần mở đầu của một bài đánh giá thật và phải sinh phần tiếp theo mang sắc thái tích cực. Để thưởng cho phần tiếp theo tích cực, chúng ta dùng bộ phân loại BERT phân tích cảm xúc của câu được sinh ra, rồi lấy đầu ra của bộ phân loại làm tín hiệu reward cho quá trình huấn luyện PPO.

## Thiết lập thí nghiệm

### Tải mô hình và dữ liệu
Tập dữ liệu
```bash
export HF_ENDPOINT=https://hf-mirror.com; huggingface-cli download --resume-download stanfordnlp/imdb --local-dir dataset/imdb --repo-type dataset
```
Mô hình tham chiếu
```bash
export HF_ENDPOINT=https://hf-mirror.com; huggingface-cli download --resume-download lvwerra/gpt2-imdb --local-dir model/gpt2-imdb
```
Reward model (mô hình chấm điểm câu trả lời)
```bash
export HF_ENDPOINT=https://hf-mirror.com; huggingface-cli download --resume-download lvwerra/distilbert-imdb --local-dir model/distilbert-imdb
```

### Import các thư viện phụ thuộc


```python
# %pip install -r requirements.txt
# import os
# os.environ['CUDA_VISIBLE_DEVICES'] = '7'
```


```python
import torch
from tqdm import tqdm
import pandas as pd

tqdm.pandas()

from transformers import pipeline, AutoTokenizer
from datasets import load_dataset

from trl import PPOTrainer, PPOConfig, AutoModelForCausalLMWithValueHead
from trl.core import LengthSampler
```

### Cấu hình


```python
config = PPOConfig(
    model_name="model/gpt2-imdb",
    learning_rate=1.41e-5,
    log_with="wandb",
)

sent_kwargs = {"top_k": None, "function_to_apply": "none", "batch_size": 16}
```


```python
import wandb

wandb.init()
```

Bạn có thể thấy chúng ta đã nạp một mô hình GPT-2 tên là `gpt2_imdb`. Mô hình này được fine-tune thêm 1 epoch (một lượt duyệt hết tập huấn luyện) trên tập dữ liệu IMDB, dùng [script](https://github.com/huggingface/transformers/blob/main/examples/legacy/run_language_modeling.py) của Hugging Face (không có thiết lập đặc biệt). Các tham số còn lại chủ yếu lấy từ bài báo gốc “[Fine-Tuning Language Models from Human Preferences](https://huggingface.co/papers/1909.08593)”. Mô hình này và mô hình BERT đều có trong kho mô hình của Hugging Face, đường dẫn cụ thể ở [đây](https://huggingface.co/models).

## Nạp dữ liệu và mô hình

### Nạp tập dữ liệu IMDB  
Tập dữ liệu IMDB gồm 50,000 bài đánh giá phim, được gán nhãn cảm xúc “tích cực”/“tiêu cực”. Chúng ta nạp tập dữ liệu IMDB vào một DataFrame và chỉ giữ lại các bài đánh giá dài ít nhất 200 ký tự. Sau đó, chúng ta tokenize (cắt văn bản thành token) từng văn bản và dùng `LengthSampler` để cắt ngẫu nhiên văn bản về một độ dài cho trước.


```python
def build_dataset(
    config,
    dataset_name="dataset/imdb",
    input_min_text_length=2,
    input_max_text_length=8,
):
    """
    Build dataset for training. This builds the dataset from `load_dataset`, one should
    customize this function to train the model on its own dataset.

    Args:
        dataset_name (`str`):
            The name of the dataset to be loaded.

    Returns:
        dataloader (`torch.utils.data.DataLoader`):
            The dataloader for the dataset.
    """
    tokenizer = AutoTokenizer.from_pretrained(config.model_name)
    tokenizer.pad_token = tokenizer.eos_token
    # load imdb with datasets
    ds = load_dataset(dataset_name, split="train")
    ds = ds.rename_columns({"text": "review"})
    ds = ds.filter(lambda x: len(x["review"]) > 200, batched=False)

    input_size = LengthSampler(input_min_text_length, input_max_text_length)

    def tokenize(sample):
        sample["input_ids"] = tokenizer.encode(sample["review"])[: input_size()]
        sample["query"] = tokenizer.decode(sample["input_ids"])
        return sample

    ds = ds.map(tokenize, batched=False)
    ds.set_format(type="torch")
    return ds
```


```python
dataset = build_dataset(config)


def collator(data):
    return dict((key, [d[key] for d in data]) for key in data[0])
```

### Nạp mô hình ngôn ngữ GPT2 đã qua pre-training (huấn luyện ban đầu trên kho dữ liệu rất lớn, chưa gắn với nhiệm vụ cụ thể)
Chúng ta nạp mô hình GPT2 có value head (lớp đầu ra phụ ước lượng value, gắn trên mô hình ngôn ngữ) cùng tokenizer (bộ chuyển văn bản thành chuỗi token id). Chúng ta nạp mô hình hai lần: mô hình thứ nhất dùng để tối ưu hóa, còn mô hình thứ hai làm mốc tham chiếu để tính KL-divergence so với điểm khởi đầu. Trong huấn luyện PPO, giá trị này đóng vai trò tín hiệu reward bổ sung, để đảm bảo mô hình sau tối ưu không đi quá xa mô hình ngôn ngữ ban đầu.


```python
model = AutoModelForCausalLMWithValueHead.from_pretrained(config.model_name)
ref_model = AutoModelForCausalLMWithValueHead.from_pretrained(config.model_name)
tokenizer = AutoTokenizer.from_pretrained(config.model_name)

tokenizer.pad_token = tokenizer.eos_token
```

### Khởi tạo PPOTrainer  
`PPOTrainer` lo việc phân bổ thiết bị và tối ưu hóa ở các bước sau:


```python
ppo_trainer = PPOTrainer(
    config, model, ref_model, tokenizer, dataset=dataset, data_collator=collator
)
```


### Nạp bộ phân loại BERT  
Chúng ta nạp một bộ phân loại BERT đã qua fine-tuning trên tập dữ liệu IMDB.


```python
device = ppo_trainer.accelerator.device
if ppo_trainer.accelerator.num_processes == 1:
    device = 0 if torch.cuda.is_available() else "cpu"  # to avoid a `pipeline` bug
sentiment_pipe = pipeline(
    "sentiment-analysis", model="model/distilbert-imdb", device=device
)
```

    Device set to use cuda:0


Mô hình trả về logits (điểm thô trước softmax cho mỗi lớp/token) của lớp tiêu cực và lớp tích cực. Chúng ta sẽ dùng logits của lớp tích cực làm tín hiệu reward cho mô hình ngôn ngữ.


```python
text = "this movie was really bad!!"
sentiment_pipe(text, **sent_kwargs)
```




    [{'label': 'NEGATIVE', 'score': 2.3350484371185303},
     {'label': 'POSITIVE', 'score': -2.726576089859009}]




```python
text = "this movie was really good!!"
sentiment_pipe(text, **sent_kwargs)
```




    [{'label': 'POSITIVE', 'score': 2.557040214538574},
     {'label': 'NEGATIVE', 'score': -2.294790267944336}]



### Thiết lập sinh văn bản  
Để sinh câu trả lời, chúng ta chỉ dùng phương pháp lấy mẫu, đồng thời đảm bảo tắt top-k và nucleus sampling (chỉ lấy mẫu trong nhóm token có tổng xác suất đạt ngưỡng p), và đặt một độ dài tối thiểu.


```python
gen_kwargs = {
    "min_length": -1,
    "top_k": 0.0,
    "top_p": 1.0,
    "do_sample": True,
    "pad_token_id": tokenizer.eos_token_id,
}
```

## Tối ưu hóa mô hình

### Vòng lặp huấn luyện

Vòng lặp huấn luyện gồm các bước chính sau:
1. Lấy câu trả lời cho query từ policy network (GPT-2; policy là quy tắc chọn hành động ở mỗi trạng thái)  
2. Lấy cảm xúc của cặp query/câu trả lời từ BERT  
3. Tối ưu hóa policy bằng PPO, dùng bộ ba (query, câu trả lời, reward)  


```python
output_min_length = 4
output_max_length = 16
output_length_sampler = LengthSampler(output_min_length, output_max_length)


generation_kwargs = {
    "min_length": -1,
    "top_k": 0.0,
    "top_p": 1.0,
    "do_sample": True,
    "pad_token_id": tokenizer.eos_token_id,
}


for epoch, batch in enumerate(tqdm(ppo_trainer.dataloader)):
    query_tensors = batch["input_ids"]

    #### Get response from gpt2
    response_tensors = []
    for query in query_tensors:
        gen_len = output_length_sampler()
        generation_kwargs["max_new_tokens"] = gen_len
        query_response = ppo_trainer.generate(query, **generation_kwargs).squeeze()
        response_len = len(query_response) - len(query)
        response_tensors.append(query_response[-response_len:])
    batch["response"] = [tokenizer.decode(r.squeeze()) for r in response_tensors]

    #### Compute sentiment score
    texts = [q + r for q, r in zip(batch["query"], batch["response"])]
    pipe_outputs = sentiment_pipe(texts, **sent_kwargs)
    positive_scores = [
        item["score"]
        for output in pipe_outputs
        for item in output
        if item["label"] == "POSITIVE"
    ]
    rewards = [torch.tensor(score) for score in positive_scores]

    #### Run PPO step
    stats = ppo_trainer.step(query_tensors, response_tensors, rewards)
    ppo_trainer.log_stats(stats, batch, rewards)
```

      0%|          | 0/194 [00:00<?, ?it/s]The attention mask is not set and cannot be inferred from input because pad token is same as eos token. As a consequence, you may observe unexpected behavior. Please pass your input's `attention_mask` to obtain reliable results.
      4%|▍         | 8/194 [01:23<32:18, 10.42s/it]You seem to be using the pipelines sequentially on GPU. In order to maximize efficiency please use a dataset
    100%|██████████| 194/194 [35:19<00:00, 10.92s/it]


### Tiến trình huấn luyện  
Nếu bạn đang dùng Weights & Biases để theo dõi tiến trình huấn luyện, bạn hẳn sẽ thấy các đường cong tương tự hình dưới đây. Xem báo cáo mẫu dạng tương tác trên wandb.ai: [liên kết](https://wandb.ai/huggingface/trl/runs/w9l3110g).  
<div style="text-align: center">
<img src='figs/gpt2_tuning_progress.png' width='800'>
<p style="text-align: center;"> <b>Hình:</b> Diễn biến của reward trung bình trong quá trình huấn luyện </p>
</div>  
Có thể thấy, sau vài bước tối ưu hóa, mô hình bắt đầu sinh ra đầu ra tích cực hơn.  

## Kiểm tra mô hình  
Hãy xem thử một vài ví dụ từ tập dữ liệu IMDB. Chúng ta có thể dùng `ref_model` để so sánh mô hình sau tối ưu `model` với mô hình trước tối ưu.


```python
#### get a batch from the dataset
bs = 16
game_data = dict()
dataset.set_format("pandas")
df_batch = dataset[:].sample(bs)
game_data["query"] = df_batch["query"].tolist()
query_tensors = df_batch["input_ids"].tolist()

response_tensors_ref, response_tensors = [], []

#### get response from gpt2 and gpt2_ref
for i in range(bs):
    query = torch.tensor(query_tensors[i]).to(device)

    gen_len = output_length_sampler()
    query_response = ref_model.generate(
        query.unsqueeze(0), max_new_tokens=gen_len, **gen_kwargs
    ).squeeze()
    response_len = len(query_response) - len(query)
    response_tensors_ref.append(query_response[-response_len:])

    query_response = model.generate(
        query.unsqueeze(0), max_new_tokens=gen_len, **gen_kwargs
    ).squeeze()
    response_len = len(query_response) - len(query)
    response_tensors.append(query_response[-response_len:])

#### decode responses
game_data["response (before)"] = [
    tokenizer.decode(response_tensors_ref[i]) for i in range(bs)
]
game_data["response (after)"] = [
    tokenizer.decode(response_tensors[i]) for i in range(bs)
]

#### sentiment analysis of query/response pairs before/after
texts = [q + r for q, r in zip(game_data["query"], game_data["response (before)"])]
pipe_outputs = sentiment_pipe(texts, **sent_kwargs)
positive_scores = [
    item["score"]
    for output in pipe_outputs
    for item in output
    if item["label"] == "POSITIVE"
]
game_data["rewards (before)"] = positive_scores

texts = [q + r for q, r in zip(game_data["query"], game_data["response (after)"])]
pipe_outputs = sentiment_pipe(texts, **sent_kwargs)
positive_scores = [
    item["score"]
    for output in pipe_outputs
    for item in output
    if item["label"] == "POSITIVE"
]
game_data["rewards (after)"] = positive_scores

# store results in a dataframe
df_results = pd.DataFrame(game_data)
df_results
```

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>query</th>
      <th>response (before)</th>
      <th>response (after)</th>
      <th>rewards (before)</th>
      <th>rewards (after)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Well I guess I know</td>
      <td>that Cantor may be an</td>
      <td>..but I loved it</td>
      <td>0.230196</td>
      <td>2.281557</td>
    </tr>
    <tr>
      <th>1</th>
      <td>This is an excellent,</td>
      <td>direct-to-video film with typical</td>
      <td>enjoyable movie.&lt;|endoftext|&gt;</td>
      <td>2.846593</td>
      <td>2.840860</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Now, I</td>
      <td>'ve never had the chance with James</td>
      <td>loved the growing episode - and the</td>
      <td>0.656194</td>
      <td>2.525894</td>
    </tr>
    <tr>
      <th>3</th>
      <td>We tend</td>
      <td>not to see Arthur</td>
      <td>to like this very</td>
      <td>-0.280880</td>
      <td>2.183822</td>
    </tr>
    <tr>
      <th>4</th>
      <td>The proverb "Never judge a book</td>
      <td>by the cover" has caught on. After glancing t...</td>
      <td>with high compliments, but it is recommended ...</td>
      <td>0.274649</td>
      <td>2.065951</td>
    </tr>
    <tr>
      <th>5</th>
      <td>I've never understood</td>
      <td>why so many artsmen,</td>
      <td>this film but it's delightful</td>
      <td>0.835574</td>
      <td>2.782384</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Hugh (Ed Harris) is</td>
      <td>an acclaimed "hero" and his fian</td>
      <td>a wonderful actor who is a good adaptation</td>
      <td>1.580167</td>
      <td>2.602940</td>
    </tr>
    <tr>
      <th>7</th>
      <td>This particular Joe McDoakes</td>
      <td>' episode brought all the wrong bits and</td>
      <td>movie is really a great movie. It</td>
      <td>0.870956</td>
      <td>2.795245</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Sisters In</td>
      <td>Vrooms 8.23, I signed up for all of the</td>
      <td>The Universe 1: Sunny is cute, and has a cute...</td>
      <td>1.175259</td>
      <td>2.062330</td>
    </tr>
    <tr>
      <th>9</th>
      <td>I was very fond of this</td>
      <td>film, it was obviously a bad idea when first ...</td>
      <td>show, and know that I have seen it several times</td>
      <td>1.058164</td>
      <td>2.511273</td>
    </tr>
    <tr>
      <th>10</th>
      <td>If he wanted to be</td>
      <td>funny, he could</td>
      <td>a genius eventually,</td>
      <td>-0.388943</td>
      <td>0.405888</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Thats My</td>
      <td>Grade...&lt;br /&gt;&lt;br /&gt;Although</td>
      <td>Way was the best movie that I watched.</td>
      <td>-0.151680</td>
      <td>2.473050</td>
    </tr>
    <tr>
      <th>12</th>
      <td>This is possibly the best short</td>
      <td>film I have come across in almost two years.</td>
      <td>film ever written. It has some very memorable...</td>
      <td>2.511835</td>
      <td>2.775994</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Some people say this is</td>
      <td>exactly what happens in Hollywood; where come...</td>
      <td>a powerful film to listen to. It really captures</td>
      <td>0.637631</td>
      <td>2.821085</td>
    </tr>
    <tr>
      <th>14</th>
      <td>A remake of</td>
      <td>"The Wizard of Oz</td>
      <td>the legendary Kingan oil</td>
      <td>0.292409</td>
      <td>0.434021</td>
    </tr>
    <tr>
      <th>15</th>
      <td>What a terrible</td>
      <td>movie!&lt;|endoftext|&gt;</td>
      <td>chopping sounded so good, I love it! We have a</td>
      <td>-2.681461</td>
      <td>2.340650</td>
    </tr>
  </tbody>
</table>


Khi xem giá trị trung bình/trung vị của reward trên các chuỗi được sinh ra, chúng ta thấy khác biệt rõ rệt.


```python
print("mean:")
display(df_results[["rewards (before)", "rewards (after)"]].mean())
print()
print("median:")
display(df_results[["rewards (before)", "rewards (after)"]].median())
```

    mean:

    rewards (before)    0.591666
    rewards (after)     2.243934
    dtype: float64


​    
    median:

    rewards (before)    0.646912
    rewards (after)     2.492161
    dtype: float64


## Lưu mô hình  
Cuối cùng, chúng ta lưu mô hình để dùng về sau.


```python
model.save_pretrained("model/gpt2-imdb-pos-v2")
tokenizer.save_pretrained("model/gpt2-imdb-pos-v2")
```




    ('model/gpt2-imdb-pos-v2/tokenizer_config.json',
     'model/gpt2-imdb-pos-v2/special_tokens_map.json',
     'model/gpt2-imdb-pos-v2/vocab.json',
     'model/gpt2-imdb-pos-v2/merges.txt',
     'model/gpt2-imdb-pos-v2/added_tokens.json',
     'model/gpt2-imdb-pos-v2/tokenizer.json')

