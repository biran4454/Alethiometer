import openai, os, json

dryRun = False
if not dryRun:
    openai.api_key = os.getenv("OpenAIKey")


symbols = ["Alpha", "Anchor", "Angel", "Ant", "Apple", "Baby", "Beehive", "Bird", "Bread", "Bull", "Camel", "Candle", "Cauldron", "Chameleon", "Compass", "Cornucopia", "Crocodile", "Dolphin", "Elephant", "Globe", "Griffin", "Helmet", "Horse", "Hourglass", "Lute", "Madonna", "Marionette", "Moon", "Owl", "Serpent", "Sun", "Sword", "Thunderbolt", "Tree", "Walled Garden", "Wild Man"]
aliases = {
    "Alpha": ["Alpha", "Omega"],
    "Anchor": ["Anchor", "Anchors"],
    "Angel": ["Angel", "Angels", "Angle", "Archangel", "Archangels"],
    "Ant": ["Ant", "Ants", "Insect", "Insects", "Bug", "Bugs"],
    "Apple": ["Apple", "Apples", "Apple Tree", "Apple Trees", "Apple-Tree", "Apple-Trees"],
    "Baby": ["Baby", "Babies", "Infant", "Infants", "Child", "Children"],
    "Beehive": ["Beehive", "Beehives", "Bee Hive", "Bee Hives", "Bee-Hive", "Bee-Hives", "Bees", "Bee"],
    "Bird": ["Bird", "Birds", "Birds Nest", "Birds Nests", "Birds-Nest", "Birds-Nests", "Bird Nest", "Bird Nests", "Bird-Nest", "Bird-Nests"],
    "Bread": ["Bread", "Breads", "Loaf", "Loaves"],
    "Bull": ["Bull", "Bulls", "Bovine", "Bovines", "Cow", "Cows", "Ox", "Oxen"],
    "Camel": ["Camel", "Camels", "Dromedary", "Dromedaries"],
    "Candle": ["Candle", "Candles", "Lamp", "Lamps"],
    "Cauldron": ["Cauldron", "Cauldrons", "Kettle", "Kettles", "Pot", "Pots", "Pot of Gold", "Pots of Gold", "Pot-of-Gold", "Pots-of-Gold"],
    "Chameleon": ["Chameleon", "Chameleons", "Chameleon's Tongue", "Chameleons' Tongues", "Chameleon's-Tongue", "Chameleons'-Tongues"],
    "Compass": ["Compass", "Compasses", "Compass Rose", "Compass Roses", "Compass-Rose", "Compass-Roses"],
    "Cornucopia": ["Cornucopia", "Cornucopias", "Horn of Plenty", "Horns of Plenty", "Horn-of-Plenty", "Horns-of-Plenty"],
    "Crocodile": ["Crocodile", "Crocodiles", "Alligator", "Alligators"],
    "Dolphin": ["Dolphin", "Dolphins", "Porpoise", "Porpoises"],
    "Elephant": ["Elephant", "Elephants", "Elephant's Trunk", "Elephants' Trunks", "Elephant's-Trunk", "Elephants'-Trunks"],
    "Globe": ["Globe", "Globes", "Globe of the World", "Globes of the World", "Globe-of-the-World", "Globes-of-the-World", "World", "Worlds"],
    "Griffin": ["Griffin", "Griffins", "Griffon", "Griffons"],
    "Helmet": ["Helmet", "Helmets", "Helm", "Helms"],
    "Horse": ["Horse", "Horses", "Horse's Head", "Horses' Heads", "Horse's-Head", "Horses'-Heads"],
    "Hourglass": ["Hourglass", "Hourglasses", "Sandglass", "Sandglasses"],
    "Lute": ["Lute", "Lutes", "Lyre", "Lyres"],
    "Madonna": ["Madonna", "Madonnas", "Virgin Mary", "Virgin Marys", "Virgin-Mary", "Virgin-Marys", "Madame", "Madames", "Madam", "Madams"],
    "Marionette": ["Marionette", "Marionettes", "Puppet", "Puppets"],
    "Moon": ["Moon", "Moons", "Lunar", "Lunars"],
    "Owl": ["Owl", "Owls", "Owl's Eyes", "Owls' Eyes", "Owl's-Eyes", "Owls'-Eyes"],
    "Serpent": ["Serpent", "Serpents", "Snake", "Snakes", "Serpent's Tail", "Serpents' Tails", "Serpent's-Tail", "Serpents'-Tails"],
    "Sun": ["Sun", "Suns", "Solar", "Solars"],
    "Sword": ["Sword", "Swords", "Sword of Justice", "Swords of Justice", "Sword-of-Justice", "Swords-of-Justice"],
    "Thunderbolt": ["Thunderbolt", "Thunderbolts", "Lightning", "Lightnings"],
    "Tree": ["Tree", "Trees", "Tree of Life", "Trees of Life", "Tree-of-Life", "Trees-of-Life"],
    "Walled Garden": ["Walled Garden", "Walled Gardens", "Walled Garden of Eden", "Walled Gardens of Eden", "Walled-Garden-of-Eden", "Walled-Gardens-of-Eden", "Eden", "Edens"],
    "Wild Man": ["Wild", "Man"]
}

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

question_examples = [
    {
        "user": "What symbol represents the word 'Evil'?",
        "assistant": "Serpent"
    },
    {
        "user": "What does the combination 'Owl' mean?",
        "assistant": "Night"
    },
    {
        "user": "What does the combination 'Owl, Owl' mean?",
        "assistant": "Winter"
    },
    {
        "user": "What symbols represent the phrase 'Fear of Fate'?",
        "assistant": "Owl, Owl, Owl, Thunderbolt, Thunderbolt"
    },
    {
        "user": "What symbols represent the question 'What is the fate of nature'?",
        "assistant": "Thunderbolt, Thunderbolt, Walled Garden"
    },
    {
        "user": "Summarise climate change.",
        "assistant": "Bull, Bread, Bread, Bread, Candle, Cornucopia"
    },
    {
        "user": "Does the combination 'Bull, Bread, Bread, Bread, Candle, Cornucopia' mean 'The earth is sacrificed in fire in return for wealth'?",
        "assistant": "Marionette, Marionette, Marionette, Marionette, Marionette, Marionette"
    },
    {
        "user": "Describe a plane using symbols.",
        "assistant": "Horse, Horse, Chameleon"
    },
    {
        "user": "Does the combination 'Horse, Horse, Chameleon' mean a journey through the air?",
        "assistant": "Marionette, Marionette, Marionette, Marionette, Marionette, Marionette"
    }
]

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
