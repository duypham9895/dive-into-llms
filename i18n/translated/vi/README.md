<p align="center">
<h1 align="center">《动手学大模型》 (Dive into LLMs): loạt bài hướng dẫn thực hành lập trình</h1>
</p>
<p align="center">
  	<a href="https://img.shields.io/badge/version-v0.1.0-blue">
      <img alt="version" src="https://img.shields.io/badge/version-v0.1.0-blue?color=FF8000?color=009922" />
    </a>
  <a >
       <img alt="Status-building" src="https://img.shields.io/badge/Status-building-blue" />
  	</a>
  <a >
       <img alt="PRs-Welcome" src="https://img.shields.io/badge/PRs-Welcome-red" />
  	</a>
   	<a href="https://github.com/Lordog/dive-into-llms/stargazers">
       <img alt="stars" src="https://img.shields.io/github/stars/Lordog/dive-into-llms" />
  	</a>
  	<a href="https://github.com/Lordog/dive-into-llms/network/members">
       <img alt="FORK" src="https://img.shields.io/github/forks/Lordog/dive-into-llms?color=FF8000" />
  	</a>
    <a href="https://github.com/Lordog/dive-into-llms/issues">
      <img alt="Issues" src="https://img.shields.io/github/issues/Lordog/dive-into-llms?color=0088ff"/>
    </a>
    <br />
</p>


<div align="center">
<p align="center">
  <a href="#项目动机">Động lực của dự án</a>/
  <a href="#教程目录">Mục lục bài hướng dẫn</a>/
  <a href="#贡献者列表">Danh sách người đóng góp</a>
</p>
</div>

## 💡 Updates

2025/06/06  Cảm ơn các bạn đã quan tâm và nhiệt tình góp ý! Chúng tôi đã cập nhật bài hướng dẫn này ở hai mặt sau:

- [x] Ra mắt bài hướng dẫn miễn phí, phi lợi nhuận 《大模型开发全流程》 (The Full Workflow of Large Model Development) trên nền tảng phần cứng/phần mềm nội địa Trung Quốc (gồm PPT, sổ tay thực hành và video); đặc biệt cảm ơn sự hỗ trợ của 华为昇腾社区 (Huawei Ascend Community)!
- [x] Cập nhật nội dung dựa trên loạt bài hướng dẫn thực hành lập trình ban đầu, đồng thời bổ sung các chủ đề mới (suy luận toán học, GUI Agent, alignment (căn chỉnh hành vi mô hình theo ý định, giá trị và yêu cầu an toàn của con người) cho mô hình lớn, steganography (kỹ thuật giấu tin: giấu thông điệp bí mật bên trong một nội dung trông bình thường), v.v.)!

## 🎯 Động lực của dự án

