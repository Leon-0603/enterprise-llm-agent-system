# lora_inference_new.py

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

BASE_MODEL_PATH = r"..."
LORA_PATH = r"..."

def load_model():
    print("Detecting device...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_PATH)

    print("Loading base model...")
    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL_PATH,
        torch_dtype=torch.float16 if device == "cuda" else torch.float32,
        device_map="auto"
    )

    print("Applying LoRA weights...")
    model = PeftModel.from_pretrained(model, LORA_PATH)
    model = model.merge_and_unload()  

    model.eval()
    return tokenizer, model, device


def lora_inference(prompt):
    tokenizer, model, device = load_model()

    print("Tokenizing...")
    inputs = tokenizer(prompt, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}  

    print("Generating...")
    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=256,
            temperature=0.7,
            do_sample=True,
            top_p=0.9,
        )

    result = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return result


# MCP Tool Entry
def run_lora(prompt: str) -> dict:
    """
    MCP tool will call this function
    must return JSON-like dict
    """
    output = lora_inference(prompt)
    return {"answer": output}
    

# ------- Local test -------
if __name__ == "__main__":
    prompt = input("Prompt: ")
    print("\n--- Output ---\n")
    print(lora_inference(prompt))