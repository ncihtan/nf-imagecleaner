process remove_svs_macro {
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
  remove_svs_macro.py $image
  """
}
