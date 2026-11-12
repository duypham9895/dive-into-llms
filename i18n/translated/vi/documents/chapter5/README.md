# Dive into LLMs: Watermark cho mô hình

Dẫn nhập: phần này giới thiệu watermark (dấu ẩn được nhúng vào văn bản do mô hình sinh để sau này máy phát hiện được) cho mô hình ngôn ngữ

> Nhúng vào nội dung do mô hình ngôn ngữ sinh ra một “watermark” mà con người không nhận ra nhưng thuật toán lại phát hiện được.

## Mục tiêu của bài hướng dẫn này

1. Nhúng watermark: nhúng watermark vào nội dung khi mô hình ngôn ngữ sinh văn bản
2. Watermark detection (kiểm tra một đoạn văn có mang watermark hay không): xác định độ mạnh watermark của một văn bản cho trước
3. Đánh giá watermark: đánh giá hiệu năng phát hiện của phương pháp watermark
4. Đánh giá robustness (khả năng giữ hiệu quả khi bị nhiễu hoặc bị tấn công) của watermark (tùy chọn)



## Chuẩn bị

### 2.1 Tìm hiểu kho mã (repository) X-SIR

https://github.com/zwhe99/X-SIR

Kho mã X-SIR chứa mã hiện thực các nội dung sau

- Ba thuật toán watermark văn bản: X-SIR, SIR và KGW
- Hai phương pháp tấn công xoá watermark: paraphrase (viết lại cùng ý bằng câu chữ khác) và translation (dịch sang ngôn ngữ khác)

![img](./assets/x-sir.png)

### 2.2 Cài đặt môi trường

```Shell
git clone https://github.com/zwhe99/X-SIR && cd X-SIR
conda create -n xsir python==3.10.10
conda activate xsir
pip3 install -r requirements.txt
# [optional] pip3 install flash-attn==2.3.3
```

> Các phiên bản trong requirements.txt chỉ là phiên bản khuyến nghị, không bắt buộc.



## Ví dụ thực hành

> Dùng thuật toán KGW để nhúng watermark vào nội dung do mô hình ngôn ngữ sinh ra

### 3.1 Chuẩn bị dữ liệu

Tổ chức các prompt (đầu vào bằng văn bản đưa cho mô hình để yêu cầu nó làm một việc) sẽ đưa vào mô hình ngôn ngữ thành một tệp jsonl:

```JSON
{"prompt": "Ghost of Emmett Till: Based on Real Life Events "}
{"prompt": "Antique Cambridge Glass Pink Decagon Console Bowl Engraved Gold Highlights\n"}
{"prompt": "2009 > Information And Communication Technology Index statistics - Countries "}
......
```

- Mỗi dòng là một json object và chứa ít nhất một khóa tên là “prompt”
- Phần sau lấy tệp `data/dataset/mc4/mc4.en.jsonl` làm ví dụ. Tệp này có tổng cộng 500 mẫu dữ liệu; nếu thấy mô hình xử lý quá lâu, bạn có thể tự cắt bớt dữ liệu.

### 3.2 Nhúng watermark

- Chọn mô hình và thuật toán watermark. Ở đây ta chọn mô hình `baichuan-inc/Baichuan-7B` và thuật toán watermark `KGW`

  - ```Shell
    MODEL_NAME=baichuan-inc/Baichuan-7B
    MODEL_ABBR=baichuan-7b
    WATERMARK_METHOD_FLAG="--watermark_method kgw"
    ```

