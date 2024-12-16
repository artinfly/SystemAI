import spacy

nlp = spacy.load("ru_core_news_sm")

def filter_irrelevant_text(text, keywords):
    doc = nlp(text)
    filtered_sentences = []
    for sent in doc.sents:
        if any(keyword in sent.text.lower() for keyword in keywords):
            filtered_sentences.append(sent.text)
    return filtered_sentences

def extract_entities_and_intents(doc):
    entities = []
    intents = []
    materials = ["кирпич", "цемент", "песок", "известь"]
    for token in doc:
        if token.text.lower() in materials:
            entities.append((token.text, "МАТЕРИАЛ"))
        if token.lemma_ in ["доставлять", "строить", "замешивать"]:
            intents.append((token.text, "НАМЕРЕНИЕ"))
    return entities, intents

def extract_causal_relations(text):
    doc = nlp(text)
    causal_relations = []
    causal_keywords = ["если", "то", "так как", "потому что"]
    for sent in doc.sents:
        if any(keyword in sent.text.lower() for keyword in causal_keywords):
            causal_relations.append(sent.text)
    return causal_relations

def check_contradictions(data_1, data_2):
    contradictions = []
    for key in data_1.keys():
        if key in data_2 and data_1[key] != data_2[key]:
            contradictions.append(f"Противоречие в данных по {key}: {data_1[key]} != {data_2[key]}")
    return contradictions

text = """
Строительство кирпичного дома требует таких материалов, как цемент, песок, кирпич и известь. 
Если на объекте работает больше бригад, то срок строительства уменьшается. 
Поставка материалов на первый объект возможна не чаще одного раза в неделю.
"""

keywords = ["материалы", "бригады", "поставка", "срок"]
filtered_text = filter_irrelevant_text(text, keywords)
print("Отфильтрованный текст:")
for sent in filtered_text:
    print(f"- {sent}")

doc = nlp(" ".join(filtered_text))
entities, intents = extract_entities_and_intents(doc)
print("\nСущности:")
for entity in entities:
    print(f"- {entity[0]} ({entity[1]})")
print("\nНамерения:")
for intent in intents:
    print(f"- {intent[0]} ({intent[1]})")

causal_relations = extract_causal_relations(" ".join(filtered_text))
print("\nПричинно-следственные связи:")
for relation in causal_relations:
    print(f"- {relation}")

data_project_1 = {"бригады": 2, "грузовики": 3, "срок": 34}
data_project_2 = {"бригады": 3, "грузовики": 3, "срок": 30}
contradictions = check_contradictions(data_project_1, data_project_2)
print("\nПротиворечия в данных:")
for contradiction in contradictions:
    print(f"- {contradiction}")
