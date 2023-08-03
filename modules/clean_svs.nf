process clean_svs {
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
  clean_svs.py $image
  """
}