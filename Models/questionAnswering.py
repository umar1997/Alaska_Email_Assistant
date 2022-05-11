from transformers import AutoModelForQuestionAnswering, AutoTokenizer

import torch


def extractAnswers(question, context, tokenizer, model):
    inputs = tokenizer.encode_plus(question, context, return_tensors="pt")
    input_ids = inputs["input_ids"].tolist()[0]

    text_tokens = tokenizer.convert_ids_to_tokens(input_ids)
    with torch.no_grad():
        output = model(**inputs)
    
    start_logits = output.start_logits[0]
    end_logits = output.end_logits[0]

    answer_start = torch.argmax(start_logits)  
    answer_end = torch.argmax(end_logits)

    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))

    return answer


if __name__ == "__main__":
    tokenizer = AutoTokenizer.from_pretrained("SpanBERT/spanbert-large-cased")
    model = AutoModelForQuestionAnswering.from_pretrained("./Span_Bert/model_weights")
    question = "What are the email addresses?"
    # question = "What is the email subject?"
    context = 'Send an email to chelseasmith@gmail.com and brian66@gmail.com with subject products for trading in brazil and body that starts like please review the attached memo to verify that i have identified all of the products that you are interested in trading in brazil i will be in sao paulo on monday september 20 1999 thank you sara'
    x = extractAnswers(question, context, tokenizer, model)
    print(x)