from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Available models:
# Pegasus: google/pegasus-large
# mT5: sebuetnlp/mT5_multilingual_XLSum
# BART: sshleifer/distilbart-cnn-12-6
tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")

model = AutoModelForSeq2SeqLM.from_pretrained("sshleifer/distilbart-cnn-12-6")


def summarize(text: str) -> str:
    inputs = tokenizer(text, max_length=1024, truncation=True, return_tensors="pt")

    summary_ids = model.generate(inputs["input_ids"])
    summary = tokenizer.batch_decode(
        summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False
    )
    return summary[0]
