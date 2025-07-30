import json
import re
from typing import List, Dict;
from mcp.server.fastmcp import FastMCP
import pandas as pd
import zipfile
from tempfile import TemporaryDirectory
from pathlib import Path

class ZipNotFoundError(FileNotFoundError):
    """zipfile.ZipFile not found, or not a zip file"""

class BadZipError(RuntimeError):
    """zipfile.BadZipFile """
    
OUTPUT_REPORT = "msbench_analysis_report.xlsx"
ERROR_BLOCK_PATTERN = re.compile(r"(╭\s*Error on Agent[\s\S]*?╰[\s\S]*?╯)", re.MULTILINE)
ERROR_TYPE_PATTERN = re.compile(r'\[([^\]]+)\]')
COLUMNS = ["File Name", "Error Information", "Error Type"]


def norm_path(path:str) -> str:
    """Normalize the path to use forward slashes"""
    return Path(path).expanduser().resolve(strict=False)


def table_markdown(rows, columns):
    df = pd.DataFrame(rows, columns=columns)
    return df.to_markdown(index=False)   

def safe_extract(
        zip_ref: zipfile.ZipFile,
        target_dir: Path,
        ignore_error: bool = False
) -> None:
    """
    Safely extract files from a zip file to the target directory.
    Returns True if any errors occurred, False if all succeeded.
    """
    error_occurred = False
    for member in zip_ref.namelist():
        mpath = Path(member)
        if mpath.is_absolute() or ".." in mpath.parts:
            if ignore_error:
                continue
            raise BadZipError(f"Illegal member: {member}")

        try:
            zip_ref.extract(member, target_dir)
        except Exception as e:
            if ignore_error:
                continue
            raise RuntimeError(f"extract {member}: {e}")
    return error_occurred

def process_cls_file(cls_file: Path) -> List[Dict[str,str]]:
    """process cls.log file, extract error messages and types"""
    errors = []
    text = cls_file.read_text(encoding="utf-8", errors="ignore")
    for blk in ERROR_BLOCK_PATTERN.findall(text):
        msg_lines, etype = [], "UNKNOWN"
        for line in map(str.strip, blk.splitlines()):
            if line.startswith(("╭","╰")) or ("Error on Agent" in line): continue
            if line.startswith("│"):
                body = line.lstrip("│").rstrip("│").strip()
                if body:
                    msg_lines.append(body)
                    if etype == "UNKNOWN":
                        m = ERROR_TYPE_PATTERN.search(body)
                        if m: etype = m.group(1)
        if msg_lines:
            errors.append({"type": etype, "msg": "\n".join(msg_lines)})
    return errors

def generate_error_report(zip_path :Path , need_write: bool = False) -> dict:
    """unzip outer zip, recursively process all inner zips, output error result"""
    zip_path = norm_path(zip_path)
    if not zip_path.exists():
        raise ZipNotFoundError(f"Zip file not found: {zip_path}")
    rows, counter = [], {}
    skipped_inner_zip=0
    skipped_cls_log=0
    with TemporaryDirectory(prefix="msbench_") as tmp:
        tmp_dir = Path(tmp)
        with zipfile.ZipFile(zip_path) as z:
            safe_extract(z, tmp_dir)

        for inner in tmp_dir.rglob("*.zip"):
            try:
                with zipfile.ZipFile(inner) as z:
                   safe_extract(z, tmp_dir/inner.stem, ignore_error=False)
            except Exception as e:
                skipped_inner_zip += 1
                continue

            # only process cls.log files in the output directory
            output_dir = tmp_dir/inner.stem/"output"
            if output_dir.exists() and output_dir.is_dir():
                for cls in output_dir.rglob("cls.log"):
                    try:
                        for item in process_cls_file(cls):
                            rows.append([inner.name, item["msg"], item["type"]])
                            counter[item["type"]] = counter.get(item["type"], 0) + 1
                    except Exception as e:
                        skipped_cls_log += 1
                        continue

    out_xlsx = zip_path.with_name(OUTPUT_REPORT) if need_write else None
    if need_write:
        write_error_report(rows, counter, out_xlsx)

    return {
        "report_path": str(out_xlsx) if need_write else "",
        "total_errors": sum(counter.values()),
        "by_type": counter,
        "skipped_inner_zip": skipped_inner_zip,
        "skipped_cls_log": skipped_cls_log,
        "errors": rows
    }

def write_error_report(errors: list, type_counter: dict, out_xlsx: Path) -> None:
    """Write errors to an excel file."""
    df_detail = pd.DataFrame(errors, columns=COLUMNS)
    df_type = pd.DataFrame(list(type_counter.items()), columns=["Error Type", "Count"])
    # add a row for all error types count
    all_count = df_type['Count'].sum()
    df_type = pd.concat([df_type, pd.DataFrame([["ALL", all_count]], columns=["Error Type", "Count"])], ignore_index=True)
    with pd.ExcelWriter(out_xlsx, engine='openpyxl') as writer:
        df_detail.to_excel(writer, sheet_name='Detail', index=False)
        df_type.to_excel(writer, sheet_name='TypeCount', index=False)

mcp = FastMCP("msbench_analysis_mcp")

@mcp.tool()
def analyze_errors_and_save_report(zipPath: str) -> str:
    """
    Analyze the errors in the MSBench log files and save the report to a excel file.
    Return a summary of the analysis results and save the error report to an Excel file.
    """
    result = generate_error_report(zipPath, True)
    info = [
        f"Report path: {result['report_path']}",
        f"Total errors: {result['total_errors']}",
        f"Error type count: {json.dumps(result['by_type'], ensure_ascii=False)}",
        f"Skipped inner zip: {result['skipped_inner_zip']}",
        f"Skipped cls.log: {result['skipped_cls_log']}"
    ]
    return "\n".join(info)

@mcp.tool()
def analyze_errors(zipPath: str) -> str:
    """
    Analyze the errors in the MSBench log files and output a detailed report of the analysis results.
    This function does not save the report to an Excel file.
    Return a summary of the analysis results and a detailed error table in markdown format
    """
    result = generate_error_report(zipPath, False)
    info = [
        f"Total errors: {result['total_errors']}",
        f"Error type count: {json.dumps(result['by_type'], ensure_ascii=False)}",
        f"Skipped inner zip: {result['skipped_inner_zip']}",
        f"Skipped cls.log: {result['skipped_cls_log']}"
    ]
    if result.get('errors'):
        info.append(table_markdown(result['errors'], COLUMNS))
    return "\n".join(info)

def runServer() -> None:
    """
    Main function to run the MCP server.
    """
    mcp.run(transport='stdio')
