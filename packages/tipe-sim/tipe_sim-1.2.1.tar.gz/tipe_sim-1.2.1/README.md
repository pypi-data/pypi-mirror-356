# TIPE SIM

A Python library to generate professional, topic-aware simulations for TIPE projects using the power of the Gemini API.

## Features

-   **AI-Powered:** Simply provide your TIPE topic (`sujet`).
-   **Intelligent Design:** The AI analyzes your topic and chooses the best visualization tools (graphs, 2D/3D canvas, etc.).
-   **Professional Dashboards:** Generates a single, complete HTML file with a modern dashboard layout.
-   **Academically Rigorous:** Includes real-time data, user controls, and correctly rendered mathematical explanations.

## Installation

You can install the library using pip:

```bash
pip install tipe-sim

Usage
Here is an example of how a user can run your library. They can save this code as a Python file (e.g., run_simulation.py) and execute it from their terminal.

# test_simulation.py
# An interactive script to test your tipe_sim library.

from tipe_sim import tsim
import os

def main():
    """Main function to run the interactive test."""
    
    print("--- TIPE Simulation Generator ---")
    
    # 1. Get API Key from environment variables.
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("\nERROR: The GEMINI_API_KEY environment variable is not set!")
        print("Please set it before running the script.")
        return # Exit the script

    # 2. Get the TIPE topic from the user interactively.
    print("\nPlease enter your TIPE topic (sujet):")
    my_sujet = input("> ")

    if not my_sujet:
        print("Topic cannot be empty. Exiting.")
        return

    # 3. Ask the user for a filename.
    print("\nEnter a filename for the output simulation (e.g., my_simulation.html):")
    output_filename = input("> ")
    if not output_filename.endswith('.html'):
        output_filename += '.html'

    # 4. Generate the simulation.
    print(f"\nGenerating simulation for: '{my_sujet}'...")
    try:
        html_content = tsim(sujet=my_sujet, api_key=api_key, output_path=output_filename)
        
        if html_content:
            print(f"\n✅ Simulation generated successfully!")
            print(f"File saved to: {os.path.abspath(output_filename)}")
        else:
            print("\n❌ Simulation generation failed. Please check the error messages above.")

    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
