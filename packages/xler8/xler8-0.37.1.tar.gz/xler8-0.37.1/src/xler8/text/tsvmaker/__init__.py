import turbocore
import sys
import xler8
import copy
import json


def cli_all(XLSX_FILENAME, OUT_PREFIX):
    sheet_outname = OUT_PREFIX
    in1 = xler8.xlsx(XLSX_FILENAME)
    in1_sheets = xler8.xlsx_sheetnames(XLSX_FILENAME)

    sheet_index = 1

    for sheetname in in1_sheets:
        hdr = list(in1[sheetname].keys())

        with open("%s.%d.tsv" % (sheet_outname, sheet_index), "w") as f:
            cols=in1[sheetname]
            data = [hdr]
            rowcount = 0
            for h in hdr:
                rowcount = len(in1[sheetname][h])
                break
            for row_index in range(0, rowcount):
                row = []
                for col_index in range(0, len(hdr)):
                    row.append(str(cols[hdr[col_index]]))
                data.append(row)

            for linecols in data:
                f.write("\t".join(linecols))
                f.write("\n")
        
        sheet_index+=1


def main():
    turbocore.cli_this(__name__, 'cli_')
