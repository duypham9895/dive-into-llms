# Dive into LLMs: Steganography

[Original deck](https://github.com/Lordog/dive-into-llms/blob/f84c04268794ef94f8949808bbc14ab8636763a0/documents/chapter7/stega.pdf)

## Slide 1

**动手学大模型 (Dive into LLMs): Steganography**

张玉龙 (Zhang Yulong)

## Slide 2

**Applications of Large Models in Secure Communication**

Steganography is an information-hiding technique whose core purpose is to embed information in various covers (such as digital images, audio, video or text) to achieve covert communication. Steganography differs from encryption: it hides not only the content of the information but also the very existence of the act of transmitting it. The technique exploits the fact that the human perceptual system is insensitive to certain information, hiding the secret message in the redundant information of a digital cover, so that on the surface it looks no different from an ordinary cover and is therefore hard for an attacker to notice.

Applications of steganography include, but are not limited to, covert transmission and copyright protection. As the technology develops, steganography is becoming increasingly important in military, commercial and other fields, while also making malicious activities easier, such as espionage and terrorist attacks.

## Slide 3

**Why Steganography Matters**

Simply put, steganography is a method of secure information transmission that differs from cryptography.

Cryptography "encrypts" the plaintext so that an intermediary cannot obtain the content of the message, but the carrier of the message may still be discovered and seized by the intermediary, who can then tamper with or intercept its delivery.

Steganography instead "hides" the fact that a message is being sent: it hides the message content on a public channel, disguised as ordinary content, with the goal that only the recipient can find the hidden message and the intermediary does not discover it.

Simple real-life examples of steganography: acrostic poems, small notes tucked inside a book, and so on.

A downstream technique derived from steganography: watermarking (can be understood as a kind of steganography that puts more weight on robustness and is willing to be found and decoded by many people).

## Slide 4

**Examples of Steganography Compared with Cryptography**

Steganography (text format):

- Operation: adjust the letter spacing in an electronic document (e.g. a 0.1pt difference) or the font color (#000000 vs #010101), encoding the information in binary (e.g. "wide spacing = 1, normal = 0")<sup>1</sup>.
- Goal: the information is hidden in public text, invisible to the naked eye.

Cryptography (Vigenère cipher):

- Operation: encrypt with a repeated keyword (e.g. key "KEY" encrypts "HELLO" → "RIJVS").
- Goal: produce unreadable ciphertext that needs the key to decrypt<sup>7</sup>.
- Comparison:
  - Steganography: the cover is a normal file (e.g. a contract) and raises no suspicion.
  - Cryptography: the ciphertext itself reveals that "there is a secret", but the content stays confidential.

## Slide 5

**Examples of Steganography**

Steganography (image LSB):

- Operation: modify the least significant bit (LSB) of image pixels to embed secret data (e.g. the binary of another image). The human eye cannot perceive the difference, but tools can extract it<sup>29</sup>.
- Goal: the information is hidden in an ordinary photo (e.g. a travel photo), bypassing censorship.

Cryptography (AES-256):

- Operation: encrypt a file into gibberish with a key (e.g. z.exe→G8x!gF2\*...
- Goal: even if the file is intercepted, its content cannot be cracked.

Combined use case:

- First encrypt the sensitive data with AES;
- Then embed the ciphertext in the image's LSBs.

  → Double protection: hides both the existence (looks like an ordinary image) and the content (needs the key to decrypt)

## Slide 6

**Examples of Steganography**

Steganography in QR codes:

Principle: design a QR code that looks completely normal (pointing to a harmless website), but embed extra hidden information (another URL, text, a small image) in its error-correction area or through a carefully designed module pattern. Ordinary scanning apps can read only the surface information; custom software is needed to read the hidden layer.

Example: a QR code on a restaurant menu shows dish descriptions when scanned (the public layer), but scanning it with a specific app retrieves the hidden coupon code of the day or internal staff information. A QR code on a poster: a normal scan gives the event description, and the hidden layer is a VIP invitation.

Real-life scenarios: marketing campaigns (treasure hunts, unlocking discounts), internal information delivery (staff announcements), copyright protection (embedding owner information in a public QR code).

Key points: you need to understand the structure of QR codes (especially the redundancy of the error-correction code) and need a special tool that generates two-layer QR codes.

## Slide 7

**Models of Steganography**

Among digital media covers, steganography today generally chooses images or video, because they have plenty of redundant space for inserting information. Text as a cover has low redundancy, but it is flexible and high in content volume, and can be embedded fairly easily in other content. This time we use large language models (LLMs) to introduce large-model steganography.

The process models of steganography (left) and watermarking (right) are shown in the figure below.

## Slide 8

**Categories of Text Steganography**

Text steganography falls into two main categories: modification-based and generative.

In recent years, with the development of deep learning and especially of large models, generative text steganography has become the mainstream.

## Slide 9

**Text Steganography with Large Models<sup>1-3</sup>**

The data of text generation models is all "sequential" data.

Given the preceding context and the parameters, the model returns a table of logits predicting the "next token", listing token ids from highest to lowest probability.

Normally, the model randomly picks one of n tokens as the next token according to the parameters, then continues the generation loop.

Generative steganography, by contrast, intervenes in the model's choice of the next token during inference according to preset rules, thereby embedding the information to be hidden into the generated text during inference.

[1] Yang, Zhong-Liang, et al. "RNN-stega: Linguistic steganography based on recurrent neural networks." IEEE Transactions on Information Forensics and Security 14.5 (2018): 1280-1295.

[2] Tang, Yifan, et al. "Linguistic Steganalysis via LLMs: Two Modes for Efficient Detection of Strongly Concealed Stego." IEEE Signal Processing Letters (2024).

[3] Yang, Zhong-Liang, et al. "VAE-Stega: linguistic steganography based on variational auto-encoder." IEEE Transactions on Information Forensics and Security 16 (2020): 880-895.

## Slide 10

**Text Steganography with Large Models**

Take the figure below as an example. Suppose I want to embed a secret message that has been converted to binary: I can encode the top n candidates the model returns for the next token at each step. For example, after I input "I", the top 8 tokens the model returns, ordered by probability, are have(000), am(001), was(010), can(011)…. Each token corresponds to a 3-bit binary value; when I want to embed "001", I choose "am" as the next token, and the loop continues.

## Slide 11

**Text Steganography with Large Models**

In essence, the method here encodes the top n token candidates to build an implicit steganographic space. When I want to decode the information, using the same model, preceding context and parameters guarantees that the model returns exactly the same coding space as during generation each time, so the original binary bitstream can be recovered backwards from the tokens, e.g. decoding "am" back to 001.

## Slide 12

**Text Steganography with Large Models**

Of course, the method above uses a very fixed coding scheme (directly encoding the top n tokens in order); the figure below actually uses Huffman coding, which ensures as much information as possible is embedded and raises the embedding rate.

## Slide 13

**The Significance and Future of Large-Model Steganography**

Large-model steganography: the advantage of using large models for steganography is that it can exploit their capabilities to output stego content that is more natural and harder to detect.

Coding space: different steganography methods depend heavily on the coding scheme; a new way of constructing the coding space can create a new form of steganography.

Cross-domain extension: the essence of large-model generative text steganography is "iterative coding of sequential data", and the technique can also be transferred to other media. For example, DNA is also sequential data: instruments combined with large-model output can be used to hide information in DNA coding, which in the military could achieve "hiding information in a bottle of water, a few cells or a few hairs", a very high level of covert information transmission.

Large-model watermarking: existing large-model watermarking techniques can also be combined with steganography, each advancing the other. For example, the well-known KGW watermark also constrains the choice of the next token during inference.

Content safety: steganalysis, the countermeasure to steganography, can be used to assess, filter and detect content on online media. "Snide sarcasm" and "cyberbullying and abuse" that trigger no keywords are in essence also a form of "steganography", so they too may be detected automatically by artificial intelligence (AI) using steganography detection methods, which will help maintain the security of humanity's cyberspace in the future.
