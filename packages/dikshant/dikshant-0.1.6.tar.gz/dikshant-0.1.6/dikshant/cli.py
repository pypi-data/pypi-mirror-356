from dikshant import Dikshant
import sys

def main():
    assistant = Dikshant()
    print("Dikshant assistant is running. Say 'hey friend' to activate.")
    assistant.start()
    
    try:
        # Keep main thread alive but responsive
        while assistant.is_active:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nStopping assistant...")
        sys.exit(0)

if __name__ == "__main__":
    main()