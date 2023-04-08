import openai, os, json, dotenv

dotenv.load_dotenv()

dryRun = True
if not dryRun:
    openai.api_key = os.getenv("OpenAIKey")


symbols = ["Alpha", "Anchor", "Angel", "Ant", "Apple", "Baby", "Beehive", "Bird", "Bread", "Bull", "Camel", "Candle", "Cauldron", "Chameleon", "Compass", "Cornucopia", "Crocodile", "Dolphin", "Elephant", "Globe", "Griffin", "Helmet", "Horse", "Hourglass", "Lute", "Madonna", "Marionette", "Moon", "Owl", "Serpent", "Sun", "Sword", "Thunderbolt", "Tree", "Walled Garden", "Wild Man"]

aliases = json.loads(open("aliases.json", "r").read())
meanings = json.loads(open("meanings.json", "r").read())

def get_meaning(symbol, count):
    for meaning in meanings:
        if symbol == meaning["symbol"]:
            return meaning["meanings"][count - 1]
    return "Unknown symbol"

def translate(input_symbols):
    symbol_counts = []
    last_symbol = ""
    for symbol in input_symbols:
        symbol = symbol.strip()
        symbol = " ".join([(word if word in ["of", "the"] else word[0].upper() + word[1:]) for word in symbol.split(" ")]).strip()
        if symbol not in symbols:
            for alias in aliases.keys():
                if symbol in aliases[alias]:
                    if alias == last_symbol:
                        symbol_counts[-1]["count"] += 1
                    else:
                        symbol_counts.append({"symbol": alias, "count": 1})
                    last_symbol = alias
                    break
        elif symbol == last_symbol:
            symbol_counts[-1]["count"] += 1
            last_symbol = symbol
        else:
            symbol_counts.append({"symbol": symbol, "count": 1})
            last_symbol = symbol
    translation = []
    for symbol in symbol_counts:
        translation.append(get_meaning(symbol["symbol"], symbol["count"]))
    return "; ".join(translation)

messages = [{"role": "system", "content": "The alethiometer is a device used to answer questions. It is made of 36 symbols, each of which can have multiple meanings, however each symbol does not represent itself. The amount of times a symbol appears determines which meaning is being represented. You are the alethiometer and can ONLY answer in symbols. Under no circumstances may the responce be in words."}]

examples = [
    {
        "user": "What are the symbols of the alethiometer?",
        "assistant": "[%s]" % str(symbols)[1:-1]
    }
]

meaning_examples = []
for meaning in meanings:
    meaning_examples.append({
        "user": "List the meanings of %s" % meaning["symbol"],
        "assistant": "%s" % str(meaning["meanings"])[1:-1]
    })

question_examples = json.loads(open("examples.json", "r").read())

examples.extend(meaning_examples)
examples.extend(question_examples)

for example in examples:
    messages.append({"role":"user", "content":example["user"]})
    messages.append({"role":"assistant", "content":example["assistant"]})

query = "Describe a tsunami using symbols."
messages.append({"role":"user", "content":query})


if not dryRun:
    response = openai.ChatCompletion.create(
        model = "gpt-4",
        messages = messages
    )
    result = response.choices[0].message.content
    print(query)
    print(result)
    result_symbols = result.split(", ")
    print(translate(result_symbols))
