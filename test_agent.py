
from agent import Agent


def main():
    try:
        agent = Agent()
    except Exception as e:
        print(f"Failed to initialize VoxMate: {e}")
        return

    print("VoxMate text test started.")
    print("Type 'exit' or 'quit' to stop.")

    while True:
        try:
            text = input("\nYou: ").strip()

            if text.lower() in {"exit", "quit"}:
                print("VoxMate test stopped.")
                break

            if not text:
                continue

            try:
                response = agent.run(text)

                if response and str(response).strip():
                    print(f"VoxMate: {response}")
                else:
                    print(
                        "VoxMate: I received an empty response. "
                        "Check the LLM RESPONSE logs in agent.py."
                    )

            except Exception as e:
                print(f"VoxMate error: {e}")

        except KeyboardInterrupt:
            print("\nVoxMate test stopped.")
            break
        except EOFError:
            print("\nInput closed. VoxMate test stopped.")
            break


if __name__ == "__main__":
    main()
