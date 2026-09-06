from agent import Agent


def main():
    print("VoxMate started.")
    print("Type 'exit' to quit.\n")

    agent = Agent()

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in {"exit", "quit"}:
                print("VoxMate: Goodbye!")
                break

            response = agent.run(user_input)

            print(f"VoxMate: {response}\n")

        except KeyboardInterrupt:
            print("\nVoxMate: Goodbye!")
            break

        except Exception as e:
            print(f"VoxMate: Error - {e}\n")


if __name__ == "__main__":
    main()