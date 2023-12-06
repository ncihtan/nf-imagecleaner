//include { remove_qptiff_label } from "../modules/remove_qptiff_label.nf"
//include { remove_qptiff_macro } from "../modules/remove_qptiff_macro.nf"
include { clean_qptiff } from "../modules/clean_qptiff.nf"


workflow CLEAN_QPTIFF {
  take:
  images

  main:

    clean_qptiff(images)
    clean_qptiff.out.set{cleaned}

  emit:
  cleaned
}
