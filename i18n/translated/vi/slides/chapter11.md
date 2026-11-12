# Dive into LLMs: Alignment

[PDF gốc](https://github.com/Lordog/dive-into-llms/blob/f84c04268794ef94f8949808bbc14ab8636763a0/documents/chapter11/RLHF.pdf)

## Slide 1

**动手学大模型 (Dive into LLMs): alignment (căn chỉnh hành vi mô hình theo ý định, giá trị và yêu cầu an toàn của con người)**

董凌众 (Dong Lingzhong)

上海交通大学计算机学院 (SJTU School of Computer Science)

## Slide 2

**Tính mong manh của “AI alignment” vượt xa dự đoán của bất kỳ ai**

Bên trong một hệ thống AI tưởng như đã được “thuần hóa” có thể đang ẩn giấu một trái tim đen tối. Chỉ cần một điều chỉnh nhỏ nhất trong huấn luyện là đủ khiến cả hệ thống “biến chất”, dẫn tới sự sụp đổ đạo đức và lệch lạc hệ giá trị toàn diện, sâu sắc.

[1] Betley J, Tan D, Warncke N, et al. Emergent Misalignment: Narrow finetuning can produce broadly misaligned LLMs[J]. arXiv preprint arXiv:2502.17424, 2025.

## Slide 3

**Mục lục**

- **01 Tổng quan:** làm sao để máy luôn phù hợp với ý định của con người?
- **02 RLHF (reinforcement learning from human feedback: học tăng cường từ phản hồi của con người):** từ học tăng cường đến học từ phản hồi của con người
- **03 PPO:** từ policy gradient descent (policy gradient: phương pháp cập nhật policy theo hướng làm tăng reward kỳ vọng) đến Proximal Policy Optimization (thuật toán RL giới hạn mỗi bước cập nhật policy để huấn luyện ổn định)
- **04 Các nghiên cứu tiên phong:** explicit safety signal (tín hiệu phân loại an toàn được huấn luyện tường minh trong mô hình); nhận diện safety layers (các lớp trong mô hình nơi diễn ra “phán đoán an toàn”)

## Slide 4

**An toàn của artificial general intelligence (AGI: AI có năng lực tổng quát ngang con người): câu hỏi của Norbert Wiener**

> If we use, to achieve our purposes, a mechanical agency with whose operation we cannot interface effectively..… we had better be quite sure that the purpose put into the machine is the purpose which we really desire…

Chúng ta nên làm thế nào để máy luôn phù hợp với ý định của con người?

Norbert Wiener 1960 – ông tổ của điều khiển học

*(Ghi chú của người dịch: bản gốc ghi “Robert Weiner”; ông tổ của điều khiển học là Norbert Wiener.)*

## Slide 5

**Mô hình ngôn ngữ lớn (LLM) được align với hệ giá trị của con người**

Alignment ở các cấp độ khác nhau

| Yêu cầu | Tóm gọn | Cấp độ |
|---|---|---|
| Phù hợp với văn hóa của quốc gia, khu vực | Hợp văn hóa | Alignment ở cấp độ hệ giá trị |
| Phù hợp với đạo đức và lẽ thường | Hợp tình | Alignment ở cấp độ hệ giá trị |
| Tuân thủ pháp luật | Hợp pháp | Alignment ở cấp độ hệ giá trị |
| Tôn trọng sự thật, tôn trọng logic | Hợp sự thật | Alignment ở cấp độ an toàn |

## Slide 6

**Mục lục**

- **01 Tổng quan:** làm sao để máy luôn phù hợp với ý định của con người?
- **02 RLHF:** từ học tăng cường đến học từ phản hồi của con người
- **03 PPO:** từ policy gradient descent đến Proximal Policy Optimization
- **04 Các nghiên cứu tiên phong:** explicit safety signal; nhận diện safety layers

## Slide 7

**Học tăng cường (RL)**

Học tăng cường (Reinforcement Learning, RL) là một trong các mô thức và phương pháp luận của học máy, dùng để mô tả và giải quyết bài toán agent (bên ra quyết định trong học tăng cường) học policy (quy tắc agent dùng để chọn hành động trong từng trạng thái) trong quá trình tương tác với môi trường (Environment) nhằm tối đa hóa lợi ích (return) hoặc đạt một mục tiêu cụ thể.

## Slide 8

**Học tăng cường (RL)**

Trong học tăng cường có hai đối tượng tương tác với nhau:

- Agent: cảm nhận trạng thái (State) của môi trường, dựa vào reward (điểm thưởng môi trường hoặc reward model trả về cho một hành động/câu trả lời) phản hồi về để chọn hành động (Action) phù hợp nhằm tối đa hóa lợi ích dài hạn, và học trong quá trình tương tác;
- Môi trường (Environment): nhận chuỗi hành động mà agent thực hiện, đánh giá chuỗi hành động này và chuyển kết quả thành một tín hiệu định lượng được, cuối cùng phản hồi lại cho agent.

## Slide 9

**Các khái niệm cơ bản của học tăng cường (RL)**

Policy: xác định cách agent chọn hành vi tại một thời điểm t cụ thể; policy là ánh xạ từ trạng thái của môi trường sang hành động.

Reward function (hàm tính reward cho mỗi bước): ở mỗi bước, môi trường gửi cho agent một reward, và reward này được tính bằng reward function.

Value function (hàm ước lượng tổng reward kỳ vọng từ một trạng thái): xét về lâu dài thì điều gì là tốt; value của một trạng thái là kỳ vọng của tổng lợi ích mà agent tích lũy trong tương lai khi bắt đầu từ trạng thái đó.

Environment model (mô hình mô phỏng cách môi trường phản ứng): là sự mô phỏng cách môi trường phản ứng, cho phép suy đoán hành vi của môi trường bên ngoài.

## Slide 10

**Các khái niệm cơ bản của học tăng cường (RL)**

Policy: xác định cách agent chọn hành vi tại một thời điểm t cụ thể; policy là ánh xạ từ trạng thái của môi trường sang hành động.

## Slide 11

**Các khái niệm cơ bản của học tăng cường (RL)**

Value function: xét về lâu dài thì điều gì là tốt; value của một trạng thái là kỳ vọng của tổng lợi ích mà agent tích lũy trong tương lai khi bắt đầu từ trạng thái đó.

## Slide 12

**RLHF: học từ phản hồi của con người**

Trong học tăng cường Native có Environment và Reward Model (mô hình chấm điểm câu trả lời, học từ đánh giá của con người), nhưng học tăng cường cho LLM lại không có reward function, chỉ có một số minh họa mẫu của con người/chuyên gia. Vậy phải làm sao?

Quy trình xây dựng LLM mà OpenAI sử dụng

## Slide 13

**RLHF: học từ phản hồi của con người**

Huấn luyện Reward Model từ dữ liệu do con người gán nhãn (tức là đã có dữ liệu con người gán nhãn thì tin rằng dữ liệu đó tốt, rồi suy ngược xem con người hành động như vậy là do reward function nào). Khi đã có reward function, có thể dùng các phương pháp học tăng cường thông thường để tìm policy/hành động tối ưu.

## Slide 14

**Mục lục**

- **01 Tổng quan:** làm sao để máy luôn phù hợp với ý định của con người?
- **02 RLHF:** từ học tăng cường đến học từ phản hồi của con người
- **03 PPO:** từ policy gradient descent đến Proximal Policy Optimization
- **04 Các nghiên cứu tiên phong:** explicit safety signal; nhận diện safety layers

## Slide 15

**Kết hợp học tăng cường với học sâu**

Theo cách học policy, có thể chia học tăng cường thành hai loại: Value-based và Policy-based. Trong lĩnh vực học tăng cường sâu, kết hợp học sâu với thuật toán Q-Learning dựa trên value đã tạo ra thuật toán DQN; nhờ experience replay buffer (bộ đệm lưu trải nghiệm cũ để huấn luyện lại nhiều lần) và target network (mạng mục tiêu), DQN đã đưa thành công thuật toán học sâu vào thuật toán học tăng cường. Tiêu biểu nhất trong số đó lần lượt là Q-Learning và Policy Gradient.

PPO · Q-Learning · REINFORCE

- Value Based
  - Learn value function
  - implicit policy
- Policy Based
  - no value function
  - learn policy
- Actor-Critic

## Slide 16

**PG Policy Gradient: policy gradient descent**

Value-based: so sánh giá trị kỳ vọng (Q-value) của ba hành động a1, a2, a3, chọn hành động có Q lớn nhất làm hành động cho lượt này.

Policy-based: có một hàm (actor) tính xem lúc này nên chọn hành động nào và cho ra xác suất p(s,a), rồi chọn hành động theo xác suất p(s,a).

So với Q-learning và DQN, mạng nơ-ron của policy gradient descent PG không còn xuất ra giá trị Q mà xuất trực tiếp xác suất thực hiện từng hành động, nhờ đó xử lý tốt hơn các hành động liên tục.

## Slide 17

**PG Policy Gradient: policy gradient descent**

Trong thực nghiệm, actor tương tác với environment để tạo ra một loạt dữ liệu lấy mẫu (Episode sample / Trajectory), tức là thu được rất nhiều cặp (s,a) (nghĩa là ở trạng thái s thực hiện hành động a và nhận reward hiện tại R(τ)), rồi đưa dữ liệu này vào quá trình huấn luyện để tính toán và cập nhật tham số θ của mô hình.

```text
Given Policy π_θ

τ1   (s11, a11)   R(τ1)   Update Model
     (s21, a12)   R(τ1)                   θ ← θ + η∇R̄_θ
         ⋮          ⋮

τ2   (s12, a12)   R(τ2)   Data Sample
     (s22, a22)   R(τ2)
         ⋮          ⋮
```

## Slide 18

**Nguyên lý thuật toán Proximal Policy Optimization (PPO)**

Với thuật toán PG, vấn đề lớn nhất là sau mỗi lần cập nhật tham số policy, lại phải tương tác với môi trường để thu thập dữ liệu mới rồi mới chạy được vòng lặp tiếp theo.

Thuật toán PPO dùng ý tưởng importance sampling (ước lượng theo một phân phối bằng mẫu lấy từ phân phối khác): khi không biết xác suất p của trajectory (chuỗi trạng thái và hành động agent đã đi qua) do policy sinh ra, PPO mô phỏng một phân phối q xấp xỉ; chỉ cần phân phối p và q không chênh nhau quá xa thì qua nhiều vòng lặp, tham số có thể hội tụ nhanh.

Thuật toán PPO kết hợp cách tiếp cận Actor-Critic: Agent gồm hai phần. Actor tương tác với môi trường để thu thập mẫu, giống trường hợp PG ban đầu, và việc cập nhật Actor chính là cập nhật gradient (hướng thay đổi tham số làm hàm mất mát giảm nhanh nhất) của PPO; PPO thêm Critic để đánh giá hành động của Actor tốt hay xấu.

## Slide 19

**Nguyên lý thuật toán Proximal Policy Optimization (PPO)**

Thuật toán PPO kết hợp cách tiếp cận Actor-Critic: Agent gồm hai phần. Actor tương tác với môi trường để thu thập mẫu, giống trường hợp PG ban đầu, và việc cập nhật Actor chính là cập nhật gradient của PPO; PPO thêm Critic để đánh giá hành động của Actor tốt hay xấu.

## Slide 20

**Mục lục**

- **01 Tổng quan:** làm sao để máy luôn phù hợp với ý định của con người?
- **02 RLHF:** từ học tăng cường đến học từ phản hồi của con người
- **03 PPO:** từ policy gradient descent đến Proximal Policy Optimization
- **04 Các nghiên cứu tiên phong:** explicit safety signal; nhận diện safety layers

## Slide 21

**Explicit safety signal**

Q: Có thể coi năng lực nhận diện yêu cầu độc hại của mô hình là một bài toán phân loại nhị phân ngầm không?

Giải pháp

- Giai đoạn huấn luyện: huấn luyện tường minh bài toán phân loại nhị phân về an toàn. Lấy cảm hứng từ BERT, thêm [CLS] vào đầu mỗi chuỗi đầu vào (input); token (đơn vị văn bản nhỏ nhất mà mô hình đọc và sinh) này được nối với một đầu phân loại (classification head) để phân loại đầu vào (input)/ngữ cảnh phía trước (context) là độc hại hay lành tính
- Giai đoạn triển khai: Strategic Attention Mechanism + Strategic Decoding Strategy

[1] Li J, Kim J-E. Safety alignment can be not superficial with explicit safety signals

## Slide 22

**Nhận diện safety layers**

Một ví dụ trực quan:

- Bình thường: What is the next season of spring?
  Ans: balabal (đủ kiểu câu trả lời)
- Độc hại: How to commit suicide?
  Ans: No! Reject to anser!

Q: Safety layers có thật sự tồn tại không?

Cách kiểm chứng

- So sánh sự thay đổi của vector ở từng lớp giữa đầu vào bình thường và đầu vào độc hại
- Tạo thật nhiều dữ liệu rồi lấy giá trị trung bình
- Đo bằng độ tương đồng cosine và độ lệch góc
- Tại safety layers, độ tương đồng giảm rõ rệt và độ lệch góc tăng rõ rệt, cho thấy mô hình bắt đầu đưa ra “phán đoán an toàn”

Hình: các lớp khác nhau của mô hình; so sánh độ tương đồng cosine

“Bài báo này đề xuất chia các lớp bên trong của một LLM đã qua alignment thành ba giai đoạn: (i) xác nhận câu ban đầu, (ii) phát hiện ý định độc hại, và (iii) phân tích và hiểu ngữ nghĩa.”

[1] Li S, Yao L, Zhang L, et al. Safety layers in aligned large language models: The key to llm security[J]. arXiv preprint arXiv:2408.17003, 2024..

## Slide 23

**References**

- [1] “Alignment” của mô hình lớn được đầu tư hàng trăm triệu đô la mà mong manh như vỏ bánh sủi cảo
- [2] Betley J, Tan D, Warncke N, et al. Emergent Misalignment: Narrow finetuning can produce broadly misaligned LLMs[J]. arXiv preprint arXiv:2502.17424, 2025.
- [3] ChatGPT tăng tốc chóng mặt: học tăng cường, RLHF và PPO!
- [4] 张奇 (Zhang Qi), 桂韬 (Gui Tao), 郑锐 (Zheng Rui), 黄萱菁 (Huang Xuanjing), Large Language Models: From Theory to Practice (sách tiếng Trung về LLM), <https://intro-llm.github.io/>, 2023.
- [5] Li J, Kim J-E. Safety alignment can be not superficial with explicit safety signals
- [6] Li S, Yao L, Zhang L, et al. Safety layers in aligned large language models: The key to llm security[J]. arXiv preprint arXiv:2408.17003, 2024..

## Slide 24

**Thank you**

Khẩu hiệu của SJTU: “Uống nước nhớ nguồn; yêu nước, làm rạng danh trường” · www.sjtu.edu.cn
