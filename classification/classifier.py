import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer


class Classifier:
    def __init__(self, model_name, num_labels, device):
        self.device = device
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name, num_labels=num_labels
        )
        self.model.load_state_dict(torch.load("dict.pt", map_location=device))
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        self.model.to(self.device)

    def predict(self, sentence):
        self.model.eval()
        tokenized_sent = self.tokenizer(
            sentence,
            return_tensors="pt",
            truncation=True,
            add_special_tokens=True,
            max_length=512,
        )
        tokenized_sent.to(self.device)

        with torch.no_grad():
            outputs = self.model(
                input_ids=tokenized_sent["input_ids"],
                attention_mask=tokenized_sent["attention_mask"],
                token_type_ids=tokenized_sent["token_type_ids"],
            )

        logits = outputs[0]
        logits = logits.detach().cpu()
        result = logits.argmax(-1)

        if result == 0:
            return True
        elif result == 1:
            return False
        else:
            return result


if __name__ == "__main__":
    classifier = Classifier("beomi/KcELECTRA-base", 2, "cpu")
    while True:
        sentence = input("Input: ")
        print(classifier.predict(sentence))
