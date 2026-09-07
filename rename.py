#!/usr/bin/env python3

import argparse
import shutil
from pathlib import Path


REPLACEMENTS = {
	# "old_name": "new_name",
	# use r"string" if strings includes something that looks like an escape sequence, e.g. "\n"
	r"\$1271": "clkd",
    # r"\$1875": "clkdd1",
    # r"\$3890": "clkdd2",
    # r"\$784": "clkdd3",
    # r"\$2216": "clkdd4",
    # r"\$3829": "clkdd5",
    # r"\$2288": "clkdd6",
    # r"\$3249": "clkdd7",
    # r"\$2295": "clkdd8",
    # r"\$983": "clkdd9",
    # r"\$1649": "clkdd10",
    # r"\$1460": "clkdd11",
    # r"\$2728": "clkdd12",
    # r"\$3588": "clkdd13",
    # r"\$2155": "clkdd14",
    # r"\$3066": "clkdd15",
    # r"\$729": "clkdd16",
	r"\$3953": "success_b",
	#r"\$933": "select",
	r"\$2527": "D00",
	r"\$2522": "D01",
	r"\$2596": "D02",
	r"\$2437": "D03",
	r"\$2423": "D04",
	r"\$2190": "D05",
	r"\$2267": "D06",
	r"\$2108": "D07",
	r"\$2136": "D08",
	r"\$2138": "D09",
	r"\$2352": "D10",
	r"\$2379": "D11",
	#r"\$2462": "Q00",
	r"\$2457": "Q01",
	r"\$2544": "Q02",
	r"\$2376": "Q03",
	r"\$2265": "Q04",
	r"\$2223": "Q05",
	r"\$2222": "Q06",
	r"\$2103": "Q07",
	r"\$2185": "Q08",
	r"\$2135": "Q09",
	r"\$2224": "Q10",
	r"\$2377": "Q11",
	#r"\$2270": "Q04_b", 
	#r"\$4210": "Q04d",
	r"\$1363": "rand0",
	r"\$1413": "rand1",
	r"\$1362": "rand2",
	r"\$1527": "rand3",
	r"\$3954": "success_b",
	r"\$4257": "success_stage",
	r"\$3813": "out_en1",
	r"\$3868": "out_en2",
	r"\$I13629": "VPWR",
	r"\$I13627": "VPWR",
	r"\$I13626": "VPWR",
	r"\$I13625": "VPWR",
	r"\$I13622": "VPWR",
	r"\$737": "or4b_85_a",
	r"\$1103": "or4b_85_c",
	r"\$3906": "or4b_85_x",
	r"\$2079": "Ib_2494",
	r"\$4180": "Ib_2495",
	r"\$3797": "Ib_2500",
	r"\$1403": "Ib_2505",
	r"\$3173": "Ib_2511",
	r"\$1275": "Ib_2512",
	r"\$3388": "Ib_2514",
	r"\$1201": "Ib_2520",

	r"\$864": "combi864",
	
	
}


def rewrite_file(input_path: Path, output_path: Path | None = None) -> None:
	if output_path is None:
		output_path = input_path

	with input_path.open("r", encoding="utf-8", newline="") as input_file:
		lines = input_file.read().splitlines(keepends=True)
	replacements_enabled = True
	rewritten_lines = []

	for line in lines:
		if replacements_enabled and line.startswith(".ENDS"):
			replacements_enabled = False

		if replacements_enabled and not line.startswith("*"):
			newline = ""
			content = line
			if line.endswith("\r\n"):
				content, newline = line[:-2], "\r\n"
			elif line.endswith("\n") or line.endswith("\r"):
				content, newline = line[:-1], line[-1]

			fields = content.split(" ")
			line = " ".join(REPLACEMENTS.get(field, field) for field in fields)
			line += newline

		rewritten_lines.append(line)

	rewritten_content = "".join(rewritten_lines)
	output_content = rewritten_content.encode("utf-8")
	if output_path.exists():
		backup_path = output_path.with_name(output_path.name + ".bak")
		shutil.copy2(output_path, backup_path)
	output_path.write_bytes(output_content)


def main() -> None:
	parser = argparse.ArgumentParser(description="Replace SPICE fields in a file.")
	parser.add_argument("paths", type=Path, nargs="+", help="input file, and optional output file")
	args = parser.parse_args()
	if len(args.paths) > 2:
		parser.error("expected one or two file names")
	rewrite_file(*args.paths)


if __name__ == "__main__":
	main()
