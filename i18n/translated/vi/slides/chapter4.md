# Suy luận toán học với LLM

[PDF gốc](https://github.com/Lordog/dive-into-llms/blob/f84c04268794ef94f8949808bbc14ab8636763a0/documents/chapter4/math.pdf)

## Slide 1

**Suy luận toán học với LLM**

陈星宇 (Chen Xingyu)

## Slide 2

**Mục lục**

1. Giới thiệu về suy luận toán học
2. Long-reasoning model (mô hình sinh chuỗi suy luận rất dài trước khi trả lời, như o1, R1)
3. Mô hình lớn chuyên toán
4. Học bằng distillation (dùng đầu ra của mô hình lớn – teacher – để huấn luyện mô hình nhỏ – student)
5. Đánh giá năng lực toán học

## Slide 3

**Giới thiệu về suy luận toán học**

Suy luận toán học: năng lực của LLM (mô hình ngôn ngữ lớn) giải bài toán bằng phân tích logic, biến đổi ký hiệu và suy diễn nhiều bước; mô hình cần hiểu các khái niệm toán học (như đại số, hình học) và sinh ra đáp án đúng

Năng lực then chốt:

- Suy luận nhiều bước: tách bài toán phức tạp thành các bước con
- Hiểu ký hiệu: xử lý ký hiệu và công thức trừu tượng
- Tính toán: thực hiện phép tính chính xác

Ứng dụng: giải đề thi học sinh giỏi toán, hỗ trợ học tập, suy diễn công thức trong nghiên cứu khoa học

## Slide 4

**Làm thế nào để LLM suy luận toán học?**

- Chain-of-thought[1] (CoT; để mô hình viết ra từng bước suy luận trước khi trả lời): sinh tường minh các bước suy luận
- Tìm kiếm trên cây: Monte Carlo tree search[2] (MCTS; tìm kiếm trên cây bằng mô phỏng ngẫu nhiên): kết hợp process reward model (PRM; reward model chấm từng bước suy luận, không chỉ đáp án cuối) để khám phá các hướng giải khác nhau
- Self-consistency[3] (tự nhất quán): lấy mẫu nhiều lần các đường suy luận khác nhau, bỏ phiếu chọn đáp án xuất hiện nhiều nhất để giảm lỗi
- Bổ sung công cụ: công cụ bên ngoài: gọi máy tính cầm tay (calculator) để xử lý phép tính phức tạp, tránh lỗi tính toán
- Hỗ trợ bằng chương trình: sinh code (ví dụ Python) để thực hiện phép tính toán học

[1] Kojima T, Gu S S, Reid M, et al. Large language models are zero-shot reasoners[J]. Advances in neural information processing systems, 2022, 35: 22199-22213.

[2] Guan X, Zhang L L, Liu Y, et al. rStar-Math: Small LLMs Can Master Math Reasoning with Self-Evolved Deep Thinking[J]. arXiv preprint arXiv:2501.04519, 2025.

[3] Wang X, Wei J, Schuurmans D, et al. Self-consistency improves chain of thought reasoning in language models[J]. arXiv preprint arXiv:2203.11171, 2022.

## Slide 5

**Long-reasoning model**

- Long-reasoning model: mô hình sinh chain-of-thought dài khi suy luận
- Đại diện tiêu biểu: OpenAI-o1[1], DeepSeek-R1[2]
- Đặc điểm của chain-of-thought:
    - Tự phản tư
    - Đổi hướng suy nghĩ
    - Kiểm chứng đáp án và sửa lỗi
- Tăng độ dài phần sinh ra lúc inference (chạy mô hình đã huấn luyện để sinh đầu ra) giúp mở rộng không gian tìm kiếm, nhờ đó cải thiện hiệu năng suy luận toán học
- Chain-of-thought lồng ghép các chiến lược suy luận giống con người

[1] https://openai.com/index/introducing-openai-o1-preview/

[2] Guo D, Yang D, Zhang H, et al. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning[J]. arXiv preprint arXiv:2501.12948, 2025.

## Slide 6

**Long-reasoning model**

Đặc điểm của chain-of-thought:

- Tự phản tư
- Đổi hướng suy nghĩ
- Kiểm chứng đáp án và sửa lỗi

Ví dụ: OpenAI-o1

*Chú thích trong hình: Tự sửa lỗi · Đổi hướng suy nghĩ · Tự phản tư*

## Slide 7

**Mô hình lớn chuyên toán**

- Mô hình lớn chuyên toán: mô hình lớn được tối ưu hóa riêng cho các nhiệm vụ suy luận toán học
- Đại diện tiêu biểu: DeepSeek-Math[1]; Qwen2.5-Math[2]
- Tập huấn luyện: DeepMath-103K[3]
- Tập dữ liệu đánh giá:
    - GSM8k[4]: tập dữ liệu toán chất lượng cao ở mức tiểu học, gồm 8.5k mẫu
    - MATH[5]: tập dữ liệu ở mức thi học sinh giỏi toán trung học phổ thông, gồm 12 500 mẫu
    - AIME: American Invitational Mathematics Examination (kỳ thi toán mời của Mỹ), tổ chức hằng năm, mỗi kỳ gồm 30 bài, độ khó cấp olympic

[1] Shao Z, Wang P, Zhu Q, et al. Deepseekmath: Pushing the limits of mathematical reasoning in open language models[J]. arXiv preprint arXiv:2402.03300, 2024.

[2] Yang A, Zhang B, Hui B, et al. Qwen2. 5-math technical report: Toward mathematical expert model via self-improvement[J]. arXiv preprint arXiv:2409.12122, 2024.

[3] He Z, Liang T, Xu J, et al. Deepmath-103k: A large-scale, challenging, decontaminated, and verifiable mathematical dataset for advancing reasoning[J]. arXiv preprint arXiv:2504.11456, 2025.

[4] Cobbe K, Kosaraju V, Bavarian M, et al. Training verifiers to solve math word problems[J]. arXiv preprint arXiv:2110.14168, 2021.

[5] Hendrycks D, Burns C, Kadavath S, et al. Measuring mathematical problem solving with the math dataset[J]. arXiv preprint arXiv:2103.03874, 2021.

## Slide 8

**Mô hình lớn chuyên toán**

DeepSeek-Math:

- Làm sạch 120B dữ liệu web toán học: lọc lặp nhiều vòng dữ liệu Common Crawl, tránh để dữ liệu bị nhiễm benchmark (bộ bài kiểm tra chuẩn để so sánh mô hình)
- Khởi tạo từ mô hình code: dựa trên DeepSeek-Coder-v1.5 thay vì một LLM đa dụng, giúp xử lý ký hiệu tốt hơn
- Học tăng cường (RL) với GRPO: Group Relative Policy Optimization (GRPO; biến thể PPO so sánh reward trong một nhóm câu trả lời, bỏ mô hình critic), giảm lượng bộ nhớ GPU (VRAM) tiêu tốn và tăng khả năng tổng quát hóa, về sau trở thành cốt lõi của mô hình R1
- Hiệu năng: mô hình 7B đạt SOTA (kết quả tốt nhất) vào thời điểm đó

## Slide 9

**Mô hình lớn chuyên toán**

Qwen2.5-Math:

- Kho ngữ liệu pre-training (huấn luyện ban đầu trên kho dữ liệu rất lớn, chưa gắn với nhiệm vụ cụ thể): Qwen Math Corpus v2 (1T token – đơn vị văn bản nhỏ nhất mà mô hình đọc và sinh), gồm dữ liệu tổng hợp và bài toán tiếng Trung
- Sinh dữ liệu: dùng Qwen2-72B-Instruct sinh các cặp QA chất lượng cao, tăng độ đa dạng
- Kết hợp CoT & TIR: suy luận chain-of-thought + tích hợp công cụ (như trình thông dịch Python), hỗ trợ lời giải song ngữ
- Cải tiến reward model qua nhiều vòng (RM; mô hình chấm điểm câu trả lời, học từ đánh giá của con người): Qwen2.5-Math-RM dẫn dắt quá trình tiến hóa của dữ liệu SFT (supervised fine-tuning; fine-tuning (tinh chỉnh mô hình đã huấn luyện cho nhiệm vụ cụ thể) trên cặp đầu vào–đáp án mẫu do người hoặc mô hình mạnh hơn viết), giai đoạn học tăng cường áp dụng GRPO

Kết quả: mô hình 7B vượt các mô hình mã nguồn mở 30B-70B trên benchmark MATH, tiệm cận GPT-4

## Slide 10

**Mô hình lớn chuyên toán**

DeepMath-103K

- Tập huấn luyện thiết kế riêng cho các bài toán khó
- Gom các tập huấn luyện phổ biến và làm sạch dữ liệu rất kỹ, bảo đảm không trùng lặp với các tập đánh giá toán thông dụng
- Có nhãn độ khó và câu trả lời của R1

Mô hình huấn luyện trên dữ liệu DeepMath-103K cải thiện rõ năng lực toán học

## Slide 11

**Học bằng distillation**

Làm sao để nhanh chóng có được năng lực suy luận toán học của long-reasoning model?

Supervised fine-tuning (SFT)

- Tác dụng: làm đầu ra của mô hình khớp với định dạng lời giải của con người, học các bước suy luận chuẩn
- Yêu cầu dữ liệu: cần dữ liệu gán nhãn theo chuỗi bước, chất lượng cao

Knowledge distillation

- Quy trình: mô hình lớn (teacher) sinh dữ liệu CoT → mô hình nhỏ (student) học các mẫu suy luận bằng SFT
- Phương án tiêu biểu: Qwen-7B bản distill từ DeepSeek-R1 có hiệu năng vượt mô hình cơ sở 32B

## Slide 12

**Học bằng distillation**

Distillation ba bước:

- Sinh dữ liệu: mô hình teacher sinh dữ liệu CoT chất lượng cao
- Rejection sampling (sinh nhiều lời giải rồi loại bỏ lời giải sai): lọc bỏ đáp án sai, giữ các chuỗi suy luận có logic rõ ràng, định dạng chuẩn
- Fine-tuning bằng SFT: mô hình nhỏ học trực tiếp đầu ra của teacher, không cần thêm giai đoạn RL

Ưu điểm: dùng dữ liệu hiệu quả, rào cản thấp, học trực tiếp được hành vi suy luận phức tạp

Hạn chế: trần hiệu năng của mô hình nhỏ phụ thuộc năng lực của teacher; bài toán phức tạp vẫn cần mô hình lớn

## Slide 13

**Đánh giá năng lực toán học**

Benchmark truyền thống:

- Tập dữ liệu: GSM8K (tiểu học), MATH (trung học phổ thông), AIME (thi học sinh giỏi)
- Chỉ số: độ chính xác, Pass@k (tỉ lệ giải đúng trong k lần lấy mẫu)

Đặc điểm của đánh giá toán học: nghiên cứu hiện nay chỉ xét các bài có đáp án số/ký hiệu rõ ràng

Hướng tiên phong: đánh giá tính đúng đắn của bài chứng minh

Thách thức:

- Đầu ra ngôn ngữ tự nhiên của LLM: làm sao trích xuất đáp án từ lời giải viết bằng ngôn ngữ tự nhiên
- Đánh giá tính nhất quán của kết quả: làm sao đánh giá hai biểu thức toán học có nhất quán với nhau không

## Slide 14

**Đánh giá năng lực toán học**

Trích xuất đáp án:

- GSM8K: dùng 4 ký tự `####` liên tiếp để đánh dấu đáp án
- MATH: dùng `\\boxed{}` để bao đáp án, là giải pháp phổ biến hiện nay

Ưu điểm:

- Thống nhất chuẩn trích xuất, thuận tiện cho đánh giá

Nhược điểm:

- Mô hình cần được huấn luyện riêng theo định dạng đầu ra
- Không bao quát được mọi tình huống đầu ra

*Chú thích trong hình: Phương án GSM8K · Phương án MATH*

## Slide 15

**Đánh giá năng lực toán học**

Đánh giá đáp án: làm sao đánh giá đáp án mô hình sinh ra có đúng không?

Đánh giá bằng quy tắc:

- Vì đáp án mô hình đưa ra hầu hết theo định dạng LaTeX, có thể dùng quy tắc LaTeX để lấy biểu thức, rồi dùng quy tắc do người thiết kế thủ công để xét xem có khớp không
- Đại diện tiêu biểu: Hugging Face Math-Verify[1]

LLM Judge:

- Đánh giá bằng quy tắc không bao quát được các trường hợp biên của cách diễn đạt bằng chữ, và việc trích xuất đáp án có thể sai
- Dùng mô hình lớn (thường đã được huấn luyện riêng) để trực tiếp xét đáp án sinh ra và đáp án chuẩn có tương đương không
- Đại diện tiêu biểu: Omni-Judge[2], một mô hình đánh giá đáp án dành riêng cho tập kiểm tra Omni-MATH

[1] https://github.com/huggingface/Math-Verify

[2] https://huggingface.co/KbsdJames/Omni-Judge

## Slide 16

**Tổng kết**

- Suy luận toán học: năng lực của LLM giải bài toán bằng phân tích logic, biến đổi ký hiệu và suy diễn nhiều bước; mô hình cần hiểu các khái niệm toán học (như đại số, hình học) và sinh ra đáp án đúng
- Long-reasoning model: mô hình sinh chain-of-thought dài khi suy luận
- Mô hình lớn chuyên toán: mô hình lớn được tối ưu hóa riêng cho nhiệm vụ toán học, pre-training trên dữ liệu toán học
- Học bằng distillation: mô hình lớn sinh dữ liệu, mô hình nhỏ học trực tiếp kết quả lấy mẫu của mô hình lớn
- Đánh giá toán học:
    - Benchmark thông dụng: GSM8K, MATH500, AIME
    - Quy trình đánh giá: sinh kết quả, trích xuất kết quả theo định dạng thống nhất, dùng quy tắc/LLM để so sánh tính nhất quán

## Slide 17

**Thank you**
