from transformers import pipeline

# Available models:
# Pegasus: google/pegasus-large
# mT5: sebuetnlp/mT5_multilingual_XLSum
# BART: sshleifer/distilbart-cnn-12-6
summarizer = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6",
    max_length=1024,
    truncation=True,
)


def get_summary(text: str) -> str:
    summarized = summarizer(
        text,
    )
    return summarized[0]["summary_text"] if summarized else ""


if __name__ == "__main__":
    text = """Over the past few years as smartphone penetration boomed, products matured, product design and user experience matured, people's expectations have increased.
No longer does a quickly thrown together prototype cut it. People expect a minimum level of good UX and ease-of-use, else they'll leave your app before even giving it a proper try.
In fact, in 2022 great UX might be one strong reason people pick your product over incumbents. That's what happened with Transistor.fm, who made podcast hosting simple and easy.
People expect good aesthetics that make a first impression, simply because that's what they have become used to from the plethora of beautiful and well-designed apps out there in the world.
People expect products to be fully functional as advertised. Buggy products are not acceptable, and in fact people might quickly take to Twitter or social media to let others know that a product is unreliable.
The MVP mindset intensely focuses on building the bare minimum, and that often leaves users frustrated and drives them to seek alternative solutions. Stiffer competition means that people WILL compare your product to alternatives in the market, it's inevitable. And unless you provide something unique and valuable that nobody else does, people are likely to leave.
All these reasons and more make MVP a dated concept, especially in the context of SaaS products. But above all, I think the MVP mindset makes product builders think too heavily about the "minimum" and often so at the cost of "viable".
That's a common pitfall and to avoid that, I propose the MLP framework."""
    summary = get_summary(text)
    assert isinstance(summary, str)
    assert len(summary) > 0
    assert summary not in text
