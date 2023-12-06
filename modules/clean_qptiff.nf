process clean_qptiff {
  input:
    tuple val(meta), file(image)
  output:
    tuple val(meta), file(image)
  stub:
  """
  touch image_cleaned.svs
  """
  script:
  """
  clean_qptiff.py $image
  """
}
