# Giới thiệu ngắn về Multimodal LLM

[PDF gốc](https://github.com/Lordog/dive-into-llms/blob/f84c04268794ef94f8949808bbc14ab8636763a0/documents/chapter8/mllms.pdf)

## Slide 1

**Giới thiệu ngắn về Multimodal LLM** (multimodal: xử lý nhiều modality cùng lúc; LLM: mô hình ngôn ngữ lớn)

- Hao Fei
- Nghiên cứu viên (Research Fellow)
- National University of Singapore
- <http://haofei.vip/>

Theo dõi loạt bài hướng dẫn về MLLM (multimodal large language model: LLM được gắn thêm khả năng hiểu/sinh ảnh, âm thanh, video): <https://mllm2024.github.io/COLING2024>

## Slide 2

**Mục lục**

- 1 Modality (loại dữ liệu: văn bản, ảnh, âm thanh, video)
    - Tổng quan
    - Hiểu dữ liệu multimodal
    - Hiểu + sinh dữ liệu multimodal
    - MLLM hợp nhất
    - MLLM fine-grained (mức chi tiết cao)
- 2 Kiến trúc
    - Tổng quan
    - Mã hóa multimodal
    - Tokenization (chuyển tín hiệu thành chuỗi token (đơn vị nhỏ nhất mà mô hình đọc và sinh))
    - Projection (phép chiếu) phía đầu vào
    - LLM nền (backbone)
    - Kết nối phía giải mã
    - Sinh dữ liệu multimodal

## Slide 3

**Trí tuệ trong dữ liệu đa giác quan**

- Xu hướng của MLLM

_Tài liệu:_

- [1] MM-LLMs: Recent Advances in MultiModal Large Language Models, 2023.

## Slide 4

**Trí tuệ trong dữ liệu đa giác quan**

- Xu hướng của MLLM

_Tài liệu:_

- [1] A Survey on Multimodal Large Language Models. <https://github.com/BradyFU/Awesome-Multimodal-Large-Language-Models>, 2023.

## Slide 5

**1 Modality và chức năng**

MLLM làm được những gì?

## Slide 6

**Tổng quan về modality và chức năng**

- Các modality
    - Ngôn ngữ + thị giác

## Slide 7

**Tổng quan về modality và chức năng**

- Toàn cảnh MLLM, theo modality (đi kèm ngôn ngữ): Image · Video · Audio · 3D
- Hiểu ở phía đầu vào (Input-side Perceiving):
    - Image: Flamingo, Kosmos-1, Blip2, mPLUG-Owl, Mini-GPT4, LLaVA, InstructBLIP, VPGTrans, CogVLM, Monkey, Chameleon, Otter, Qwen-VL, GPT-4v, SPHINX, Yi-VL, Fuyu, …
    - Video: VideoChat, Video-ChatGPT, Video-LLaMA, PandaGPT, MovieChat, Video-LLaVA, LLaMA-VID, Momentor, …
    - Audio: AudioGPT, SpeechGPT, VIOLA, AudioPaLM, SALMONN, MU-LLaMA, …
    - 3D: 3D-LLM, 3D-GPT, LL3DA, SpatialVLM, PointLLM, Point-Bind, …
    - Mức pixel (Pixel-wise): Image: GPT4RoI, LION, MiniGPT-v2, NExT-Chat, Kosmos-2, GLaMM, LISA, DetGPT, Osprey, PixelLM, …; Video: PG-Video-LLaVA, Merlin, MotionEpic, …; Audio: -; 3D: -
    - Image + Video: Video-LLaVA, Chat-UniVi, LLaMA-VID (Audio: -; 3D: -)
    - Image + Video + Audio: Panda-GPT, Video-LLaMA, AnyMAL, Macaw-LLM, Gemini, VideoPoet, ImageBind-LLM, LLMBind, LLaMA-Adapter, … (3D: -)
- Hiểu + sinh (Perceiving + Generating):
    - Image: GILL, EMU, MiniGPT-5, DreamLLM, LLaVA-Plus, InternLM-XComposer2, SEED-LLaMA, LaVIT, Mini-Gemini, …
    - Video: GPT4Video, Video-LaVIT, VideoPoet, …
    - Audio: AudioGPT, SpeechGPT, VIOLA, AudioPaLM, …
    - 3D: -
    - Mức pixel (Pixel-wise): Vitron (Audio: -; 3D: -)
    - Nhiều modality: NExT-GPT, Unified-IO 2, AnyGPT, CoDi-2, Modaverse, ViT-Lens, … (3D: -)

## Slide 8

**Hiểu dữ liệu multimodal**

- MLLM hiểu ảnh
    - Flamingo,
    - Kosmos-1,
    - Blip2, mPLUG-Owl,
    - Mini-GPT4, LLaVA,
    - InstructBLIP, Otter,
    - VPGTrans
    - Chameleon,
    - Qwen-VL, GPT-4v,
    - SPHINX,
    - …

_Sơ đồ: Image + Text → LLM → Text_

Mã hóa ảnh đầu vào bằng các encoder (khối biến đầu vào thành biểu diễn vector) ảnh bên ngoài, tạo ra đặc trưng thị giác mà LLM hiểu được, rồi đưa vào LLM. Sau đó LLM diễn giải ảnh đầu vào dựa trên instruction (yêu cầu/chỉ dẫn bằng ngôn ngữ tự nhiên giao cho mô hình) dạng văn bản đi kèm và sinh câu trả lời dạng văn bản.

_Tài liệu:_

- [1] Flamingo: a Visual Language Model for Few-Shot Learning. 2022
- [2] Language Is Not All You Need: Aligning Perception with Language Models. 2023
- [3] BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models. 2023
- [4] MiniGPT-4: Enhancing Vision-Language Understanding with Advanced Large Language Models. 2024
- …

## Slide 9

**Hiểu dữ liệu multimodal**

- MLLM hiểu ảnh
    - Blip2
    - Flamingo
    - LLaVA
    - Mini-GPT4

_Tài liệu:_

- [1] Flamingo: a Visual Language Model for Few-Shot Learning. 2022
- [2] BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models. 2023
- [3] Visual Instruction Tuning. 2023
- [4] A Survey on Multimodal Large Language Models. <https://github.com/BradyFU/Awesome-Multimodal-Large-Language-Models>, 2023.

## Slide 10

**Hiểu dữ liệu multimodal**

- MLLM hiểu video
    - VideoChat,
    - Video-ChatGPT,
    - Video-LLaMA,
    - PandaGPT,
    - MovieChat,
    - Video-LLaVA,
    - LLaMA-VID,
    - Momentor
    - …

_Sơ đồ: Video + Text → LLM → Text_

Mã hóa video đầu vào bằng các encoder video bên ngoài, tạo ra đặc trưng thị giác mà LLM hiểu được rồi đưa vào LLM; sau đó LLM diễn giải video đầu vào dựa trên instruction dạng văn bản đi kèm và sinh câu trả lời dạng văn bản.

_Tài liệu:_

- [1] VideoChat: Chat-Centric Video Understanding. 2023
- [2] Video-ChatGPT: Towards Detailed Video Understanding via Large Vision and Language Models. 2023
- [3] Video-LLaMA: An Instruction-tuned Audio-Visual Language Model for Video Understanding. 2023
- [4] Video-LLaVA: Learning United Visual Representation by Alignment Before Projection. 2023
- [5] Momentor: Advancing Video Large Language Model with Fine-Grained Temporal Reasoning. 2024
- …

## Slide 11

**Hiểu dữ liệu multimodal**

- MLLM hiểu video
    - Video-ChatGPT
    - Video-LLaVA

_Tài liệu:_

- [1] Video-ChatGPT: Towards Detailed Video Understanding via Large Vision and Language Models. 2023
- [2] Video-LLaVA: Learning United Visual Representation by Alignment Before Projection. 2023
- [3] Video Understanding with Large Language Models: A Survey. <https://github.com/yunlong10/Awesome-LLMs-for-Video-Understanding>, 2023

## Slide 12

**Hiểu dữ liệu multimodal**

- MLLM hiểu 3D
    - 3D-LLM,
    - 3D-GPT,
    - LL3DA,
    - SpatialVLM
    - PointLLM
    - Point-Bind
    - …

_Sơ đồ: 3D/điểm + Text → LLM → Text_

Mã hóa thông tin 3D đầu vào bằng các encoder bên ngoài, tạo ra đặc trưng 3D mà LLM hiểu được rồi đưa vào LLM; sau đó LLM diễn giải dữ liệu 3D/điểm đầu vào dựa trên instruction dạng văn bản đi kèm và sinh câu trả lời dạng văn bản.

_Tài liệu:_

- [1] 3D-LLM: Injecting the 3D World into Large Language Models. 2023
- [2] 3D-GPT: Procedural 3D Modeling with Large Language Models. 2023
- [3] LL3DA: Visual Interactive Instruction Tuning for Omni-3D Understanding, Reasoning, and Planning. 2023
- [4] PointLLM: Empowering Large Language Models to Understand Point Clouds. 2023
- [5] SpatialVLM: Endowing Vision-Language Models with Spatial Reasoning Capabilities. 2024
- …

## Slide 13

**Hiểu dữ liệu multimodal**

- MLLM hiểu 3D
    - 3D-LLM
    - PointLLM

_Tài liệu:_

- [1] 3D-LLM: Injecting the 3D World into Large Language Models. 2023
- [2] PointLLM: Empowering Large Language Models to Understand Point Clouds. 2023

## Slide 14

**Hiểu dữ liệu multimodal**

- MLLM hiểu âm thanh
    - AudioGPT,
    - SpeechGPT,
    - VIOLA,
    - AudioPaLM
    - SALMONN
    - MU-LLaMA
    - …

_Sơ đồ: Audio (âm thanh, tiếng nói, âm nhạc, …) + Text → LLM → Text_

Mã hóa tín hiệu âm thanh đầu vào bằng các encoder bên ngoài, tạo ra đặc trưng tín hiệu mà LLM hiểu được rồi đưa vào LLM; sau đó LLM diễn giải âm thanh dựa trên instruction dạng văn bản đi kèm và sinh câu trả lời dạng văn bản.

_Tài liệu:_

- [1] AudioGPT: Understanding and Generating Speech, Music, Sound, and Talking Head. 2023
- [2] SpeechGPT: Empowering Large Language Models with Intrinsic Cross-Modal Conversational Abilities. 2023
- [3] VioLA: Unified Codec Language Models for Speech Recognition, Synthesis, and Translation. 2023
- [4] AudioPaLM: A Large Language Model That Can Speak and Listen. 2023
- [5] SALMONN: Towards Generic Hearing Abilities for Large Language Models. 2023
- …

## Slide 15

**Hiểu dữ liệu multimodal**

- MLLM hiểu âm thanh
    - SpeechGPT
    - SALMONN

_Tài liệu:_

- [1] SpeechGPT: Empowering Large Language Models with Intrinsic Cross-Modal Conversational Abilities. 2023
- [2] SALMONN: Towards Generic Hearing Abilities for Large Language Models. 2023
- [3] Sparks of Large Audio Models: A Survey and Outlook. <https://github.com/EmulationAI/awesome-large-audio-models>, 2023

## Slide 16

**Hiểu dữ liệu multimodal**

- MLLM hiểu modality X
    - Sinh học/y khoa & chăm sóc sức khỏe
        - BioGPT, DrugGPT, BioMedLM, OphGLM, GatorTron, GatorTronGPT, MEDITRON
        - DoctorGLM, BianQue, ClinicalGPT, Qilin-Med, ChatDoctor, BenTsao, HuatuoGPT
        - MedAlpaca, AlpaCare, Zhongjing, PMC-LLaMA, CPLLM, MedPaLM 2, BioMedGPT

_Sơ đồ: Y sinh + Text → LLM → Text_

_Tài liệu:_

- [1] BioGPT: Generative Pre-trained Transformer for Biomedical Text Generation and Mining. 2022
- [2] DrugGPT: A GPT-based Strategy for Designing Potential Ligands Targeting Specific Proteins. 2023
- [3] MEDITRON-70B: Scaling Medical Pretraining for Large Language Models. 2023
- [4] HuaTuo: Tuning LLaMA Model with Chinese Medical Knowledge. 2023
- [5] AlpaCare:Instruction-tuned Large Language Models for Medical Application. 2023
- [6] A Survey of Large Language Models in Medicine: Progress, Application, and Challenge, <https://github.com/AI-in-Health/MedLLMsPracticalGuide>. 2023.
- …

## Slide 17

**Hiểu dữ liệu multimodal**

- MLLM hiểu modality X
    - Phân tử & hóa học
        - ChemGPT, SPT, T5 Chem, ChemLLM, MolCA, MolXPT, MolSTM, GIMLET, …
    - Đồ thị (graph)
        - StructGPT, GPT4Graph, GraphGPT, LLaGA, HiGPT, …
    - Hệ thống thông tin địa lý (GIS)
        - GeoGPT

_Sơ đồ: Hóa học/đồ thị + Text → LLM → Text_

_Tài liệu:_

- [1] Neural Scaling of Deep Chemical Models. 2022
- [2] ChemLLM: A Chemical Large Language Model. 2023
- [3] MolCA: Molecular Graph-Language Modeling with Cross-Modal Projector and Uni-Modal Adapter. 2023
- [4] StructGPT: A General Framework for Large Language Model to Reason on Structured Data. 2023
- [5] LLaGA: Large Language and Graph Assistant. 2023
- [6] Awesome-Graph-LLM, <https://github.com/XiaoxinHe/Awesome-Graph-LLM>. 2023

## Slide 18

**MLLM hợp nhất: hiểu + sinh**

- Các tình huống

Thường thì MLLM không chỉ cần hiểu thông tin multimodal đầu vào mà còn cần sinh thông tin ở chính modality đó.

- Sinh caption (chú thích mô tả) cho ảnh (Image Captioning)
- Hỏi đáp trực quan (Visual Question Answering)
- Tổng hợp hình ảnh từ văn bản (Text-to-Vision Synthesis)
- Chuyển đổi hình ảnh sang hình ảnh (Vision-to-Vision Translation)
- Nhận dạng chữ trong cảnh (Scene Text Recognition)
- Inpainting (tô lấp vùng bị thiếu hoặc bị che) chữ trong cảnh (Scene Text Inpainting)
- …

## Slide 19

**MLLM hợp nhất: hiểu + sinh**

- Image
    - GILL
    - EMU
    - MiniGPT-5
    - DreamLLM
    - LLaVA-Plus
    - LaVIT
    - …

_Sơ đồ: Text + Image → LLM → Text + Image_

LLM trung tâm nhận cả văn bản lẫn ảnh làm đầu vào, hiểu ngữ nghĩa, rồi sinh cả văn bản lẫn ảnh.

_Tài liệu:_

- [1] Generating Images with Multimodal Language Models. 2023
- [2] Generative Pretraining in Multimodality. 2023
- [3] MiniGPT-5: Interleaved Vision-and-Language Generation via Generative Vokens. 2023
- [4] DreamLLM: Synergistic Multimodal Comprehension and Creation. 2023
- [5] LLaVA-Plus: Learning to Use Tools for Creating Multimodal Agents. 2023
- …

## Slide 20

**MLLM hợp nhất: hiểu + sinh**

- Image
    - GILL
    - EMU

_Tài liệu:_

- [1] Generating Images with Multimodal Language Models. 2023
- [2] Generative Pretraining in Multimodality. 2023

## Slide 21

**MLLM hợp nhất: hiểu + sinh**

- Video
    - GPT4Video
    - VideoPoet
    - Video-LaVIT
    - …

_Sơ đồ: Text + Video → LLM → Text + Video_

LLM trung tâm nhận cả văn bản lẫn video làm đầu vào, hiểu ngữ nghĩa, rồi sinh cả văn bản lẫn video.

_Tài liệu:_

- [1] GPT4Video: A Unified Multimodal Large Language Model for lnstruction-Followed Understanding and Safety-Aware Generation. 2023
- [2] VideoPoet: A Large Language Model for Zero-Shot Video Generation. 2023
- [3] Video-LaVIT: Unified Video-Language Pre-training with Decoupled Visual-Motional Tokenization. 2024
- …

## Slide 22

**MLLM hợp nhất: hiểu + sinh**

- Video
    - GPT4Video
    - VideoPoet

_Tài liệu:_

- [1] GPT4Video: A Unified Multimodal Large Language Model for lnstruction-Followed Understanding and Safety-Aware Generation. 2023
- [2] VideoPoet: A Large Language Model for Zero-Shot Video Generation. 2023

## Slide 23

**MLLM hợp nhất: hiểu + sinh**

- Audio
    - AudioGPT,
    - SpeechGPT,
    - VIOLA,
    - AudioPaLM,
    - …

_Sơ đồ: Text + Audio → LLM → Text + Audio_

LLM trung tâm nhận cả văn bản lẫn âm thanh làm đầu vào, hiểu ngữ nghĩa, rồi sinh cả văn bản lẫn âm thanh.

_Tài liệu:_

- [1] AudioGPT: Understanding and Generating Speech, Music, Sound, and Talking Head. 2023
- [2] SpeechGPT: Empowering Large Language Models with Intrinsic Cross-Modal Conversational Abilities. 2023
- [3] VioLA: Unified Codec Language Models for Speech Recognition, Synthesis, and Translation. 2023
- [4] AudioPaLM: A Large Language Model That Can Speak and Listen. 2023
- …

## Slide 24

**MLLM hợp nhất: hiểu + sinh**

- Audio
    - SpeechGPT
    - AudioGPT

_Tài liệu:_

- [1] SpeechGPT: Empowering Large Language Models with Intrinsic Cross-Modal Conversational Abilities. 2023
- [2] AudioGPT: Understanding and Generating Speech, Music, Sound, and Talking Head. 2023

## Slide 25

**MLLM hợp nhất: khai thác nhiều modality**

- Các tình huống:

Trong thực tế, các modality thường gắn kết chặt chẽ với nhau cùng một lúc. Vì vậy, MLLM thường phải xử lý việc hiểu nhiều modality phi văn bản cùng lúc, chứ không chỉ một modality (phi văn bản) duy nhất.

- Image+Video
- Audio+Video
- Image+Video+Audio
- Any-to-Any (từ modality bất kỳ sang modality bất kỳ)
- …

## Slide 26

**MLLM hợp nhất: khai thác nhiều modality**

- Text+Image+Video
    - Video-LLaVA
    - Chat-UniVi
    - LLaMA-VID
    - …

_Sơ đồ: Text + Image + Video → LLM → Text + Image + Video_

LLM trung tâm nhận văn bản, ảnh và video làm đầu vào, hiểu ngữ nghĩa, rồi sinh văn bản (có thể cả ảnh và video, hoặc kết hợp).

_Tài liệu:_

- [1] Video-LLaVA: Learning United Visual Representation by Alignment Before Projection. 2023
- [2] Chat-UniVi: Unified Visual Representation Empowers Large Language Models with Image and Video Understanding. 2023
- [3] LLaMA-VID: An Image is Worth 2 Tokens in Large Language Models. 2023
- …

## Slide 27

**MLLM hợp nhất: khai thác nhiều modality**

- Text+Image+Video
    - Chat-UniVi

_Tài liệu:_

- [1] Chat-UniVi: Unified Visual Representation Empowers Large Language Models with Image and Video Understanding. 2023

## Slide 28

**MLLM hợp nhất: khai thác nhiều modality**

- Text+Image+Video+Audio
    - Panda-GPT
    - Video-LLaMA
    - AnyMAL
    - Macaw-LLM
    - VideoPoet
    - ImageBind-LLM
    - LLMBind
    - LLaMA-Adapter
    - …

_Sơ đồ: Text + Image + Audio + Video → LLM → Text + Image + Audio + Video_

LLM trung tâm nhận văn bản, âm thanh, ảnh và video làm đầu vào, rồi sinh văn bản (có thể cả âm thanh, ảnh và video, hoặc kết hợp).

_Tài liệu:_

- [1] PandaGPT: One Model to Instruction-Follow Them All. 2023
- [2] Video-LLaMA: An Instruction-tuned Audio-Visual Language Model for Video Understanding. 2023
- [3] AnyMAL: An Efficient and Scalable Any-Modality Augmented Language Model. 2023
- [4] Macaw-LLM: Multi-Modal Language Modeling with Image, Audio, Video, and Text Integration. 2023
- …

## Slide 29

**MLLM hợp nhất: khai thác nhiều modality**

- Text+Image+Video+Audio
    - Macaw-LLM

_Tài liệu:_

- [1] Macaw-LLM: Multi-Modal Language Modeling with Image, Audio, Video, and Text Integration. 2023

## Slide 30

**MLLM hợp nhất: khai thác nhiều modality**

- MLLM Any-to-Any
    - NExT-GPT
    - Unified-IO 2 (không có video)
    - AnyGPT (không có video)
    - CoDi-2
    - Modaverse
    - …

_Sơ đồ: Text + Image + Audio + Video → LLM → Text + Image + Audio + Video_

LLM trung tâm nhận văn bản, âm thanh, ảnh và video làm đầu vào, rồi tự do sinh văn bản, âm thanh, ảnh và video, hoặc kết hợp.

_Tài liệu:_

- [1] NExT-GPT: Any-to-Any Multimodal LLM. 2023
- [2] AnyGPT: Unified Multimodal LLM with Discrete Sequence Modeling. 2023
- [3] CoDi-2: In-Context, Interleaved, and Interactive Any-to-Any Generation. 2023
- [4] ModaVerse: Efficiently Transforming Modalities with LLMs. 2023

## Slide 31

**MLLM hợp nhất: khai thác nhiều modality**

- MLLM Any-to-Any
    - NExT-GPT

- Dự án: <https://next-gpt.github.io>
- Bài báo: <https://arxiv.org/pdf/2309.05519>
- Code: <https://github.com/NExT-GPT/NExT-GPT>

_Tài liệu:_

- [1] NExT-GPT: Any-to-Any Multimodal LLM. 2023

## Slide 32

**MLLM hợp nhất: khai thác nhiều modality**

- MLLM Any-to-Any
    - NExT-GPT

_Tài liệu:_

- [1] NExT-GPT: Any-to-Any Multimodal LLM. 2023

## Slide 33

**MLLM hợp nhất: khai thác nhiều modality**

- MLLM Any-to-Any
    - NExT-GPT

_Tài liệu:_

- [1] NExT-GPT: Any-to-Any Multimodal LLM. 2023

## Slide 34

**MLLM hợp nhất: khai thác nhiều modality**

- MLLM Any-to-Any
    - NExT-GPT

_Sơ đồ: Giai đoạn mã hóa multimodal → Giai đoạn LLM hiểu và suy luận → Giai đoạn sinh multimodal_

_Tài liệu:_

- [1] NExT-GPT: Any-to-Any Multimodal LLM. 2023

## Slide 35

**MLLM hợp nhất: khai thác nhiều modality**

- MLLM Any-to-Any
    - NExT-GPT
- Dùng ImageBind làm encoder multimodal hợp nhất
- Một input projection layer (lớp biến đổi biểu diễn của modality sang không gian của LLM) để nối encoder multimodal với LLM

_Sơ đồ: ImageBind → Input Projection_

_Tài liệu:_

- [1] NExT-GPT: Any-to-Any Multimodal LLM. 2023

## Slide 36

**MLLM hợp nhất: khai thác nhiều modality**

- MLLM Any-to-Any
    - NExT-GPT
- Tận dụng các mô hình sinh ảnh, video, âm thanh từ văn bản dựa trên diffusion (diffusion model: mô hình sinh ảnh/âm thanh/video bằng cách khử nhiễu dần) đạt SoTA (tốt nhất hiện nay) để sinh nội dung multimodal
    - Text encoder: điều khiển quá trình sinh
    - VAE
    - UNet

_Tài liệu:_

- [1] NExT-GPT: Any-to-Any Multimodal LLM. 2023

## Slide 37

**MLLM hợp nhất: khai thác nhiều modality**

- MLLM Any-to-Any
    - NExT-GPT
- Dùng LLM làm lõi để quyết định có xuất nội dung modality hay không và xuất nội dung modality nào tương ứng.
- Thay vì sinh instruction dạng văn bản, LLM sinh ra các token “tín hiệu modality” riêng, đóng vai trò instruction dẫn dắt quá trình sinh.

_Tài liệu:_

- [1] NExT-GPT: Any-to-Any Multimodal LLM. 2023

## Slide 38

**MLLM hợp nhất: khai thác nhiều modality**

- MLLM Any-to-Any
    - NExT-GPT

_Tài liệu:_

- [1] NExT-GPT: Any-to-Any Multimodal LLM. 2023

## Slide 39

**MLLM hợp nhất: khai thác nhiều modality**

- MLLM Any-to-Any
    - NExT-GPT

_Tài liệu:_

- [1] NExT-GPT: Any-to-Any Multimodal LLM. 2023

## Slide 40

**MLLM hợp nhất: khai thác nhiều modality**

- MLLM Any-to-Any
    - NExT-GPT

_Tài liệu:_

- [1] NExT-GPT: Any-to-Any Multimodal LLM. 2023

## Slide 41

**MLLM hợp nhất: khai thác nhiều modality**

- MLLM Any-to-Any
    - NExT-GPT

_Tài liệu:_

- [1] NExT-GPT: Any-to-Any Multimodal LLM. 2023

## Slide 42

**MLLM hợp nhất: khai thác nhiều modality**

- MLLM Any-to-Any
    - NExT-GPT
- Điểm then chốt I: huấn luyện tiết kiệm tham số, chi phí thấp

```text
Tham số được tinh chỉnh / (Tham số đóng băng + Tham số được tinh chỉnh)
  = (4M+33M+31M+31M+32M) / ((4M+33M+31M+31M+32M) + (1.2B+7B+1.3B+1.8B+0.975B))
  = 131M / (131M + 12.275B)
  ≅ 0.01
```

_Tài liệu:_

- [1] NExT-GPT: Any-to-Any Multimodal LLM. 2023

## Slide 43

**MLLM hợp nhất: khai thác nhiều modality**

- MLLM Any-to-Any
    - NExT-GPT
- Điểm then chốt II: instruction tuning (fine-tuning trên dữ liệu dạng (instruction, câu trả lời) để mô hình biết làm theo yêu cầu) chuyển đổi modality

_Tài liệu:_

- [1] NExT-GPT: Any-to-Any Multimodal LLM. 2023

## Slide 44

**Năng lực fine-grained của MLLM**

- MLLM thị giác mức pixel

Các MLLM thị giác nói ở trên nhìn chung chỉ hỗ trợ hiểu hình ảnh ở mức thô, mức instance (từng đối tượng). Điều này có thể dẫn tới diễn giải hình ảnh thiếu chính xác. Ngoài ra, do thiếu visual grounding (gắn nội dung với vùng cụ thể trong ảnh), các MLLM này có thể sinh ra hallucination (mô hình sinh nội dung sai sự thật hoặc không bám nguồn).

- Visual grounding
- Phân đoạn hình ảnh (Visual Segmentation)
- Chỉnh sửa hình ảnh (Visual Editing)
- Inpainting hình ảnh (Visual Inpainting)
- …

## Slide 45

**Năng lực fine-grained của MLLM**

- MLLM theo vùng mức pixel, hướng ảnh
    - GPT4RoI
    - NExT-Chat
    - MiniGPT-v2
    - Shikra
    - Kosmos-2
    - GLaMM
    - LISA
    - DetGPT
    - Osprey
    - PixelLM
    - LION
    - …

Người dùng đưa vào một ảnh (có thể chỉ định một vùng), và LLM xuất nội dung dựa trên hiểu biết của nó, gắn (grounding) nội dung hình ảnh với các vùng cụ thể ở mức pixel của ảnh.

_Sơ đồ: Text + Image + Region/Pixels → LLM → Text + Image + Region_

_Tài liệu:_

- [1] GPT4RoI: Instruction Tuning Large Language Model on Region-of-Interest. 2023
- [2] NExT-Chat: An LMM for Chat, Detection and Segmentation. 2023
- [3] MiniGPT-v2: large language model as a unified interface for vision-language multi-task learning. 2023
- [4] Osprey: Pixel Understanding with Visual Instruction Tuning. 2023
- [5] GLaMM: Pixel Grounding Large Multimodal Model. 2023
- [6] Kosmos-2: Grounding Multimodal Large Language Models to the World. 2023
- [7] DetGPT: Detect What You Need via Reasoning. 2023
- [8] PixelLM: Pixel Reasoning with Large Multimodal Model. 2023
- [9] Lisa: Reasoning segmentation via large language model. 2023
- [10] Shikra: Unleashing Multimodal LLM's Referential Dialogue Magic. 2023
- …

## Slide 46

**Năng lực fine-grained của MLLM**

- MLLM theo vùng mức pixel, hướng ảnh
    - NExT-Chat
    - GLaMM

## Slide 47

**Năng lực fine-grained của MLLM**

- MLLM theo vùng mức pixel, hướng video
    - PG-Video-LLaVA
    - Merlin
    - MotionEpic
    - …

_Sơ đồ: Text + Video + Region/Pixels → LLM → Text + Video + Region_

Người dùng đưa vào một video (có thể chỉ định một vùng), và LLM xuất nội dung dựa trên hiểu biết của nó, gắn (grounding) hoặc theo dõi nội dung tới các vùng cụ thể ở mức pixel của video.

_Tài liệu:_

- [1] PG-Video-LLaVA: Pixel Grounding in Large Multimodal Video Models. 2023
- [2] Merlin: Empowering Multimodal LLMs with Foresight Minds. 2023
- [3] Video-of-Thought: Step-by-Step Video Reasoning from Perception to Cognition. 2024
- …

## Slide 48

**Năng lực fine-grained của MLLM**

- MLLM theo vùng mức pixel, hướng video
    - PG-Video-LLaVA
    - MotionEpic

_Tài liệu:_

- [1] PG-Video-LLaVA: Pixel Grounding in Large Multimodal Video Models. 2023
- [2] Video-of-Thought: Step-by-Step Video Reasoning from Perception to Cognition. 2024

## Slide 49

**Năng lực fine-grained của MLLM**

- MLLM mức pixel hợp nhất
    - Vitron

Người dùng đưa vào một ảnh hoặc một video (có thể chỉ định một vùng), và LLM xuất nội dung dựa trên hiểu biết của nó, sinh, gắn (grounding) hoặc theo dõi nội dung tới các vùng cụ thể ở mức pixel của ảnh, video.

_Sơ đồ: Text + Image + Video + Region/Pixels → LLM → Text + Image + Video + Region_

_Tài liệu:_

- [1] VITRON: A Unified Pixel-level Vision LLM for Understanding, Generating, Segmenting, Editing. 2024

## Slide 50

**Năng lực fine-grained của MLLM**

- MLLM mức pixel hợp nhất
    - Vitron

_Tài liệu:_

- [1] VITRON: A Unified Pixel-level Vision LLM for Understanding, Generating, Segmenting, Editing. 2024

## Slide 51

**Năng lực fine-grained của MLLM**

- MLLM mức pixel hợp nhất
    - Vitron

_Tài liệu:_

- [1] VITRON: A Unified Pixel-level Vision LLM for Understanding, Generating, Segmenting, Editing. 2024

## Slide 52

**2 Kiến trúc của MLLM**

Thiết kế một MLLM như thế nào?

## Slide 53

**Tổng quan kiến trúc MLLM**

- Ý tưởng tiền đề: trí tuệ dựa trên ngôn ngữ

Nhờ scaling law (quy luật hiệu năng tăng theo kích thước mô hình, dữ liệu và compute), các hiện tượng emergent (năng lực chỉ xuất hiện khi mô hình đủ lớn) đã xuất hiện rộng rãi ở các LLM dựa trên ngôn ngữ. Các LLM này nay nhìn chung có năng lực hiểu ngữ nghĩa rất mạnh. Điều đó cũng cho thấy ngôn ngữ là một modality then chốt để mang trí tuệ.

_Sơ đồ: ngôn ngữ_

## Slide 54

**Tổng quan kiến trúc MLLM**

- Ý tưởng tiền đề: trí tuệ ngôn ngữ làm trục xoay

Từ tiền đề này, gần như mọi MLLM HIỆN NAY đều lấy LLM dựa trên ngôn ngữ làm module ra quyết định cốt lõi (tức là bộ não hay bộ xử lý trung tâm). Bằng cách thêm các module hay encoder ngoài cho các modality phi văn bản, LLM có thêm năng lực tri giác/thao tác multimodal.

_Sơ đồ: ngôn ngữ ở trung tâm; xung quanh là thị giác, video, 3D, khứu giác, âm thanh, xúc giác_

## Slide 55

**Tổng quan kiến trúc MLLM**

- Kiến trúc I: LLM làm bộ điều phối/bộ điều khiển rời rạc

Vai trò của LLM là nhận tín hiệu dạng văn bản và đưa ra lệnh dạng văn bản để gọi các module downstream (module xử lý phía sau).

- Đặc điểm chính:

Mọi việc truyền thông điệp trong hệ thống, như “encoder multimodal tới LLM” hay “LLM tới các module downstream”, đều dùng lệnh văn bản thuần làm phương tiện.

_Sơ đồ: Người dùng → Text → LLM → Text → các module downstream_

## Slide 56

**Tổng quan kiến trúc MLLM**

- Kiến trúc I: LLM làm bộ điều phối/bộ điều khiển rời rạc
    - Các MLLM tiêu biểu:
        - Visual-ChatGPT
        - HuggingGPT
        - MM-REACT
        - ViperGPT
        - AudioGPT
        - LLaVA-Plus
        - …

_Sơ đồ: Người dùng → Text → LLM → Text → các module downstream_

## Slide 57

**Tổng quan kiến trúc MLLM**

- Kiến trúc I: LLM làm bộ điều phối/bộ điều khiển rời rạc
    - Visual-ChatGPT
    - HuggingGPT

_Tài liệu:_

- [1] Visual ChatGPT: Talking, Drawing and Editing with Visual Foundation Models. 2023
- [2] HuggingGPT: Solving AI Tasks with ChatGPT and its Friends in Hugging Face. 2023

## Slide 58

**Tổng quan kiến trúc MLLM**

- Kiến trúc II: LLM là một bộ phận khớp nối của hệ thống

Vai trò của LLM là tự tri giác thông tin multimodal và tự phản hồi, trong một cấu trúc Encoder-LLM-Decoder.

- Đặc điểm chính:

LLM là bộ phận khớp nối then chốt của hệ thống: nhận thông tin multimodal trực tiếp từ bên ngoài và chuyển instruction tới các decoder (khối sinh đầu ra từ biểu diễn)/bộ sinh một cách trơn tru hơn.

_Sơ đồ: Tín hiệu multimodal → Encoder multimodal (Encoder) → LLM (Lõi) → Decoder multimodal (Decoder) → Đầu ra multimodal; văn bản đi thẳng vào và ra khỏi LLM_

## Slide 59

**Tổng quan kiến trúc MLLM**

- Kiến trúc II: LLM là một bộ phận khớp nối của hệ thống (triển vọng hơn)
    - ≈ 96% MLLM thuộc nhóm này.

_Tài liệu:_

- [1] A Survey on Multimodal Large Language Models. <https://github.com/BradyFU/Awesome-Multimodal-Large-Language-Models>, 2023.

## Slide 60

**Mã hóa multimodal**

- Encoder thị giác (ảnh & video)
    - CLIP-ViT là lựa chọn phổ biến nhất cho các mô hình thị giác-ngôn ngữ.
    - Ưu điểm:
        - Cung cấp biểu diễn ảnh có alignment (căn chỉnh biểu diễn của các modality với LLM) tốt với không gian văn bản.
        - Mở rộng tốt theo số tham số và lượng dữ liệu.

## Slide 61

**Mã hóa multimodal**

- Encoder phi thị giác
    - Âm thanh:
        - HuBERT
        - Whisper
        - BEATs
    - Điểm 3D:
        - Point-BERT

## Slide 62

**Mã hóa multimodal**

- Encoder multimodal hợp nhất
    - ImageBind:
        - Nhúng mọi modality vào một không gian biểu diễn chung của ảnh.
        - Biểu diễn các modality có alignment tốt sẽ giúp LLM hiểu tốt hơn

_Tài liệu:_

- [1] ImageBind: One Embedding Space To Bind Them All. 2023

## Slide 63

**Mã hóa multimodal**

- Encoder multimodal hợp nhất
    - LanguageBind:
        - Nhúng mọi modality vào một không gian biểu diễn chung của ngôn ngữ.
        - Biểu diễn các modality có alignment tốt sẽ giúp LLM hiểu tốt hơn

_Tài liệu:_

- [1] LanguageBind: Extending Video-Language Pretraining to N-modality by Language-based Semantic Alignment. 2023

## Slide 64

**Tokenization tín hiệu multimodal**

- Tokenization
    - SEED

_Tài liệu:_

- [1] Planting a SEED of Vision in Large Language Model. 2023

## Slide 65

**Tokenization tín hiệu multimodal**

- Tokenization
    - AnyGPT

_Tài liệu:_

- [1] AnyGPT: Unified Multimodal LLM with Discrete Sequence Modeling. 2023

## Slide 66

**Tokenization tín hiệu multimodal**

- Tokenization
    - VideoPoet

_Tài liệu:_

- [1] VideoPoet: A Large Language Model for Zero-Shot Video Generation. 2023

## Slide 67

**Tokenization tín hiệu multimodal**

- Tokenization thị giác (ảnh & video) bằng codebook
    - Biểu diễn tín hiệu multimodal thành các token rời rạc trong một codebook (bảng mã gồm các vector rời rạc)
        - Ưu điểm: hỗ trợ hiểu và sinh tín hiệu multimodal một cách hợp nhất trong khung autoregressive (sinh từng token dựa trên các token trước đó) dự đoán token kế tiếp
        - Thường dùng hơn trong tổng hợp ảnh
            - Parti
            - Muse (song song)
            - MaskGIT (song song)
        - Các LLM multimodal tiêu biểu
            - Gemini
            - CM3
            - VideoPoet

## Slide 68

**Tokenization tín hiệu multimodal**

- Tokenization âm thanh
    - SpeechTokenizer +RVQ-VAE
    - SoundStream +RVQ-VAE

_Tài liệu:_

- [1] SpeechTokenizer: Unified Speech Tokenizer for Speech Large Language Models. 2023
- [2] SoundStream: An End-to-End Neural Audio Codec. 2021

## Slide 69

**Projection phía đầu vào**

- Các phương pháp nối biểu diễn multimodal với LLM
    - Chiếu biểu diễn multimodal (ví dụ: ảnh) vào không gian ngữ nghĩa của LLM
        - Linear projection (phép chiếu tuyến tính): LLaVA, MiniGPT-4, NExT-GPT
        - MLP hai lớp: LLaVA-1.5/NeXT, CogVLM, DeepSeek-VL, Yi-VL
        - Perceiver Resampler: Flamingo, Qwen-VL, MiniCPM-V, LLaVA-UHD
        - Q-Former: BLIP-2, InstructBLIP, VisCPM, VisualGLM
        - C-Abstractor: HoneyBee, MM1

## Slide 70

**Projection phía đầu vào**

- Một số nhận xét
    - Các bài báo khác nhau đưa ra kết luận khác nhau về các phương pháp projection khác.
    - MLP hai lớp tốt hơn linear projection. (LLaVA)
    - Linear projection hữu ích hơn các lớp Q-former. (MiniGPT-4)

_Tài liệu:_

- [1] Improved Baselines with Visual Instruction Tuning. 2023
- [2] MiniGPT-4: Enhancing Vision-Language Understanding with Advanced Large Language Models. 2021

## Slide 71

**LLM nền**

- Các LLM mã nguồn mở dựa trên ngôn ngữ

| LLM | Kích thước (B) | Quy mô dữ liệu (T) | Thời điểm | Ngôn ngữ | Kiến trúc |
|---|---|---|---|---|---|
| Flan-T5 | 3/11 | - | 10/2022 | en, fr, de | Encoder-Decoder |
| LLaMA | 7/13 | 1.4 | 02/2023 | en | Decoder |
| Alpaca | 7 | - | 03/2023 | en | Decoder |
| Vicuna | 7/13 | 1.4 | 03/2023 | en | Decoder |
| LLaMA-2 | 7/13 | 2 | 07/2023 | en | Decoder |
| GLM | 2/10 | 0.4 | 10/2022 | en | Decoder |
| Qwen | 1.8/7/14 | 3 | 09/2023 | en, zh | Decoder |
| Skywork | 13 | 3.2 | 10/2023 | en | Decoder |

_Tài liệu:_

- [1] A Survey of Large Language Models. <https://github.com/RUCAIBox/LLMSurvey>, 2023

## Slide 72

**Kết nối phía giải mã**

- Truyền thông điệp qua 1) token rời rạc của ngôn ngữ
    - Các MLLM tiêu biểu:
        - Visual-ChatGPT
        - HuggingGPT
        - GPT4Video
        - MM-REACT
        - ViperGPT
        - ModaVerse
        - Vitron
        - …
    - Ưu điểm:
        - Cận dưới hiệu năng cao
        - Tiết kiệm hơn, tức là không cần tinh chỉnh
    - Nhược điểm:
        - Mất khả năng tinh chỉnh end-to-end (tinh chỉnh toàn bộ hệ thống cùng lúc).
        - Cận trên hiệu năng bị giới hạn, tức là một số tín hiệu multimodal không thể truyền tải tối ưu qua văn bản.

