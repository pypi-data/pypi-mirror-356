from dikshant import Dikshant

def main():
    """Command line entry point for Dikshant assistant"""
    assistant = Dikshant()
    print("Dikshant assistant is running. Say 'hey friend' to activate.")
    assistant.start()
    
    try:
        while assistant.is_active:
            pass
    except KeyboardInterrupt:
        print("\nStopping assistant...")

if __name__ == "__main__":
    main()