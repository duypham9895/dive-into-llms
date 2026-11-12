# Fine-tuning và triển khai mô hình ngôn ngữ pre-trained

> Dẫn nhập: phần này giới thiệu fine-tuning (tinh chỉnh một mô hình đã huấn luyện trên dữ liệu của một nhiệm vụ cụ thể) cho mô hình pre-trained (mô hình đã qua huấn luyện ban đầu trên kho dữ liệu rất lớn, chưa gắn với nhiệm vụ cụ thể)
Muốn cải thiện hiệu năng của mô hình pre-trained trên một tác vụ cụ thể? Hãy chọn một mô hình pre-trained phù hợp, fine-tune nó trên tác vụ đó, rồi triển khai mô hình đã fine-tune thành một demo (bản chạy thử minh họa) tiện dùng!
## Mục tiêu của bài hướng dẫn này:
1. Làm quen với bộ công cụ Transformers
2. Nắm vững fine-tuning và inference (chạy mô hình đã huấn luyện để sinh đầu ra) với mô hình pre-trained (phiên bản tách rời, tùy biến được & phiên bản tích hợp mặc định)
3. Nắm vững cách triển khai demo bằng Gradio Spaces
4. Hiểu cách chọn giữa các loại mô hình pre-trained khác nhau và tình huống ứng dụng của từng loại
## Nội dung của bài hướng dẫn này:
### 1. Chuẩn bị:
#### 1.1 Tìm hiểu bộ công cụ: Transformers
https://github.com/huggingface/transformers

> 🤗 Transformers cung cấp API (giao diện lập trình ứng dụng) và công cụ để dễ dàng tải về và huấn luyện các mô hình pre-trained tiên tiến. Dùng mô hình pre-trained giúp giảm chi phí tính toán và lượng khí thải carbon, đồng thời tiết kiệm thời gian và tài nguyên cần để huấn luyện từ đầu. Các mô hình này hỗ trợ những tác vụ phổ biến ở nhiều modality (loại dữ liệu: văn bản, ảnh, âm thanh, video) khác nhau, chẳng hạn:
📝 Xử lý ngôn ngữ tự nhiên (NLP): phân loại văn bản, nhận dạng thực thể có tên (NER), hỏi đáp, mô hình hóa ngôn ngữ, tóm tắt, dịch máy, trắc nghiệm nhiều lựa chọn và sinh văn bản.
🖼️ Thị giác máy tính: phân loại ảnh, phát hiện đối tượng và phân đoạn ngữ nghĩa.
🗣️ Âm thanh: nhận dạng giọng nói tự động và phân loại âm thanh.
🐙 Multimodal (xử lý nhiều modality cùng lúc): hỏi đáp trên bảng, nhận dạng ký tự quang học, trích xuất thông tin từ tài liệu scan, phân loại video và hỏi đáp về hình ảnh.

Tài liệu tiếng Trung chi tiết: https://huggingface.co/docs/transformers/main/zh/index

![huggingface](./assets/huggingface.PNG)

#### 1.2 Cài đặt môi trường: lấy phân loại văn bản (e.g., phát hiện tin giả) làm ví dụ
1. Vào kho ví dụ về phân loại văn bản, đọc readme để nắm các tham số chính, rồi tải về requirements.txt và run_classification.py

https://github.com/huggingface/transformers/tree/main/examples/pytorch/text-classification

2. Cài đặt môi trường:
- 1. Tạo môi trường mới bằng conda: conda create -n llm python=3.9
- 2. Vào môi trường ảo: conda activate llm
- 3. pip install transformers
- 4. Xóa torch (gói được cài tự động) khỏi requirements.txt, rồi pip install -r requirements.txt

> Nếu tải chậm, có thể dùng mirror (máy chủ sao chép để tải nhanh hơn trong Trung Quốc): pip [Packages] -i https://pypi.tuna.tsinghua.edu.cn/simple

> Nếu cài pytorch từ mirror tại Trung Quốc đại lục, bản cpu của pytorch sẽ được chọn tự động và không chạy được trên gpu, vì vậy:

- 5. conda install pytorch

> Nếu tải chậm, có thể cấu hình mirror cho conda theo blog này: https://blog.csdn.net/weixin_42797483/article/details/132048218

3. Chuẩn bị dữ liệu: ta lấy tập dữ liệu tweet giả trên Kaggle làm ví dụ: https://www.kaggle.com/c/nlp-getting-started/data

#### 1.3 Gói dự án đã xử lý sẵn (code demo và dữ liệu)
(1) Phiên bản tách rời, tùy biến được (các module chính được tách riêng cho dễ hiểu; có thể tự định nghĩa cách nạp dữ liệu, kiến trúc mô hình, chỉ số đánh giá, v.v.)