_Sơ đồ: LLM → câu trả lời dạng văn bản → Decoder multimodal → Text / nội dung multimodal_

_Tài liệu:_

- [1] Visual-ChatGPT: Talking, Drawing and Editing with Visual Foundation Models. 2023
- [2] HuggingGPT: Solving AI Tasks with ChatGPT and its Friends in Hugging Face. 2023
- [3] ModaVerse: Efficiently Transforming Modalities with LLMs. 2024
- [4] VITRON: A Unified Pixel-level Vision LLM for Understanding, Generating, Segmenting, Editing. 2024

## Slide 73

**Kết nối phía giải mã**

- Truyền thông điệp qua 2) embedding liên tục

Truyền thông điệp từ LLM tới các decoder phía sau bằng các embedding mềm (embedding: vector số biểu diễn ý nghĩa của văn bản/ảnh/âm thanh), tức là signal token (token đặc biệt LLM sinh ra để kích hoạt bộ giải mã modality).

- Ưu điểm
    - Tinh chỉnh end-to-end được, nhờ đó truyền instruction hiệu quả hơn
    - Truyền tải tốt hơn nhiều loại tín hiệu multimodal mà riêng văn bản không diễn đạt được, ví dụ:
        - số lượng của đối tượng thị giác
        - ngữ nghĩa quan hệ không gian thị giác

