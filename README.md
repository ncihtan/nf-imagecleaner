# nf-imagecleaner

The nf-imagecleaner is a Nextflow pipeline that prepares images for upload by removing sensitive data. This includes `AcquisitionDate` and `StructuredAnnotations` from OME-TIFF files, label images and `Date` from SVS files, and specified metadata tags from TIFFs. It handles Synapse URIs, local file paths, and mixtures of both in its input samplesheet.

### Requirements

- Nextflow
- Python 3.x with the following packages:
  - `tifftools`
  - `ome_types`
  - `synapseclient`

### Usage

Clone the GitHub repository:

```
git clone https://github.com/ncihtan/nf-imagecleaner.git
```

Move into the directory:

```
cd nf-imagecleaner
```

To run the pipeline with default parameters, use:

```
nextflow run main.nf --input <path/to/samplesheet.csv>
```

### Inputs

The input to the pipeline is a CSV file (specified with `--input`) where the `image` column contains paths to images. If the path is a Synapse URL (starts with `syn://`), this file will be downloaded from Synapse.

For example:

```
image
syn://syn00123
/local/path/to/image.svs
```

### Parameters

- `outdir`: Directory for outputs (default: `outputs`)
- `outsuffix`: Suffix for output files (default: `_cleaned`)
- ~~`rm_svs_macro`: Boolean indicating whether to remove the macro image in SVS files (default: `false`)~~ Coming soon!
- `rm_svs_label`: Boolean indicating whether to remove the label image in SVS files (default: `true`)
- `rm_ome_sa`: Boolean indicating whether to remove structural annotations in OME-XML files (default: `true`)

### Outputs

The cleaned images will be placed in the directory specified by `--outdir`.

### Metadata Redaction

The specific tags removed are:

for TIFFs:

- DateTime
- NDPI_ScanTime
- NDPI_WriteTime
- Artist
- HostComputer
- WangAnnotation
- WriterSerialNumber
- MDLabName
- MDPrepDate
- MDSampleInfo
- Software

for SVSs:

- Date
- Time Zone
- ScanScope ID
- User
- Time
- DSR ID

for OME-TIFFs:

- Whole StructuredAnnotations block
- Experimenter's e-mail, first name, and last name
- AcquisitionDate

### Tools Used

- `tifftools`: for handling TIFF and OME-TIFF metadata
- `ome_types`: for handling OME-XML
- `synapseclient`: for downloading data from Synapse

This `README.md` was automatically generated by [jaredcd/ai-tools](https://github.com/jaredcd/ai-tools) and GPT-4.
