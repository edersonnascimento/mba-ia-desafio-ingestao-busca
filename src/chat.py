from config import load_settings
from providers import get_llm
from search import build_prompt, search_context

def main():
    try:
        settings = load_settings(require_llm=True)
        llm = get_llm(settings)
    except Exception as exc:
        print(
            "Nao foi possivel iniciar o chat. Verifique os erros de "
            f"inicializacao. Detalhes: {exc}"
        )
        return

    while True:
        question = input("Pergunta (ou 'exit' para sair): ").strip()
        if not question or question.lower() == "exit":
            break

        try:
            context, _ = search_context(question, settings=settings)
            prompt = build_prompt(context, question)
            response = llm.invoke(prompt)
            print(response.content.strip())
        except Exception as exc:
            print(f"Erro ao responder pergunta: {exc}")

if __name__ == "__main__":
    main()