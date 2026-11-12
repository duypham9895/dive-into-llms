# 动手学大模型 (Dive into LLMs): Multimodal large language model

Dẫn nhập: phần này giới thiệu các kiến trúc phổ biến của multimodal large language model (MLLM; LLM được gắn thêm khả năng hiểu/sinh ảnh, âm thanh, video) và cách xây dựng chúng

> Sự xuất hiện của mô hình ngôn ngữ lớn (LLM) cho mọi người thấy trí tuệ bậc cao đã được thể hiện đầy đủ ở modality (loại dữ liệu: văn bản, ảnh, âm thanh, video) ngôn ngữ. Là loại mô hình có thể mô phỏng thế giới thực đầy đủ hơn, MLLM làm thế nào để đạt được năng lực hiểu và sinh multimodal (xử lý nhiều modality cùng lúc) mạnh hơn? MLLM có giúp hiện thực hóa AGI (artificial general intelligence; AI có năng lực tổng quát ngang con người) hay không?


## Mục tiêu của bài hướng dẫn này

1. Làm quen với các loại MLLM
2. Nắm vững khung kỹ thuật chung của MLLM
3. Nắm vững cách xây dựng, huấn luyện và chạy inference (chạy mô hình đã huấn luyện để sinh đầu ra) với MLLM



## 1. Chuẩn bị kiến thức lý thuyết



### 1.1 Tìm hiểu các loại MLLM

- Phân loại các MLLM hiện có theo chức năng và modality được hỗ trợ


> Trước khi xây dựng MLLM (multimodal large language model), các nhà nghiên cứu trong lĩnh vực này đều đạt được một đồng thuận, cũng là một tiền đề then chốt: nhờ scaling law (quy luật hiệu năng tăng theo kích thước mô hình, dữ liệu và compute) và emergent phenomena (các hiện tượng chỉ xuất hiện khi mô hình đủ lớn), các LLM dựa trên ngôn ngữ hiện nay đã có năng lực hiểu ngữ nghĩa mạnh mẽ, nghĩa là ngôn ngữ đã trở thành modality then chốt mang trí tuệ, nên trí tuệ ngôn ngữ được xem là trung tâm của trí tuệ multimodal. Vì vậy, gần như mọi MLLM đều được xây dựng trên nền LLM dựa trên ngôn ngữ, với LLM làm mô-đun ra quyết định cốt lõi, giống như bộ não hay bộ xử lý trung tâm. Nói cách khác, bằng cách thêm các mô-đun hoặc encoder (khối biến đầu vào thành biểu diễn vector) bên ngoài cho các modality phi văn bản, LLM được trao năng lực cảm nhận/thao tác multimodal.

Chúng tôi chia các MLLM hiện có thành nhiều loại khác nhau theo modality và chức năng mà chúng hỗ trợ.

![mllm](assets/MLLM-summary.png)


