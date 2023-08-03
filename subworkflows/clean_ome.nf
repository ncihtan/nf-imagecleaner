include { clean_ome } from "../modules/clean_ome.nf"

workflow CLEAN_OME {
  take:
  images

  main:
  clean_ome(images)
  clean_ome.out.set{cleaned}

  emit:
  cleaned
}
