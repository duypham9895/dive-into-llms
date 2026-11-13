[Tiếng Việt](README.md) · **English** · [中文 (original)](/README.md)

📖 Read the translation on the web: [https://duypham9895.github.io/dive-into-llms/en/](https://duypham9895.github.io/dive-into-llms/en/)

Unofficial Vietnamese/English translation of 《动手学大模型》 Dive into LLMs ([github.com/Lordog/dive-into-llms @ f84c042](https://github.com/Lordog/dive-into-llms/tree/f84c04268794ef94f8949808bbc14ab8636763a0)). Original work by Zhang Zhuosheng (张倬胜), Yuan Tongxin (袁童鑫) et al. (SJTU, NUS), with support from the Huawei Ascend community. Translated with AI and checked automatically; not fully reviewed by a human. Not affiliated with or endorsed by the authors. Copyright remains with the original authors. Removal requests: [https://github.com/duypham9895/dive-into-llms/issues](https://github.com/duypham9895/dive-into-llms/issues)

The star/fork/issue badges, the "PRs Welcome" badge, the Star History chart, and the "Contributing" section below all belong to the original repository (Lordog/dive-into-llms), not to this fork -- they invite contributions to the original project, not to this translation. Translation errors: open an issue at [https://github.com/duypham9895/dive-into-llms/issues](https://github.com/duypham9895/dive-into-llms/issues).

---

<p align="center">
<h1 align="center">《动手学大模型》 (Dive into LLMs): A Hands-on Programming Tutorial Series</h1>
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
  <a href="#-motivation">Motivation</a>/
  <a href="#-contents">Contents</a>/
  <a href="#️-contributors">Contributors</a>
</p>
</div>

## 💡 Updates

2025/06/06  Thank you all for your interest and enthusiastic feedback! We have updated this tutorial in two ways:

- [x] Launched the free, non-profit tutorial 《大模型开发全流程》 (The Full Workflow of Large Model Development), built on China-made (domestic) hardware and software (with PPT slides, a lab manual and videos). Special thanks to the 华为昇腾社区 (Huawei Ascend Community) for its support!
- [x] Updated the content of the original programming practice tutorial series and added new topics (mathematical reasoning, GUI Agent, large model alignment, steganography, etc.)!

## 🎯 Motivation

The Dive into LLMs programming practice tutorial series grew out of the lecture notes of the 上海交通大学 (Shanghai Jiao Tong University, SJTU) courses 《自然语言处理前沿技术》 (Frontier Technologies in Natural Language Processing, NIS8021) and 《人工智能安全技术》 (Artificial Intelligence Security Technology, NIS3353) (instructor: [张倬胜 (Zhang Zhuosheng)](https://bcmi.sjtu.edu.cn/home/zhangzs/)). It aims to provide an introductory programming reference for large models. This tutorial is non-profit and completely free. Through simple hands-on practice, it helps students get started with large models quickly and carry out course projects or academic research more effectively.

## 📚 Contents

| Tutorial | Overview | Links |
| ---------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Fine-Tuning and Deployment | A guide to fine-tuning and deploying pre-trained models: want to improve a pre-trained model's performance on a specific task? Let's pick a suitable pre-trained model, fine-tune it on that task, and deploy the fine-tuned model as an easy-to-use demo! | [[Slides](https://github.com/Lordog/dive-into-llms/blob/f84c04268794ef94f8949808bbc14ab8636763a0/documents/chapter1/dive-into-llm.pdf)] [[Tutorial](https://duypham9895.github.io/dive-into-llms/en/chapter1/)] [[Notebook](https://github.com/Lordog/dive-into-llms/blob/f84c04268794ef94f8949808bbc14ab8636763a0/documents/chapter1/dive-tuning.ipynb)] |
| Prompting and Chain-of-Thought | A guide to large model API calls and reasoning: “AI asking for encouragement online? Large models give some jaw-dropping answers to certain questions, but maybe all they want is a word of ‘encouragement’”  | [[Slides](https://github.com/Lordog/dive-into-llms/blob/f84c04268794ef94f8949808bbc14ab8636763a0/documents/chapter2/dive-into-prompting.pdf)] [[Tutorial](https://duypham9895.github.io/dive-into-llms/en/chapter2/)] [[Notebook](https://github.com/Lordog/dive-into-llms/blob/f84c04268794ef94f8949808bbc14ab8636763a0/documents/chapter2/dive-prompting.ipynb)] |
| Knowledge Editing | Editing methods and tools for language models: want to control what a language model remembers about specific knowledge? Let's pick a suitable editing method, edit that specific knowledge, and then verify the edited model! | [[Slides](https://github.com/Lordog/dive-into-llms/blob/f84c04268794ef94f8949808bbc14ab8636763a0/documents/chapter3/dive_edit_0410.pdf)] [[Tutorial](https://duypham9895.github.io/dive-into-llms/en/chapter3/)]  [[Notebook](https://github.com/Lordog/dive-into-llms/blob/f84c04268794ef94f8949808bbc14ab8636763a0/documents/chapter3/dive_edit.ipynb)] |
| Mathematical Reasoning | How can a large model learn mathematical reasoning? Let's quickly build a mini R1 through distillation! | [[Slides](https://github.com/Lordog/dive-into-llms/blob/f84c04268794ef94f8949808bbc14ab8636763a0/documents/chapter4/math.pdf)] [[Tutorial](https://duypham9895.github.io/dive-into-llms/en/chapter4/)]  [[Notebook](https://duypham9895.github.io/dive-into-llms/en/chapter4/sft_math/)] |
| Model Watermarking | Text watermarks for language models: embedding watermarks that humans cannot see into content generated by language models | [[Slides](https://github.com/Lordog/dive-into-llms/blob/f84c04268794ef94f8949808bbc14ab8636763a0/documents/chapter5/watermark.pdf)] [[Tutorial](https://duypham9895.github.io/dive-into-llms/en/chapter5/)]  [[Notebook](https://github.com/Lordog/dive-into-llms/blob/f84c04268794ef94f8949808bbc14ab8636763a0/documents/chapter5/watermark.ipynb)] |
| Jailbreak Attacks | Better safety starts with learning how to attack. Let's see how jailbreak attacks pry open a large model's mouth! | [[Slides](https://github.com/Lordog/dive-into-llms/blob/f84c04268794ef94f8949808bbc14ab8636763a0/documents/chapter6/dive-Jailbreak.pdf)] [[Tutorial](https://duypham9895.github.io/dive-into-llms/en/chapter6/)] [[Notebook](https://github.com/Lordog/dive-into-llms/blob/f84c04268794ef94f8949808bbc14ab8636763a0/documents/chapter6/dive-jailbreak.ipynb)] |
| LLM-Based Steganography | “Invisible ink”! Want a large model to answer fluently while quietly carrying information that only “insiders” can recognize? LLM-based steganography shows you how! | [[Slides](https://github.com/Lordog/dive-into-llms/blob/f84c04268794ef94f8949808bbc14ab8636763a0/documents/chapter7/stega.pdf)] [[Tutorial](https://duypham9895.github.io/dive-into-llms/en/chapter7/)] [[Notebook](https://github.com/Lordog/dive-into-llms/blob/f84c04268794ef94f8949808bbc14ab8636763a0/documents/chapter7/llm_stega.ipynb)] |
| Multimodal Models | As models that can more fully simulate the real world, how do multimodal large language models (MLLMs) achieve stronger multimodal understanding and generation? Can MLLMs help achieve AGI? | [[Slides](https://github.com/Lordog/dive-into-llms/blob/f84c04268794ef94f8949808bbc14ab8636763a0/documents/chapter8/mllms.pdf)]  [[Tutorial](https://duypham9895.github.io/dive-into-llms/en/chapter8/)] [[Notebook](https://github.com/Lordog/dive-into-llms/blob/f84c04268794ef94f8949808bbc14ab8636763a0/documents/chapter8/mllms.ipynb)] |
| GUI Agents | Want everything handed to you, hands-free? Then let's have an AI Agent order takeout, reply to messages, and compare prices while shopping for you! | [[Slides](https://github.com/Lordog/dive-into-llms/blob/f84c04268794ef94f8949808bbc14ab8636763a0/documents/chapter9/GUIagent.pdf)]  [[Tutorial](https://duypham9895.github.io/dive-into-llms/en/chapter9/)] [[Notebook](https://duypham9895.github.io/dive-into-llms/en/chapter9/GUIagent/)] |
| Agent Safety | LLM agents have set out on a journey toward the operating systems of the future. But can large models recognize risks and threats in open agent scenarios? | [[Slides](https://github.com/Lordog/dive-into-llms/blob/f84c04268794ef94f8949808bbc14ab8636763a0/documents/chapter10/dive-into-safety.pdf)] [[Tutorial](https://duypham9895.github.io/dive-into-llms/en/chapter10/)] [[Notebook](https://github.com/Lordog/dive-into-llms/blob/f84c04268794ef94f8949808bbc14ab8636763a0/documents/chapter10/agent.ipynb)] |
| RLHF Safety Alignment | A PPO-based RLHF lab guide: this tutorial is “extremely dangerous”; after reading it, check whether your large model is sneering. | [[Slides](https://github.com/Lordog/dive-into-llms/blob/f84c04268794ef94f8949808bbc14ab8636763a0/documents/chapter11/RLHF.pdf)] [[Tutorial](https://duypham9895.github.io/dive-into-llms/en/chapter11/)] [[Notebook](https://duypham9895.github.io/dive-into-llms/en/chapter11/RLHF/)] |



## 🔥 New: “The Full Workflow of Large Model Development”, Built on China-Made Hardware and Software

- **✨ The free, non-profit tutorial “The Full Workflow of Large Model Development”, which we created together with 华为昇腾 (Huawei Ascend), is now live! Cutting-edge technology + code practice, guiding you step by step to master large AI models ✨**: 

  Building on the original Dive into LLMs tutorial series, we partnered with Huawei to develop the course series “The Full Workflow of Large Model Development”. This tutorial series is developed on the foundational software and hardware of 昇腾 (Ascend) and comes in several formats, including PPT slides, lab manuals and videos. It is divided into beginner, intermediate and advanced series for different large model practice needs. Through hands-on code, it aims to bring cutting-edge technology to researchers and developers as a full-workflow development guide that goes from basic to advanced: getting started quickly, applying models Ascend already supports, and migrating and tuning new models.
  
- **🚀 Explore the course series “The Full Workflow of Large Model Development” on the 昇腾社区 (Ascend Community)**: 
  
  👉 “[大模型开发学习专区 (Large Model Development Learning Zone)](https://www.hiascend.com/edu/growth/lm-development#classification-floor-1)” @ Ascend Community 👈 
  
- **✨ Course Content Preview ✨**

  

Course images: see the [original README](https://github.com/Lordog/dive-into-llms/blob/f84c04268794ef94f8949808bbc14ab8636763a0/README.md).

## 🙏 Disclaimer

All content in this tutorial comes solely from the contributors' personal experience, internet data, and what they have accumulated in their day-to-day research. All tips are for reference only and are not guaranteed to be 100% correct. If you have any questions, feel free to submit an Issue or PR. In addition, the badges used in this project come from the internet; if they infringe your image copyright, please contact us and we will remove them. Thank you.

## 🤝 Contributing

This tutorial is a work in progress, so omissions are inevitable. Any PRs and issue discussions are welcome.

## ❤️ Contributors

Thanks to the following teachers and students for their support of and contributions to this project:

**Dive into LLMs tutorial series development team**:

- Shanghai Jiao Tong University: [Zhang Zhuosheng](https://bcmi.sjtu.edu.cn/home/zhangzs/), [袁童鑫 (Yuan Tongxin)](https://github.com/Lordog), [马欣贝 (Ma Xinbei)](https://scholar.google.com/citations?user=LpUi3EgAAAAJ&hl=zh-CN&oi=ao), [何志威 (He Zhiwei)](https://zwhe99.github.io), [杜巍 (Du Wei)](https://scholar.google.com/citations?user=tFYUBLkAAAAJ&hl=en), [赵皓东 (Zhao Haodong)](https://dongdongzhaoup.github.io/), [吴宗儒 (Wu Zongru)](https://zrw00.github.io/), [吴铮 (Wu Zheng)](https://wuzheng02.github.io/), [董凌众 (Dong Lingzhong)](https://github.com/LZ-Dong), [张玉龙 (Zhang Yulong)](https://aslan-yulong.github.io/)

- 新加坡国立大学 (National University of Singapore, NUS): [费豪 (Fei Hao)](http://haofei.vip/)

**“The Full Workflow of Large Model Development” tutorial series development team:**

- Shanghai Jiao Tong University: [Zhang Zhuosheng](https://bcmi.sjtu.edu.cn/home/zhangzs/), [刘功申 (Liu Gongshen)](https://infosec.sjtu.edu.cn/DirectoryDetail.aspx?id=75), [陈星宇 (Chen Xingyu)](https://scholar.google.com/citations?user=d-dNtjrMJ5YC&hl=en), [程彭洲 (Cheng Pengzhou)](https://scholar.google.com/citations?user=qxnwzDUAAAAJ&hl=en), [Dong Lingzhong](https://github.com/LZ-Dong), [He Zhiwei](https://zwhe99.github.io), [鞠天杰 (Ju Tianjie)](https://scholar.google.com/citations?user=f8PPcnoAAAAJ&hl=en), [Ma Xinbei](https://scholar.google.com/citations?user=LpUi3EgAAAAJ&hl=zh-CN&oi=ao), [Wu Zheng](https://scholar.google.com/citations?hl=zh-CN&user=qBM1UbUAAAAJ&view_op=list_works&gmla=AIfU4H6PG9JyjRub6BYIIZ4isQE7MBAM3Eoec6OJfX4z_8-pOE8bI1Wgdo3XL5qOZWR3U-h-lIP2q0zXt5gzyFKMSg7MNnBBWLv5d1IVG30UANczTP0), [Wu Zongru](https://zrw00.github.io/), [闫子赫 (Yan Zihe)](https://scholar.google.com/citations?user=O2YfSHoAAAAJ&hl=zh-CN), [姚杳 (Yao Yao)](https://scholar.google.com/citations?user=tLMP3IkAAAAJ), [Yuan Tongxin](https://github.com/Lordog), [Zhao Haodong](https://dongdongzhaoup.github.io/);

- Huawei Ascend Community: ZOMI, 谢乾 (Xie Qian), 程黎明 (Cheng Liming), 楼梨华 (Lou Lihua), 焦泽昱 (Jiao Zeyu)

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Lordog/dive-into-llms&type=Date)](https://star-history.com/#Lordog/dive-into-llms&Date)
