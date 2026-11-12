# Text Steganography with LLMs

This project implements text steganography based on large language models (LLMs), using the GPT-2 model to hide information in generated text. It includes two coding methods: Huffman coding and fixed-length coding (FLC).

## Features

- Implements steganography in GPT-2 text generation
- Two coding methods supported:
  - Huffman coding (Huffman Coding)
  - Fixed-length coding (Fixed Length Coding, FLC)
- Generates both stegotext and normal text for comparison

## Requirements

- Python 3.8+
- PyTorch
- Transformers
- CUDA (optional, for GPU acceleration)

## Installation

Install the dependencies:

```bash
pip install torch # If you use a GPU, make sure to install the GPU build of torch
pip install transformers
pip install jupyter
```

## Usage

1. Open the Jupyter notebook:
```bash
jupyter notebook llm_stega.ipynb
```

2. The notebook has three main parts:
   - Huffman coding implementation
   - Fixed-length coding (FLC) implementation
   - Text generation and steganography

3. Generate stegotext:
   - Choose the coding method (Huffman coding or FLC)
   - Set the parameters (the k value for the coding)
   - Run the main function with a custom prompt

Example code:
```python
# Initialize the steganography handler
k = 2
handle = Huffman(k=2**k, bits=bits)
# Or use FLC
# handle = FLC(k=k, bits=bits)

# Generate text with steganography
prompt = "Hello，I'm"
stega_output, normal_output = generate_text_with_steganography(
    model, tokenizer, prompt, handle
)
```

## Output files

The program writes two text files:
- `outputs-gpt2-stega.txt`: the stegotext
- `outputs-gpt2-normal.txt`: the text that would normally have been generated without the steganographic constraint

## Notes

- The GPT-2 model is downloaded automatically on the first run; inside mainland China you can also download the GPT-2 model in advance from the https://hf-mirror.com mirror, or use another large model.
- Make sure you have enough disk space (the model is about 500MB)
- A CUDA-capable GPU is recommended for better performance
- The length of the hidden message affects the length of the generated text

## How it works

1. Embedding process:
   - Convert the secret message into a binary sequence
   - Generate text with the GPT-2 model
   - Embed the message bits into the generated text through the coding method

2. Decoding process:
   - Use the same GPT-2 model and context
   - Extract the hidden message bits from the text through the decoding method
   - Convert the binary sequence back into the original message
