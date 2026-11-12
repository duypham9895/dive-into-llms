# Dive into LLMs: Steganography

[PDF gốc](https://github.com/Lordog/dive-into-llms/blob/f84c04268794ef94f8949808bbc14ab8636763a0/documents/chapter7/stega.pdf)

## Slide 1

**动手学大模型 (Dive into LLMs): steganography (kỹ thuật giấu tin: giấu thông điệp bí mật bên trong một nội dung trông bình thường)**

张玉龙 (Zhang Yulong)

## Slide 2

**Ứng dụng của mô hình lớn trong truyền thông bảo mật**

Steganography là một kỹ thuật ẩn giấu thông tin, với mục đích cốt lõi là nhúng thông tin vào nhiều loại vật mang tin (như ảnh số, âm thanh, video hoặc văn bản) để truyền tin bí mật. Steganography khác với kỹ thuật mã hóa bảo mật (encryption): nó không chỉ giấu nội dung thông tin mà còn giấu cả sự tồn tại của hành vi truyền tin. Kỹ thuật này tận dụng đặc điểm hệ thống cảm nhận của con người không nhạy với một số thông tin, giấu thông điệp bí mật vào phần thông tin dư thừa của vật mang tin số, khiến bề ngoài thông tin trông không khác gì một vật mang tin bình thường, nhờ đó kẻ tấn công khó nhận ra.

Ứng dụng của steganography gồm, nhưng không giới hạn ở, truyền tin bí mật, bảo vệ bản quyền, v.v. Cùng với sự phát triển của công nghệ, steganography ngày càng quan trọng trong các lĩnh vực quân sự, thương mại, nhưng đồng thời cũng tạo điều kiện cho các hành vi độc hại như hoạt động gián điệp, tấn công khủng bố, v.v.

## Slide 3

**Ý nghĩa của steganography**

Nói đơn giản, steganography là một phương pháp truyền tin an toàn khác với mật mã.

Mật mã “mã hóa bảo mật” bản rõ để người trung gian không lấy được nội dung thông điệp, nhưng vật mang thông điệp vẫn có thể bị người trung gian phát hiện và chiếm lấy, từ đó sửa đổi hoặc chặn việc truyền thông điệp.

Steganography thì “giấu” chính việc đang truyền thông điệp: giấu nội dung cần truyền trên một kênh công khai, ngụy trang thành nội dung bình thường, với mục tiêu chỉ bên nhận mới phát hiện được thông điệp ẩn, còn người trung gian thì không.

Ví dụ steganography đơn giản trong đời thực: thơ giấu chữ đầu dòng, mẩu giấy nhỏ kẹp trong sách, v.v.

Kỹ thuật phái sinh ở hạ nguồn của steganography: watermark (dấu ẩn được nhúng vào nội dung để sau này phát hiện được): có thể hiểu là một dạng steganography coi trọng robustness (khả năng giữ hiệu quả khi bị nhiễu hoặc bị tấn công) hơn, chấp nhận để nhiều người phát hiện và đọc ra thông tin.

## Slide 4

**Ví dụ về steganography: so sánh với mật mã**

Steganography (dạng văn bản):

- Thao tác: điều chỉnh khoảng cách giữa các chữ cái trong tài liệu điện tử (ví dụ chênh 0.1pt), màu chữ (#000000 vs #010101), mã hóa (encoding) thông tin dưới dạng nhị phân (ví dụ “khoảng cách lớn = 1, bình thường = 0”)<sup>1</sup>.
- Mục tiêu: giấu thông tin trong văn bản công khai, mắt thường không thấy được.

Mật mã học (mật mã Vigenère):

- Thao tác: dùng một từ khóa lặp lại để mã hóa bảo mật (ví dụ dùng khóa "KEY" mã hóa bảo mật "HELLO" → "RIJVS").
- Mục tiêu: tạo ra bản mã vô nghĩa, cần khóa mới giải mã bảo mật được<sup>7</sup>.
- So sánh:
  - Steganography: vật mang tin là tệp bình thường (ví dụ hợp đồng), không gây nghi ngờ.
  - Mật mã học: bản thân bản mã đã lộ ra là “có bí mật”, nhưng nội dung được giữ kín.

## Slide 5

**Ví dụ về steganography**

Steganography (LSB trên ảnh):

- Thao tác: sửa least significant bit (LSB; bit cuối của mỗi điểm ảnh, thay đổi mà mắt không thấy) của các điểm ảnh để nhúng dữ liệu bí mật (ví dụ dạng nhị phân của một ảnh khác). Mắt người không nhận ra khác biệt, nhưng công cụ có thể trích xuất được<sup>29</sup>.
- Mục tiêu: giấu thông tin trong một bức ảnh bình thường (ví dụ ảnh du lịch), vượt qua kiểm duyệt.

Mật mã học (AES-256):

- Thao tác: dùng khóa để mã hóa bảo mật tệp thành chuỗi vô nghĩa (ví dụ z.exe→G8x!gF2\*...
- Mục tiêu: dù tệp bị chặn bắt cũng không thể phá được nội dung.

Trường hợp dùng kết hợp:

- Trước tiên dùng AES để mã hóa bảo mật dữ liệu nhạy cảm;
- Sau đó nhúng bản mã vào LSB của ảnh.

  → Bảo vệ kép: vừa giấu sự tồn tại (trông như ảnh bình thường), vừa giấu nội dung (cần khóa mới giải mã bảo mật được)

## Slide 6

**Ví dụ về steganography**

Steganography trong mã QR:

Nguyên lý: thiết kế một mã QR trông hoàn toàn bình thường (trỏ tới một trang web vô hại), nhưng nhúng thêm thông tin ẩn (một URL khác, văn bản, ảnh nhỏ) vào vùng sửa lỗi của nó hoặc thông qua mẫu điểm mã được thiết kế kỹ lưỡng. Phần mềm quét mã thông thường chỉ đọc được thông tin bề mặt, cần phần mềm tùy biến mới đọc được lớp ẩn.

Ví dụ: mã QR trên thực đơn nhà hàng, quét thì hiện phần giới thiệu món ăn (lớp công khai), nhưng quét bằng một app riêng thì lấy được mã ưu đãi trong ngày hoặc thông tin nội bộ của nhân viên được giấu bên trong. Mã QR trên áp phích: quét thông thường là phần giới thiệu sự kiện, lớp ẩn là thư mời VIP.

Tình huống trong đời sống: hoạt động marketing (truy tìm kho báu, mở khóa ưu đãi), truyền thông tin nội bộ (thông báo cho nhân viên), bảo vệ bản quyền (nhúng thông tin chủ sở hữu vào mã QR công khai).

Điểm chính: cần hiểu cấu trúc mã QR (nhất là tính dư thừa của mã sửa lỗi), cần công cụ chuyên dụng để tạo mã QR hai lớp.

## Slide 7

**Mô hình của steganography**

Hiện nay, khi chọn vật mang tin là phương tiện số, steganography thường chọn ảnh hoặc video, vì chúng có nhiều không gian dư thừa để chèn thông tin. Còn văn bản làm vật mang tin thì độ dư thừa thấp, nhưng lại linh hoạt, lượng nội dung lớn, có thể khá dễ dàng nhúng vào các nội dung khác. Lần này chúng tôi dùng mô hình ngôn ngữ lớn (LLM) để giới thiệu steganography với mô hình lớn.

Mô hình quá trình của steganography (trái) và watermark (phải) như hình dưới đây.

## Slide 8

**Phân loại steganography văn bản**

Steganography văn bản chủ yếu gồm hai loại: dạng sửa đổi và dạng sinh.

Những năm gần đây, cùng với sự phát triển của học sâu, đặc biệt là mô hình lớn, steganography văn bản dạng sinh đã trở thành xu hướng chủ đạo.

## Slide 9

**Steganography văn bản với mô hình lớn<sup>1-3</sup>**

Dữ liệu của mô hình sinh văn bản đều là dữ liệu “dạng chuỗi”.

Khi đưa vào ngữ cảnh phía trước và các tham số, mô hình trả về một bảng logits (điểm thô trước softmax cho mỗi lớp/token) dự đoán “next token” (token: đơn vị văn bản nhỏ nhất mà mô hình đọc và sinh, có thể là một từ, một phần từ hoặc một ký tự); trong bảng là các token id xếp từ xác suất cao nhất đến thấp nhất.

Bình thường, mô hình sẽ dựa vào các tham số để chọn ngẫu nhiên một trong n token làm token tiếp theo, rồi tiếp tục vòng lặp sinh.

Còn steganography dạng sinh thì trong quá trình inference (chạy mô hình đã huấn luyện để sinh đầu ra), can thiệp vào việc mô hình chọn next token theo các quy tắc đã đặt sẵn, nhờ đó nhúng thông tin muốn giấu vào văn bản được sinh ra ngay trong quá trình inference.

[1] Yang, Zhong-Liang, et al. "RNN-stega: Linguistic steganography based on recurrent neural networks." IEEE Transactions on Information Forensics and Security 14.5 (2018): 1280-1295.

[2] Tang, Yifan, et al. "Linguistic Steganalysis via LLMs: Two Modes for Efficient Detection of Strongly Concealed Stego." IEEE Signal Processing Letters (2024).

[3] Yang, Zhong-Liang, et al. "VAE-Stega: linguistic steganography based on variational auto-encoder." IEEE Transactions on Information Forensics and Security 16 (2020): 880-895.

## Slide 10

**Steganography văn bản với mô hình lớn**

Lấy hình dưới đây làm ví dụ: giả sử tôi muốn nhúng thông điệp bí mật đã được chuyển sang nhị phân, tôi có thể mã hóa n token đầu tiên mà mô hình trả về cho next token ở mỗi bước. Chẳng hạn, khi tôi nhập “I”, 8 token đầu tiên mà mô hình trả về, xếp theo xác suất giảm dần, lần lượt là have(000), am(001), was(010), can(011)…. Mỗi token ứng với một giá trị nhị phân 3 bit; khi tôi muốn nhúng “001”, tôi chọn “am” làm next token, rồi vòng lặp tiếp tục.

## Slide 11

**Steganography văn bản với mô hình lớn**

Về bản chất, phương pháp ở đây là mã hóa n token ứng viên đầu tiên, tạo ra một không gian steganography ngầm; còn khi muốn giải mã thông tin, chỉ cần dùng cùng mô hình, cùng ngữ cảnh phía trước và cùng tham số thì có thể bảo đảm mỗi lần mô hình đều trả về một không gian mã hóa giống hệt lúc sinh, từ đó suy ngược từ token ra luồng thông tin nhị phân ban đầu, ví dụ từ “am” giải mã ngược ra 001.

## Slide 12

**Steganography văn bản với mô hình lớn**

Tất nhiên, phương pháp trên dùng cách mã hóa rất cố định (mã hóa trực tiếp n token đầu tiên theo thứ tự); hình dưới đây thực ra dùng mã hóa Huffman, nhờ đó nhúng được nhiều thông tin nhất có thể, nâng cao embedding rate (số bit tin giấu được trên mỗi token).

## Slide 13

**Ý nghĩa và tương lai của steganography với mô hình lớn**

Steganography với mô hình lớn: ưu điểm của việc dùng mô hình lớn để làm steganography là tận dụng được năng lực của mô hình lớn, cho ra nội dung giấu tin tự nhiên hơn, khó bị phát hiện hơn.

Không gian mã hóa: các phương pháp steganography khác nhau phụ thuộc nhiều vào cách mã hóa; nếu có phương pháp mới để xây dựng không gian mã hóa thì có thể tạo ra một kỹ thuật steganography mới.

Mở rộng liên ngành: bản chất của steganography văn bản dạng sinh với mô hình lớn là “mã hóa lặp trên dữ liệu dạng chuỗi”; kỹ thuật này cũng có thể chuyển sang các phương tiện khác. Ví dụ, DNA cũng là dữ liệu dạng chuỗi, có thể dùng thiết bị kết hợp với đầu ra của mô hình lớn để giấu tin vào mã DNA, nhờ đó trong quân sự có thể “giấu thông tin ẩn trong một chai nước, vài tế bào, vài sợi tóc”, đạt mức truyền tin ẩn rất cao.

Watermark cho mô hình lớn: các kỹ thuật watermark hiện có cho mô hình lớn cũng có thể kết hợp và thúc đẩy lẫn nhau với steganography. Ví dụ, watermark KGW nổi tiếng cũng ràng buộc việc chọn next token trong quá trình inference.

An toàn nội dung: kỹ thuật đối phó với steganography là “steganalysis (kỹ thuật phát hiện tin giấu)”, có thể dùng để đánh giá, sàng lọc và phát hiện nội dung trên các phương tiện truyền thông mạng. Những lời “mỉa mai bóng gió”, “bạo lực mạng, chửi bới” không chạm vào từ khóa thì về bản chất cũng là một dạng “steganography”, vì vậy cũng có khả năng bị trí tuệ nhân tạo (AI) tự động phát hiện bằng các phương pháp phát hiện steganography; điều này sẽ có lợi cho việc giữ gìn an ninh không gian mạng của con người trong tương lai.
