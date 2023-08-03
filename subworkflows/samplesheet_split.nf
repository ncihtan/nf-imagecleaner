include { synapse_get } from "../modules/synapse_get.nf"

synapse_config = file('~/.synapseConfig')

workflow SAMPLESHEET_SPLIT {
    take:
    samplesheet
    main:
    Channel
        .fromPath(samplesheet)
        .splitCsv (header:true, sep:',' )
        .branch {
            row ->
            syn: row.image =~ /syn\:\/\/syn\d+/
            other: true
            }
        .set{ branched }

        // Make meta map from the samplesheet where local
        branched.other
        .map {
            row ->
            def meta = [:]
            meta.id = file(row.image).simpleName
            image = file(row.image)
            [meta, image]
        }
        .set {other }

        /// Where is a synapse ID fetch with synapse_get
        branched.syn
        .map {
            row ->
            def meta = [:]
            meta.id = row.image.replace('syn://', '')
            meta
        }.set{ syn }

        synapse_get(syn)
            .mix(other)
            .branch {
                ome: it[1] =~ /.+\.ome\.tif{1,2}$/
                svs: it[1] =~ /.+\.svs$/
                other: true
            }
            .set{ images }

    emit:
        ome = images.ome
        svs = images.svs
        other = images.other
}
