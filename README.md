# AI Writer for User Stories and Test cases

Dirty script that generates user stories and test cases from your application screenshots

## Setup Instructions

Follow these instructions to run the script on your local machine.

### Installation

1. Open a terminal and navigate to the folder containing the unpacked script.

```bash
cd path/to/your/script
```

2. Create a virtual environment:

```bash
python3 -m venv ./venv
```

3. Activate the virtual environment:

```bash
source ./venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

### Running the Script

After installing the dependencies, you can run the script by specifying the OpenAI key and the path to the images:

```bash
python3 main.py --openai-key=xxx --directory=./images
```

The script will create `_us.md` and `_tc.md` files, which are the user story and test cases, respectively