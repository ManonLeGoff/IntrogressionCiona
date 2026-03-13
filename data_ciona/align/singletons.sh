#Rule to eliminate “singletons” (reads present alone on a molecule): 
#Edit by B. Penaud in the script previously implemented in harpy: 
#$CONDA_PREFIX/lib/python3.13/site-packages/harpy/snakefiles/align_bwa.smk

rule singleton_bams:
    input:
        bx = "reports/data/bxstats/{sample}.bxstats.gz",
        bams = "{sample}.bam",
        molcov = "reports/data/coverage/{sample}.molcov.gz",
        fai = f"{workflow_geno}.fai",
        bed = "reports/data/coverage/coverage.bed",
    output:
        bams_Nosingletons = "NoSingletons/{sample}_NoSingletons.bam",
        bai_Nosingletons = "NoSingletons/{sample}_NoSingletons.bam.bai",
        report_Nosingletons = "reports_NoSingletons/data/bxstats/{sample}_NoSingletons.bxstats.gz",
        report_cov_Nosingletons = "reports_NoSingletons/data/coverage/{sample}_NoSingletons.cov.gz",
        report_mol_Nosingletons = "reports_NoSingletons/data/coverage/{sample}_NoSingletons.molcov.gz",
        stats_Nosingletons = temp("reports_NoSingletons/data/samtools_stats/{sample}_NoSingletons.stats"),
        flagstat_Nosingletons = temp("reports_NoSingletons/data/samtools_flagstat/{sample}_NoSingletons.flagstat"),
        bams_singletons = "Singletons/{sample}_Singletons.bam",
        bai_singletons = "Singletons/{sample}_Singletons.bam.bai",
        report_singletons = "reports_Singletons/data/bxstats/{sample}_Singletons.bxstats.gz",
        report_cov_singletons = "reports_Singletons/data/coverage/{sample}_Singletons.cov.gz",
        report_mol_singletons = "reports_Singletons/data/coverage/{sample}_Singletons.molcov.gz",
        stats_singletons = temp("reports_Singletons/data/samtools_stats/{sample}_Singletons.stats"),
        flagstat_singletons = temp("reports_Singletons/data/samtools_flagstat/{sample}_Singletons.flagstat"),
    container:
        None
    params:
        windowsize
    log:
        "logs/bxstats/{sample}_Singletons.bxstats.log"
    shell:
        """
        samtools view -h {input.bams} | awk -F "\\t" 'fname != FILENAME {{fname = FILENAME; idx++}} idx==1 {{if(FNR>1){{if($2!~/invalid/){{if($3>1){{keep["MI:i:"$2]}}}}}}}} idx==2 {{if($0 ~ /^@/){{print >"Singletons/{wildcards.sample}_Singletons.sam" ; print >"NoSingletons/{wildcards.sample}_NoSingletons.sam"}}else{{for(c=1;c<=NF;c++){{if($c ~ /^MI:i:/){{if($c in keep){{print >"NoSingletons/{wildcards.sample}_NoSingletons.sam"}}else{{ print >"Singletons/{wildcards.sample}_Singletons.sam" }}}}}}}}}}' <(gzip -dc {input.bx}) - 
        
        samtools view -b NoSingletons/{wildcards.sample}_NoSingletons.sam -o {output.bams_Nosingletons}
        samtools view -b Singletons/{wildcards.sample}_Singletons.sam -o {output.bams_singletons}
        
        samtools index {output.bams_Nosingletons}
        samtools index {output.bams_singletons}
        
        rm NoSingletons/{wildcards.sample}_NoSingletons.sam
        rm Singletons/{wildcards.sample}_Singletons.sam

        bx_stats {output.bams_Nosingletons} > {output.report_Nosingletons} 2> {log}
        bx_stats {output.bams_singletons} > {output.report_singletons} 2> {log}
        
        samtools bedcov -c {input.bed} {output.bams_Nosingletons} | awk '{{ $6 = ($4 / ($3 + 1 - $2)); print }}' | gzip > {output.report_cov_Nosingletons}
        samtools bedcov -c {input.bed} {output.bams_singletons} | awk '{{ $6 = ($4 / ($3 + 1 - $2)); print }}' | gzip > {output.report_cov_singletons}
        
        molecule_coverage -f {input.fai} -w {params} {output.report_Nosingletons} | gzip > {output.report_mol_Nosingletons}
        molecule_coverage -f {input.fai} -w {params} {output.report_singletons} | gzip > {output.report_mol_singletons}
        
        samtools stats -d {output.bams_Nosingletons} > {output.stats_Nosingletons}
        samtools stats -d {output.bams_singletons} > {output.stats_singletons}
        
        samtools flagstat {output.bams_Nosingletons} > {output.flagstat_Nosingletons}
        samtools flagstat {output.bams_singletons} > {output.flagstat_singletons}
