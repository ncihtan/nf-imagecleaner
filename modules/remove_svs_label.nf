process remove_svs_label {
  input:
    tuple val(meta), file(image)
  output:
    tuple val(meta), file(image)
  stub:
  """
  touch image.svs
  """
  script:
  """
  remove_svs_label.py $image
  """
}