_Sơ đồ: LLM → embedding của các signal token → Decoder multimodal → Text / nội dung multimodal_

_Tài liệu:_

- [1] Generating Images with Multimodal Language Models. 2023
- [2] NExT-GPT: Any-to-Any Multimodal LLM. 2023

## Slide 74

**Kết nối phía giải mã**

- Truyền thông điệp qua 1) token rời rạc của ngôn ngữ
    - Instruction: Ban đầu trên bàn có 7 quả táo, nhưng tôi đã ăn một quả. Vậy bây giờ còn lại bao nhiêu quả táo? Hãy tạo một bức ảnh mô tả kết quả.

_Tài liệu:_

- [1] NExT-GPT: Any-to-Any Multimodal LLM. 2023

## Slide 75

**Kết nối phía giải mã**

- Truyền thông điệp qua 2) embedding liên tục
    - Instruction: Ban đầu trên bàn có 7 quả táo, nhưng tôi đã ăn một quả. Vậy bây giờ còn lại bao nhiêu quả táo? Hãy tạo một bức ảnh mô tả kết quả.

_Tài liệu:_

- [1] NExT-GPT: Any-to-Any Multimodal LLM. 2023

## Slide 76

**Kết nối phía giải mã**

- Truyền thông điệp qua 3) codebook

