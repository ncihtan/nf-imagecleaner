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
  reset_datetime.py $image "1970:01:01 00:00:00"
  """
}
