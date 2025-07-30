from dikshant import Dikshant
import signal

def main():
    assistant = Dikshant()
    
    # Handle Ctrl+C gracefully
    signal.signal(signal.SIGINT, lambda s, f: assistant.stop())
    
    print("Dikshant assistant is running. Say 'hey friend' to activate.")
    assistant.start()

if __name__ == "__main__":
    main()