# Agent tự chủ trên giao diện người dùng đồ họa

[PDF gốc](https://github.com/Lordog/dive-into-llms/blob/f84c04268794ef94f8949808bbc14ab8636763a0/documents/chapter9/GUIagent.pdf)

## Slide 1

**Agent tự chủ trên giao diện người dùng đồ họa**

吴铮 (Wu Zheng)

上海交通大学计算机学院 (SJTU School of Computer Science)

## Slide 2

**Mục lục**

- Tổng quan về agent (tác tử AI: hệ thống dùng mô hình để tự lập kế hoạch, gọi công cụ và hành động trong môi trường) tự chủ trên giao diện người dùng đồ họa
    - Bối cảnh nghiên cứu
    - Hiện trạng phát triển
    - Các nhánh kỹ thuật
- Toàn bộ chuỗi kỹ thuật của agent tự chủ trên giao diện người dùng đồ họa
    - Triển khai GUI agent (agent thao tác giao diện đồ họa như người dùng: chạm, gõ, vuốt)
    - Giải pháp cho kịch bản tĩnh: supervised fine-tuning (SFT; fine-tuning trên cặp đầu vào–đáp án mẫu do người hoặc mô hình mạnh hơn viết)
    - Giải pháp cho kịch bản động: học tăng cường (RL)
    - Giải pháp cho kịch bản phức tạp: hệ thống điều phối
- An toàn và độ tin cậy của agent tự chủ trên giao diện người dùng đồ họa
    - Vấn đề an toàn của GUI agent
    - Vấn đề độ tin cậy của GUI agent

## Slide 3

**Mục lục**

- Tổng quan về agent tự chủ trên giao diện người dùng đồ họa
    - Bối cảnh nghiên cứu
    - Hiện trạng phát triển
    - Các nhánh kỹ thuật
- Toàn bộ chuỗi kỹ thuật của agent tự chủ trên giao diện người dùng đồ họa
    - Triển khai GUI agent
    - Giải pháp cho kịch bản tĩnh: supervised fine-tuning
    - Giải pháp cho kịch bản động: học tăng cường
    - Giải pháp cho kịch bản phức tạp: hệ thống điều phối
- An toàn và độ tin cậy của agent tự chủ trên giao diện người dùng đồ họa
    - Vấn đề an toàn của GUI agent
    - Vấn đề độ tin cậy của GUI agent

## Slide 4

**Bối cảnh nghiên cứu: năm giai đoạn tiến tới AGI**

- OpenAI chia quá trình loài người tiến tới artificial general intelligence (AGI; AI có năng lực tổng quát ngang con người) thành năm giai đoạn
- Ngày nay, AGI đã phát triển đến giai đoạn thứ ba: agent (Agents); agent đang dẫn dắt làn sóng cách mạng của AI tạo sinh

Các giai đoạn trong hình:

- L1: Chatbots. GPT-4, DeepSeek-V3. Tương tác ngôn ngữ tổng quát. Ứng dụng: hỏi đáp, hội thoại, tìm kiếm
- L2: Reasoners. o1, DeepSeek-R1. Tư duy và suy luận sâu. Ứng dụng: toán học, suy luận logic
- L3: Agents. Operator, Deep Research. Hành động và tương tác tự chủ. Ứng dụng: gọi công cụ (tool calling), điều khiển, khám phá
- L4: Innovators. Đổi mới và phát minh
- L5: Organizations. Tổ chức và quản lý

Ngôn ngữ -> hành động: từ trí tuệ nội dung đến trí tuệ hành vi, tạo nên mắt xích then chốt trên đường tiến tới AGI

## Slide 5

**Bối cảnh nghiên cứu: định nghĩa agent**

- LLM agent (multimodal; xử lý nhiều modality cùng lúc): hệ thống được xây dựng dựa trên mô hình lớn (multimodal), có thể tự điều hướng động quy trình của chính nó và việc dùng công cụ, đồng thời điều chỉnh thao tác của mình theo phản hồi thời gian thực

So sánh trong hình:

- Mô hình ngôn ngữ lớn (LLM) multimodal: người dùng → mô hình lớn → người dùng
    - Bên cung cấp năng lực tổng quát:
        - Xử lý chuỗi dài
        - Suy luận chain-of-thought (CoT; để mô hình viết ra từng bước suy luận trước khi trả lời)
        - Hiểu ý định ở phạm vi rộng
- LLM agent (hệ thống): người dùng → agent ↔ môi trường
    - Có năng lực tự chủ và tiến hóa:
        - Tương tác với môi trường: cảm nhận và hiểu, lập kế hoạch và ra quyết định, thực thi hành động
        - Vận hành lâu dài: phản tư và tối ưu hóa, tiến hóa lặp, bảo vệ an toàn
    - Cập nhật tri thức: kho tri thức, kho kinh nghiệm
    - Tích hợp công cụ: APP, API (giao diện lập trình ứng dụng), hàm

## Slide 6

**Bối cảnh nghiên cứu: GUI agent**

- Agent tự chủ trên giao diện người dùng đồ họa (Graphical User Interface, GUI), gọi tắt là GUI agent, là ví dụ điển hình của agent
- Định nghĩa: agent chủ động lập kế hoạch và ra quyết định, mô phỏng hành vi của con người (như nhấn, vuốt, nhập), để lấy thông tin và thực thi chức năng

So sánh trong hình:

- Trước đây: kịch bản bị giới hạn, nhiệm vụ đơn giản cụ thể, quy trình cố định, hệ thống dạng pipeline
    - Ví dụ: Hôm nay thời tiết thế nào, tăng âm lượng lên một chút, gọi điện cho Zhang San, 30 nhân 15 bằng bao nhiêu?
- Hiện nay: phạm vi bao phủ rộng, nhiệm vụ phức tạp và đa dạng, tự chủ lập kế hoạch và ra quyết định, thích ứng động với thay đổi
    - Ví dụ: Đặt lại phần đồ ăn giao tận nơi tối qua, mở Suishenma (mã QR dịch vụ công của Thượng Hải), đặt một vé tàu cao tốc từ Thượng Hải đến Bắc Kinh vào trưa mai

## Slide 7

**Bối cảnh nghiên cứu: GUI vs API**

- API agent: gọi công cụ, gọi API của môi trường, function call. Đặc điểm: nhanh, ổn định, hình thức hóa
- GUI agent: nhấn, nhập, vuốt, nhấn giữ, nhấn đúp, quay lại. Đặc điểm: linh hoạt, tự nhiên, giống con người
- API cồng kềnh hơn ta tưởng, GUI mong manh hơn ta tưởng, không có giải pháp hoàn hảo. Sự phát triển theo hình xoắn ốc mang lại một mô thức (paradigm) mới cho tương tác người–máy

[1] Zhang, Chaoyun, et al. API Agents vs. GUI Agents: Divergence and Convergence.

## Slide 8

**Mục lục**

- Tổng quan về agent tự chủ trên giao diện người dùng đồ họa
    - Bối cảnh nghiên cứu
    - Hiện trạng phát triển
    - Các nhánh kỹ thuật
- Toàn bộ chuỗi kỹ thuật của agent tự chủ trên giao diện người dùng đồ họa
    - Triển khai GUI agent
    - Giải pháp cho kịch bản tĩnh: supervised fine-tuning
    - Giải pháp cho kịch bản động: học tăng cường
    - Giải pháp cho kịch bản phức tạp: hệ thống điều phối
- An toàn và độ tin cậy của agent tự chủ trên giao diện người dùng đồ họa
    - Vấn đề an toàn của GUI agent
    - Vấn đề độ tin cậy của GUI agent

## Slide 9

**Hiện trạng phát triển**

- Nhờ giá trị thực tiễn nổi bật, việc xây dựng GUI agent được giới học thuật và công nghiệp quan tâm rộng rãi, và phát triển bùng nổ trong những năm gần đây
- Trên nhiều nền tảng như web, điện thoại, máy tính đều xuất hiện rất nhiều công trình xây dựng GUI agent

[1] Zhang, Chaoyun, et al. Large Language Model-Brained GUI Agents: A Survey.

## Slide 10

**Mục lục**

- Tổng quan về agent tự chủ trên giao diện người dùng đồ họa
    - Bối cảnh nghiên cứu
    - Hiện trạng phát triển
    - Các nhánh kỹ thuật
- Toàn bộ chuỗi kỹ thuật của agent tự chủ trên giao diện người dùng đồ họa
    - Triển khai GUI agent
    - Giải pháp cho kịch bản tĩnh: supervised fine-tuning
    - Giải pháp cho kịch bản động: học tăng cường
    - Giải pháp cho kịch bản phức tạp: hệ thống điều phối
- An toàn và độ tin cậy của agent tự chủ trên giao diện người dùng đồ họa
    - Vấn đề an toàn của GUI agent
    - Vấn đề độ tin cậy của GUI agent

## Slide 11

**Các nhánh kỹ thuật**

- GUI Agent xây dựng trên mô hình mã nguồn đóng: xây dựng bằng các mô hình mã nguồn đóng như GPT-4o, Qwen-VL-Max, GLM-4v; gọi mô hình qua API
- GUI Agent xây dựng trên mô hình mã nguồn mở: xây dựng bằng các mô hình mã nguồn mở như kiến trúc Blip+T5, Qwen2-VL, LLaVa2; triển khai mô hình cục bộ

*Chú thích trong hình: Hệ thống multi-agent (nhiều agent tương tác với nhau) cộng tác, xây dựng trên mô hình mã nguồn đóng · GUI agent multimodal xây dựng trên mô hình mã nguồn mở*

[1] Wang, Junyang, et al. Mobile-Agent-v2: Mobile Device Operation Assistant with Effective Navigation via Multi-Agent Collaboration.

[2] Xv, Yiheng, et al. Aguvis: Unified Pure Vision Agents for Autonomous GUI Interaction.

## Slide 12

**Các nhánh kỹ thuật: GUI Agent tiêu biểu xây dựng trên mô hình mã nguồn đóng**

- Dòng Mobile-Agent là một trong những GUI Agent tiêu biểu xây dựng trên mô hình mã nguồn đóng
- Mobile-Agent-v2 xây dựng một hệ thống multi-agent gồm ba agent:
    - Agent lập kế hoạch: tạo tiến độ nhiệm vụ dựa trên lịch sử thao tác; đơn vị bộ nhớ lưu nội dung trọng tâm
    - Agent ra quyết định: tạo thao tác dựa trên đơn vị bộ nhớ và tiến độ nhiệm vụ
    - Agent phản tư: quan sát thay đổi của màn hình trước và sau thao tác, khi cần thì thực hiện biện pháp để chạy lại

[1] Wang, Junyang, et al. Mobile-Agent-v2: Mobile Device Operation Assistant with Effective Navigation via Multi-Agent Collaboration.

## Slide 13

**Các nhánh kỹ thuật: GUI Agent tiêu biểu xây dựng trên mô hình mã nguồn đóng**

- Dòng AppAgent là một nhóm GUI Agent tiêu biểu khác xây dựng trên mô hình mã nguồn đóng
- AppAgentX có thể học và tối ưu hóa khuôn mẫu hành vi của chính nó trong quá trình thực thi nhiệm vụ, ghi nhớ các nút lối tắt

[1] Jiang, Wenjia, et al. AppAgentX: Evolving GUI Agents as Proficient Smartphone Users

## Slide 14

**Các nhánh kỹ thuật: GUI Agent xây dựng trên mô hình mã nguồn mở**

- GUI Agent xây dựng trên mô hình mã nguồn mở rất linh hoạt, có thể dùng các phương pháp như pre-training (huấn luyện ban đầu trên kho dữ liệu rất lớn, chưa gắn với nhiệm vụ cụ thể), instruction tuning (fine-tuning trên dữ liệu dạng (instruction, câu trả lời) để mô hình biết làm theo yêu cầu) và học tăng cường để xây dựng giải pháp kỹ thuật

Ba cột trong hình:

- Pre-training: nhận diện vị trí phần tử UI và diễn giải thành phần. Then chốt: phụ thuộc dữ liệu gán nhãn quy mô lớn. Đại diện: OS-Atlas, Auto-GLM
- Instruction tuning: khớp theo mẫu, phụ thuộc dữ liệu gán nhãn chất lượng cao. Đặc điểm: sao chép hành vi của chuyên gia, dễ huấn luyện. Đại diện: Auto-GUI, AutoAct, ToolLLM
- Học tăng cường: học từ trajectory (chuỗi trạng thái và hành động agent đã đi qua), phụ thuộc vào thiết kế reward function (hàm tính reward cho mỗi bước). Đặc điểm: tự chủ khám phá và tối ưu hóa policy (quy tắc agent dùng để chọn hành động trong từng trạng thái), chi phí huấn luyện cao. Đại diện: DigiRL, DistRL, Agent Q

Ví dụ trong hình: Goal: Look up the best rated coffee maker on Lowe’s

*Chú thích trong hình: instruction (yêu cầu/chỉ dẫn bằng ngôn ngữ tự nhiên giao cho mô hình) · môi trường · dự đoán*

```
action_type:
[DUAL_POINT],
touch_point:
[0.5595, 0.6261],
lift_point:
[0.5595, 0.6261]
```

## Slide 15

**Mục lục**

- Tổng quan về agent tự chủ trên giao diện người dùng đồ họa
    - Bối cảnh nghiên cứu
    - Hiện trạng phát triển
    - Các nhánh kỹ thuật
- Toàn bộ chuỗi kỹ thuật của agent tự chủ trên giao diện người dùng đồ họa
    - Triển khai GUI agent
    - Giải pháp cho kịch bản tĩnh: supervised fine-tuning
    - Giải pháp cho kịch bản động: học tăng cường
    - Giải pháp cho kịch bản phức tạp: hệ thống điều phối
- An toàn và độ tin cậy của agent tự chủ trên giao diện người dùng đồ họa
    - Vấn đề an toàn của GUI agent
    - Vấn đề độ tin cậy của GUI agent

## Slide 16

**Triển khai GUI agent**

- GUI agent có nhiều dự án mã nguồn mở xuất sắc có thể triển khai trực tiếp:
    - Framework GUI agent xây dựng trên mô hình mã nguồn đóng: như dòng Mobile-Agent, dòng AppAgent, v.v.
    - Foundation model (mô hình nền dùng chung cho nhiều ứng dụng) mã nguồn mở mạnh cho lĩnh vực GUI: như OS-Atlas, UI-TARS, CogAgent, Aguvis, v.v.
- Làm thế nào để dùng các dự án này tương tác với thiết bị thật?

[1] Zhang, Chaoyun, et al. Large Language Model-Brained GUI Agents: A Survey.

## Slide 17

**Triển khai GUI agent: làm thế nào để mô hình lớn tương tác với thiết bị?**

- Thiết bị Android
    - Thiết bị Android thật: dùng Android Debug Bridge (ADB) để điều khiển bằng dòng lệnh chiếc máy thật đang kết nối với máy tính
    - Thiết bị Android ảo: dùng Android Virtual Device (AVD) để chạy song song các thiết bị Android ảo trên máy
- Máy tính: chuyển đầu ra của agent thành lệnh theo đúng định dạng của thư viện pyautogui để điều khiển chuột và bàn phím, mô phỏng các thao tác GUI của người dùng

| Mục đích thao tác | Lệnh ADB | Định dạng thư viện Pyautogui |
|---|---|---|
| Mô phỏng nhấn | `adb shell input tap <x> <y>` | `pyautogui.click(x, y)` |
| Chụp màn hình | `adb shell screencap` + `adb pull` | `pyautogui.screenshot("screen.png")` |
| Nhập văn bản | `adb shell input text "hello"` | `pyautogui.typewrite("hello")` |
| Mô phỏng phím bấm | `adb shell input keyevent 3` | `pyautogui.press('home')` |

## Slide 18

**Mục lục**

- Tổng quan về agent tự chủ trên giao diện người dùng đồ họa
    - Bối cảnh nghiên cứu
    - Hiện trạng phát triển
    - Các nhánh kỹ thuật
- Toàn bộ chuỗi kỹ thuật của agent tự chủ trên giao diện người dùng đồ họa
    - Triển khai GUI agent
    - Giải pháp cho kịch bản tĩnh: supervised fine-tuning
    - Giải pháp cho kịch bản động: học tăng cường
    - Giải pháp cho kịch bản phức tạp: hệ thống điều phối
- An toàn và độ tin cậy của agent tự chủ trên giao diện người dùng đồ họa
    - Vấn đề an toàn của GUI agent
    - Vấn đề độ tin cậy của GUI agent

## Slide 19

**Giải pháp cho kịch bản tĩnh: supervised fine-tuning**

- Trong tình huống tĩnh, khi môi trường thực tế thay đổi ít so với dữ liệu huấn luyện, cách trực quan nhất là supervised fine-tuning dựa trên dữ liệu

Ví dụ trong hình: Goal: Look up the best rated coffee maker

Khung bên phải:

- Dựa trên nguyên lý gốc (first principles)
    - Cơ chế cảm nhận lấy thị giác làm trung tâm
    - Không phụ thuộc vào giao diện API của hệ thống/ứng dụng
    - Chế độ làm việc
        - Đầu vào: instruction của người dùng + màn hình hiện tại
        - Đầu ra: instruction hành động
- Tính tổng quát
- Gọn nhẹ

*Chú thích trong hình: i-th screen · (i+1)-th screen*

[1] Zhang, Zhuosheng, et al. You Only Look at Screens: Multimodal Chain-of-Action Agents

## Slide 20

**Mục lục**

- Tổng quan về agent tự chủ trên giao diện người dùng đồ họa
    - Bối cảnh nghiên cứu
    - Hiện trạng phát triển
    - Các nhánh kỹ thuật
- Toàn bộ chuỗi kỹ thuật của agent tự chủ trên giao diện người dùng đồ họa
    - Triển khai GUI agent
    - Giải pháp cho kịch bản tĩnh: supervised fine-tuning
    - Giải pháp cho kịch bản động: học tăng cường
    - Giải pháp cho kịch bản phức tạp: hệ thống điều phối
- An toàn và độ tin cậy của agent tự chủ trên giao diện người dùng đồ họa
    - Vấn đề an toàn của GUI agent
    - Vấn đề độ tin cậy của GUI agent

## Slide 21

**Giải pháp cho kịch bản động: học tăng cường**

- Môi trường thực tế mà GUI agent đối mặt luôn thay đổi. Làm thế nào để GUI agent thích ứng với tính động của môi trường thực?
    - Bố cục trang web: ví dụ cùng một lượt tìm kiếm, thứ tự kết quả mỗi lần có thể khác nhau
    - Cập nhật phần mềm: bản cập nhật có thể thay đổi mạnh bố cục của phần mềm
    - Ngày lễ đặc biệt: vào một số ngày lễ đặc biệt, biểu tượng của phần mềm có thể được thay giao diện mang màu sắc lễ hội

[1] Bai, Hao, et al. DigiRL:Training In-The-Wild Device-Control Agents with Autonomous Reinforcement Learning

## Slide 22

**Giải pháp cho kịch bản động: học tăng cường: DigiRL**

- DigiRL dùng curriculum learning (huấn luyện từ ví dụ dễ đến khó) để thích ứng với tính động của môi trường: GUI agent học các nhiệm vụ đơn giản trước, rồi mới học các nhiệm vụ khó

[1] Bai, Hao, et al. DigiRL:Training In-The-Wild Device-Control Agents with Autonomous Reinforcement Learning

## Slide 23

**Giải pháp cho kịch bản động: học tăng cường: DistRL**

- DistRL làm thêm các bước tiếp theo trên nền DigiRL:
    - Dùng thêm framework phân tán bất đồng bộ để tách rời quá trình thu thập dữ liệu và quá trình huấn luyện, nâng cao hiệu quả huấn luyện
    - Đề xuất kỹ thuật phát lại ưu tiên phân tán (distributed prioritized replay), xác định trajectory nào có giá trị hơn để ưu tiên học lại

[1]Wang, Taiyi, et al. DISTRL: AN ASYNCHRONOUS DISTRIBUTED RE INFORCEMENT LEARNING FRAMEWORK FOR ON DEVICE CONTROL AGENTS

## Slide 24

**Giải pháp cho kịch bản động: học tăng cường: GRPO xuất hiện**

- Khi Deepseek trở nên nổi đình nổi đám, ý tưởng học tăng cường của GRPO (biến thể PPO so sánh reward trong một nhóm câu trả lời, bỏ mô hình critic) với reward (điểm thưởng môi trường hoặc reward model trả về cho một hành động/câu trả lời) dựa trên quy tắc nhanh chóng được lĩnh vực GUI agent học theo
- UI-R1, GUI-R1 và InfiGUI-R1 lần lượt kiểm chứng tính khả thi của ý tưởng reward dựa trên quy tắc trong lĩnh vực GUI agent

[1]Lu, Zhengxini, et al. UI-R1: Enhancing Action Prediction of GUI Agents by Reinforcement Learning.

## Slide 25

**Mục lục**

- Tổng quan về agent tự chủ trên giao diện người dùng đồ họa
    - Bối cảnh nghiên cứu
    - Hiện trạng phát triển
    - Các nhánh kỹ thuật
- Toàn bộ chuỗi kỹ thuật của agent tự chủ trên giao diện người dùng đồ họa
    - Triển khai GUI agent
    - Giải pháp cho kịch bản tĩnh: supervised fine-tuning
    - Giải pháp cho kịch bản động: học tăng cường
    - Giải pháp cho kịch bản phức tạp: hệ thống điều phối
- An toàn và độ tin cậy của agent tự chủ trên giao diện người dùng đồ họa
    - Vấn đề an toàn của GUI agent
    - Vấn đề độ tin cậy của GUI agent

## Slide 26

**Giải pháp cho kịch bản phức tạp: hệ thống điều phối**

- Nhu cầu trong kịch bản thực tế đang thúc đẩy GUI agent ở cấp hệ thống: từ thực thi các nhiệm vụ đơn giản có quy tắc rõ ràng đến đảm đương được các nhiệm vụ phức tạp có thứ tự và phức tạp không thứ tự
- Phân loại instruction phức hợp theo quan hệ phụ thuộc giữa các nhiệm vụ con: kiểu ghép nối, kiểu truyền tiếp, kiểu phân tích sâu

[1]Guo, Yuan et al. Atomic-to-Compositional Generalization for Mobile Agents with A New Benchmark and Scheduling System

## Slide 27

**Giải pháp cho kịch bản phức tạp: hệ thống điều phối**

- UI-NEXUS: benchmark (bộ bài kiểm tra chuẩn để so sánh mô hình) toàn diện đầu tiên dành riêng cho bối cảnh nhiệm vụ phức hợp của GUI agent
- Các foundation model và framework agent hiện có bộc lộ khiếm khuyết rõ rệt, khó xử lý phụ thuộc phức tạp, quản lý tiến độ, truyền thông tin, cũng như việc kết hợp hành động với suy luận tổng quát

[1]Guo, Yuan et al. Atomic-to-Compositional Generalization for Mobile Agents with A New Benchmark and Scheduling System

## Slide 28

**Giải pháp cho kịch bản phức tạp: hệ thống điều phối**

- Một mô hình agent đơn lẻ khó xử lý việc phối hợp nhiều kịch bản và phụ thuộc phức tạp, dễ gặp vấn đề tràn ngữ cảnh và rối tiến độ
- Xây dựng hệ thống điều phối nhiệm vụ cho agent, phân rã và điều phối các nhiệm vụ phức tạp

Instruction ví dụ: Lần lượt tìm KFC Super Family Bucket trên Meituan và Ele.me, sau đó đặt hàng trên nền tảng có giá rẻ nhất, dừng lại ở màn hình đặt hàng

[1]Guo, Yuan et al. Atomic-to-Compositional Generalization for Mobile Agents with A New Benchmark and Scheduling System

## Slide 29

**Mục lục**

- Tổng quan về agent tự chủ trên giao diện người dùng đồ họa
    - Bối cảnh nghiên cứu
    - Hiện trạng phát triển
    - Các nhánh kỹ thuật
- Toàn bộ chuỗi kỹ thuật của agent tự chủ trên giao diện người dùng đồ họa
    - Triển khai GUI agent
    - Giải pháp cho kịch bản tĩnh: supervised fine-tuning
    - Giải pháp cho kịch bản động: học tăng cường
    - Giải pháp cho kịch bản phức tạp: hệ thống điều phối
- An toàn và độ tin cậy của agent tự chủ trên giao diện người dùng đồ họa
    - Vấn đề an toàn của GUI agent
    - Vấn đề độ tin cậy của GUI agent

## Slide 30

**Vấn đề an toàn của GUI agent: rủi ro bảo mật**

- Môi trường triển khai GUI agent không đáng tin cậy tuyệt đối, có thể gặp rủi ro bảo mật:
    - Instruction của người dùng có thể bị chèn thao tác độc hại
    - Môi trường có thể chứa thông tin độc hại gây nhiễu

[1] Ma, Xinbei, et al. Caution for the Environment: Multimodal Agents are Susceptible to Environmental Distractions

## Slide 31

**Vấn đề an toàn của GUI agent: tấn công injection**

- GUI agent mong manh ngay cả trước những tấn công injection đơn giản (chèn chỉ dẫn độc hại vào đầu vào hoặc môi trường của agent): prompt (đầu vào bằng văn bản đưa cho mô hình để yêu cầu nó làm một việc) độc hại giấu trong điều khoản người dùng có thể khiến agent gửi thông tin người dùng tới trang web độc hại

[1] Chen, Chaoran, et al. The Obvious Invisible Threat: LLM-Powered GUI Agents’ Vulnerability to Fine-Print Injections

## Slide 32

**Vấn đề an toàn của GUI agent: tấn công injection**

- Mảnh ảnh (image patch) độc hại nhúng trong màn hình cũng có thể vượt qua cơ chế phòng vệ của GUI agent

[1] Lukas Aichberger, et al. Attacking Multimodal OS Agents with Malicious Image Patches.

## Slide 33

**Vấn đề an toàn của GUI agent: vấn đề robustness**

- Nghiên cứu cho thấy robustness (khả năng giữ hiệu quả khi bị nhiễu hoặc bị tấn công) của GUI agent hiện nay còn rất xa mới đạt chuẩn ứng dụng thực tế. Tỉ lệ tấn công thành công rất cao đồng nghĩa với rủi ro rất lớn
- Tương ứng, việc nâng cao robustness của GUI agent có tiềm năng nghiên cứu rất lớn

[1] Zhao, Haoren, et al. On the Robustness of GUI Grounding Models Against Image Attack

## Slide 34

**Vấn đề an toàn của GUI agent: alignment an toàn**

- Alignment an toàn (alignment: căn chỉnh hành vi mô hình theo ý định, giá trị và yêu cầu an toàn của con người) của GUI agent cũng tiềm ẩn rủi ro
- GUI agent không thể từ chối hiệu quả các yêu cầu thực hiện thao tác vi phạm pháp luật, gây hiểu lầm hoặc thậm chí độc hại

[1] Ada Defne Tur et al. SAFEARENA: Evaluating the Safety of Autonomous Web Agents

## Slide 35

**Vấn đề an toàn của GUI agent: alignment an toàn**

- Thí nghiệm cho thấy trên nhiều agent, tỉ lệ hoàn thành nhiệm vụ có hại thậm chí gần bằng tỉ lệ hoàn thành nhiệm vụ an toàn

[1] Ada Defne Tur et al. SAFEARENA: Evaluating the Safety of Autonomous Web Agents

## Slide 36

**Mục lục**

- Tổng quan về agent tự chủ trên giao diện người dùng đồ họa
    - Bối cảnh nghiên cứu
    - Hiện trạng phát triển
    - Các nhánh kỹ thuật
- Toàn bộ chuỗi kỹ thuật của agent tự chủ trên giao diện người dùng đồ họa
    - Triển khai GUI agent
    - Giải pháp cho kịch bản tĩnh: supervised fine-tuning
    - Giải pháp cho kịch bản động: học tăng cường
    - Giải pháp cho kịch bản phức tạp: hệ thống điều phối
- An toàn và độ tin cậy của agent tự chủ trên giao diện người dùng đồ họa
    - Vấn đề an toàn của GUI agent
    - Vấn đề độ tin cậy của GUI agent

## Slide 37

**Vấn đề độ tin cậy của GUI agent: vấn đề OOD**

- Các foundation model mạnh hiện có của GUI agent được huấn luyện trên dữ liệu tĩnh, nên khi thực thi trong thế giới thực sẽ gặp vấn đề out-of-distribution (OOD; dữ liệu khác xa phân phối lúc huấn luyện)
    - OOD nội sinh (Internalization-OOD): GUI agent huấn luyện trên một hệ điều hành cụ thể không có năng lực thực thi nhiệm vụ trên các hệ điều hành khác
    - OOD ngoại suy (Extrapolation-OOD): GUI agent huấn luyện trên dữ liệu tĩnh không thích ứng tốt với ứng dụng và công cụ mới

[1] Wu, Zheng, et al. GEM: Gaussian Embedding Modeling for Out-of-Distribution Detection for GUI Agents

## Slide 38

**Vấn đề độ tin cậy của GUI agent: vấn đề OOD**

- So với phát hiện OOD truyền thống, phát hiện OOD cho GUI agent còn có những thách thức riêng của lĩnh vực:
    - Hiểu không gian ngữ nghĩa đầu vào phức tạp: GUI agent cần đồng thời hiểu bố cục màn hình phức tạp và instruction đa dạng của người dùng
    - Môi trường thực thay đổi động: bố cục của ứng dụng và trang web trong thế giới thực có thể được cập nhật bất cứ lúc nào

*Chú thích trong hình: Không gian ngữ nghĩa phức tạp: một ảnh chụp màn hình được nhận diện ra 40 box · Môi trường thực động: Taobao tạm thời cập nhật giao diện khuyến mãi dịp lễ 1/5*

[1] Wu, Zheng, et al. GEM: Gaussian Embedding Modeling for Out-of-Distribution Detection for GUI Agents

## Slide 39

**Vấn đề độ tin cậy của GUI agent: thực thi quá mức**

- Khi gặp kịch bản phức tạp vượt quá năng lực của mình, GUI agent nên dừng thực thi để tránh thao tác không đáng tin cậy
- Tuy nhiên, GUI agent tự động hóa hoàn toàn vẫn thực thi quá mức. Nhận ra đúng thời điểm để con người can thiệp có thể giảm thực thi quá mức

[1] Cheng, Pengzhou et al. OS-Kairos: Adaptive Interaction for MLLM-Powered GUI Agents.

[2] Wu, Zheng et al. Universal Confidence Integration Framework for Adaptive Interaction in Computer-Using Agent.

## Slide 40

**Vấn đề độ tin cậy của GUI agent: cơ chế quay lui**

- Nếu GUI agent đã đi vào một đường sai, các thao tác tiếp theo của agent rất có thể không đáng tin cậy
- Cơ chế quay lui (rollback) phù hợp giúp GUI agent tránh tiếp tục thực thi các hành động không đáng tin cậy trên đường sai

[1] Zhang, Zhisong et al. Enhancing Web Agents with Explicit Rollback Mechanisms

## Slide 41

**Vấn đề độ tin cậy của GUI agent: nhiệm vụ mơ hồ**

- Đôi khi instruction người dùng đưa ra không đầy đủ, có thể thiếu một số thông tin then chốt
- Nếu bản thân instruction đã mơ hồ thì độ tin cậy của GUI agent sẽ bị giảm
- Khi instruction mơ hồ, việc học cách chủ động đặt câu hỏi cho người dùng có thể nâng cao độ tin cậy của GUI agent

[1] Cheng, Ziming et al. Navi-plus: Managing Ambiguous GUI Navigation Tasks with Follow-up Questions

## Slide 42

**Mục lục**

- Tổng quan về agent tự chủ trên giao diện người dùng đồ họa
    - Bối cảnh nghiên cứu
    - Hiện trạng phát triển
    - Các nhánh kỹ thuật
- Toàn bộ chuỗi kỹ thuật của agent tự chủ trên giao diện người dùng đồ họa
    - Triển khai GUI agent
    - Giải pháp cho nhiệm vụ tĩnh: supervised fine-tuning
    - Giải pháp cho nhiệm vụ động: học tăng cường
    - Giải pháp cho nhiệm vụ phức tạp: hệ thống điều phối
- An toàn và độ tin cậy của agent tự chủ trên giao diện người dùng đồ họa
    - Vấn đề an toàn của GUI agent
    - Vấn đề độ tin cậy của GUI agent

## Slide 43

**Thank You**
