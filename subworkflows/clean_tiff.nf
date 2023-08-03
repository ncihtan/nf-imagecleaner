include { clean_tiff } from "../modules/clean_tiff.nf"

workflow CLEAN_TIFF {
  take:
  images
  
  main:
  clean_tiff(images)
  clean_tiff.out.set{cleaned}

  emit: 
  cleaned
}