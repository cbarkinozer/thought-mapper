---
date: 2024-08-24T12:25:55
platform: YouTube
topics:
  - Python
  - Artificial Intelligence
  - AI Code Generation
source: https://www.youtube.com/watch?v=Zn7CWiXf6lA
---
# Yalnızca CPU Kullanarak Metin ve Görüntü LLM'leri Nasıl Kullanılır?

Moondream Vision Model: https://github.com/vikhyat/moondream
Ollama llama3.1:8b Modeli: https://ollama.com/library/llama3.1:8b
Ollama phi3 Modeli: https://ollama.com/library/phi3
(Videoda yok ama phi3'ün yeni versiyonu da varmış) phi3.5 Modeli: https://ollama.com/library/phi3.5
Moondb ile yapılan Agentic Yazılım: https://www.youtube.com/watch?v=oDGQrOlmC1s

#üretkenyapayzeka #moondream #ollama #cpullm #smallllm #küçükllm #phi3 #görselllm

Kodlar:

### ollama_seq2seq.py

# pip install langchain_ollama
from langchain_ollama import ChatOllama
import time
# For Turkish: llama3.1:8b, for English: phi3
llm = ChatOllama(model="llama3.1:8b", temperature=0.0)
messages = [
    ("system", "You are a translator that translates from English to Turkish."),
    ("human", "Specifically, LLM quantization is an approach to processing large amounts of language data, which converts a continuous data set to a discrete data set – ultimately minimising the number of bits needed to display the signal."),
]
"""
messages = [
    ("system", "You are an explainer. Explain the given concept to me like I am high schooler."),
    ("human", "Specifically, LLM quantization is an approach to processing large amounts of language data, which converts a continuous data set to a discrete data set – ultimately minimising the number of bits needed to display the signal."),
]
"""
start_time = time.time()
print("Thinking...")
response = llm.invoke(messages)
end_time = time.time()
duration = end_time - start_time
print(f"Duration: {duration}\n")
print(response)



###  moondream_vision.py

# pip install transformers pillow torch einops torchvision
from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image
import time
model_id = "vikhyatk/moondream2"
revision = "2024-07-23"
model = AutoModelForCausalLM.from_pretrained(
    model_id, trust_remote_code=True, revision=revision
)
tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision, cache_dir="/model")
image_list = []
chilling_flooded = Image.open('chilling_flooded.jpg')
image_list.append(chilling_flooded)
flipflop_mass = Image.open('flipflop_mass.jpg')
image_list.append(flipflop_mass)
sausage_cuffed = Image.open('sausage_cuffed.jpg')
image_list.append(sausage_cuffed)
shoey_Driver = Image.open('shoey_Driver.jpg')
image_list.append(shoey_Driver)
for image in image_list:
    enc_image = model.encode_image(image)
    start_time = time.time()
    print("Thinking...")
    response = model.answer_question(enc_image, "Describe this image.", tokenizer)
    end_time = time.time()
    duration = end_time - start_time
    print(f"Duration: {duration}\n")
    print(response)

## Topics
- [[Python]]
- [[Artificial Intelligence]]
- [[AI Code Generation]]

## Tags
#Python #ArtificialIntelligence #AICodeGeneration