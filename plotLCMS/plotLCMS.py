import os
import numpy as np
import pandas as pd
from matplotlib import ticker
import matplotlib.pyplot as plt


def load_ASR(ASR_path):
    with open(ASR_path) as f:
        asr = f.readlines()
    return asr

def get_trace_number(asr):
    lineNumber_TraceNumber = []
    for line_number, line in enumerate(asr):
        if "TraceNumber" in line:
            lineNumber_TraceNumber.append(line_number)
    number_of_trace = len(lineNumber_TraceNumber)
    print(f"There are {number_of_trace} traces, with line numbers: {lineNumber_TraceNumber}")

    trace_description_list = [asr[line_number + 1].strip() for line_number in lineNumber_TraceNumber]

    print(f"Description: {trace_description_list}")

    trace_info_list = [get_trace_info(description) for description in trace_description_list]
    print(f"trace_info_list: {trace_info_list}")

    return lineNumber_TraceNumber, trace_info_list

def get_trace_info(description):
    trace_info = description.split("Description")[1].strip()
    return trace_info

def getSampleID(asr):
    SampleID = [line for line in asr if "SampleID" in line][0].split("SampleID")[1].strip()
    print(f"SampleID: {SampleID}")
    return SampleID


def extract_trace_from_ASR(asr):
    SampleID = getSampleID(asr)
    lcms_data = []
    lineNumber_TraceNumber, trace_info_list = get_trace_number(asr)

    for k, trace in enumerate(lineNumber_TraceNumber):
        indicator = ""
        trace_data = []
        i = lineNumber_TraceNumber[k] + 10
        while indicator != "}":
            indicator = asr[i].strip().replace("\t", ",")
            print(f"indicator: {indicator}")
            trace_data.append(indicator)
            i += 1

        trace_data = trace_data[:-1]
        trace_data = [d.split(",") for d in trace_data]
        print(f"Number of trace data points: {len(trace_data)}")

        lcms_data.append(trace_data)

    return SampleID, trace_info_list, lcms_data

def plotLCMS(SampleID, trace_info_list, lcms_data):
    number_of_trace = len(lcms_data)
    fig, ax = plt.subplots(number_of_trace, 1, sharex=True)
    fig.suptitle(SampleID, fontsize = 16, color = 'k', fontweight="bold")

    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((-1, 1))

    for i in range(number_of_trace):
        trace = lcms_data[i]
        df = pd.DataFrame(trace, columns = ['retention_time', 'signal']).astype(np.float64)
        trace_label = trace_info_list[i]

        if number_of_trace > 1:
            ax[i].plot(df["retention_time"], df["signal"], color = 'k', linewidth = 0.8)
            ax[i].set_title(trace_label, color = 'b')
            ax[i].yaxis.set_major_formatter(formatter)

        else:
            ax.plot(df["retention_time"], df["signal"])
            ax.set_title(trace_label)
            ax.yaxis.set_major_formatter(formatter)

    plt.xlabel("Retention time (minute)")
    plt.tight_layout()
    # plt.savefig(SampleID + ".png")
    # plt.close()
    plt.show()

def process_ASR(ASR_path, graph = False):
    asr = load_ASR(ASR_path)
    SampleID, trace_info_list, lcms_data = extract_trace_from_ASR(asr)
    # print(f"lcms_data: \n{lcms_data}")

    if graph:
        plotLCMS(SampleID, trace_info_list, lcms_data)

    return SampleID, trace_info_list, lcms_data



def main():
    src_dir = r'./data/Sulfa Drug LCMS Standard.D'
    ASR_path = [f for f in os.scandir(src_dir) if ".asr" in f.name.lower()]

    if ASR_path != []:
        ASR_path = ASR_path[0]
        # print(ASR_path)

        process_ASR(ASR_path, graph = True)
    else:
        print("Attention, there is no ASR file in this found!")

if __name__ == "__main__":
    main()