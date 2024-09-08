from virtual_pi import VirtualPiBoard

def main():
    try:
        app = VirtualPiBoard()
        app.screen.mainloop()  # Start the Tkinter event loop
    except Exception as e:
        print(f"Uncaught exception in main application: {e}")

if __name__ == "__main__":
    main()
