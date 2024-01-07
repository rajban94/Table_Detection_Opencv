# Table Detection with OpenCV

Table Detection with OpenCV is a Python project that takes PDFs as input, checks the alignment, re-aligns if required, detects the table structure, extracts data, and dumps it into an Excel file. The current implementation focuses on bordered and Un-bordered tables.

## Features

- **PDF Input:** Accepts PDF files as input for table detection, which needs to be placed in the Input Folder.
- **Image Creation:** It will create Images for each pdf and will dump it in the Images Folder.
- **Alignment Check:** Verifies and adjusts image alignment if necessary and the re-aligned image will also be placed in the respective folders inside Images Folder.
- **Table Detection:** Identifies bordered tables in the PDF document.
- **Data Extraction:** Extracts data from the detected tables.
- **Excel Output:** Dumps the extracted data into an Excel spreadsheet in the Output Folder.

## Libraries Used

- Python 3.x
- OpenCV
- NumPy
- pdf2image
- Pillow
- Pandas
- openpyxl
- easyocr

## Create and Activate Environment
```bash
conda create -n <env_name> python=3.7
conda activate <env_name>
```
## Installation of packages

```bash
pip install -r requirements.txt
```

## Clone the repository

```bash
git clone https://github.com/your-username/Table_Detection_Opencv.git
```

## Run the Script

- Activate the environment if not activated.
- Change the path of the env in run.bat and double click the run.bat for execution.