- Sinh nội dung và nhúng watermark

  - ```Shell
    python3 gen.py \
        --base_model $MODEL_NAME \
        --fp16 \
        --batch_size 32 \
        --input_file data/dataset/mc4/mc4.en.jsonl \
        --output_file gen/$MODEL_ABBR/kgw/mc4.en.mod.jsonl \
        $WATERMARK_METHOD_FLAG
    ```

  - Lệnh này lưu nội dung do mô hình sinh ra vào tệp đầu ra: `gen/$MODEL_ABBR/kgw/mc4.en.mod.jsonl`

  - Định dạng của tệp đầu ra như sau, trong đó response là nội dung đầu ra của mô hình:

    - ```JSON
      {"prompt": "Ghost of Emmett Till: Based on Real Life Events ", "response": ".In August if 1955 African American Emmett Louis Till (21)\nThe second part of The Man From Waco, about Dan Millers trial for murdering his friend Michael Capps in a Texas wiener wrastle as I believe the statute says called it then; back at that time that would have surely occurred since Dan kept his pistol in one of those watery doggy bags he keeps around to clean himself with after emptying can into a nearby lake just minutes before committing his crime. If what we read is true thats exactly where Dan left his stolen gun and later used it in the robbery gone wrong which killed two innocent boys when his own accomplice got into an argument over not being paid enough therefore wanting out. This angered Miller whos history of mental instability could be taken one way or another but this criminal act was unavoidable once they entered FBIs hands and some other very powerful law officers who were involved either directly"}
      {"prompt": "Antique Cambridge Glass Pink Decagon Console Bowl Engraved Gold Highlights\n", "response": "An exceptionally fine decorative antique pink decagonal glass side bowl is the perfect example of early art and innovation . Fully engraved, this beautiful English vintage tableware piece exhibits a great degree on craftsmanship! Made in England during the mid 1800's it features three sets of concentric ribbons on the exterior to elegantly highlight an intricate, deep reddish color which evokes warmth and comfort for years to come! This historically significant vase has been featured within numerous museum exhibitions including \"Glass at The Corning Museum\" ; \"The First Half Century\" & a special travelling exhibit called:\" Sight Of Glass: British Cut Glass\" by ibex limited (retailer) as well as \"SIGNALS - Celebrating History In American Silver Through The Articulated Bottle Vessel\" presented at the Corning Museum of Glass 2012 ASA national symposium! We provide our customers with quality phot"}
      {"prompt": "2009 > Information And Communication Technology Index statistics - Countries ", "response": "5/22/2016\nAnnual change of mobile telephone subscriptions in Armenia (per 1 population). 2.2% increase is equivalent to 38 subscriptions per 100 people. Density rank: 121 out of 222.\nCyclist(s)/month(S). Likes bike riding? Take advantage of discount and cheap rental bikes at Rimon Bike Rentals in Yerevan! No advance payments or additional deposits are required. They have a good range of bicycles, including mountainbikes. More on their Facebook page \nYou must know about electric cars. The Renault Fluence KZERO gets it right in the city but I'm not sure what mileage you can expect from it. Still its fun project http://www.renault-kzen.com\nFor more on this and related issues : Armenian Institute for Electronic Governance reports |"}
      ......
      ```



### 3.3 Watermark detection

> Watermark detection là việc tính độ mạnh watermark (z-score; điểm chuẩn hóa) của một đoạn văn bản cho trước.

- Tính độ mạnh watermark của văn bản **có watermark**

  - ```python
    python3 detect.py \
        --base_model $MODEL_NAME \
        --detect_file gen/$MODEL_ABBR/kgw/mc4.en.mod.jsonl \
        --output_file gen/$MODEL_ABBR/kgw/mc4.en.mod.z_score.jsonl \
        $WATERMARK_METHOD_FLAG
    ```

- Tính độ mạnh watermark của văn bản **không có watermark**

  - ```python
    python3 detect.py \
        --base_model $MODEL_NAME \
        --detect_file data/dataset/mc4/mc4.en.jsonl \
        --output_file gen/$MODEL_ABBR/kgw/mc4.en.hum.z_score.jsonl \
        $WATERMARK_METHOD_FLAG
    ```

