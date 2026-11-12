# Suy luận toán học với LLM
Dự án này hiện thực code giúp mô hình ngôn ngữ lớn (LLM) học suy luận toán học. Kỹ thuật chính là dùng Supervised Finetuning (SFT; fine-tuning trên cặp đầu vào–đáp án mẫu do người hoặc mô hình mạnh hơn viết) để mô hình học theo các câu trả lời do DeepSeek-R1 sinh ra, từ đó học được các kỹ năng suy luận toán học phức tạp (như tự phản tư, tính lại để kiểm tra, v.v.).
Bài thực hành này dựa trên tập dữ liệu [DeepMath-103K](https://huggingface.co/datasets/zwhe99/DeepMath-103K) và mô hình [Qwen/Qwen2.5-Math-1.5B](https://huggingface.co/Qwen/Qwen2.5-Math-1.5B), dẫn người đọc thử bước đầu toàn bộ quy trình data distillation (dùng đầu ra của mô hình lớn – teacher – để huấn luyện mô hình nhỏ – student) trên các bài toán.

## Mục tiêu thực hành
- Hiểu cách làm sạch và tiền xử lý tập dữ liệu toán học
- Hiểu các phương pháp cơ bản để fine-tuning (tinh chỉnh một mô hình đã huấn luyện trên dữ liệu của một nhiệm vụ cụ thể) mô hình lớn
- Hiểu các phương pháp cơ bản để chạy inference (chạy mô hình đã huấn luyện để sinh đầu ra) với mô hình lớn
- Hiểu các phương pháp cơ bản để đánh giá năng lực toán học của mô hình

## Yêu cầu môi trường

- Python 3.8+
- PyTorch
- Transformers
- Datasets
- vllm
- GPU có tối thiểu 40GB bộ nhớ GPU (VRAM)

## Tài liệu thực hành

1. Mở Jupyter notebook (tệp Jupyter gồm code và lời giải thích):
```bash
jupyter notebook sft_math.ipynb
```

2. Notebook gồm một số phần chính:
   - Tải và tiền xử lý tập dữ liệu
   - Nạp và huấn luyện mô hình
   - Sinh đầu ra và đánh giá mô hình

3. Xem các bước cụ thể và phần giải thích trong notebook.

## Tệp đầu ra

Quá trình huấn luyện sẽ tạo ra các tệp checkpoint (bản lưu trọng số mô hình tại một thời điểm huấn luyện); sau khi sinh xong, kết quả sinh sẽ được lưu lại.

## Lưu ý

- Mô hình và dữ liệu cần được tải từ Hugging Face (huggingface); ở Trung Quốc đại lục có thể tải qua mirror https://hf-mirror.com (máy chủ sao chép để tải nhanh hơn).
- Đảm bảo có đủ dung lượng đĩa để lưu tệp mô hình gốc, tệp dữ liệu và checkpoint sau huấn luyện (hãy chừa ít nhất 50GB)
- Cần dùng card GPU có tối thiểu 40GB bộ nhớ GPU (VRAM)
