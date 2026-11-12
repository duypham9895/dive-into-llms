# 动手学大模型 (Dive into LLMs): Knowledge editing cho mô hình lớn
Dẫn nhập: các phương pháp và công cụ chỉnh sửa mô hình ngôn ngữ
> Muốn điều khiển những gì mô hình ngôn ngữ ghi nhớ về một mẩu tri thức cụ thể? Hãy chọn phương pháp editing (chỉnh sửa tri thức đã lưu trong mô hình) phù hợp, chỉnh sửa mẩu tri thức đó, rồi kiểm chứng mô hình sau khi chỉnh sửa!

## 1. Mục tiêu của bài hướng dẫn này:

- Làm quen với bộ công cụ EasyEdit
- Nắm vững phương pháp editing mô hình ngôn ngữ (bản tối giản)
- Hiểu cách chọn các loại phương pháp editing khác nhau và tình huống ứng dụng của từng loại

## 2. Chuẩn bị:
### 2.1 Tìm hiểu EasyEdit

https://github.com/zjunlp/EasyEdit

EasyEdit là một gói Python dùng để chỉnh sửa mô hình ngôn ngữ, như GPT-J, Llama, GPT-NEO, GPT2, T5, v.v. Mục tiêu của nó là thay đổi hiệu quả hành vi của mô hình ngôn ngữ đối với một mẩu tri thức cụ thể mà không ảnh hưởng xấu đến hiệu năng trên các đầu vào khác, đồng thời dễ dùng và dễ mở rộng.

EasyEdit tích hợp các phương pháp editing phổ biến hiện có:
![](./assets/1.png)

### 2.2 Khung chính

![](./assets/2.png)
EasyEdit gồm một khung thống nhất với Editor, Method và Evaluate, lần lượt đại diện cho kịch bản chỉnh sửa, kỹ thuật chỉnh sửa và phương pháp đánh giá.
- Editor: mô tả kịch bản làm việc, gồm mô hình cần chỉnh sửa, tri thức cần chỉnh sửa và các siêu tham số cần thiết khác.
- Method: phương pháp knowledge editing (sửa một mẩu tri thức cụ thể trong mô hình mà không huấn luyện lại toàn bộ) cụ thể được dùng (ví dụ ROME, MEND, v.v.).
- Evaluate: các chỉ số đánh giá hiệu quả knowledge editing, gồm Reliability (độ tin cậy: bản sửa có đúng trên chính câu đã sửa), Generalization (mức bản sửa áp dụng cho các câu hỏi diễn đạt khác), Locality (mức bản sửa không làm hỏng các tri thức không liên quan) và Portability (mức bản sửa lan sang các suy luận liên quan).
- Trainer: một số phương pháp editing cần một quá trình huấn luyện nhất định, phần này do module Trainer đảm nhận.
## 3. Cài đặt môi trường:
```
git clone https://github.com/zjunlp/EasyEdit.git
(Tùy chọn) conda create -n EasyEdit python=3.9.7
cd EasyEdit
pip install -r requirements.txt
```
## 4. Ví dụ chỉnh sửa
> Mục tiêu: thay đổi tri thức mà GPT-2-XL ghi nhớ, đổi nghề nghiệp của Lionel Messi từ bóng đá sang bóng rổ (football->basketball).
Các bước:
- Chọn phương pháp editing, chuẩn bị tham số
- Chuẩn bị dữ liệu cho knowledge editing
- Khởi tạo Editor
- Run!
Dưới đây trình bày chi tiết, lấy phương pháp ROME làm ví dụ:
### 4.1 ROME
Jupiter Notebook: [https://colab.research.google.com/drive/1KkyWqyV3BjXCWfdrrgbR-QS3AAokVZbr?usp=sharing#scrollTo=zWfGkNb9FBJQ] 
- Chọn phương pháp editing, chuẩn bị tham số
  - Chọn ROME làm phương pháp editing, chuẩn bị các tham số mà ROME và GPT2-XL cần.
  - Ví dụ: alg_name: "ROME", model_name: "./hugging_cache/gpt2-xl" hoặc đường dẫn cục bộ tới mô hình này, "device": số hiệu GPU được dùng
  - Các tham số còn lại có thể để mặc định
![](./assets/3.png)
- Chuẩn bị dữ liệu cho knowledge editing
    ```
    prompts = ['Question:What sport does Lionel Messi play? Answer:'] # x_e
    ground_truth = ['football'] # y
    target_new = ['basketball'] # y_e
    subject = ['Lionel Messi'] 
    ```
- Khởi tạo Editor: truyền các tham số đã chuẩn bị vào lớp BaseEditor để khởi tạo, nhận về một đối tượng Editor tùy biến.
    ```
    hparams = ROMEHyperParams.from_hparams('./hparams/ROME/gpt2-xl.yaml')
    editor=BaseEditor.from_hparams(hparams)
    ```
- Run! Gọi phương thức edit của editor:
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
> Ghi chú: khi chỉnh sửa một mô hình lần đầu, kho ngữ liệu Wiki sẽ được tải về, trạng thái của từng lớp được tính cho mô hình đó (stats_dir: "./data/stats") và lưu lại để dùng lại ở mọi lần chỉnh sửa sau. Vì vậy lần chỉnh sửa đầu tiên sẽ mất thời gian; hãy đảm bảo kết nối mạng thông suốt và kiên nhẫn chờ.
### 4.2 Kiểm chứng và đánh giá
editor.edit trả về metrics (do module Evaluate của EasyEdit tính), có dạng:
![](./assets/5.png)
Để có giá trị Generalization, Locality và Portability, cần truyền dữ liệu dùng để đánh giá vào phương thức edit.

Lấy Locality làm ví dụ: việc này khiến phương thức edit tính chỉ số Locality, tức độ chính xác câu trả lời của mô hình trên locality_inputs.
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
Hoặc so sánh trực tiếp hành vi generte của mô hình trước và sau khi chỉnh sửa.
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
## 5. Chỉnh sửa quy mô lớn (tùy chọn)
### 5.1 Batch edit
Nhiều mẩu dữ liệu có thể được xếp thành các danh sách song song và truyền cùng lúc vào phương thức edit để batch edit (chỉnh sửa hàng loạt trong một lần gọi); khi đó MEMIT là phương pháp tốt nhất. (https://colab.research.google.com/drive/1P1lVklP8bTyh8uxxSuHnHwB91i-1LW6Z)
```
prompts = ['Question:What sport does Lionel Messi play? Answer:',
            'The law in Ikaalinen declares the language']
ground_truth = ['football', 'Finnish']
target_new = ['basketball', 'Swedish']
subject = ['Lionel Messi', 'Ikaalinen']
```
### 5.2 Kiểm thử trên benchmark
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
