include { reset_datetime } from "../modules/reset_datetime.nf"

workflow RESET_DATETIME {
  take:
  images

  main:
  reset_datetime(images)
  reset_datetime.out.set{reset}

  emit:
  reset
}
