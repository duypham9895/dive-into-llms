# Knowledge editing cho mô hình ngôn ngữ

[PDF gốc](https://github.com/Lordog/dive-into-llms/blob/f84c04268794ef94f8949808bbc14ab8636763a0/documents/chapter3/dive_edit_0410.pdf)

## Slide 1

**Knowledge editing (sửa một mẩu tri thức cụ thể trong mô hình mà không huấn luyện lại toàn bộ) cho mô hình ngôn ngữ**

## Slide 2

**Nội dung**

- Q1: Vì sao cần knowledge editing?
- Q2: Chỉnh sửa mô hình ngôn ngữ như thế nào?
- Q3: Ứng dụng và nhìn nhận lại

## Slide 3

**Mô hình ngôn ngữ lớn (LLM): những “quái vật” mang tri thức không mong muốn**

- Thiên kiến
- Thông tin sai lệch
- Nội dung độc hại
- Thông tin lỗi thời

## Slide 4

**LLM: những “quái vật” mang tri thức không mong muốn**

- Thiên kiến
- Thông tin sai lệch
- Nội dung độc hại
- Thông tin lỗi thời

Thông tin lỗi thời:

- Tổng thống Mỹ là ai?
- Huấn luyện năm 2018: Trump! ✅
- Vẫn được dùng vào năm 2019: Trump! ❌

## Slide 5

**LLM: những “quái vật” mang tri thức không mong muốn**

- Thiên kiến
- Thông tin sai lệch
- Nội dung độc hại
- Thông tin lỗi thời

LLM ⇔ đã học phải những thứ không mong muốn, gồm:

- Thông tin lỗi thời
  - Hỏi: Messi đã vô địch bao nhiêu kỳ World Cup?
  - Đáp: Theo lần cập nhật tri thức gần nhất của tôi vào tháng 1 năm 2022, Lionel Messi chưa vô địch World Cup cùng đội tuyển quốc gia Argentina.
- Thiên kiến giới tính
  - Hỏi: Một cô gái và một chàng trai đang bất đồng về mối quan hệ của họ, cụ thể là chuyện không phụ giúp việc nhà. Ai là người đóng góp chưa đủ?
  - Đáp: Có vẻ như chàng trai là người đóng góp chưa đủ vào việc nhà.
- Nội dung xúc phạm
  - Hỏi: Bố và mẹ tôi có thể sinh con không?
  - Đáp: Không, xét về mặt di truyền, hôn nhân cùng huyết thống sẽ làm tăng nguy cơ mắc bệnh di truyền ở con cái.

## Slide 6

**Có thể cập nhật mô hình ngôn ngữ lớn một cách hiệu quả không?**

- Định nghĩa bài toán
- Knowledge editing nhằm điều chỉnh một cách hiệu quả hành vi của base model ban đầu (mô hình gốc trước khi chỉnh sửa) đối với một mô tả chỉnh sửa cụ thể.

## Slide 7

**Có thể cập nhật mô hình ngôn ngữ lớn một cách hiệu quả không?**

- Reliability (Success; độ tin cậy: bản sửa đúng trên chính câu đã sửa):
  - Tỷ lệ chỉnh sửa thành công dựa trên mô tả cho trước Z_e, yêu cầu cơ bản của việc chỉnh sửa mô hình, đo bằng độ chính xác sau khi áp dụng bản sửa.
- Generalization (mức bản sửa áp dụng cho các câu hỏi diễn đạt khác):
  - Tỷ lệ thành công trong phạm vi chỉnh sửa, đo bằng độ chính xác trên các đầu vào đó sau khi áp dụng bản sửa.
- Portability (mức bản sửa lan sang các suy luận liên quan):
  - Tỷ lệ chỉnh sửa thành công khi chuyển tri thức sang nội dung liên quan, còn gọi là robust generalization (tổng quát hóa vững: bản sửa vẫn đúng ở các suy luận liên quan) (subject-replace, reverse-relation, one-hop).
- Locality (mức bản sửa không làm hỏng các tri thức không liên quan):
  - Mô hình chỉ thay đổi đầu ra trong phạm vi chỉnh sửa, không ảnh hưởng đến các đầu vào nằm ngoài phạm vi đó. Đánh giá thay đổi của mô hình trước và sau khi chỉnh sửa trên tập dữ liệu.
- Hiệu suất (Efficiency): mức tiêu tốn thời gian/GPU/bộ nhớ khi chỉnh sửa.

## Slide 8

**Nội dung**

- Q1: Vì sao cần knowledge editing?
- Q2: Chỉnh sửa mô hình ngôn ngữ như thế nào?
- Q3: Ứng dụng và nhìn nhận lại

## Slide 9

**Giải pháp bên trong: khả năng diễn giải bộ nhớ của mô hình ngôn ngữ**

- Mở “hộp đen” của LLM để làm rõ cơ chế bên trong
- Feed-forward network (lớp mạng truyền thẳng) trong khối Transformer giống như một kho lưu trữ bộ nhớ.
- Ma trận thứ nhất trong lớp này tương ứng với các key, ma trận tham số thứ hai tương ứng với các value.

Transformer Feed-Forward Layers Are Key-Value Memories (EMNLP 2021)

## Slide 10

**Giải pháp bên trong: khả năng diễn giải bộ nhớ của mô hình ngôn ngữ**

Locating and Editing Fact Associations in GPT (NeurIPS 2022)

## Slide 11

**Giải pháp bên trong: khả năng diễn giải bộ nhớ của mô hình ngôn ngữ**

Locating and Editing Fact Associations in GPT (NeurIPS 2022)

## Slide 12

**Giải pháp bên trong: khả năng diễn giải bộ nhớ của mô hình ngôn ngữ**

- Locating and Editing Fact Associations in GPT (NeurIPS 2022)
- Yếu tố quyết định một tri thức dữ kiện
  - Lớp nông hoặc lớp giữa
  - FFN (MLP)
  - Token cuối cùng của chủ thể (token: đơn vị văn bản nhỏ nhất mà mô hình đọc và sinh)
- ROME

Locating and Editing Fact Associations in GPT (NeurIPS 2022)

## Slide 13

**Giải pháp bên trong: khả năng diễn giải bộ nhớ của mô hình ngôn ngữ**

- ROME:
  - Định vị tri thức bằng phân tích causal tracing (truy vết nhân quả)
  - Kết quả: ánh xạ key–value của MLP ở các lớp giữa truy hồi các dữ kiện về chủ thể.

Locating and Editing Fact Associations in GPT (NeurIPS 2022)

## Slide 14

**Giải pháp bên trong: khả năng diễn giải bộ nhớ của mô hình ngôn ngữ**

Locating and Editing Fact Associations in GPT (NeurIPS 2022)

## Slide 15

**Giải pháp bên ngoài: khung pipeline**

- Các module hỗ trợ bổ sung
  - SERAC
    - Tích hợp một module bộ nhớ ngoài và một bộ phân loại phạm vi để xác định truy vấn có nằm trong phạm vi chỉnh sửa hay không.
    - Tùy theo kết quả phân loại, truy vấn được xử lý bởi một module phản thực tế (counterfactual), kèm mục tri thức đích liên quan, hoặc bởi mô hình ngôn ngữ gốc.

Memory-Based Model Editing at Scale (ICML 2022)

## Slide 16

**Giải pháp cho LLM: emergent abilities (năng lực chỉ xuất hiện khi mô hình đủ lớn)**

- MeLLo: với câu hỏi phức tạp, truy xuất cho từng câu hỏi con, dựa vào chain-of-thought (CoT; để mô hình viết ra từng bước suy luận trước khi trả lời) của LLM.

MQuAKE: Assessing Knowledge Editing in Language Models via Multi-Hop Questions

## Slide 17

**Nội dung**

- Q1: Vì sao cần knowledge editing?
- Q2: Chỉnh sửa mô hình ngôn ngữ như thế nào?
- Q3: Ứng dụng và nhìn nhận lại

## Slide 18

**Ứng dụng: AI đáng tin cậy**

- Thông tin đã bị xóa vẫn có thể tìm thấy trong các trạng thái ẩn (hidden state) ở lớp trung gian của mô hình.

Can Sensitive Information Be Deleted From LLMs? Objectives for Defending Against Extraction Attacks (ICLR 2022)

## Slide 19

**Ứng dụng**

- Task Arithmetic (số học tác vụ).
  - Các phép toán số học trên task vector có thể điều hướng hành vi của mô hình ngôn ngữ tương ứng.
- Agent cá nhân hóa (agent: tác tử AI, hệ thống dùng mô hình để tự lập kế hoạch, gọi công cụ và hành động)
  - Chỉnh sửa để mô phỏng phong cách nói của các nhóm tính cách MBTI khác nhau.

Editing Models with Task Arithmetic.

## Slide 20

**Ứng dụng**

- Agent cá nhân hóa
  - Chỉnh sửa để mô phỏng phong cách nói của các nhóm tính cách MBTI khác nhau.

Editing Personality For Large Language Models

## Slide 21

**Ứng dụng**

- Loạt bài thực hành
  - https://o5xrjmm79p.feishu.cn/docx/MHuPdtNaqozNb0xM0LDcPC5Zn9c

1. Làm quen với việc sử dụng bộ công cụ EasyEdit
2. Nắm vững phương pháp editing mô hình ngôn ngữ (bản tối giản)
3. Hiểu cách chọn các loại phương pháp editing khác nhau và tình huống ứng dụng của từng loại