LLM sinh id của các token đặc biệt, tức là codebook, cho các decoder (thị giác) phía sau.

- Ưu điểm
    - Tinh chỉnh end-to-end được, nhờ đó truyền lệnh hiệu quả hơn
    - Diễn đạt tốt hơn nhiều loại tín hiệu multimodal mà riêng văn bản không nắm bắt được
    - Hỗ trợ sinh token multimodal theo kiểu autoregressive

_Sơ đồ: LLM → codebook → de-tokenize → embedding multimodal → Decoder multimodal → Text / nội dung multimodal_

_Tài liệu:_

- [1] Unified-IO 2: Scaling Autoregressive Multimodal Models with Vision, Language, Audio, and Action. 2023
- [2] LVM: Sequential Modeling Enables Scalable Learning for Large Vision Models. 2023
- [3] AnyGPT: Unified Multimodal LLM with Discrete Sequence Modeling. 2024
- [4] VideoPoet: A Large Language Model for Zero-Shot Video Generation. 2024

## Slide 77

**Sinh dữ liệu multimodal**

- Sinh văn bản
    - LLM vốn hỗ trợ sinh văn bản trực tiếp, ví dụ qua giải mã BPE, beam search, …

## Slide 78

**Sinh dữ liệu multimodal**

- Sinh bằng diffusion model
    - Bộ sinh thị giác (ảnh/video)
        - Image Diffusion
        - Video Diffusion
    - Bộ sinh âm thanh
        - Speech Diffusion
        - Audio Diffusion

_Tài liệu:_

- [1] NExT-GPT: Any-to-Any Multimodal LLM. 2023

## Slide 79

**Sinh dữ liệu multimodal**

- Sinh bằng codebook
    - Bộ sinh thị giác (ảnh/video)
        - VQ-VAE + Codebooks
        - VQ-GAN + Codebooks
    - Bộ sinh âm thanh
        - SpeechTokenizer + Residual Vector Quantizer (bộ lượng tử hóa vector phần dư)
        - SoundStream + Residual Vector Quantizer

_Tài liệu:_

- [1] Unified-IO 2: Scaling Autoregressive Multimodal Models with Vision, Language, Audio, and Action. 2023

## Slide 80

**Sinh dữ liệu multimodal**

- Sinh bằng codebook
    - VQ-GAN trong Stable-diffusion
        - 64 ✕ 64 ✕ 3 hoặc 32 ✕ 32 ✕ 4

## Slide 81

**Cảm ơn!**

Có câu hỏi nào không?
