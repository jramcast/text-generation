from sanic import Sanic
from sanic.response import json
from transformers import pipeline, set_seed, GPT2Tokenizer


set_seed(42)
tokenizer = GPT2Tokenizer.from_pretrained('.output/')
generator = pipeline('text-generation', model='.output/')


app = Sanic("RH Curriculum writing assistant")


@app.route("/")
async def test(request):
    text = request.args.get("text", "")
    num_predicted_tokens = int(request.args.get("length", 2))
    no_topp = request.args.get("no_top", False)

    num_tokens = tokenizer(text, return_length=True)["length"]
    max_length = num_tokens + num_predicted_tokens

    print("Text:", text)

    kargs = {
        "do_sample": True,
        "top_k": max_length,
        "top_p": 0.9
    }
    if no_topp:
        kargs = {}

    # For info about the args: https://huggingface.co/blog/how-to-generate
    predictions = generator(
        text,
        max_length=max_length,
        num_return_sequences=5,
        **kargs
    )

    return json([p["generated_text"] for p in predictions])

if __name__ == '__main__':
    app.run()