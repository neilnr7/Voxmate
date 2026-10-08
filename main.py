from agent import Agent
from stt.whisper_stt import WhisperSTT


def main():
    print("VoxMate started.")
    print("Press Enter to speak.")
    print("Type 'exit' to quit.\n")

    agent = Agent()
    stt = WhisperSTT()

    while True:
        try:
            user_input = input("Press Enter to speak: ")

            if user_input.strip().lower() in {"exit", "quit"}:
                print("VoxMate: Goodbye!")
                break

            text = stt.listen()

            if not text:
                continue

            print(f"You: {text}")

            response = agent.run(text)

            print(f"VoxMate: {response}\n")

        except KeyboardInterrupt:
            print("\nVoxMate: Goodbye!")
            break

        except Exception as e:
            print(f"VoxMate: Error - {e}\n")


if __name__ == "__main__":
    main()