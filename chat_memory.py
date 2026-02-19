history = []


def save_exchange(question, answer):
    history.append({
        "question": question,
        "answer": answer
    })


def get_context(last_n=5):
    return "\n".join([
        f"Question: {item['question']}\nAnswer: {item['answer']}"
        for item in history[-last_n:]
    ])
