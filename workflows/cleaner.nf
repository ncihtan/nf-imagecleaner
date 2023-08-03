include { SAMPLESHEET_SPLIT } from '../subworkflows/samplesheet_split.nf'
include { CLEAN_OME } from '../subworkflows/clean_ome.nf'
include { CLEAN_SVS } from '../subworkflows/clean_svs.nf'
include { CLEAN_TIFF } from '../subworkflows/clean_tiff.nf'

workflow CLEANER {
    SAMPLESHEET_SPLIT (params.input)
    CLEAN_OME ( SAMPLESHEET_SPLIT.out.ome )
    CLEAN_SVS ( SAMPLESHEET_SPLIT.out.svs )
    SAMPLESHEET_SPLIT.out.other
        .mix ( CLEAN_OME.out.cleaned, CLEAN_SVS.out.cleaned )
        .set { combined }
    CLEAN_TIFF ( combined )
}