Loạt bài hướng dẫn thực hành lập trình Dive into LLMs được mở rộng từ tài liệu bài giảng của các môn học 《自然语言处理前沿技术》 (Frontier Technologies in Natural Language Processing, NIS8021) và 《人工智能安全技术》 (Artificial Intelligence Security Technology, NIS3353) tại 上海交通大学 (Shanghai Jiao Tong University, SJTU) (giảng viên: [张倬胜 (Zhang Zhuosheng)](https://bcmi.sjtu.edu.cn/home/zhangzs/)), nhằm cung cấp tài liệu tham khảo lập trình nhập môn về mô hình lớn. Bài hướng dẫn này mang tính phi lợi nhuận và hoàn toàn miễn phí. Thông qua các bài thực hành đơn giản, chúng tôi muốn giúp các bạn sinh viên nhanh chóng làm quen với mô hình lớn để thực hiện đồ án môn học hoặc nghiên cứu học thuật tốt hơn.

## 📚 Mục lục bài hướng dẫn

| Nội dung bài hướng dẫn | Giới thiệu | Liên kết |
| ---------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Fine-tuning (tinh chỉnh một mô hình đã huấn luyện trên dữ liệu của một nhiệm vụ cụ thể) và triển khai | Hướng dẫn fine-tuning và triển khai mô hình pre-trained (mô hình đã qua pre-training, tức huấn luyện ban đầu trên kho dữ liệu rất lớn): muốn cải thiện hiệu năng của mô hình pre-trained trên một nhiệm vụ cụ thể? Hãy chọn một mô hình pre-trained phù hợp, fine-tune nó trên nhiệm vụ đó, rồi triển khai mô hình đã fine-tune thành một demo (bản chạy thử minh họa) dễ dùng! | [[Slide bài giảng](https://github.com/Lordog/dive-into-llms/tree/main/documents/chapter1/dive-into-llm.pdf)] [[Bài hướng dẫn](https://github.com/Lordog/dive-into-llms/tree/main/documents/chapter1/README.md)] [[Notebook](https://github.com/Lordog/dive-into-llms/tree/main/documents/chapter1/dive-tuning.ipynb)] |
| Prompting (điều khiển mô hình bằng cách thiết kế prompt thay vì huấn luyện lại) và chain-of-thought (CoT; để mô hình viết ra từng bước suy luận trước khi trả lời) | Hướng dẫn gọi API (giao diện lập trình ứng dụng) và suy luận với mô hình lớn: “AI lên mạng xin một lời động viên? Mô hình lớn trả lời một số câu hỏi khiến người ta ngỡ ngàng, nhưng có thể nó chỉ muốn một lời ‘động viên’”  | [[Slide bài giảng](https://github.com/Lordog/dive-into-llms/tree/main/documents/chapter2/dive-into-prompting.pdf)] [[Bài hướng dẫn](https://github.com/Lordog/dive-into-llms/tree/main/documents/chapter2/README.md)] [[Notebook](https://github.com/Lordog/dive-into-llms/tree/main/documents/chapter2/dive-prompting.ipynb)] |
| Knowledge editing (sửa một mẩu tri thức cụ thể trong mô hình mà không huấn luyện lại toàn bộ) | Phương pháp và công cụ editing cho mô hình ngôn ngữ: muốn điều khiển những gì mô hình ngôn ngữ ghi nhớ về một tri thức cụ thể? Hãy chọn phương pháp editing phù hợp, edit tri thức cụ thể đó, rồi kiểm chứng mô hình sau khi edit! | [[Slide bài giảng](https://github.com/Lordog/dive-into-llms/blob/main/documents/chapter3/dive_edit_0410.pdf)] [[Bài hướng dẫn](https://github.com/Lordog/dive-into-llms/tree/main/documents/chapter3/README.md)]  [[Notebook](https://github.com/Lordog/dive-into-llms/tree/main/documents/chapter3/dive_edit.ipynb)] |
| Suy luận toán học | Làm sao để mô hình lớn học được suy luận toán học? Hãy cùng dùng distillation (dùng đầu ra của mô hình lớn làm teacher để huấn luyện mô hình nhỏ làm student) để nhanh chóng tạo ra một R1 mini! | [[Slide bài giảng](https://github.com/Lordog/dive-into-llms/blob/main/documents/chapter4/math.pdf)] [[Bài hướng dẫn](https://github.com/Lordog/dive-into-llms/tree/main/documents/chapter4/README.md)]  [[Notebook](https://github.com/Lordog/dive-into-llms/tree/main/documents/chapter4/sft_math.ipynb)] |
| Watermark (dấu ẩn được nhúng vào văn bản do mô hình sinh để sau này máy phát hiện được) cho mô hình | Watermark văn bản cho mô hình ngôn ngữ: nhúng watermark mà con người không nhìn thấy vào nội dung do mô hình ngôn ngữ sinh ra | [[Slide bài giảng](https://github.com/Lordog/dive-into-llms/blob/main/documents/chapter5/watermark.pdf)] [[Bài hướng dẫn](https://github.com/Lordog/dive-into-llms/tree/main/documents/chapter5/README.md)]  [[Notebook](https://github.com/Lordog/dive-into-llms/tree/main/documents/chapter5/watermark.ipynb)] |
| Tấn công jailbreak (dùng prompt khéo léo để vượt qua cơ chế an toàn của mô hình) | Muốn an toàn tốt hơn thì trước hết phải học cách tấn công. Hãy cùng tìm hiểu tấn công jailbreak cạy miệng mô hình lớn như thế nào! | [[Slide bài giảng](https://github.com/Lordog/dive-into-llms/blob/main/documents/chapter6/dive-Jailbreak.pdf)] [[Bài hướng dẫn](https://github.com/Lordog/dive-into-llms/tree/main/documents/chapter6/README.md)] [[Notebook](https://github.com/Lordog/dive-into-llms/tree/main/documents/chapter6/dive-jailbreak.ipynb)] |
| Steganography với mô hình lớn | “Mực tàng hình”! Muốn mô hình lớn vừa trả lời trôi chảy, vừa lặng lẽ mang theo thông tin mà chỉ “người nhà” mới nhận ra? Steganography với mô hình lớn sẽ cho bạn biết! | [[Slide bài giảng](https://github.com/Lordog/dive-into-llms/blob/main/documents/chapter7/stega.pdf)] [[Bài hướng dẫn](https://github.com/Lordog/dive-into-llms/tree/main/documents/chapter7/README.md)] [[Notebook](https://github.com/Lordog/dive-into-llms/tree/main/documents/chapter7/llm_stega.ipynb)] |
| Mô hình multimodal (xử lý nhiều modality, tức loại dữ liệu như văn bản, ảnh, âm thanh, video, cùng lúc) | Là loại mô hình mô phỏng thế giới thực đầy đủ hơn, multimodal large language model (MLLM; LLM được gắn thêm khả năng hiểu/sinh ảnh, âm thanh, video) đạt được khả năng hiểu và sinh multimodal mạnh hơn bằng cách nào? MLLM có giúp hiện thực hóa AGI được không? | [[Slide bài giảng](https://github.com/Lordog/dive-into-llms/blob/main/documents/chapter8/mllms.pdf)]  [[Bài hướng dẫn](https://github.com/Lordog/dive-into-llms/tree/main/documents/chapter8/README.md)] [[Notebook](https://github.com/Lordog/dive-into-llms/tree/main/documents/chapter8/mllms.ipynb)] |
| GUI agent (agent thao tác giao diện đồ họa như người dùng: chạm, gõ, vuốt) | Muốn cơm bưng nước rót, rảnh cả hai tay? Vậy hãy cùng để AI Agent (tác tử AI: hệ thống dùng mô hình để tự lập kế hoạch, gọi công cụ và hành động trong môi trường) đặt đồ ăn, trả lời tin nhắn, so giá khi mua sắm thay bạn! | [[Slide bài giảng](https://github.com/Lordog/dive-into-llms/blob/main/documents/chapter9/GUIagent.pdf)]  [[Bài hướng dẫn](https://github.com/Lordog/dive-into-llms/tree/main/documents/chapter9/README.md)] [[Notebook](https://github.com/Lordog/dive-into-llms/tree/main/documents/chapter9/GUIagent.ipynb)] |
| An toàn của agent | LLM agent đã bước vào hành trình hướng tới hệ điều hành của tương lai. Nhưng trong các kịch bản agent mở, mô hình lớn có nhận ra được rủi ro và mối đe dọa không? | [[Slide bài giảng](https://github.com/Lordog/dive-into-llms/blob/main/documents/chapter10/dive-into-safety.pdf)] [[Bài hướng dẫn](https://github.com/Lordog/dive-into-llms/tree/main/documents/chapter10/README.md)] [[Notebook](https://github.com/Lordog/dive-into-llms/tree/main/documents/chapter10/agent.ipynb)] |
| Alignment an toàn bằng RLHF (reinforcement learning from human feedback; học tăng cường từ phản hồi của con người) | Hướng dẫn thí nghiệm RLHF dựa trên PPO: bài hướng dẫn này “cực kỳ nguy hiểm”, đọc xong hãy kiểm tra xem mô hình lớn của bạn có đang cười khẩy không. | [[Slide bài giảng](https://github.com/Lordog/dive-into-llms/blob/main/documents/chapter11/RLHF.pdf)] [[Bài hướng dẫn](https://github.com/Lordog/dive-into-llms/tree/main/documents/chapter11/README.md)] [[Notebook](https://github.com/Lordog/dive-into-llms/tree/main/documents/chapter11/RLHF.ipynb)] |



## 🔥 Mới ra mắt: “The Full Workflow of Large Model Development” trên nền tảng phần cứng/phần mềm nội địa Trung Quốc

- **✨ Bài hướng dẫn miễn phí, phi lợi nhuận “The Full Workflow of Large Model Development” do chúng tôi phối hợp cùng 华为昇腾 (Huawei Ascend) xây dựng đã chính thức ra mắt! Công nghệ tiên tiến + thực hành code, cầm tay chỉ việc giúp bạn làm chủ các mô hình AI lớn ✨**: 

  Dựa trên loạt bài hướng dẫn Dive into LLMs ban đầu, chúng tôi đã phối hợp cùng Huawei xây dựng loạt khóa học “The Full Workflow of Large Model Development”. Loạt bài hướng dẫn này được phát triển trên phần mềm và phần cứng nền tảng của 昇腾 (Ascend), gồm nhiều hình thức như PPT, sổ tay thực hành, video. Bài hướng dẫn chia thành các loạt sơ cấp, trung cấp và cao cấp, phục vụ các nhu cầu thực hành mô hình lớn khác nhau; mục tiêu là đưa công nghệ tiên tiến đến với các nhà nghiên cứu và nhà phát triển thông qua thực hành code, cung cấp một hướng dẫn phát triển toàn quy trình đi từ dễ đến khó: bắt đầu nhanh, ứng dụng các mô hình Ascend đã hỗ trợ, cũng như chuyển đổi và tối ưu các mô hình mới.
  
- **🚀 Vào 昇腾社区 (Ascend Community) để khám phá loạt khóa học “The Full Workflow of Large Model Development”**: 
  
  👉 “[大模型开发学习专区 (Large Model Development Learning Zone)](https://www.hiascend.com/edu/growth/lm-development#classification-floor-1)” @ Ascend Community 👈 
  
- **✨ Giới thiệu nội dung khóa học ✨**

  <!-- <img src="./pics/icon/title.jpg" width="300"/>
  <img src="./pics/icon/cover.png" width="300"/>
  <img src="./pics/icon/team.png" width="300"/>
  <img src="./pics/icon/agent.png" width="300"/> -->

<p align = "center">
  <img src="./pics/icon/title.jpg" width="48%"/>
  <img src="./pics/icon/cover.png" width="48%"/>
  <img src="./pics/icon/team.png" width="48%"/>
  <img src="./pics/icon/agent.png" width="48%"/>
</p>

## 🙏 Tuyên bố miễn trừ trách nhiệm

Toàn bộ nội dung của bài hướng dẫn này chỉ đến từ kinh nghiệm cá nhân của những người đóng góp, dữ liệu trên Internet và những gì tích lũy được trong công việc nghiên cứu khoa học hằng ngày. Mọi mẹo chỉ mang tính tham khảo, không đảm bảo đúng 100%. Nếu có bất kỳ vấn đề nào, rất hoan nghênh bạn gửi Issue hoặc PR. Ngoài ra, các huy hiệu (badge) dùng trong dự án này được lấy từ Internet; nếu chúng vi phạm bản quyền hình ảnh của bạn, vui lòng liên hệ để chúng tôi gỡ bỏ. Xin cảm ơn.

## 🤝 Hoan nghênh đóng góp

Bài hướng dẫn này hiện vẫn là một dự án đang thực hiện, nên khó tránh khỏi thiếu sót; rất hoan nghênh mọi PR và thảo luận qua issue.

## ❤️ Danh sách người đóng góp

Cảm ơn các thầy cô và các bạn sinh viên sau đây đã hỗ trợ và đóng góp cho dự án:

**Nhóm phát triển loạt bài hướng dẫn Dive into LLMs**:

- Shanghai Jiao Tong University: [Zhang Zhuosheng](https://bcmi.sjtu.edu.cn/home/zhangzs/), [袁童鑫 (Yuan Tongxin)](https://github.com/Lordog), [马欣贝 (Ma Xinbei)](https://scholar.google.com/citations?user=LpUi3EgAAAAJ&hl=zh-CN&oi=ao), [何志威 (He Zhiwei)](https://zwhe99.github.io), [杜巍 (Du Wei)](https://scholar.google.com/citations?user=tFYUBLkAAAAJ&hl=en), [赵皓东 (Zhao Haodong)](https://dongdongzhaoup.github.io/), [吴宗儒 (Wu Zongru)](https://zrw00.github.io/), [吴铮 (Wu Zheng)](https://wuzheng02.github.io/), [董凌众 (Dong Lingzhong)](https://github.com/LZ-Dong), [张玉龙 (Zhang Yulong)](https://aslan-yulong.github.io/)

- 新加坡国立大学 (National University of Singapore, NUS): [费豪 (Fei Hao)](http://haofei.vip/)

**Nhóm phát triển loạt bài hướng dẫn “The Full Workflow of Large Model Development”:**

- Shanghai Jiao Tong University: [Zhang Zhuosheng](https://bcmi.sjtu.edu.cn/home/zhangzs/), [刘功申 (Liu Gongshen)](https://infosec.sjtu.edu.cn/DirectoryDetail.aspx?id=75), [陈星宇 (Chen Xingyu)](https://scholar.google.com/citations?user=d-dNtjrMJ5YC&hl=en), [程彭洲 (Cheng Pengzhou)](https://scholar.google.com/citations?user=qxnwzDUAAAAJ&hl=en), [Dong Lingzhong](https://github.com/LZ-Dong), [He Zhiwei](https://zwhe99.github.io), [鞠天杰 (Ju Tianjie)](https://scholar.google.com/citations?user=f8PPcnoAAAAJ&hl=en), [Ma Xinbei](https://scholar.google.com/citations?user=LpUi3EgAAAAJ&hl=zh-CN&oi=ao), [Wu Zheng](https://scholar.google.com/citations?hl=zh-CN&user=qBM1UbUAAAAJ&view_op=list_works&gmla=AIfU4H6PG9JyjRub6BYIIZ4isQE7MBAM3Eoec6OJfX4z_8-pOE8bI1Wgdo3XL5qOZWR3U-h-lIP2q0zXt5gzyFKMSg7MNnBBWLv5d1IVG30UANczTP0), [Wu Zongru](https://zrw00.github.io/), [闫子赫 (Yan Zihe)](https://scholar.google.com/citations?user=O2YfSHoAAAAJ&hl=zh-CN), [姚杳 (Yao Yao)](https://scholar.google.com/citations?user=tLMP3IkAAAAJ), [Yuan Tongxin](https://github.com/Lordog), [Zhao Haodong](https://dongdongzhaoup.github.io/);

- Huawei Ascend Community: ZOMI, 谢乾 (Xie Qian), 程黎明 (Cheng Liming), 楼梨华 (Lou Lihua), 焦泽昱 (Jiao Zeyu)

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Lordog/dive-into-llms&type=Date)](https://star-history.com/#Lordog/dive-into-llms&Date)
