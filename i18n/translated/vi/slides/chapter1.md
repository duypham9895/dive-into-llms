# Công nghệ và sự phát triển của mô hình lớn

[PDF gốc](https://github.com/Lordog/dive-into-llms/blob/f84c04268794ef94f8949808bbc14ab8636763a0/documents/chapter1/dive-into-llm.pdf)

## Slide 1

**Công nghệ và sự phát triển của mô hình lớn**

张倬胜 (Zhang Zhuosheng)

上海交通大学计算机学院 (SJTU School of Computer Science)

zhangzs@sjtu.edu.cn

<https://bcmi.sjtu.edu.cn/~zhangzs>

## Slide 2

**Mục lục**

- Tổng quan về mô hình lớn
    - Tổng quan quá trình phát triển
    - Phạm vi khái niệm
- Mô hình pre-trained (mô hình đã qua pre-training: huấn luyện ban đầu trên kho dữ liệu rất lớn, chưa gắn với nhiệm vụ cụ thể)
    - Các loại chính
    - Kiến trúc mô hình
- Mô hình quy mô lớn
    - Thay đổi về mô thức
    - Các đại diện chính
    - Công nghệ then chốt
    - Cách triển khai
- Mở rộng khái niệm
    - Mô hình lớn chuyên ngành
    - Foundation model (mô hình nền dùng chung cho nhiều ứng dụng) multimodal (xử lý nhiều loại dữ liệu cùng lúc)
    - Foundation model cho agent (tác tử AI: hệ thống dùng mô hình để tự lập kế hoạch, gọi công cụ và hành động trong môi trường)

## Slide 3

**Mục lục**

- Tổng quan về mô hình lớn
    - Tổng quan quá trình phát triển
    - Phạm vi khái niệm
- Mô hình pre-trained
    - Các loại chính
    - Kiến trúc mô hình
- Mô hình quy mô lớn
    - Thay đổi về mô thức
    - Các đại diện chính
    - Công nghệ then chốt
    - Cách triển khai
- Mở rộng khái niệm
    - Mô hình lớn chuyên ngành
    - Foundation model multimodal
    - Foundation model cho agent

## Slide 4

**Sự phát triển của trí tuệ nhân tạo**

- Công nghệ trí tuệ nhân tạo (AI) đã đi từ dữ liệu nhỏ đến dữ liệu lớn, từ mô hình nhỏ đến mô hình lớn, từ chuyên dụng đến đa dụng, và đang dần bước vào thời đại mô hình lớn
- Pre-training tự giám sát quy mô lớn trên lượng dữ liệu khổng lồ không gán nhãn, học được rất nhiều tri thức ngôn ngữ và tri thức về thế giới
- Hoàn thành nhiều loại nhiệm vụ thông qua tương tác bằng ngôn ngữ tự nhiên, có năng lực xử lý nhiệm vụ đa kịch bản, đa mục đích, liên ngành

*Trong hình:* Mở rộng khái niệm · Mô hình lớn chuyên ngành · Foundation model multimodal · Foundation model cho agent

[1] Zhao, Wayne Xin, et al. A Survey of Large Language Models. arXiv preprint arXiv:2303.18223.

## Slide 5

**Phạm vi của mô hình lớn**

*Trong hình:* Mô hình ngôn ngữ lớn (LLM) · Mô hình lớn chuyên ngành · Foundation model multimodal · Mô hình ngôn ngữ pre-trained · Foundation model cho agent

## Slide 6

**Mục lục**

- Tổng quan về mô hình lớn
    - Tổng quan quá trình phát triển
    - Phạm vi của mô hình lớn
- Mô hình pre-trained
    - Các loại chính
    - Kiến trúc mô hình
- Mô hình quy mô lớn
    - Thay đổi về mô thức
    - Các đại diện chính
    - Công nghệ then chốt
- Mở rộng khái niệm
    - Mô hình lớn chuyên ngành
    - Foundation model multimodal
    - Foundation model cho agent

## Slide 7

**Mô hình ngôn ngữ pre-trained**

- Mô thức mới của trí tuệ ngôn ngữ: mô hình ngôn ngữ pre-trained (đại diện: ELMo, BERT, GPT-1/2)
    - Pre-training tự giám sát trên dữ liệu quy mô lớn, sau khi fine-tuning (tinh chỉnh mô hình đã huấn luyện trên dữ liệu của một nhiệm vụ cụ thể) thì thích ứng được với nhiều loại nhiệm vụ, tận dụng hiệu quả dữ liệu lớn, mô hình lớn và năng lực tính toán lớn
    - Chủ yếu dùng cho các nhiệm vụ phân tích và hiểu ngôn ngữ

[1] Zhang, Zhuosheng, et al. Machine Reading Comprehension: The Role of Contextualized Language Models and Beyond. arXiv preprint arXiv:2005.06249.

## Slide 8

**Các loại chính**

- Mô hình encoder (Encoder-Only; encoder là khối biến đầu vào thành biểu diễn vector)
- Mô hình decoder (Decoder-Only; decoder là khối sinh đầu ra từ biểu diễn)
- Mô hình encoder-decoder (Encoder-Decoder)

Mức độ quan tâm tới từng loại mô hình thay đổi theo thời gian

- Trước khoảng năm 2021, các biến thể của mô hình encoder và mô hình encoder-decoder liên tục xuất hiện. Các phiên bản này được gọi vui là “BERTology”
- Sau khoảng năm 2021, mô hình decoder phát triển rất nhanh, mở ra thời đại mô hình lớn tạo sinh “Next-Level”

[1] Rogers, Anna, et al. A primer in BERTology: What we know about how BERT works. TACL, 2021. [2] Minaee, Shervin, et al. Large language models: A survey. arXiv preprint arXiv:2402.06196.

## Slide 9

**Từ góc nhìn mô hình hóa pre-training**

- Xét theo cách mô hình hóa pre-training tự giám sát, mục tiêu huấn luyện của các kiến trúc khác nhau là khác nhau
    - Mô hình encoder: masked language modeling (Masked Language Modeling, MLM; che một số token rồi bắt mô hình đoán lại)
    - Mô hình decoder: mô hình hóa ngôn ngữ autoregressive (Auto-regressive Language Modeling; sinh từng token dựa trên các token trước đó)
    - Mô hình encoder-decoder: mô hình hóa sequence-to-sequence (Sequence to Sequence Modeling, seq2seq; biến một chuỗi đầu vào thành một chuỗi đầu ra)

[1] Ding, Ning, et al. Parameter-efficient fine-tuning of large-scale pre-trained language models. Nature Machine Intelligence, 2023.

## Slide 10

**Mô hình encoder**

- Mục tiêu huấn luyện chính: masked language modeling (Masked Language Modeling, MLM)
- Các mô hình tiêu biểu: BERT, RoBERTa, ALBERT

*Trong hình:* đầu ra `NotNext` · `học`; Transformer Encoder; đầu vào `[CLS] | hãy | chúng ta | cùng nhau | bắt tay | [MASK] | mô hình lớn | phát triển | toàn quy trình`

## Slide 11

**Mô hình decoder**

- Mục tiêu huấn luyện chính: mô hình hóa ngôn ngữ autoregressive (Auto-regressive Language Modeling)
- Các mô hình tiêu biểu: các dòng GPT, Llama, PaLM, v.v.

*Trong hình:* đầu ra `hãy | chúng ta | cùng nhau | bắt tay | học | mô hình lớn | then chốt | công nghệ`; Decoder; đầu vào `[BOS] | hãy | chúng ta | cùng nhau | bắt tay | học | mô hình lớn | then chốt`

## Slide 12

**So sánh ưu và nhược điểm**

| Mô hình encoder (BERT) | Mô hình decoder (GPT) |
|---|---|
| Ưu điểm: tận dụng ngữ cảnh hai chiều, hiểu ngôn ngữ tốt | Ưu điểm: tự nhiên phù hợp với các nhiệm vụ sinh, dễ xây dựng dữ liệu huấn luyện quy mô lớn |
| Nhược điểm: dùng ký hiệu đặc biệt [mask] nên có chênh lệch giữa pre-training và fine-tuning; giả định mọi token (đơn vị văn bản nhỏ nhất mà mô hình đọc và sinh) bị mask là độc lập với nhau | Nhược điểm: bị giới hạn ở mô hình hóa một chiều, khó tận dụng cùng lúc thông tin ngữ cảnh hai chiều |

## Slide 13

**Mô hình encoder-decoder**

- Mục tiêu huấn luyện chính: mô hình hóa sequence-to-sequence (Sequence to Sequence Modeling)
- Các mô hình tiêu biểu: T5, BART

*Trong hình:* Decoder sinh `<X> bắt tay <Y> mô hình lớn <Z>`; Encoder nhận `hãy cùng nhau <Y> học <Y> công nghệ then chốt của mô hình lớn`

## Slide 14

**Chọn mô hình theo kịch bản ứng dụng**

| Mô hình encoder | Mô hình decoder | Mô hình encoder-decoder |
|---|---|---|
| Các nhiệm vụ phân biệt như phân loại, hồi quy | Phù hợp với nhiệm vụ sinh mở | Có cả năng lực phân biệt lẫn năng lực sinh |

## Slide 15

**Mô hình ngôn ngữ pre-trained: kiến trúc mô hình**

- RNN (LSTM)
    - Nắm bắt quan hệ phụ thuộc giữa các từ. Nhưng do vấn đề khi tính gradient, RNN thường khó huấn luyện
    - Tính toán rất chậm, khả năng học phụ thuộc xa cũng hạn chế
- Transformer √ (Attention is all you need)
    - Bỏ hoàn toàn cơ chế hồi tiếp (recurrence) của RNN, dùng self-attention (cơ chế để mỗi token cân nhắc mọi token khác trong chuỗi) để xử lý toàn cục
    - Ba ma trận trọng số (Query, Key và Value) nắm bắt quan hệ phụ thuộc ngữ cảnh
    - Mạng nhiều lớp: mỗi lớp gồm cơ chế multi-head attention và feed-forward network (lớp mạng truyền thẳng trong mỗi khối Transformer)
    - Thêm positional encoding (Positional Encoding; thông tin vị trí cộng vào biểu diễn token)

## Slide 16

**Mục lục**

- Tổng quan về mô hình lớn
    - Tổng quan quá trình phát triển
    - Phạm vi của mô hình lớn
- Mô hình pre-trained
    - Các loại chính
    - Kiến trúc mô hình
- Mô hình quy mô lớn
    - Thay đổi về mô thức
    - Công nghệ then chốt
    - Các đại diện chính
    - Cách triển khai
- Mở rộng khái niệm
    - Mô hình lớn chuyên ngành
    - Foundation model multimodal
    - Foundation model cho agent

## Slide 17

**Tổng quan về mô hình lớn**

[1] Zhao, Wayne Xin, et al. A Survey of Large Language Models. arXiv preprint arXiv:2303.18223.

## Slide 18

**Thay đổi về mô thức trong thời đại mô hình lớn**

- Chuyển dịch mô thức công nghệ: từ huấn luyện chuyên biệt cho từng nhiệm vụ riêng lẻ sang mô thức tập trung “pre-training + post-training (các bước huấn luyện sau pre-training: SFT (supervised fine-tuning; fine-tuning trên cặp đầu vào–đáp án mẫu), RL, alignment (căn chỉnh hành vi mô hình theo ý định, giá trị và yêu cầu an toàn của con người))” và “pre-training + prompting (prompt learning; điều khiển mô hình bằng cách thiết kế prompt (đầu vào bằng văn bản đưa cho mô hình để yêu cầu nó làm một việc) thay vì huấn luyện lại)”
- Thống nhất mô thức nhiệm vụ: từ các dạng nhiệm vụ độc lập riêng rẽ tiến tới một dạng mô hình hóa sequence-to-sequence thống nhất

| Trước đây | Hiện nay (huấn luyện) | Hiện nay (ứng dụng) |
|---|---|---|
| Ở từng nhiệm vụ, mỗi người dùng tự xây dựng mô hình và tự hoàn thành toàn bộ quá trình huấn luyện học máy | Một nút trung tâm hoàn thành pre-training tổng quát quy mô lớn, cung cấp mô hình gần hoàn chỉnh, dùng nó như một mô-đun tiêu chuẩn để post-training (instruction tuning / học tăng cường; instruction tuning là fine-tuning trên dữ liệu dạng instruction–câu trả lời để mô hình biết làm theo yêu cầu) nhằm thích ứng với nhiều kịch bản | Prompt engineering (kỹ thuật thiết kế và tối ưu prompt): in-context learning (mô hình học nhiệm vụ từ ví dụ trong prompt, không cập nhật tham số), chain-of-thought prompting (CoT; để mô hình viết ra từng bước suy luận trước khi trả lời), điều phối luồng công việc (workflow); huấn luyện gọn nhẹ |
| *Trong hình:* training riêng cho từng cá thể | *Trong hình:* + post-… | |

## Slide 19

**Thay đổi về mô thức trong thời đại mô hình lớn**

- Chuyển dịch mô thức công nghệ: từ huấn luyện chuyên biệt cho từng nhiệm vụ riêng lẻ sang mô thức tập trung “pre-training + post-training” và “pre-training + prompting”
- Thống nhất mô thức nhiệm vụ: từ các dạng nhiệm vụ độc lập riêng rẽ tiến tới một dạng mô hình hóa sequence-to-sequence thống nhất

[1] Chung, H.W., et al. Scaling instruction-finetuned language models. JMLR, 2024.

## Slide 20

**Mô hình ngôn ngữ lớn**

- Mô hình ngôn ngữ lớn (LLM): dùng thuật toán mạnh, tiêu tốn rất nhiều năng lực tính toán để huấn luyện từ lượng dữ liệu khổng lồ ra một hàm phân phối xác suất phức tạp
    - Khối lượng tính toán lớn hơn, chi phí inference (chạy mô hình đã huấn luyện để sinh đầu ra) cao hơn
    - Khả năng tổng quát hóa mạnh hơn, xuất hiện emergent abilities (năng lực chỉ xuất hiện khi mô hình đủ lớn)

| Loại so sánh | Mô hình ngôn ngữ pre-trained (mô hình vừa và nhỏ, mô hình thông thường) | Mô hình ngôn ngữ quy mô lớn hơn (mô hình lớn tạo sinh) |
|---|---|---|
| Mô hình tiêu biểu | ELMo, BERT, GPT-1/2 | GPT-3, ChatGPT, LLaMA |
| Cấu trúc mô hình | RNN, Transformer | Transformer |
| Cơ chế attention | Hai chiều, một chiều | Một chiều |
| Cách huấn luyện | Mô hình tự mã hóa khử nhiễu | Sinh autoregressive |
| Loại nhiệm vụ thế mạnh | Hiểu, phán đoán | Sinh |
| Quy mô mô hình | Khoảng dưới 10B tham số | Khoảng 10B-100B tham số trở lên |
| Cách áp dụng cho nhiệm vụ hạ nguồn | Fine-tuning | Fine-tuning & prompting |
| Emergent abilities | Chuyển giao sang lĩnh vực ít dữ liệu | In-context learning, chain-of-thought prompting |

[1] Minaee, Shervin, et al. Large language models: A survey. arXiv preprint arXiv:2402.06196.

## Slide 21

**Mô hình ngôn ngữ lớn**

- Dữ liệu huấn luyện: đa dạng hóa
    - Không còn chỉ là văn bản ngôn ngữ tự nhiên mà là tổ hợp nhiều loại dữ liệu: văn bản ngôn ngữ tự nhiên, mã lập trình, công thức phân tử hóa học, thậm chí cả chuỗi gen, hay cả hình ảnh
- Cách huấn luyện: chuyển hẳn từ pre-training phân biệt (tiêu biểu là BERT) sang pre-training tạo sinh (tiêu biểu là GPT)
- Kiến trúc mô hình: từ Transformer hai chiều chuyển sang Transformer một chiều (Decoder-only)
- Cách ứng dụng: từ fine-tuning chuyển sang prompting thân thiện hơn
    - Cần ít mẫu hơn: từ chỗ bắt buộc phải có một lượng mẫu gán nhãn nhất định, sang few-shot (chỉ đưa vài ví dụ mẫu), thậm chí zero-shot (không đưa ví dụ mẫu nào)
    - Cách làm việc của prompting tiến gần tới hình thức đối thoại người–máy

## Slide 22

**Công nghệ then chốt**

- Ba giai đoạn xây dựng chính kinh điển: pre-training, instruction tuning, alignment

| | Pre-training | Instruction tuning | Alignment |
|---|---|---|---|
| Dữ liệu | Dữ liệu thô: văn bản, sách, trang web, code, v.v. ở quy mô hàng trăm tỷ | Instruction (yêu cầu/chỉ dẫn bằng ngôn ngữ tự nhiên giao cho mô hình) của người dùng có gán nhãn: hàng chục nghìn instruction bằng ngôn ngữ tự nhiên của người dùng và câu trả lời tương ứng | Cặp so sánh có gán nhãn: hàng trăm nghìn/hàng triệu cặp so sánh có gán nhãn, kèm instruction của người dùng |
| Mô hình | Base model (mô hình mới pre-train, chưa instruction tuning) | Mô hình SFT | Mô hình đã qua alignment |
| Mục tiêu | Học tri thức chuyên ngành/tổng quát | Nâng cao năng lực instruction following (khả năng làm đúng theo instruction) | Sinh instruction an toàn hơn |
| | Thời gian huấn luyện cỡ tháng | Thời gian huấn luyện cỡ ngày | Thời gian huấn luyện cỡ ngày |

## Slide 23

**Quy trình xây dựng mô hình lớn**

| | Pre-training | Instruction tuning | Alignment |
|---|---|---|---|
| Dữ liệu | Dữ liệu thô: văn bản, sách, trang web, code, v.v. ở quy mô hàng trăm tỷ | Instruction của người dùng có gán nhãn: hàng chục nghìn instruction bằng ngôn ngữ tự nhiên của người dùng và câu trả lời tương ứng | Cặp so sánh có gán nhãn: hàng trăm nghìn/hàng triệu cặp so sánh có gán nhãn, kèm instruction của người dùng |
| Mô hình | Base model | Mô hình SFT | Mô hình đã qua alignment |
| Mục tiêu | Học tri thức chuyên ngành/tổng quát | Nâng cao năng lực instruction following | Sinh instruction an toàn hơn |
| | Thời gian huấn luyện cỡ tháng | Thời gian huấn luyện cỡ ngày | Thời gian huấn luyện cỡ ngày |

## Slide 24

**Công nghệ then chốt 1: pre-training**

*Trong hình:* Thuật toán · Dữ liệu · Năng lực tính toán

## Slide 25

**Công nghệ then chốt 2: instruction tuning**

- Fine-tuning mô hình bằng dữ liệu instruction chất lượng cao (cho mô hình biết phải làm nhiệm vụ gì)
    - Giúp mô hình hiểu đặc điểm của nhiệm vụ, nâng cao rõ rệt hiệu năng trên từng nhiệm vụ
    - Cải thiện độ ổn định của prompting, giúp văn bản mô hình sinh ra dễ kiểm soát hơn
- Lấy “natural language inference” (NLI, suy luận ngôn ngữ tự nhiên) làm ví dụ để xây dựng dữ liệu huấn luyện instruction tuning

*Trong hình:* Fine-tuning thông thường · Instruction tuning

## Slide 26

**Công nghệ then chốt 2: instruction tuning**

- Các cách instruction tuning
    - Dựa vào tập dữ liệu có sẵn: con người thêm vào đầu vào một prompt chỉ rõ loại nhiệm vụ hiện tại làm tiền tố (instruction), rồi fine-tuning trên nhiều loại tập dữ liệu
    - Supervised fine-tuning dựa trên demonstration (câu trả lời mẫu do con người viết) của con người: mô hình được supervised fine-tuning trên các câu trả lời chất lượng cao do con người viết theo prompt (instruction)
- Điểm cốt lõi khi xây dựng dữ liệu
    - Số lượng nhiệm vụ
    - Độ đa dạng của nhiệm vụ

*Trong hình:* Dựa vào tập dữ liệu có sẵn (FLAN) · Dựa trên demonstration của con người (InstructGPT)

Wei, Jason, et al. "Finetuned Language Models are Zero-Shot Learners." International Conference on Learning Representations. 2021.

## Slide 27

**Công nghệ then chốt 2: instruction tuning**

- Instruction tuning FLAN: dùng instruction tuning để nâng cao năng lực zero-shot của mô hình
    - Chia 62 nhiệm vụ xử lý ngôn ngữ tự nhiên thành 12 nhóm
    - Với mỗi nhiệm vụ, xây dựng thủ công 10 mẫu instruction riêng biệt
- Mức cải thiện nhờ instruction tuning thể hiện rõ hiệu ứng mô hình lớn
    - Chỉ khi mô hình đạt quy mô khoảng chục tỷ tham số, instruction tuning mới mang lại cải thiện trên các nhiệm vụ ngoài mẫu

Wei, Jason, et al. "Finetuned Language Models are Zero-Shot Learners." International Conference on Learning Representations. 2021.

## Slide 28

**Công nghệ then chốt 3: alignment**

- LLM thường sinh ra câu trả lời vô ích, độc hại, không đúng sự thật
- Với chi phí nhân lực tương đối ít, dùng phương pháp học tăng cường để tiếp tục fine-tuning LLM
    - Để đầu ra của LLM được “alignment” theo ý định của con người, đưa ra câu trả lời được con người ưa thích
    - Đầu ra của mô hình ngôn ngữ càng khớp ý định con người, càng đúng chuẩn mực đạo đức thì mô hình nhận được càng nhiều reward (điểm thưởng trả về cho một câu trả lời)
- Giảm mạnh việc sinh ra thông tin có hại và sai lệch

*Trong hình:*

- Người dùng: hỏi cách đột nhập vào một ngôi nhà
- ChatGPT: chỉ ra việc này không phù hợp, có thể dẫn tới phạm tội
- Người dùng: đổi lời, nói chỉ muốn bảo vệ nhà mình khỏi bị đột nhập
- ChatGPT: đưa ra 7 lời khuyên cụ thể

## Slide 29

**Công nghệ then chốt 3: alignment**

- “Alignment” với sở thích, hệ giá trị, ý định, an toàn, v.v. của con người
    - Định nghĩa: định hướng hành vi của hệ thống trí tuệ nhân tạo để nó phù hợp với lợi ích và mục tiêu mong đợi của người thiết kế
- Nhà nước ban hành *Provisions on the Administration of Deep Synthesis Internet Information Services* (văn bản quản lý AI của Trung Quốc) và *Interim Measures for the Management of Generative Artificial Intelligence Services*

*Trong hình:* ChatGPT đã bị dùng để phạm tội: tấn công mạng, hướng dẫn phạm tội, v.v. · Không được dùng dịch vụ deep synthesis để tạo, sao chép, đăng tải, phát tán thông tin sai sự thật; không được dùng dịch vụ deep synthesis để tạo, sao chép, đăng tải, phát tán thông tin mà luật và văn bản pháp quy hành chính cấm

## Slide 30

**Công nghệ then chốt 3: alignment**

- Nguyên tắc: hữu ích, trung thực và vô hại
    - Phù hợp với văn hóa quốc gia và khu vực, phù hợp với luật pháp, phù hợp với đạo đức, tôn trọng sự thật và logic
- Điểm kỹ thuật chính:
    - Tập dữ liệu: tập dữ liệu SFT (13k), tập dữ liệu RM (33k), tập dữ liệu RL (31k)
    - Mô hình: SFT — mô hình supervised fine-tuning, RM — reward model (mô hình chấm điểm câu trả lời, học từ đánh giá của con người), RL — mô hình học tăng cường

Ouyang, Long, et al. "Training language models to follow instructions with human feedback." Advances in Neural Information Processing Systems 35 (2022): 27730-27744.

## Slide 31

**Công nghệ then chốt 3: alignment**

Bước 1: Supervised fine-tuning (SFT)

*Trong hình:* “Mặt trăng là gì?” · Dữ liệu lấy mẫu, thu thập qua API (giao diện lập trình ứng dụng) · Mô hình SFT · 175B GPT-3 · “Thiên thể hình cầu quay quanh Trái Đất” · Câu trả lời đích có gán nhãn

Ouyang, Long, et al. "Training language models to follow instructions with human feedback." Advances in Neural Information Processing Systems 35 (2022): 27730-27744.

## Slide 32

**Công nghệ then chốt 3: alignment**

Bước 2: Reward modeling (RM)

*Trong hình:* “Mặt trăng là gì?” · Mô hình SFT · 175B GPT-3 đã pre-train · “A. Mặt trăng là thiên thể gần Trái Đất nhất trong hệ Mặt Trời.” … “D. Mặt trăng là vệ tinh của Trái Đất, đường kính xấp xỉ 1/4 Trái Đất.” · Mô hình 6B (rẻ + ổn định) · Mô hình RM · Mô hình xếp hạng (câu hỏi + câu trả lời → xuất điểm) · D>C>A=B

Ouyang, Long, et al. "Training language models to follow instructions with human feedback." Advances in Neural Information Processing Systems 35 (2022): 27730-27744.

## Slide 33

**Công nghệ then chốt 3: alignment**

Bước 2: Reward modeling (RM)

*Trong hình:* “Mặt trăng là gì?” · Mô hình SFT · 175B GPT-3 đã pre-train · “A. Mặt trăng là thiên thể gần Trái Đất nhất trong hệ Mặt Trời.” … “D. Mặt trăng là vệ tinh của Trái Đất, đường kính xấp xỉ 1/4 Trái Đất.” · Mô hình RM · D>C>A=B

*Chú thích công thức:* hai câu trả lời ứng với câu hỏi x trong tập dữ liệu, và yw được xếp hạng cao hơn yl · Câu hỏi trong tập dữ liệu · Hiệu điểm do mô hình RM chấm

Ouyang, Long, et al. "Training language models to follow instructions with human feedback." Advances in Neural Information Processing Systems 35 (2022): 27730-27744.

## Slide 34

**Công nghệ then chốt 3: alignment**

Bước 3: Reinforcement learning (RL)

*Trong hình:* “Siêu dẫn ở nhiệt độ phòng là gì?” · yl · Mô hình SFT · Mô hình RL · Mô hình RM · PPO

Ghi chú: PPO, Proximal Policy Optimization (thuật toán RL giới hạn mỗi bước cập nhật policy để huấn luyện ổn định)

Ouyang, Long, et al. "Training language models to follow instructions with human feedback." Advances in Neural Information Processing Systems 35 (2022): 27730-27744.

## Slide 35

**Công nghệ then chốt 3: alignment**

Bước 3: Reinforcement learning (RL)

*Trong hình:* “Siêu dẫn ở nhiệt độ phòng là gì?” · yl · Mô hình SFT · Mô hình RL · Mô hình RM · PPO · Hàm mất mát của mô hình ngôn ngữ gốc · InstructGPT

Ghi chú: PPO, Proximal Policy Optimization

Ouyang, Long, et al. "Training language models to follow instructions with human feedback." Advances in Neural Information Processing Systems 35 (2022): 27730-27744.

## Slide 36

**Công nghệ then chốt 3: alignment**

## Slide 37

**Scaling law (Scaling Law; quy luật hiệu năng tăng theo kích thước mô hình, dữ liệu và năng lực tính toán) của LLM**

- Quan hệ giữa hiệu năng mô hình với ba yếu tố: kích thước mô hình, quy mô dữ liệu và năng lực tính toán
    - Khi số tham số và quy mô dữ liệu pre-training liên tục tăng, năng lực mô hình và hiệu quả trên nhiệm vụ cũng được cải thiện theo
    - Chinchilla khuyến nghị: mô hình 10B dùng 200B tokens (1:20)

[1] Kaplan, Jared, et al. Scaling laws for neural language models. arXiv preprint arXiv:2001.08361.

## Slide 38

**Emergent abilities (Emergent Abilities) của LLM**

- Khi số tham số của mô hình ngôn ngữ đạt tới một quy mô nhất định, một số năng lực (suy luận ngôn ngữ) đột ngột tăng mạnh
- Là những năng lực không quan sát thấy ở mô hình nhỏ nhưng thể hiện ra ở mô hình lớn

*Trong hình:* Các đại diện của emergent abilities: in-context learning · suy luận chain-of-thought

[1] Wei, Jason, et al. Emergent Abilities of Large Language Models. TMLR, 2022.

## Slide 39

**Hallucination (Hallucination; mô hình sinh nội dung sai sự thật hoặc không bám nguồn) của LLM**

- Định nghĩa: văn bản do mô hình sinh ra không bám sát văn bản gốc (Faithfulness) hoặc không đúng sự thật (Factualness)
- Mặt ưu thế: thể hiện tính sáng tạo và khả năng tư duy phân kỳ của mô hình lớn
- Ảnh hưởng tiềm ẩn: làm giảm độ tin cậy của mô hình, dễ bị tấn công, bị lạm dụng (như sinh nội dung độc hại và tung tin đồn), gây ô nhiễm internet

*Trong hình:*

- Hỏi: Lu Xun và Zhou Shuren có phải là cùng một người không?
- Đáp: Không. Lu Xun và Zhou Shuren là hai người khác nhau. Lu Xun là bậc thầy văn học hiện đại Trung Quốc, nổi tiếng với phong cách văn chương độc đáo và những câu chuyện cuốn hút. Zhou Shuren là nhà văn nổi tiếng đương đại của Trung Quốc, được đánh giá cao nhờ ngòi bút sắc sảo và óc quan sát tinh tế.

[1] Huang, Lei, et al. A survey on hallucination in large language models: Principles, taxonomy, challenges, and open questions. arXiv preprint arXiv:2311.05232

## Slide 40

**Bản đồ năng lực của mô hình lớn**

[1] Minaee, Shervin, et al. Large language models: A survey. arXiv preprint arXiv:2402.06196.

## Slide 41

**Từ GPT-3 đến ChatGPT**

- GPT-1: mô hình hóa autoregressive một chiều + supervised fine-tuning, khám phá năng lực giải nhiệm vụ ngôn ngữ tự nhiên trong mô thức “pre-training + fine-tuning”
- GPT-2: mô hình hóa autoregressive một chiều + nhiều dữ liệu hơn, mô hình lớn hơn, khám phá năng lực giải nhiều nhiệm vụ dựa trên prompt bằng ngôn ngữ tự nhiên
- GPT-3: khám phá hiệu quả của mô hình ngôn ngữ cỡ hàng trăm tỷ tham số, đề xuất cách giải nhiệm vụ dựa trên “in-context learning”
- GPT-3.5/ChatGPT: instruction tuning + phản hồi của con người + tối ưu hóa cho hội thoại
- GPT-4: năng lực multimodal, năng lực hiểu và xử lý ngữ cảnh dài hơn, huấn luyện và dự đoán hiệu quả hơn, kịch bản ứng dụng giá trị cao rộng hơn

*Trong hình:* 45TB dữ liệu · Quá trình tiến hóa của dòng GPT

## Slide 42

**Quá trình tiến hóa các phiên bản của dòng GPT**

- GPT-4 đạt trình độ tương đương con người trên nhiều benchmark (bộ bài kiểm tra chuẩn để so sánh mô hình) chuyên môn và học thuật, trong đó vượt qua kỳ thi luật sư mô phỏng với điểm nằm trong khoảng 10% cao nhất
- Năng lực xử lý multimodal mạnh mở rộng phạm vi ứng dụng của GPT-4, đồng thời các vấn đề hallucination khi sinh và vấn đề an toàn đều được cải thiện đáng kể

OpenAI công bố hướng dẫn sử dụng GPT-4

- Viết instruction rõ ràng
- Cung cấp văn bản tham khảo
- Chia nhiệm vụ phức tạp thành các nhiệm vụ con đơn giản hơn
- Cho mô hình thời gian để “suy nghĩ”
- Dùng công cụ bên ngoài
- Kiểm thử các thay đổi một cách có hệ thống

[1] Achiam, Josh, et al. Gpt-4 technical report. arXiv preprint arXiv:2303.08774.
[2] OpenAI. Prompt engineering. <https://platform.openai.com/docs/guides/prompt-engineering>.

## Slide 43

**Dòng mô hình lớn Llama**

- Mô hình autoregressive mã nguồn mở, dựa trên kiến trúc Transformer, số tham số từ 7B đến 405B
- Giấy phép thương mại: Llama 1 không được dùng thương mại miễn phí, Llama 2 và Llama 3 được dùng thương mại (cần xin giấy phép thương mại)

| Đặc điểm phiên bản | Llama-1 | Llama-2 | Llama-3 | Llama-3.1 | Llama-3.2 |
|---|---|---|---|---|---|
| Quy mô mô hình | 7B-65B | 7B-70B | 8B-70B | 8B-405B | 1B-90B |
| Quy mô dữ liệu | 1.4T | 2T | 15T | 15T | 9T |
| Multimodal | × | × | × | × | √ |
| Đa ngôn ngữ | × | × | × | √ | √ |
| Gọi công cụ (tool calling) | × | × | × | √ | √ |
| Mô thức huấn luyện | Pre-training | Pre-training + instruction tuning + RLHF (reinforcement learning from human feedback; học tăng cường từ phản hồi của con người) | Pre-training + instruction tuning + DPO | Pre-training + instruction tuning + DPO | Pre-training + instruction tuning + DPO |
| Độ dài ngữ cảnh (context length) | 2K | 4k | 8k | 131K | 131K |
| Thay đổi chính | -- | Bổ sung post-training | Mở rộng pre-training | 1. Tăng quy mô mô hình; 2. Bổ sung năng lực đa ngôn ngữ và dùng công cụ; 3. Mở rộng độ dài ngữ cảnh | 1. Bổ sung mô hình chạy trên thiết bị đầu cuối; 2. Bổ sung năng lực multimodal |

[1] Touvron, Hugo, et al. Llama: Open and efficient foundation language models. arXiv preprint arXiv:2302.13971.
[2] Touvron, Hugo, et al. Llama 2: Open foundation and fine-tuned chat models. arXiv preprint arXiv:2307.09288.
[3] Dubey, Abhimanyu, et al. The llama 3 herd of models. arXiv preprint arXiv:2407.21783.

## Slide 44

**Dòng mô hình lớn Llama**

- Dữ liệu huấn luyện: CommonCrawl, C4, Github, Wikipedia, books, ArXiv, and StackExchange, v.v.
- Địa chỉ mã nguồn mở: <https://github.com/facebookresearch/llama>
- Llama 3.1 405B vượt GPT-3.5 Turbo trong nhiều đợt đánh giá rộng, và đạt điểm cao hơn GPT-4 0125 trên phần lớn các benchmark

[1] Dubey, Abhimanyu, et al. The llama 3 herd of models. arXiv preprint arXiv:2407.21783.

## Slide 45

**Phân loại mô hình AI lớn của Trung Quốc và các trường hợp tiêu biểu**

- “Trăm mô hình đại chiến”: theo thống kê chưa đầy đủ, tính đến cuối tháng 4/2024, Trung Quốc đã ra mắt tổng cộng 305 mô hình lớn

[1] Nhóm SuperGLUE. Báo cáo thường niên 2024 về đánh giá benchmark mô hình lớn tiếng Trung.

## Slide 46

**Dòng mô hình lớn Qwen**

- Qwen (Tongyi Qianwen) là mô hình ngôn ngữ pre-trained do Alibaba Cloud phát triển, thực hiện các nhiệm vụ như hiểu, sinh và giải thích ngôn ngữ của con người, hình ảnh và tài liệu, mang lại trải nghiệm tương tác phong phú cho người dùng trong viết nội dung sáng tạo, trợ lý văn phòng, trợ lý học tập, đời sống giải trí, v.v.
- Có các năng lực như hiểu tiếng Trung và tiếng Anh, suy luận toán học, hiểu code

*Trong hình:* Qwen-Audio · Qwen-Audio-Chat

[1] Bai, Jinze, et al. Qwen technical report. arXiv preprint arXiv:2309.16609.
[2] Yang, An, et al. Qwen2 technical report. arXiv preprint arXiv:2407.10671.

## Slide 47

**Quá trình tiến hóa các phiên bản của dòng Qwen**

- Qwen1.5: Model Scaling mở rộng theo cả hướng lớn hơn và nhỏ hơn, MoE (mixture of experts; kiến trúc chỉ kích hoạt một số “chuyên gia” con cho mỗi token), AWQ/GGUF
- Qwen2: tăng cường đa ngôn ngữ, tăng cường năng lực xử lý văn bản dài
- Qwen2.5: tăng cường năng lực toán và code, tăng cường đa ngôn ngữ
- Scaling
    - Qwen: 1.8B, 7B, 14B, and 72B models
    - Qwen1.5: 0.5B, 1.8B, 4B, 14BA2.7B, 7B, 14B, 32B, 72B, and 110B models
    - Qwen2: 0.5B, 1.5B, 7B, 57A14B, and 72B models
    - Qwen2.5: 0.5B, 1.5B, 3B, 7B, 14B, 32B, and 72B models

Đặc điểm qua các lần cập nhật phiên bản

- Tối ưu cấu trúc (MoE nâng cao hiệu quả huấn luyện)
- Mở rộng số lượng và nâng cao chất lượng dữ liệu pre-training
- Làm phong phú các nhiệm vụ và lĩnh vực trong giai đoạn Post-training
- Mở rộng độ dài cửa sổ (cả về dữ liệu huấn luyện lẫn chiến lược huấn luyện)
- Mở rộng các hướng ngôn ngữ và tăng cường năng lực đa ngôn ngữ
- Tăng cường các năng lực chuyên biệt (huấn luyện mô hình chuyên gia + dùng mô hình chuyên gia kéo base model đi lên)
- Mở rộng modality (loại dữ liệu: văn bản, ảnh, âm thanh, video) (Qwen-VL, Qwen-Audio)

## Slide 48

**Dòng mô hình lớn DeepSeek**

2023.11

1. DeepSeek LLM
    - Số tham số: 70B, 67B tham số
    - Kiến trúc: mô hình Transformer Dense (dense: mọi tham số đều được dùng cho mỗi token)
    - Dữ liệu huấn luyện: kho ngữ liệu tiếng Trung và tiếng Anh 2T token
    - Mô thức huấn luyện: theo mô thức huấn luyện mô hình lớn tiêu chuẩn pre-training + SFT + DPO
    - Hiệu năng: mô hình lớn đầu tiên của DeepSeek, lấy dòng Llama2 làm đối chuẩn. Bản 67B Base vượt Llama2 70B Base ở suy luận, viết code, v.v. Kiến trúc mô hình dùng cấu trúc Dense

## Slide 49

**Dòng mô hình lớn DeepSeek**

2023.11 · 2024.5

1. DeepSeek LLM
    - Số tham số: 70B, 67B tham số
    - Kiến trúc: mô hình Transformer Dense
    - Dữ liệu huấn luyện: kho ngữ liệu tiếng Trung và tiếng Anh 2T token
    - Mô thức huấn luyện: theo mô thức huấn luyện mô hình lớn tiêu chuẩn pre-training + SFT + DPO
    - Hiệu năng: mô hình lớn đầu tiên của DeepSeek, lấy dòng Llama2 làm đối chuẩn. Bản 67B Base vượt Llama2 70B Base ở suy luận, viết code, v.v. Kiến trúc mô hình dùng cấu trúc Dense
2. DeepSeek-V2
    - Số tham số: 236B tham số, 21B tham số được kích hoạt
    - Kiến trúc: đưa vào kiến trúc DeepSeekMoE (mixture of experts). Đưa vào MLA (Multi-head Latent Attention)
    - Dữ liệu huấn luyện: kho ngữ liệu 8.1T token
    - Mô thức huấn luyện: theo mô thức tiêu chuẩn pre-training + SFT + học tăng cường
    - Đặc điểm: hiệu năng ngang GPT-4 Turbo. MLA giúp tiết kiệm hơn 90% KV cache, tốc độ inference tăng hơn 5 lần. Kiến trúc MoE giúp khi tăng số tham số thì chi phí inference gần như không đổi, chi phí huấn luyện giảm mạnh, nâng cao năng lực mô hình

## Slide 50

**Dòng mô hình lớn DeepSeek**

2024.5 · 2024.9

2. DeepSeek-V2
    - Số tham số: 236B tham số, 21B tham số được kích hoạt
    - Kiến trúc: đưa vào kiến trúc DeepSeekMoE (mixture of experts). Đưa vào MLA (Multi-head Latent Attention)
    - Dữ liệu huấn luyện: kho ngữ liệu 8.1T token
    - Mô thức huấn luyện: theo mô thức tiêu chuẩn pre-training + SFT + học tăng cường
    - Đặc điểm: hiệu năng ngang GPT-4 Turbo. MLA giúp tiết kiệm hơn 90% KV cache, tốc độ inference tăng hơn 5 lần. Kiến trúc MoE giúp khi tăng số tham số thì chi phí inference gần như không đổi, chi phí huấn luyện giảm mạnh, nâng cao năng lực mô hình
3. DeepSeek-V2.5
    - Dựa trên V2, chủ yếu tối ưu năng lực nhiệm vụ tổng quát và năng lực code

## Slide 51

**Dòng mô hình lớn DeepSeek**

2024.9 · 2024.12

3. DeepSeek-V2.5
    - Dựa trên V2, chủ yếu tối ưu năng lực nhiệm vụ tổng quát và năng lực code
4. DeepSeek-V3
    - Số tham số: 671B tham số, 37B tham số được kích hoạt
    - Dữ liệu huấn luyện: kho ngữ liệu 14.8T token
    - Kiến trúc: trên nền V2, đưa vào Auxiliary-loss-free strategy để cân bằng tải giữa các chuyên gia. Đưa vào Multi-Token Prediction training để nâng cao hiệu năng mô hình và tăng tốc inference. Đưa vào độ chính xác hỗn hợp FP8 để giảm chi phí huấn luyện và inference
    - Dữ liệu huấn luyện: kho ngữ liệu 14.8T token
    - Mô thức huấn luyện: theo mô thức huấn luyện mô hình lớn tiêu chuẩn pre-training + SFT + DPO
    - Đặc điểm: hiệu năng vượt các dòng chủ lưu Llama3 và Qwen2.5, đồng thời chi phí huấn luyện và chi phí inference giảm mạnh

## Slide 52

**Dòng mô hình lớn DeepSeek**

2024.12 · 2025.01

4. DeepSeek-V3
    - Số tham số: 671B tham số, 37B tham số được kích hoạt
    - Dữ liệu huấn luyện: kho ngữ liệu 14.8T token
    - Kiến trúc: trên nền V2, đưa vào Auxiliary-loss-free strategy để cân bằng tải giữa các chuyên gia. Đưa vào Multi-Token Prediction training để nâng cao hiệu năng mô hình và tăng tốc inference. Đưa vào độ chính xác hỗn hợp FP8 để giảm chi phí huấn luyện và inference
    - Dữ liệu huấn luyện: kho ngữ liệu 14.8T token
    - Mô thức huấn luyện: theo mô thức huấn luyện mô hình lớn tiêu chuẩn pre-training + SFT + DPO
    - Đặc điểm: hiệu năng vượt các dòng chủ lưu Llama3 và Qwen2.5, đồng thời chi phí huấn luyện và chi phí inference giảm mạnh
5. DeepSeek-R1
    - Base model: DeepSeek-V3-Base
    - Dữ liệu huấn luyện: kho ngữ liệu 14.8T token
    - Mô thức huấn luyện: huấn luyện nhiều giai đoạn trực tiếp trên base model, huấn luyện khởi động nguội (cold start) và học tăng cường
    - Đặc điểm: lần đầu đạt năng lực suy luận kiểu GPT4-O1

## Slide 53

**Triển khai mô hình lớn**

- Loại mô hình lớn:
    - LLM: Qwen
    - Mô hình multimodal: MiniCPM
- Cách triển khai:
    - Gọi API
    - Triển khai cục bộ

## Slide 54

**Triển khai mô hình lớn (ví dụ chức năng)**

## Slide 55

**Triển khai mô hình lớn (gọi API)**

- Lấy quyền gọi mô hình lớn
    - Qwen (Tongyi Qianwen): <https://help.aliyun.com/zh/dashscope/developer-reference/quick-start>
    - DeepSeek: <https://www.deepseek.com>
    - Llama: <https://github.com/Meta-Llama/llama>
    - Zhipu AI: <https://open.bigmodel.cn/>
    - OpenAI: <https://platform.openai.com/playground>
    - Khác: ERNIE Bot (Wenxin Yiyan), Baichuan

\*Quy trình cơ bản: kích hoạt dịch vụ để nhận API-KEY (kèm hạn mức tính toán được tặng), rồi dùng API Key để gọi dịch vụ (riêng OpenAI cần dùng VPN hoặc proxy nếu ở Trung Quốc đại lục)

## Slide 56

**Triển khai mô hình lớn (gọi API)**

- Gọi qua giao diện đồ họa GUI (phù hợp để thử từng ví dụ)
    - <https://help.aliyun.com/zh/dashscope/developer-reference/quick-start>
    - <https://huggingface.co/spaces/Qwen/Qwen2-72B-Instruct>

## Slide 57

**Triển khai mô hình lớn (gọi API)**

- Gọi bằng code:
- Chuẩn bị môi trường (tùy chọn):
    - Công cụ phát triển VS Code: <https://code.visualstudio.com/>
    - Quản lý môi trường Python bằng Miniconda: <https://docs.anaconda.com/free/miniconda/miniconda-install>

## Slide 58

**Triển khai mô hình lớn (triển khai cục bộ)**

- Nền tảng mã nguồn mở để triển khai mô hình lớn cục bộ: Ollama, LM Studio
- Gọi qua Web và API: OpenAI, Dashscope API
- Triển khai riêng tư tại chỗ (on-premises) cho mô hình lớn: Flask, MindIE

<https://ollama.com/>

<https://lmstudio.ai/>

## Slide 59

**Triển khai mô hình lớn (triển khai cục bộ)**

- Yêu cầu cấu hình

*Trong hình:* Yêu cầu bộ nhớ GPU (VRAM) · Yêu cầu ổ cứng

## Slide 60

**Triển khai mô hình lớn (triển khai cục bộ)**

- 1\. Cài đặt Ollama
    - Vào trang web chính thức: mở trình duyệt, truy cập trang web chính thức của Ollama.
    - Chọn phiên bản: chọn gói cài đặt phù hợp với hệ điều hành của bạn. Ollama hỗ trợ MacOS, Linux và Windows
    - Tải gói cài đặt: bấm nút Download để tải gói cài đặt Ollama phù hợp với thiết bị của bạn
    - Cài đặt Ollama: tùy theo định dạng gói cài đặt đã tải, chạy trình cài đặt hoặc giải nén vào thư mục bạn chọn
- 2\. Chạy một mô hình cụ thể (`ollama run qwen2:7b`)

## Slide 61

**Triển khai mô hình lớn (triển khai cục bộ)**

- 1\. Cài đặt Ollama
- 2\. Chạy một mô hình cụ thể (`ollama run qwen2:7b`)

## Slide 62

**Triển khai mô hình lớn (triển khai cục bộ)**

- 1\. Cài đặt Ollama
- 2\. Chạy một mô hình cụ thể (`ollama run qwen2:7b`)

Nâng cao:

1. Dùng open web UI để cấu hình WebUI
2. Dựng kho tri thức cục bộ bằng AnythingLLM

## Slide 63

**Mục lục**

- Tổng quan về mô hình lớn
    - Tổng quan quá trình phát triển
    - Phạm vi của mô hình lớn
- Mô hình pre-trained
    - Các loại chính
    - Kiến trúc mô hình
- Mô hình quy mô lớn
    - Thay đổi về mô thức
    - Công nghệ then chốt
    - Các đại diện chính
    - Cách triển khai
- Mở rộng khái niệm
    - Mô hình lớn chuyên ngành
    - Foundation model multimodal
    - Foundation model cho agent

## Slide 64

**Mở rộng khái niệm mô hình lớn**

*Trong hình:*

- Mô hình lớn chuyên ngành: người dùng · mô hình lớn · dữ liệu chuyên ngành
- Mô hình lớn multimodal: người dùng · mô hình lớn · dữ liệu multimodal
- LLM agent: người dùng · agent · môi trường

## Slide 65

**Mô hình lớn chuyên ngành**

- Mô thức cơ bản: tăng cường bằng huấn luyện chuyên ngành trên nền mô hình lớn đa dụng; tính chuyên môn cao, đưa vào ứng dụng nhanh, hiệu quả chi phí cao, dễ tuân thủ quy định
- Cách huấn luyện: huấn luyện trên dữ liệu chuyên ngành (tiếp tục pre-training, fine-tuning, prompt), retrieval augmentation (truy xuất tài liệu liên quan rồi mới sinh câu trả lời), v.v.
- Các lĩnh vực thường gặp: giáo dục, y tế, pháp luật, tài chính, v.v.

[1] Ling, Chen, et al. Domain specialization as the key to make large language models disruptive: A comprehensive survey. arXiv preprint arXiv:2305.18703.

## Slide 66

**Những phát triển tiên tiến nhất của mô hình lớn multimodal**

- Bước đột phá về năng lực của mô hình lớn multimodal trở thành xu hướng và tâm điểm mới trong những phát triển tiên tiến nhất của mô hình lớn
- Mở rộng đáng kể giới hạn năng lực và kịch bản ứng dụng của mô hình lớn, là động cơ then chốt tiếp theo cho bước nhảy về trí tuệ

A Survey on Multimodal Large Language Models (<https://arxiv.org/pdf/2306.13549>)

## Slide 67

**Ví dụ về năng lực của mô hình lớn multimodal**

## Slide 68

**Những phát triển tiên tiến nhất của mô hình lớn multimodal**

Tóm tắt kỹ thuật

- Mục tiêu chính: học từ dữ liệu lớn và phản hồi của con người, tương tác với người dùng qua hội thoại, xử lý được thông tin multimodal và nhiều loại nhiệm vụ, năng lực suy luận sâu và vận dụng kiến thức thông thường tăng mạnh
- Công nghệ then chốt: kiến trúc mô hình multimodal, instruction following multimodal, suy luận multimodal, triển khai gọn nhẹ, alignment multimodal, v.v.

Các mốc sự kiện

- 2023/03/15: OpenAI công bố mô hình hội thoại multimodal GPT-4
- 2023/09/20: OpenAI công bố mô hình sinh ảnh từ văn bản DALL·E 3
- 2023/09/25: ChatGPT tích hợp toàn diện năng lực multimodal
- 2023/12/06: Google công bố mô hình multimodal Gemini
- 2024/03/04 : Anthropic công bố mô hình multimodal Claude 3
- 2024/05/13: OpenAI công bố mô hình multimodal nguyên bản GPT-4o

Thay đổi về mô thức làm việc

*Trong hình:* văn bản → mô hình ngôn ngữ lớn → văn bản; văn bản, giọng nói, hình ảnh, video, … → mô hình lớn multimodal → văn bản, giọng nói, hình ảnh, video, …

[1] Fei, Hao, et al. From Multimodal LLM to Human-level AI: Modality, Instruction, Reasoning and Beyond. ACM MM, 2024.
<https://mllm2024.github.io/ACM-MM2024/>

## Slide 69

**Những phát triển tiên tiến nhất của mô hình lớn multimodal**

- Cách làm việc chung: mã hóa multimodal > mô-đun hợp nhất đặc trưng > decoder multimodal, hỗ trợ đầu vào multimodal và sinh multimodal
- Các modality thường gặp: văn bản, hình ảnh, video, giọng nói, v.v.

[1] Zhang, Duzhen, et al. Mm-llms: Recent advances in multimodal large language models. arXiv preprint arXiv:2401.13601.

## Slide 70

**Các kiến trúc tiêu biểu của mô hình lớn multimodal**

Kiến trúc lấy LLM làm trung tâm

- Visual-ChatGPT
- HuggingGPT
- MM-REACT
- LLaVA-Plus
- …

*Trong hình:* người dùng → LLM → các mô-đun hạ nguồn …

Kiến trúc multimodal hợp nhất: loại kiến trúc của phần lớn mô hình lớn multimodal

*Trong hình:* đầu vào (văn bản, multimodal) → encoder multimodal → LLM → decoder multimodal → đầu ra (văn bản, multimodal)

## Slide 71

**Các bài hướng dẫn về hướng nghiên cứu tiên tiến của mô hình lớn multimodal (CVPR & MM & COLING)**

Slide bài giảng + video

<https://mllm2024.github.io/CVPR2024>

## Slide 72

**LLM agent**

“Jarvis” ở khắp mọi nơi: LLM agent cho thấy triển vọng ứng dụng rộng lớn

- OpenAI Operator: <https://openai.com/index/introducing-operator>
- Anthropic Claude: <https://www.anthropic.com/claude>
- Manus AI: <https://manus.im/>

## Slide 73

**LLM agent**

- Hệ thống được xây dựng trên mô hình lớn, có thể điều hướng một cách linh động quy trình của chính nó và việc dùng công cụ, đồng thời điều chỉnh thao tác của mình theo phản hồi thời gian thực [1]

Mô hình ngôn ngữ lớn (multimodal): người dùng · mô hình lớn

- Bên cung cấp năng lực tổng quát
    - Xử lý chuỗi dài
    - Suy luận chain-of-thought
    - Hiểu ý định ở phạm vi rộng

LLM agent (hệ thống): người dùng · agent · môi trường

- Có năng lực tự chủ và tiến hóa
    - Tương tác với môi trường: nhận thức và hiểu, lập kế hoạch và ra quyết định, thực thi hành động
    - Vận hành bền bỉ: tự phản tư để tối ưu, lặp lại để tiến hóa, phòng vệ an toàn
- Cập nhật tri thức: kho tri thức, kho kinh nghiệm
- Tích hợp công cụ: APP, API, hàm

[1] Anthropic. Building effective agents. Published Dec 19, 2024

## Slide 74

**LLM agent**

| Điều phối luồng công việc | Foundation model cho agent |
|---|---|
| Điều phối LLM và công cụ theo đường đi định sẵn, giống một script (tệp lệnh chạy được) tự động hóa phức tạp. Thường hiện thực bằng Prompt | Tự điều hướng quá trình hành động và việc dùng công cụ, lập kế hoạch và cập nhật đường đi một cách động, giữ quyền kiểm soát cách hoàn thành nhiệm vụ. Thường mở rộng năng lực bằng huấn luyện |
| Xem AI như một thành phần có thể điều phối | Trao cho AI nhiều quyền tự chủ hơn, có thể tiến hóa |

## Slide 75

**Đột phá giới hạn năng lực của mô hình lớn**

- Bước đột phá về năng lực của LLM agent trở thành tâm điểm mới, mở rộng đáng kể giới hạn năng lực và kịch bản ứng dụng của mô hình lớn

| L1: Chatbots | L2: Reasoners | L3: Agents | L4: Innovators | L5: Organizations |
|---|---|---|---|---|
| GPT-4, DeepSeek-V3 | o1, DeepSeek-R1 | Operator, Deep Research | Đổi mới và phát minh | Tổ chức và quản lý |
| Tương tác ngôn ngữ tổng quát | Tư duy và suy luận sâu | Tự chủ hành động và tương tác | | |
| Ứng dụng: hỏi đáp, hội thoại, tìm kiếm | Ứng dụng: toán học, suy luận logic | Ứng dụng: gọi công cụ, thao tác, khám phá | | |

Ngôn ngữ -> hành động: từ trí tuệ nội dung đến trí tuệ hành vi, tạo mắt xích then chốt hướng tới artificial general intelligence (AGI; AI có năng lực tổng quát ngang con người)

## Slide 76

**Tài liệu đọc thêm**

《大模型开发全流程》 (The Full Workflow of Large Model Development)

Khóa học mô hình lớn trên nền tảng phần cứng/phần mềm nội địa Trung Quốc: 54 bài học, 26 sổ tay thực hành

<https://www.hiascend.com/edu/growth/lm-development>

## Slide 77

**Xin cảm ơn!**

zhangzs@sjtu.edu.cn

<https://bcmi.sjtu.edu.cn/~zhangzs>