- Đọc toàn bộ bài hướng dẫn: [[Slides](https://github.com/Lordog/dive-into-llms/blob/main/documents/chapter6/mllms.pdf)]


- Các bài tổng quan liên quan khác
    - [A Survey on Multimodal Large Language Models, https://github.com/BradyFU/Awesome-Multimodal-Large-Language-Models, 2023](https://github.com/BradyFU/Awesome-Multimodal-Large-Language-Models)
    - [MM-LLMs: Recent Advances in MultiModal Large Language Models, 2023](https://arxiv.org/pdf/2401.13601)


### 1.2 Tìm hiểu khung kỹ thuật chung của MLLM


- Kiến trúc 1: LLM as Task Scheduler

> Hiện nay cộng đồng có hai kiến trúc MLLM phổ biến.
Thứ nhất là kiến trúc “LLM làm bộ điều phối/bộ điều khiển rời rạc”. Như hình dưới đây, vai trò của LLM là nhận tín hiệu văn bản và phát lệnh dạng văn bản cho các mô-đun phía sau. Mọi việc truyền thông điệp bên trong hệ thống đều lấy các lệnh văn bản thuần do LLM xuất ra làm trung gian. Giữa các mô-đun chức năng khác nhau không có tương tác nào.


![Architecture1](assets/Architecture1.png)

- Kiến trúc 2: LLM as Joint Part of System

> Kiến trúc thứ hai là khung encoder-LLM-decoder (decoder: khối sinh đầu ra từ biểu diễn).
Đây cũng là kiến trúc phổ biến nhất hiện nay. Trong đó, vai trò của LLM là cảm nhận thông tin multimodal và tự đưa ra phản hồi, thao tác trong một cấu trúc encoder-LLM-decoder. Vì vậy, điểm khác biệt then chốt giữa kiến trúc này và kiến trúc thứ nhất là: LLM là một phần kết hợp then chốt của hệ thống, trực tiếp nhận thông tin multimodal từ bên ngoài và giao instruction (yêu cầu/chỉ dẫn bằng ngôn ngữ tự nhiên giao cho mô hình) cho decoder/bộ sinh một cách trơn tru hơn. Trong khung encoder-LLM-decoder, như hình dưới đây, encoder xử lý tín hiệu đã mã hóa từ nhiều modality, LLM đóng vai trò bộ ra quyết định cốt lõi, còn decoder quản lý đầu ra multimodal.

![Architecture2](assets/Architecture2.png)





## 2. Thực hành với MLLM đa năng

> Thực hành quy trình xây dựng một MLLM đa năng “any-to-any” (từ modality bất kỳ sang modality bất kỳ)


### 2.1 MLLM “any-to-any modality” đa năng, thống nhất: NExT-GPT

> Nghiên cứu MLLM trong tương lai chắc chắn sẽ phát triển theo hướng generalist ngày càng đa năng, nên sẽ bao gồm càng nhiều modality và chức năng càng tốt. NExT-GPT là một trong những công trình tiên phong nhất trong lĩnh vực này hiện nay, lần đầu tiên đưa ra khái niệm MLLM “any-to-any”. Kiến trúc này đạt được những chức năng mạnh mẽ, đặt nền móng cho hướng nghiên cứu MLLM trong tương lai.

![NExT-GPT](assets/NExT-GPT-screen.png)


> Phần thực hành code về MLLM của buổi học này sẽ lấy code của NExT-GPT làm đối tượng, phân tích và thực hành theo cách dễ hiểu mà vẫn đi sâu.

[NExT-GPT Project](https://next-gpt.github.io/)

[Kho mã (repository) GitHub của NExT-GPT](https://github.com/NExT-GPT/NExT-GPT)




### 2.2 Tổng quan cấu trúc code


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


### 2.3 Cài đặt môi trường

Trước tiên, hãy clone kho mã và cài đặt môi trường cần thiết; có thể chạy các lệnh sau để hoàn tất việc cài đặt môi trường:

```
conda env create -n nextgpt python=3.8

conda activate nextgpt

# CUDA 11.6
conda install pytorch==1.13.1 torchvision==0.14.1 torchaudio==0.13.1 pytorch-cuda=11.6 -c pytorch -c nvidia

git clone https://github.com/NExT-GPT/NExT-GPT.git
cd NExT-GPT

pip install -r requirements.txt
```




### 2.4 Bắt đầu chạy inference với hệ thống


#### 2.4.1 Tải checkpoint của mô hình NExT-GPT đã qua pre-training

- **Bước 1**: tải `tham số đóng băng`. [NExT-GPT](https://github.com/NExT-GPT/NExT-GPT) được huấn luyện dựa trên các mô hình hoặc mô-đun có sẵn dưới đây; hãy làm theo hướng dẫn sau để chuẩn bị checkpoint (bản lưu trọng số mô hình tại một thời điểm huấn luyện).
    - `ImageBind` là encoder thống nhất cho ảnh/video/âm thanh. Có thể tải checkpoint pre-trained (đã qua pre-training: huấn luyện ban đầu trên kho dữ liệu rất lớn, chưa gắn với nhiệm vụ cụ thể) từ [đây](https://dl.fbaipublicfiles.com/imagebind/imagebind_huge.pth), phiên bản `huge`. Sau đó, đặt tệp `imagebind_huge.pth` vào [[./ckpt/pretrained_ckpt/imagebind_ckpt/huge]](ckpt/pretrained_ckpt/imagebind_ckpt/).
    - `Vicuna`: trước tiên chuẩn bị LLaMA theo hướng dẫn [[tại đây]](ckpt/pretrained_ckpt/prepare_vicuna.md). Sau đó đặt mô hình pre-trained vào [[./ckpt/pretrained_ckpt/vicuna_ckpt/]](ckpt/pretrained_ckpt/vicuna_ckpt/).
    - `Image Diffusion` dùng để sinh ảnh. NExT-GPT dùng phiên bản `v1-5` của [Stable Diffusion](https://huggingface.co/runwayml/stable-diffusion-v1-5). (_code sẽ tự động tải về_)
    - `Audio Diffusion` dùng để sinh nội dung âm thanh. NExT-GPT dùng phiên bản `l-full` của [AudioLDM](https://github.com/haoheliu/AudioLDM). (_code sẽ tự động tải về_)
    - `Video Diffusion` dùng để sinh video. Chúng tôi dùng phiên bản `v2_576w` của [ZeroScope](https://huggingface.co/cerspense/zeroscope_v2_576w). (_code sẽ tự động tải về_)

- **Bước 2**: tải `tham số huấn luyện được`.

Đặt hệ thống NExT-GPT vào [[./ckpt/delta_ckpt/nextgpt/7b_tiva_v0]](./ckpt/delta_ckpt/nextgpt/7b_tiva_v0). Có thể chọn 1) dùng tham số do chính bạn huấn luyện, hoặc 2) tải checkpoint đã qua pre-training từ [Huggingface](https://huggingface.co/ChocoWu/nextgpt_7b_tiva_v0).


#### 2.4.2 Triển khai demo Gradio

Sau khi tải xong checkpoint, bạn có thể chạy demo (bản chạy thử minh họa) trên máy cục bộ như sau:
```angular2html
cd ./code
bash scripts/app.sh
```
Các tham số chính cần chỉ định như sau:
- `--nextgpt_ckpt_path`: đường dẫn tới tham số NExT-GPT đã qua pre-training.



#### 2.4.3 Thực hành với các ví dụ thử nghiệm

Phiên bản hiện tại hỗ trợ đầu vào là tổ hợp bất kỳ của bốn modality văn bản, ảnh, video và âm thanh, cũng như đầu ra ở tổ hợp modality bất kỳ.
Ngoài ra còn hỗ trợ tương tác nhiều lượt có ngữ cảnh.

Mọi người hãy tự chạy để kiểm tra kết quả.

- **Case-1**: đầu vào T+I, đầu ra T+A

![case1](assets/T+I-T+A.png)


- **Case-2**: đầu vào T+V, đầu ra T+A

![case2](assets/T+V-T+A.png)


- **Case-3**: đầu vào T+I, đầu ra T+I+V

![case3](assets/T+I-T+I+V.png)


- **Case-4**: đầu vào T, đầu ra T+I+V+A

![case4](assets/T-T+I+V+A.png)







### 2.5 Quy trình huấn luyện hệ thống


#### 2.5.1 Chuẩn bị dữ liệu

Hãy tải các tập dữ liệu sau để huấn luyện mô hình:

A) Dữ liệu cặp T-X
  - Dữ liệu `CC3M` gồm các cặp ***văn bản-ảnh***: làm theo hướng dẫn này [[here]](./data/T-X_pair_data/cc3m/prepare.md). Sau đó đặt dữ liệu vào [[./data/T-X_pair_data/cc3m]](./data/T-X_pair_data/cc3m).
  - Dữ liệu `WebVid` gồm các cặp ***văn bản-video***: xem [[instruction]](./data/T-X_pair_data/webvid/prepare.md). Tệp cần được lưu tại [[./data/T-X_pair_data/webvid]](./data/T-X_pair_data/webvid).
  - Dữ liệu `AudioCap` gồm các cặp ***văn bản-âm thanh***: xem [[instruction]](./data/T-X_pair_data/audiocap/prepare.md). Lưu dữ liệu tại [[./data/T-X_pair_data/audiocap]](./data/T-X_pair_data/audiocap).

B) Dữ liệu instruction tuning (fine-tuning trên các cặp instruction–câu trả lời để mô hình biết làm theo yêu cầu)
  - T+X-T
    - ***Dữ liệu instruction thị giác*** (from `LLaVA`): tải từ [đây](https://github.com/haotian-liu/LLaVA/blob/main/docs/Data.md) và đặt vào [[./data/IT_data/T+X-T_data/llava]](./data/IT_data/T+X-T_data/llava/).
    - ***Dữ liệu instruction dạng văn bản*** (from `Alpaca`): tải từ [đây](https://github.com/tatsu-lab/stanford_alpaca) và đặt vào [[./data/IT_data/T+X-T_data/alpaca/]](data/IT_data/T+X-T_data/alpaca/).
    - ***Dữ liệu instruction dạng video*** (from `VideoChat`): tải từ [đây](https://github.com/OpenGVLab/InternVideo/tree/main/Data/instruction_data) và đặt vào [[./data/IT_data/T+X-T_data/videochat/]](data/IT_data/T+X-T_data/videochat/).

    Lưu ý: sau khi tải tập dữ liệu, hãy chạy `preprocess_dataset.py` để tiền xử lý, đưa về cùng một định dạng.
  - T-X+T (T2M)
    - Tập dữ liệu instruction `T-X+T` (T2M) được lưu tại [[./data/IT_data/T-T+X_data]](./data/IT_data/T-T+X_data).
   
  - MosIT
    - Xem hướng dẫn tải dữ liệu [tại đây](./data/IT_data/MosIT_data/). Cuối cùng đặt dữ liệu vào [[./data/IT_data/MosIT_data/]](./data/IT_data/MosIT_data/).




#### 2.5.2 Chuẩn bị embedding

Trong huấn luyện alignment (căn chỉnh biểu diễn của các modality với LLM) phía decoder của NExT-GPT, chúng tôi tối thiểu hóa khoảng cách giữa biểu diễn của Signal Token (token đặc biệt LLM sinh ra để kích hoạt bộ giải mã modality) và biểu diễn của captions (chú thích mô tả). Để hệ thống đạt hiệu quả cao, tiết kiệm thời gian và chi phí bộ nhớ, chúng tôi dùng text encoder trong từng diffusion model (mô hình sinh ảnh/âm thanh/video bằng cách khử nhiễu dần) để tính trước embedding (vector số biểu diễn ý nghĩa của văn bản/ảnh/âm thanh) văn bản của caption ảnh, âm thanh và video.

Trước khi huấn luyện NExT-GPT, hãy chạy lệnh sau; tệp `embedding` được sinh ra sẽ lưu tại [[./data/embed]](./data/embed).
```
cd ./code/
python process_embeddings.py ../data/T-X_pair_data/cc3m/cc3m.json image ../data/embed/ runwayml/stable-diffusion-v1-5
```


Giải thích tham số:
- args[1]: đường dẫn tệp caption;
- args[2]: modality, có thể là `image`, `video` hoặc `audio`;
- args[3]: đường dẫn lưu tệp embedding;
- args[4]: tên của diffusion model đã qua pre-training tương ứng.




#### 2.5.3 Huấn luyện ba giai đoạn


Trước tiên, tham khảo tệp cấu hình cơ sở [[./code/config/base.yaml]](./code/config/base.yaml) để nắm các thiết lập hệ thống cơ bản của toàn bộ mô-đun.

Sau đó chạy script (tệp lệnh chạy được) sau để bắt đầu huấn luyện NExT-GPT:
```
cd ./code
bash scripts/train.sh
```

Lệnh cụ thể như sau:
```
deepspeed --include localhost:0 --master_addr 127.0.0.1 --master_port 28459 train.py \
    --model nextgpt \
    --stage 1\
    --save_path  ../ckpt/delta_ckpt/nextgpt/7b_tiva_v0/\
    --log_path ../ckpt/delta_ckpt/nextgpt/7b_tiva_v0/log/
```
Trong đó, các tham số chính:
- `--include`: `localhost:0` nghĩa là CUDA device `0` được DeepSpeed sử dụng (ghi chú người dịch: bản gốc ghi “GPT cuda”).
- `--stage`: giai đoạn huấn luyện.
- `--save_path`: thư mục lưu trọng số delta sau khi huấn luyện. Thư mục này sẽ được tạo tự động.
- `--log_path`: thư mục lưu tệp log.



Toàn bộ quá trình huấn luyện NExT-GPT chia thành 3 bước:

- **Bước 1**: alignment multimodal lấy LLM làm trung tâm ở phía encoder. Giai đoạn này huấn luyện ***input projection layer*** (lớp biến đổi biểu diễn của modality sang không gian của LLM), đồng thời đóng băng ImageBind, LLM và output projection layer.
  
  Chỉ cần chạy script `train.sh` ở trên và đặt: `--stage 1`
  
  Xem thêm tệp cấu hình chạy [[./code/config/stage_1.yaml]](./code/config/stage_1.yaml) và tệp cấu hình DeepSpeed [[./code/dsconfig/stage_1.yaml]](./code/dsconfig/stage_1.yaml) để biết thêm thông tin cấu hình chi tiết cho từng bước.

  Lưu ý: các tập dữ liệu dùng ở bước này nằm trong `dataset_name_list`, và tên tập dữ liệu phải khớp chính xác với định nghĩa trong [[./code/dataset/catalog.py]](./code/dataset/catalog.py).



- **Bước 2**: alignment instruction following (khả năng làm đúng theo instruction) ở phía decoder. Giai đoạn này huấn luyện ***output projection layer***, đồng thời đóng băng ImageBind, LLM và input projection layer.

  Chỉ cần chạy script `train.sh` ở trên và đặt: `--stage 2`

  Xem thêm tệp cấu hình chạy [[./code/config/stage_2.yaml]](./code/config/stage_2.yaml) và tệp cấu hình DeepSpeed [[./code/dsconfig/stage_2.yaml]](./code/dsconfig/stage_2.yaml) để biết thêm thông tin cấu hình chi tiết cho từng bước.



- **Bước 3**: instruction tuning. Giai đoạn này điều chỉnh những phần sau trên tập dữ liệu instruction: 1) điều chỉnh ***LLM*** qua LoRA, 2) điều chỉnh ***input projection layer*** và 3) điều chỉnh ***output projection layer***.

  Chỉ cần chạy script `train.sh` ở trên và đặt: `--stage 3`

  Xem thêm tệp cấu hình chạy [[./code/config/stage_3.yaml]](./code/config/stage_3.yaml) và tệp cấu hình DeepSpeed [[./code/dsconfig/stage_3.yaml]](./code/dsconfig/stage_3.yaml) để biết thêm thông tin cấu hình chi tiết cho từng bước.
