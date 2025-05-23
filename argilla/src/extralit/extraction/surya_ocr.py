import subprocess
import pandas as pd
from extralit.metrics.extraction import grits_multi_tables

def run_surya_ocr(input_pdf_path, output_json_path, surya_args=None):
    """
    Runs Surya OCR CLI on the given PDF and saves result to output_json_path.
    """
    surya_cmd = [
        "surya-ocr",  # replace with actual Surya OCR command
        "--input", input_pdf_path,
        "--output", output_json_path,
    ]
    if surya_args:
        surya_cmd.extend(surya_args)
    subprocess.run(surya_cmd, check=True)

def parse_surya_output(json_path):
    """
    Parses Surya OCR JSON output and converts tables to pd.DataFrame(s).
    """
    import json
    with open(json_path) as f:
        data = json.load(f)
    tables = []
    for table in data.get("tables", []):
        df = pd.DataFrame(table["data"], columns=table["columns"])
        tables.append(df)
    return tables

def benchmark_surya_ocr(input_pdf, ground_truth_tables):
    """
    Runs Surya OCR, parses output, and benchmarks against ground truth.
    """
    output_json = "surya_output.json"
    run_surya_ocr(input_pdf, output_json)
    pred_tables = parse_surya_output(output_json)
    metrics = grits_multi_tables(ground_truth_tables, pred_tables)
    return metrics