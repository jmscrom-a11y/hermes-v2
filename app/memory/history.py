from app.memory.store import load_memory, save_memory

MAX_HISTORY = 20


def add(role: str, content: str):
    memory = load_memory()

    memory.append(
        {
            "role": role,
            "content": content,
        }
    )

    memory = memory[-MAX_HISTORY:]

    save_memory(memory)


def get():
    return load_memory()


def clear():
    save_memory([])