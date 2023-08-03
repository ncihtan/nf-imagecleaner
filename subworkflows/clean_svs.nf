include { remove_svs_label } from "../modules/remove_svs_label.nf"
//include { remove_svs_macro } from "../modules/remove_svs_macro.nf"
include { clean_svs } from "../modules/clean_svs.nf"


workflow CLEAN_SVS {
  take:
  images
  
  main:

  if ( params.rm_svs_label ) {
    remove_svs_label(images)
    clean_svs(remove_svs_label.out)
    clean_svs.out.set{cleaned}
  } else {
    clean_svs(images)
    clean_svs.out.set{cleaned}
  }

  emit: 
  cleaned
}