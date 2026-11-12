# Steganography văn bản bằng LLM

Dự án này hiện thực steganography (kỹ thuật giấu tin: giấu thông điệp bí mật bên trong một nội dung trông bình thường) cho văn bản, dựa trên mô hình ngôn ngữ lớn (LLM), dùng mô hình GPT-2 để giấu thông tin trong văn bản được sinh ra. Dự án có hai phương pháp mã hóa: mã hóa Huffman (Huffman Coding) và mã hóa độ dài cố định (Fixed Length Coding, FLC).

## Tính năng

- Hiện thực steganography trong quá trình sinh văn bản của GPT-2
- Hỗ trợ hai phương pháp mã hóa:
  - Mã hóa Huffman (Huffman Coding)
  - Mã hóa độ dài cố định (Fixed Length Coding, FLC)
- Sinh đồng thời văn bản chứa tin giấu (stegotext) và văn bản thường để so sánh

## Yêu cầu môi trường

- Python 3.8+
- PyTorch
- Transformers
- CUDA (tùy chọn, để tăng tốc bằng GPU)

## Các bước cài đặt

Cài các gói phụ thuộc:

```bash
pip install torch # Nếu dùng GPU, lưu ý cài bản torch dành cho GPU
pip install transformers
pip install jupyter
```

## Cách sử dụng

1. Mở Jupyter notebook (tệp Jupyter gồm code và lời giải thích):
```bash
jupyter notebook llm_stega.ipynb
```

2. Notebook gồm ba phần chính:
   - Hiện thực mã hóa Huffman
   - Hiện thực mã hóa độ dài cố định (FLC)
   - Sinh văn bản và steganography

3. Sinh văn bản chứa tin giấu:
   - Chọn phương pháp mã hóa (mã hóa Huffman hoặc FLC)
   - Đặt tham số (giá trị k của phép mã hóa)
   - Chạy hàm chính với prompt (đầu vào bằng văn bản đưa cho mô hình để yêu cầu nó làm một việc) tự chọn

Code ví dụ:
```python
# Khởi tạo bộ xử lý steganography
k = 2
handle = Huffman(k=2**k, bits=bits)
# Hoặc dùng FLC
# handle = FLC(k=k, bits=bits)

# Sinh văn bản có giấu tin
prompt = "Hello，I'm"
stega_output, normal_output = generate_text_with_steganography(
    model, tokenizer, prompt, handle
)
```

## Tệp đầu ra

Chương trình sẽ tạo hai tệp văn bản:
- `outputs-gpt2-stega.txt`: văn bản chứa tin giấu
- `outputs-gpt2-normal.txt`: văn bản mà mô hình vốn sinh ra bình thường khi không có ràng buộc giấu tin

## Lưu ý

- Mô hình GPT-2 sẽ được tự động tải về ở lần chạy đầu tiên; ở Trung Quốc đại lục cũng có thể tải trước mô hình GPT-2 qua mirror (máy chủ sao chép để tải nhanh hơn) https://hf-mirror.com, và cũng có thể dùng mô hình lớn khác.
- Đảm bảo có đủ dung lượng đĩa (mô hình khoảng 500MB)
- Nên dùng GPU hỗ trợ CUDA để có hiệu năng tốt hơn
- Độ dài thông tin cần giấu sẽ ảnh hưởng đến độ dài văn bản được sinh ra

## Nguyên lý hoạt động

1. Quá trình nhúng tin:
   - Chuyển thông điệp bí mật thành chuỗi nhị phân
   - Dùng mô hình GPT-2 để sinh văn bản
   - Dùng phương pháp mã hóa để nhúng các bit thông tin vào văn bản được sinh ra

2. Quá trình giải mã:
   - Dùng cùng mô hình GPT-2 và cùng ngữ cảnh
   - Dùng phương pháp giải mã để trích xuất các bit thông tin đã giấu từ văn bản
   - Chuyển chuỗi nhị phân trở lại thông điệp ban đầu
