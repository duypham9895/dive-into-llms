# Watermark cho LLM

[PDF gốc](https://github.com/Lordog/dive-into-llms/blob/f84c04268794ef94f8949808bbc14ab8636763a0/documents/chapter5/watermark.pdf)

## Slide 1

**Watermark cho LLM**

- Zhiwei He
- School of Electronic Information and Electrical Engineering
- Shanghai Jiao Tong University
- 14 tháng 4 năm 2024

_Điều hướng: Động lực · Phương pháp watermark · Watermark có còn tồn tại sau khi dịch không? · Hạn chế_

## Slide 2

**Dàn ý**

1. Động lực
2. Phương pháp watermark
    - Giới thiệu
    - KGW (ICML 23 Outstanding)
    - SIR (ICLR 24)
3. Watermark có còn tồn tại sau khi dịch không?
    - Giới thiệu
    - Đánh giá
    - Tấn công
    - Phòng thủ

## Slide 3

**Động lực**

- Các mô hình ngôn ngữ lớn (LLM) đã cho thấy khả năng sinh nội dung ấn tượng.
- Hạn chế việc lạm dụng LLM là điều quan trọng.
- Gắn dấu và nhận diện được nội dung do LLM sinh ra sẽ có ích.

## Slide 4

_Điều hướng: Giới thiệu · KGW (ICML 23 Outstanding) · SIR (ICLR 24)_

**Dàn ý**

1. Động lực
2. Phương pháp watermark
    - Giới thiệu
    - KGW (ICML 23 Outstanding)
    - SIR (ICLR 24)
3. Watermark có còn tồn tại sau khi dịch không?
    - Giới thiệu
    - Đánh giá
    - Tấn công
    - Phòng thủ

## Slide 5

_Điều hướng: Giới thiệu · KGW (ICML 23 Outstanding) · SIR (ICLR 24)_

**Giới thiệu**

- Text watermarking (nhúng watermark vào văn bản; watermark là dấu ẩn được nhúng vào văn bản do mô hình sinh để sau này máy phát hiện được) nhúng một “thông điệp” vào nội dung do LLM sinh ra.

## Slide 6

_Điều hướng: Giới thiệu · KGW (ICML 23 Outstanding) · SIR (ICLR 24)_

**Giới thiệu**

- Text watermarking nhúng một “thông điệp” vào nội dung do LLM sinh ra.
    - con người không nhìn thấy
    - thuật toán phát hiện được

## Slide 7

_Điều hướng: Giới thiệu · KGW (ICML 23 Outstanding) · SIR (ICLR 24)_

**Giới thiệu**

- Text watermarking nhúng một “thông điệp” vào nội dung do LLM sinh ra.
    - con người không nhìn thấy
    - thuật toán phát hiện được
- Ở dạng đơn giản nhất, “thông điệp” có thể chỉ là một bit cho biết có watermark hay không.

## Slide 8

_Điều hướng: Giới thiệu · KGW (ICML 23 Outstanding) · SIR (ICLR 24)_

**Dàn ý**

1. Động lực
2. Phương pháp watermark
    - Giới thiệu
    - KGW (ICML 23 Outstanding)
    - SIR (ICLR 24)
3. Watermark có còn tồn tại sau khi dịch không?
    - Giới thiệu
    - Đánh giá
    - Tấn công
    - Phòng thủ

## Slide 9

_Điều hướng: Giới thiệu · KGW (ICML 23 Outstanding) · SIR (ICLR 24)_

**Ký hiệu**

- Mô hình ngôn ngữ: `M`
- Bộ từ vựng: `V`
- Một chuỗi token (đơn vị văn bản nhỏ nhất mà mô hình đọc và sinh: một từ, một phần từ hoặc một ký tự): `x^{1:n} = (x^1, x^2, ..., x^n)`
- Xác suất có điều kiện của token kế tiếp: `P_M(x^{n+1} | x^{1:n})`
- Logits (điểm thô trước softmax cho mỗi lớp/token) của token kế tiếp: `z^{n+1} = M(x^{1:n}) ∈ R^{|V|}`
- Do đó, ta có `P_M(x^{n+1} | x^{1:n}) = softmax(z^{n+1})`.

## Slide 10

_Điều hướng: Giới thiệu · KGW (ICML 23 Outstanding) · SIR (ICLR 24)_

**KGW (ICML 23 Outstanding)**

## Slide 11

_Điều hướng: Giới thiệu · KGW (ICML 23 Outstanding) · SIR (ICLR 24)_

**Ý tưởng cốt lõi**

Phân hoạch bộ từ vựng dựa trên văn bản đứng trước.

- Phân hoạch bộ từ vựng: ở mỗi bước, chia ngẫu nhiên bộ từ vựng `V` thành hai tập con rời nhau: danh sách xanh `V_g` và danh sách đỏ `V_r`.
- Dựa trên văn bản đứng trước: tính ngẫu nhiên được khởi tạo (seed) bằng giá trị băm của văn bản đứng trước.
- Tăng xác suất cho các token xanh (các token thuộc `V_g`).

## Slide 12

_Điều hướng: Giới thiệu · KGW (ICML 23 Outstanding) · SIR (ICLR 24)_

**Nhúng watermark (Watermark Ironing)**

Ở mỗi bước giải mã:

1. Tính giá trị băm của `x^{1:n}`: `h^{n+1} = H(x^{1:n})`. `H(·)` chỉ được dùng `k` token cuối `x^{n−k+1:n}`.
2. Dùng `h^{n+1}` làm seed cho một bộ sinh số ngẫu nhiên và chia ngẫu nhiên `V` thành hai danh sách rời nhau: danh sách xanh `V_g` và danh sách đỏ `V_r`.
3. Điều chỉnh logits `z^{n+1}` bằng cách cộng một độ lệch hằng `δ` (`δ > 0`) cho các token thuộc danh sách xanh:

```text
∀i ∈ {1, 2, ..., |V|},
z̃_i^{n+1} = z_i^{n+1} + δ,   nếu v_i ∈ V_g,
z̃_i^{n+1} = z_i^{n+1},       nếu v_i ∈ V_r.          (1)
```

## Slide 13

_Điều hướng: Giới thiệu · KGW (ICML 23 Outstanding) · SIR (ICLR 24)_

**Nhúng watermark (Watermark Ironing)**

- Kết quả là văn bản có watermark, xét về thống kê, sẽ chứa nhiều token xanh hơn, một đặc điểm khó xuất hiện trong văn bản do người viết.

## Slide 14

_Điều hướng: Giới thiệu · KGW (ICML 23 Outstanding) · SIR (ICLR 24)_

**Watermark detection (kiểm tra một đoạn văn có mang watermark hay không)**

Khi phát hiện, có thể áp dụng bước (1) và (2), rồi tính z-score (điểm chuẩn hóa đo độ mạnh của watermark) của `x`:

```text
s = (|x|_g − γ|V|) / sqrt(|V| γ (1 − γ)),          (2)
```

trong đó `|x|_g` là số token xanh trong `x` và `γ = |V_g| / |V|`. Có watermark hay không được xác định bằng cách so sánh `s` với một ngưỡng thích hợp.

## Slide 15

_Điều hướng: Giới thiệu · KGW (ICML 23 Outstanding) · SIR (ICLR 24)_

**Hiệu năng: ROC curve (đường cong đánh đổi giữa tỉ lệ phát hiện đúng và báo nhầm), AUC 0.998**

## Slide 16

_Điều hướng: Giới thiệu · KGW (ICML 23 Outstanding) · SIR (ICLR 24)_

**Chất lượng văn bản**

```text
∀i ∈ {1, 2, ..., |V|},
z̃_i^{n+1} = z_i^{n+1} + δ,   nếu v_i ∈ V_g,
z̃_i^{n+1} = z_i^{n+1},       nếu v_i ∈ V_r.
```

## Slide 17

_Điều hướng: Giới thiệu · KGW (ICML 23 Outstanding) · SIR (ICLR 24)_

**Dàn ý**

1. Động lực
2. Phương pháp watermark
    - Giới thiệu
    - KGW (ICML 23 Outstanding)
    - SIR (ICLR 24)
3. Watermark có còn tồn tại sau khi dịch không?
    - Giới thiệu
    - Đánh giá
    - Tấn công
    - Phòng thủ

## Slide 18

_Điều hướng: Giới thiệu · KGW (ICML 23 Outstanding) · SIR (ICLR 24)_

**SIR (ICLR 24)**

## Slide 19

_Điều hướng: Giới thiệu · KGW (ICML 23 Outstanding) · SIR (ICLR 24)_

**Giới thiệu**

- Robustness (khả năng giữ hiệu quả khi bị nhiễu hoặc bị tấn công) của watermark, tức khả năng phát hiện văn bản có watermark ngay cả sau khi văn bản đã bị sửa đổi, là điều quan trọng.
- Semantic invariant robust watermark (SIR; watermark bền vững, bất biến theo ngữ nghĩa) được thiết kế để tăng robustness trước tấn công viết lại văn bản.
- Tấn công viết lại văn bản: thay đổi câu chữ của văn bản mà không đổi ngữ nghĩa, chẳng hạn dịch đi dịch lại (re-translation) và paraphrase (viết lại cùng ý bằng câu chữ khác).

## Slide 20

_Điều hướng: Giới thiệu · KGW (ICML 23 Outstanding) · SIR (ICLR 24)_

**Một góc nhìn tổng quát về việc điều chỉnh logits**

```text
∀i ∈ {1, 2, ..., |V|},
z̃_i^{n+1} = z_i^{n+1} + δ,   nếu v_i ∈ V_g,
z̃_i^{n+1} = z_i^{n+1},       nếu v_i ∈ V_r.
```

Có thể xem quá trình điều chỉnh logits là việc áp dụng một hàm `∆` (`∆ ∈ R^{|V|}`): `z̃^{n+1} = z^{n+1} + ∆(x^{1:n})`.

## Slide 21

_Điều hướng: Giới thiệu · KGW (ICML 23 Outstanding) · SIR (ICLR 24)_

**Phương pháp**

**Ý tưởng cốt lõi**

`Sim(∆(x), ∆(y)) ≈ Sim(E(x), E(y))`, trong đó `E(·)` là một mô hình embedding (vector số biểu diễn ý nghĩa của văn bản/ảnh/âm thanh) và `Sim(·)` là một hàm tương đồng.

Cho trước một mô hình embedding `E`, SIR huấn luyện một hàm `∆` với mục tiêu chính:

```text
L = |Sim(E(x), E(y)) − Sim(∆(x), ∆(y))|.          (3)
```

Ngoài ra, `∀i ∈ {1, 2, ..., |V|}`, `∆_i` được huấn luyện để gần với +1 hoặc −1. Vì vậy, có thể xem SIR là một cải tiến dựa trên KGW, trong đó `∆_i > 0` cho biết `v_i` là một token xanh.

## Slide 22

_Điều hướng: Giới thiệu · KGW (ICML 23 Outstanding) · SIR (ICLR 24)_

**Hiệu năng (bản cài đặt của chúng tôi)**

## Slide 23

_Điều hướng: Giới thiệu · Đánh giá · Tấn công · Phòng thủ_

**Dàn ý**

1. Động lực
2. Phương pháp watermark
    - Giới thiệu
    - KGW (ICML 23 Outstanding)
    - SIR (ICLR 24)
3. Watermark có còn tồn tại sau khi dịch không?
    - Giới thiệu
    - Đánh giá
    - Tấn công
    - Phòng thủ

## Slide 24

_Điều hướng: Giới thiệu · Đánh giá · Tấn công · Phòng thủ_

**Watermark có còn tồn tại sau khi dịch không?**

- Các công trình hiện có về robustness của watermark chủ yếu tập trung vào tiếng Anh.
- Tuy nhiên, thế giới của chúng ta đa ngôn ngữ.
- Nếu ta dịch văn bản có watermark sang ngôn ngữ khác thì sao? Watermark có còn tồn tại sau khi dịch không?

## Slide 25

_Điều hướng: Giới thiệu · Đánh giá · Tấn công · Phòng thủ_

**Dàn ý**

1. Động lực
2. Phương pháp watermark
    - Giới thiệu
    - KGW (ICML 23 Outstanding)
    - SIR (ICLR 24)
3. Watermark có còn tồn tại sau khi dịch không?
    - Giới thiệu
    - Đánh giá
    - Tấn công
    - Phòng thủ

## Slide 26

_Điều hướng: Giới thiệu · Đánh giá · Tấn công · Phòng thủ_

**Đánh giá: tính nhất quán xuyên ngôn ngữ của text watermark**

- Chúng tôi định nghĩa tính nhất quán xuyên ngôn ngữ (cross-lingual consistency) để đánh giá khả năng text watermark giữ được hiệu quả sau khi văn bản được dịch sang ngôn ngữ khác.
- Cho độ mạnh watermark ban đầu `S` và độ mạnh sau khi dịch `Ŝ`:
    - Hệ số tương quan Pearson (Pearson Correlation Coefficient, PCC) phản ánh mức nhất quán về xu hướng:

      ```text
      PCC(S, Ŝ) = cov(S, Ŝ) / (σ_S σ_Ŝ),          (4)
      ```

    - Sai số tương đối (Relative Error, RE) phản ánh mức nhất quán về độ lớn:

      ```text
      RE(S, Ŝ) = E[ |Ŝ − S| / |S| ] × 100%.          (5)
      ```

## Slide 27

_Điều hướng: Giới thiệu · Đánh giá · Tấn công · Phòng thủ_

**PCC và RE**

- PCC nhìn chung nhỏ hơn 0.2, còn RE phần lớn trên 80%.
- SIR nhỉnh hơn các phương pháp khác.

## Slide 28

_Điều hướng: Giới thiệu · Đánh giá · Tấn công · Phòng thủ_

**Độ mạnh watermark theo độ dài văn bản**

Các phương pháp text watermarking hiện nay thiếu tính nhất quán xuyên ngôn ngữ.

## Slide 29

_Điều hướng: Giới thiệu · Đánh giá · Tấn công · Phòng thủ_

**Dàn ý**

1. Động lực
2. Phương pháp watermark
    - Giới thiệu
    - KGW (ICML 23 Outstanding)
    - SIR (ICLR 24)
3. Watermark có còn tồn tại sau khi dịch không?
    - Giới thiệu
    - Đánh giá
    - Tấn công
    - Phòng thủ

## Slide 30

_Điều hướng: Giới thiệu · Đánh giá · Tấn công · Phòng thủ_

**Tấn công: khoảng cách so với tình huống thực tế**

- Đổi ngôn ngữ: kẻ tấn công muốn xoá watermark thường không muốn đổi ngôn ngữ của câu trả lời.
- Chất lượng văn bản: việc dịch có thể ảnh hưởng đến chất lượng văn bản, nhưng chúng tôi chưa đánh giá điều này vì ở phần trước chúng tôi đã đổi ngôn ngữ của câu trả lời.

## Slide 31

_Điều hướng: Giới thiệu · Đánh giá · Tấn công · Phòng thủ_

**Cross-lingual Watermark Removal Attack (CWRA; tấn công xoá watermark xuyên ngôn ngữ)**

## Slide 32

_Điều hướng: Giới thiệu · Đánh giá · Tấn công · Phòng thủ_

**Hiệu năng: watermark detection** (chú thích 1, 2)

1. Chúng tôi cố định công cụ paraphrase và công cụ dịch dùng trong mọi phương pháp là gpt-3.5-turbo-0613.
2. Mô hình gốc (base model) là Baichuan, hỗ trợ tiếng Anh và tiếng Trung.

## Slide 33

_Điều hướng: Giới thiệu · Đánh giá · Tấn công · Phòng thủ_

**Hiệu năng: chất lượng văn bản**

- Các phương pháp tấn công này không chỉ giữ được chất lượng văn bản mà còn cải thiện nhẹ trong đa số trường hợp. Điều này có thể nhờ công cụ dịch và công cụ paraphrase tốt.
- CWRA cho kết quả tổng thể tốt nhất. Chúng tôi phỏng đoán rằng Baichuan còn làm tốt hơn ở ngôn ngữ trung gian (pivot language, tiếng Trung) so với ngôn ngữ gốc (tiếng Anh).

## Slide 34

_Điều hướng: Giới thiệu · Đánh giá · Tấn công · Phòng thủ_

**Dàn ý**

1. Động lực
2. Phương pháp watermark
    - Giới thiệu
    - KGW (ICML 23 Outstanding)
    - SIR (ICLR 24)
3. Watermark có còn tồn tại sau khi dịch không?
    - Giới thiệu
    - Đánh giá
    - Tấn công
    - Phòng thủ

## Slide 35

_Điều hướng: Giới thiệu · Đánh giá · Tấn công · Phòng thủ_

**Phòng thủ: làm sao cải thiện tính nhất quán xuyên ngôn ngữ?**

- Các phương pháp watermark dựa trên KGW về bản chất phụ thuộc vào cách phân hoạch bộ từ vựng, tức danh sách đỏ và danh sách xanh, như đã bàn ở Phần 2.

**Tính nhất quán xuyên ngôn ngữ**

Các token xanh trong văn bản có watermark vẫn được nhận ra là token xanh sau khi văn bản được dịch sang ngôn ngữ khác.

## Slide 36

_Điều hướng: Giới thiệu · Đánh giá · Tấn công · Phòng thủ_

**Một ví dụ đơn giản nhất - 1**

- ✓ Yếu tố 1: các token gần nghĩa nhau phải nằm cùng một danh sách (cùng đỏ hoặc cùng xanh)
- ✓ Yếu tố 2: cách phân hoạch bộ từ vựng cho các tiền tố (phần văn bản đứng trước) gần nghĩa nhau phải giống nhau.

## Slide 37

_Điều hướng: Giới thiệu · Đánh giá · Tấn công · Phòng thủ_

**Một ví dụ đơn giản nhất - 2**

- ✗ Yếu tố 1: các token gần nghĩa nhau phải nằm cùng một danh sách (cùng đỏ hoặc cùng xanh)
- ✓ Yếu tố 2: cách phân hoạch bộ từ vựng cho các tiền tố gần nghĩa nhau phải giống nhau.

## Slide 38

_Điều hướng: Giới thiệu · Đánh giá · Tấn công · Phòng thủ_

**Một ví dụ đơn giản nhất - 3**

- ✓ Yếu tố 1: các token gần nghĩa nhau phải nằm cùng một danh sách (cùng đỏ hoặc cùng xanh)
- ✗ Yếu tố 2: cách phân hoạch bộ từ vựng cho các tiền tố gần nghĩa nhau phải giống nhau.

## Slide 39

_Điều hướng: Giới thiệu · Đánh giá · Tấn công · Phòng thủ_

**Một ví dụ đơn giản nhất - 3**

- ✓ Yếu tố 1: các token gần nghĩa nhau phải nằm cùng một danh sách (cùng đỏ hoặc cùng xanh)
- ✗ Yếu tố 2: cách phân hoạch bộ từ vựng cho các tiền tố gần nghĩa nhau phải giống nhau.

Yếu tố 1 và 2 phải được thoả mãn đồng thời.

## Slide 40

_Điều hướng: Giới thiệu · Đánh giá · Tấn công · Phòng thủ_

**Phương pháp phòng thủ**

SIR đã tối ưu cho Yếu tố 2 vì mục tiêu của nó là:

```text
L = |Sim(E(x), E(y)) − Sim(∆(x), ∆(y))|.          (6)
```

Dựa trên SIR, chúng tôi bàn cách đạt Yếu tố 1 và đặt tên phương pháp của mình là X-SIR.

## Slide 41

_Điều hướng: Giới thiệu · Đánh giá · Tấn công · Phòng thủ_

**Phương pháp phòng thủ (X-SIR): điều chỉnh hàm ∆**

- Chúng tôi định nghĩa phân cụm ngữ nghĩa là một phân hoạch `C` của bộ từ vựng `V`:

  ```text
  C = {C_1, C_2, ..., C_|C|},          (7)
  ```

  trong đó mỗi cụm `C_i` gồm các token tương đương về ngữ nghĩa.
- Chúng tôi điều chỉnh hàm `∆` để nó cho ra độ lệch cho từng cụm trong `C`, tức `∆ ∈ R^{|C|}` (thay cho `∆ ∈ R^{|V|}`).
- Như vậy, quá trình điều chỉnh logits trở thành:

  ```text
  ∀i ∈ {1, 2, ..., |V|},
  z̃_i^{n+1} = z_i^{n+1} + ∆_{C(i)},          (8)
  ```

  trong đó `C(i)` là chỉ số của cụm chứa `v_i` trong `C`.

## Slide 42

_Điều hướng: Giới thiệu · Đánh giá · Tấn công · Phòng thủ_

**Phương pháp phòng thủ (X-SIR): phân cụm ngữ nghĩa cho bộ từ vựng**

```text
Thuật toán 1  Xây dựng các cụm ngữ nghĩa
Đầu vào: bộ từ vựng V, từ điển song ngữ D
Đầu ra: các cụm ngữ nghĩa 𝒞
 1: Khởi tạo đồ thị G chưa có cạnh, mỗi token trong V là một đỉnh
 2: for mỗi mục (v_i, v_j) trong từ điển song ngữ D do
 3:     if cả v_i và v_j đều thuộc V then
 4:         Thêm cạnh (v_i, v_j) vào G
 5:     end if
 6: end for
 7: Khởi tạo 𝒞 là tập rỗng
 8: for mỗi thành phần liên thông C trong G do
 9:     Thêm C vào 𝒞
10: end for
11: return 𝒞
```

## Slide 43

_Điều hướng: Giới thiệu · Đánh giá · Tấn công · Phòng thủ_

**Phương pháp phòng thủ (X-SIR): phân cụm ngữ nghĩa cho bộ từ vựng**

```text
Thuật toán 2  Xây dựng các cụm ngữ nghĩa
Đầu vào: bộ từ vựng V, từ điển song ngữ D
Đầu ra: các cụm ngữ nghĩa 𝒞
 1: Khởi tạo đồ thị G chưa có cạnh, mỗi token trong V là một đỉnh
 2: for mỗi mục (v_i, v_j) trong từ điển song ngữ D do
 3:     if cả v_i và v_j đều thuộc V then
 4:         Thêm cạnh (v_i, v_j) vào G
 5:     end if
 6: end for
 7: Khởi tạo 𝒞 là tập rỗng
 8: for mỗi thành phần liên thông C trong G do
 9:     Thêm C vào 𝒞
10: end for
11: return 𝒞
```

Dòng 2-3: chúng tôi chỉ xét các token có mặt trong cả V và D, điều này dẫn đến các hạn chế (bàn ở phần sau).

## Slide 44

_Điều hướng: Giới thiệu · Đánh giá · Tấn công · Phòng thủ_

**Phương pháp phòng thủ (X-SIR): phân cụm ngữ nghĩa cho bộ từ vựng**

- Chúng tôi cũng xét ký hiệu meta (U+2581) của sentencepiece.

## Slide 45

_Điều hướng: Giới thiệu · Đánh giá · Tấn công · Phòng thủ_

**Hiệu năng: watermark detection**

## Slide 46

_Điều hướng: Giới thiệu · Đánh giá · Tấn công · Phòng thủ_

**Hiệu năng: chất lượng văn bản**

## Slide 47

**Hạn chế**

Phân cụm ngữ nghĩa chỉ xét các token có mặt trong cả bộ từ vựng `V` của mô hình và từ điển ngoài `D`, dẫn đến các hạn chế sau.

- Độ phủ ngôn ngữ: chỉ hỗ trợ các ngôn ngữ mà mô hình hỗ trợ. Trong tình huống thực tế, kẻ tấn công có thể tự do chọn ngôn ngữ gốc và ngôn ngữ trung gian.
- Độ phủ bộ từ vựng (20.76%): vì từ điển ngoài `D` chỉ chứa từ hoàn chỉnh, các đơn vị nhỏ hơn từ không phân cụm được. Tokenizer (bộ chuyển văn bản thành chuỗi token id) của Llama có xu hướng tách một ký tự tiếng Trung thành nhiều byte.

## Slide 48

**Bài báo và mã nguồn**

- Bài báo: https://arxiv.org/abs/2402.14007
- Mã nguồn: https://github.com/zwhe99/X-SIR
