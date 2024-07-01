process clean_tiff {
  input:
    tuple val(meta), file(image)
  output:
    tuple val(meta), file('*$params.outsuffix*')
  publishDir "$params.outdir/", mode: 'copy', overwrite: true
  stub:
  """
  touch image_cleaned.ome.tiff
  """
  script:
  """
  clean_tiff.py $image --suffix $params.outsuffix
  """
}
