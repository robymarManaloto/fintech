# Readme for SeedWave Project

## Prerequisites

Before running the SeedWave program, make sure you have the following prerequisites installed on your system:

1. **Python:** You will need Python installed on your machine. If you don't have Python installed, you can download it from [Python's official website](https://www.python.org/downloads/).

2. **Virtual Environment (venv):** It is recommended to use a virtual environment to isolate the project dependencies. You can create a virtual environment using the following command:
   ```
   python -m venv venv
   ```

3. **Install Dependencies:** After creating the virtual environment, activate it and install the project's dependencies from the `requirements.txt` file using the following command:
   ```
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On macOS and Linux

   pip install -r requirements.txt
   ```

## Running the Program

Follow these steps to run the SeedWave program:

1. Open your terminal.

2. Activate the virtual environment by running the appropriate command based on your operating system:
   ```
   venv\Scripts\Activate  # On Windows
   source venv/bin/activate  # On macOS and Linux
   ```

3. Change the working directory to the SeedWave project folder:
   ```
   cd seedwave
   ```

4. Run the SeedWave program by executing the following command:
   ```
   python manage.py runserver
   ```

The program should now be running, and you can access it by opening a web browser and navigating to the appropriate URL (usually `http://localhost:8000/`).


## Changing Data Sources

To switch between using dummy or clean data sources, follow these steps:

1. Navigate to the 'views' folder in the root directory of the SeedWave project.

2. Depending on your choice, replace the 'views' folder with either 'views (dummy)' or 'views (clean)' from the 'seedwave/campaignwizard' directory.

Now, the program will use the data source you selected for its operation.
# fintech
