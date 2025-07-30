import os
import re
import torch
import threading
import time
from transformers import AutoTokenizer, AutoModelForCausalLM

# ===== CONFIGURATION =====
BASE_MODEL = "Qwen/Qwen2.5-Coder-0.5B-Instruct"

# Disable Hugging Face progress bar
os.environ["TRANSFORMERS_NO_PROGRESS_BAR"] = "1"

# Load tokenizer and base model
print("⏳ Loading model and tokenizer from Hugging Face...", end="", flush=True)
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    trust_remote_code=True,
    device_map="auto",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
)

model.eval()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
print("\r✅ Model and tokenizer loaded successfully.        ")

# Spinner animation
class Spinner:
    def __init__(self, message="⏳ Generating code"):
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._spin)
        self.message = message

    def _spin(self):
        symbols = ['|', '/', '-', '\\']
        i = 0
        while not self._stop_event.is_set():
            print(f"\r{self.message}... {symbols[i % len(symbols)]}", end="", flush=True)
            i += 1
            time.sleep(0.1)

    def start(self):
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        self._thread.join()
        print("\r✅ Code generated successfully.           ")

# Strict Python code prompt
PROMPT = (
    "You are a Python code generation assistant.\n"
    "Respond ONLY with valid Python code for the task below.\n"
    "Do not include any print statements, comments, markdown, explanations, or docstrings.\n"
    "Return only the exact line(s) of code that directly solve the task.\n"
    "Be strict. If the task asks for an expression, do not wrap it in a function.\n\n"
    "Task: {}"
)

def extract_code(output: str) -> str:
    # Remove triple-quoted docstrings
    output = re.sub(r'(""".*?"""|\'\'\'.*?\'\'\')', '', output, flags=re.DOTALL)
    match = re.search(r"(def\s+[^\n]+\n(?:\s+.+\n?)*)", output)
    if match:
        return match.group(0).strip()
    return output.strip()

def generate(task: str, max_tokens: int = 64, temperature: float = 0.0) -> str:
    prompt = PROMPT.format(task.strip())
    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    spinner = Spinner()
    spinner.start()

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=temperature,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
        )

    spinner.stop()

    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return extract_code(result)
