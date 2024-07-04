process reset_datetime {
  input:
    tuple val(meta), file(image)
  output:
    tuple val(meta), file(image)
  publishDir "$params.outdir/", mode: 'copy', overwrite: true
  stub:
  """
  touch image_cleaned.ome.tiff
  """
  script:
  """
  reset_datetime.py $image --datetags $params.datetags
  """
}