[Link tải TextClassificationCustom](https://pan.quark.cn/s/00dae5c2b128)

(2) Phiên bản tích hợp mặc định (code phong phú và phức tạp hơn, thường gọi trực tiếp qua siêu tham số, đòi hỏi một chút kinh nghiệm phát triển)

[Link tải TextClassification](https://pan.quark.cn/s/9d0510f1c98d)


### 2. Phát triển tùy biến trên phiên bản tách rời (sản phẩm khả thi tối thiểu, MVP)
Gồm ba file chính: main.py là chương trình chính, utils_data.py lo việc nạp và xử lý dữ liệu, modeling_bert.py định nghĩa kiến trúc mô hình

![project structure](./assets/0.png)

#### 2.1 Hiểu các module chính
1. Nạp và xử lý dữ liệu (utils_data.py)
![utils_data.py](./assets/1.png)

2. Nạp mô hình (modeling_bert.py)

![modeling_bert_1.py](./assets/2.png)

![modeling_bert_2.py](./assets/3.png)


3. Huấn luyện/kiểm định (validation)/dự đoán (main.py)

![main.py](./assets/4.png)

#### 2.2 Chạy trọn gói huấn luyện/kiểm định/dự đoán
```shell
python main.py
```

### 3. Fine-tuning trên phiên bản tích hợp (tùy chọn, dựa trên run_classification.py)

#### 3.1 Hiểu các module chính:
1. Nạp dữ liệu (định dạng csv hoặc json)
![load data](./assets/5.png)

2. Xử lý dữ liệu
![process data](./assets/6.png)

3. Nạp mô hình
![load model](./assets/7.png)

4. Huấn luyện/kiểm định/dự đoán
![train dev predict](./assets/8.png)

#### 3.2 Huấn luyện mô hình
Huấn luyện, đồng thời kiểm định trên tập phát triển (dev set) và dự đoán trên tập kiểm tra; chạy script (tệp lệnh chạy được) dưới đây:

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

Nếu gặp lỗi hoặc bị treo, thường là do vấn đề mạng:

1. <u>Nếu khi tải mô hình báo “Network is unreachable”, hãy tải mô hình về máy thủ công: https://huggingface.co/google-bert/bert-base-uncased</u>
2. <u>Nếu bị treo sau khi nạp xong dữ liệu, và sau khi dừng bằng CTRL+C thấy báo kẹt ở “connection”, thì nguyên nhân là kết nối mạng thất bại khi gói evaluate tải chỉ số đánh giá.</u>

![bug](./assets/9.png)

Khi đó, có thể tải toàn bộ gói từ GitHub của evaluate: https://github.com/huggingface/evaluate/tree/main, rồi trong siêu tham số đổi đường dẫn --metric_name thành đường dẫn tới chỉ số trên máy, tức là:

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


### 4. Triển khai mô hình: sau khi huấn luyện xong, ta có thể dựng demo trực tuyến trên Gradio Spaces
#### 4.1 Bài hướng dẫn Gradio Spaces
https://huggingface.co/docs/hub/en/spaces-sdks-gradio
#### 4.2 Tạo Space
1. https://huggingface.co/new-space?sdk=gradio
2. Note: nếu không mở được, hãy thử dùng VPN hoặc proxy (cần khi truy cập từ Trung Quốc đại lục)

![Gradio Spaces](./assets/gradio.png)

#### 4.3 Code inference chính
Chi tiết xem app.py trong gói dự án

![app.py](./assets/11.png)

#### 4.4 Tải app.py, file cấu hình môi trường và mô hình lên Gradio Spaces
1. File cấu hình (requirements.txt)
```
transformers==4.30.2
torch==2.0.0
```

2. Tổng quan các file

![file overview](./assets/12.png)


3. Kết quả Demo
Ví dụ đã triển khai thành công để tham khảo: https://huggingface.co/spaces/cooelf/text-classification
Có thể xem mã nguồn ở mục “Files” góc trên bên phải.

![Files](./assets/13.png)


4. Mẹo bonus: trên nền tảng Spaces có thể xem các Demo nổi bật mỗi tuần, cũng có thể tìm các mô hình lớn, Demo mà bạn quan tâm để dùng thử
![Spaces](./assets/14.png)


### 5. Bài tập nâng cao
1. Thử các tác vụ phân loại/hồi quy khác, ví dụ phân loại cảm xúc, phân loại tin tức, phân loại lỗ hổng bảo mật, v.v.
2. Thử các loại mô hình khác, ví dụ T5, ELECTRA, v.v.
### 6. Các mô hình thường dùng khác
1. Mô hình hỏi đáp: https://github.com/huggingface/transformers/tree/main/examples/pytorch/question-answering
2. Tóm tắt văn bản: https://github.com/huggingface/transformers/tree/main/examples/pytorch/summarization
3. Gọi Llama2 để chạy inference: https://huggingface.co/docs/transformers/en/model_doc/llama2
4. Parameter-efficient fine-tuning (lightweight fine-tuning; fine-tuning chỉ cập nhật một phần nhỏ tham số) cho Llama2 (LoRA):  https://github.com/peremartra/Large-Language-Model-Notebooks-Course/blob/main/5-Fine%20Tuning/LoRA_Tuning_PEFT.ipynb


### 7. Đọc thêm
1. Một [bài tổng quan](https://mp.weixin.qq.com/s?__biz=Mzk0MTYzMzMxMA==&mid=2247484539&idx=1&sn=6ee42baab4ad792e74ac6a89d7dd87d9) dài 43 trang phân tích toàn diện, sâu sắc về mô hình ngôn ngữ lớn (LLMs) (do tác giả của Word2Vec thực hiện)
   
    Tên bài báo: Large Language Models: A Survey

    Link bài báo: https://arxiv.org/pdf/2402.06196.pdf

2. [Đọc kỹ bài báo GPT, GPT-2, GPT-3 (Đọc kỹ bài báo)](https://www.bilibili.com/video/BV1AF411b7xQ?t=0.0)

3. [Đọc kỹ bài báo InstructGPT (Đọc kỹ bài báo · 48)](https://www.bilibili.com/video/BV1hd4y187CR?t=0.4)