- Định dạng của tệp đầu ra:

  - ```JSON
    {"z_score": 12.105422509165574, "prompt": "Ghost of Emmett Till: Based on Real Life Events ", "response": ".In August if 1955 African American Emmett Louis Till (21)\nThe second part of The Man From Waco, about Dan Millers trial for murdering his friend Michael Capps in a Texas wiener wrastle as I believe the statute says called it then; back at that time that would have surely occurred since Dan kept his pistol in one of those watery doggy bags he keeps around to clean himself with after emptying can into a nearby lake just minutes before committing his crime. If what we read is true thats exactly where Dan left his stolen gun and later used it in the robbery gone wrong which killed two innocent boys when his own accomplice got into an argument over not being paid enough therefore wanting out. This angered Miller whos history of mental instability could be taken one way or another but this criminal act was unavoidable once they entered FBIs hands and some other very powerful law officers who were involved either directly", "biases": null}
    {"z_score": 12.990684249887122, "prompt": "Antique Cambridge Glass Pink Decagon Console Bowl Engraved Gold Highlights\n", "response": "An exceptionally fine decorative antique pink decagonal glass side bowl is the perfect example of early art and innovation . Fully engraved, this beautiful English vintage tableware piece exhibits a great degree on craftsmanship! Made in England during the mid 1800's it features three sets of concentric ribbons on the exterior to elegantly highlight an intricate, deep reddish color which evokes warmth and comfort for years to come! This historically significant vase has been featured within numerous museum exhibitions including \"Glass at The Corning Museum\" ; \"The First Half Century\" & a special travelling exhibit called:\" Sight Of Glass: British Cut Glass\" by ibex limited (retailer) as well as \"SIGNALS - Celebrating History In American Silver Through The Articulated Bottle Vessel\" presented at the Corning Museum of Glass 2012 ASA national symposium! We provide our customers with quality phot", "biases": null}
    {"z_score": 11.455466938203664, "prompt": "2009 > Information And Communication Technology Index statistics - Countries ", "response": "5/22/2016\nAnnual change of mobile telephone subscriptions in Armenia (per 1 population). 2.2% increase is equivalent to 38 subscriptions per 100 people. Density rank: 121 out of 222.\nCyclist(s)/month(S). Likes bike riding? Take advantage of discount and cheap rental bikes at Rimon Bike Rentals in Yerevan! No advance payments or additional deposits are required. They have a good range of bicycles, including mountainbikes. More on their Facebook page \nYou must know about electric cars. The Renault Fluence KZERO gets it right in the city but I'm not sure what mileage you can expect from it. Still its fun project http://www.renault-kzen.com\nFor more on this and related issues : Armenian Institute for Electronic Governance reports |", "biases": null}
    ......
    ```

- Xem bằng mắt sự khác biệt về độ mạnh watermark giữa hai tệp

### 3.4 Đánh giá watermark
<a name="eval"></a>

- Đưa vào các tệp z-score từ bước watermark detection, tính độ chính xác phát hiện và vẽ ROC curve (đường cong đánh đổi giữa tỉ lệ phát hiện đúng và báo nhầm)

  - ```Shell
    python3 eval_detection.py \
            --hm_zscore gen/$MODEL_ABBR/kgw/mc4.en.hum.z_score.jsonl \
            --wm_zscore gen/$MODEL_ABBR/kgw/mc4.en.mod.z_score.jsonl \
            --roc_curve roc
    
    AUC: 1.000
    
    TPR@FPR=0.1: 0.998
    TPR@FPR=0.01: 0.998
    
    F1@FPR=0.1: 0.999
    F1@FPR=0.01: 0.999
    ```

![img](./assets/curve.png)

## Đánh giá robustness của watermark (tùy chọn)

> Sau khi tấn công xoá watermark bằng paraphrase và translation lên văn bản có watermark, đánh giá lại hiệu quả phát hiện

### 4.1 Chuẩn bị

Ta dùng mô hình gpt-3.5-turbo-1106 để thực hiện paraphrase và translation trên văn bản có watermark. Bạn cũng có thể tự chọn công cụ khác.

- Thiết lập apikey của OpenAI

  - ```Shell
    export OPENAI_API_KEY=xxxx
    ```

- Sửa RPM (requests per min) and TPM (tokens per min) trong `attack/const.py`

### 4.2 Tấn công xoá watermark (lấy dịch làm ví dụ)

- Dịch văn bản có watermark sang tiếng Trung

  - ```Shell
    python3 attack/translate.py \
        --input_file gen/$MODEL_ABBR/kgw/mc4.en.mod.jsonl \
        --output_file gen/$MODEL_ABBR/kgw/mc4.en-zh.mod.jsonl \
        --model gpt-3.5-turbo-1106 \
        --src_lang en \
        --tgt_lang zh
    ```

- Đánh giá lại

  -  Xem [3.4](#eval)

- So sánh sự thay đổi hiệu năng watermark trước và sau khi tấn công



## Bài tập nâng cao

- Đọc tài liệu của [X-SIR](https://github.com/zwhe99/X-SIR), học cách dùng hai thuật toán còn lại (X-SIR, SIR) và đánh giá hiệu năng của chúng trước các phương pháp tấn công khác nhau