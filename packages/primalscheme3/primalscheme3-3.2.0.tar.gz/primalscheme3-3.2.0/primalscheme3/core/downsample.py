# Downsample to count
import pathlib

import networkx as nx

# type: ignore
from primalscheme3.core.config import Config
from primalscheme3.core.msa import MSA
from primalscheme3.core.progress_tracker import ProgressManager
from primalscheme3.core.thermo import calc_annealing_hetro


def downsample_thermo(dr, config: Config) -> list:
    included_list = []

    return included_list


if __name__ == "__main__":
    # Example usage
    config = Config()
    config.primer_annealing_tempc = 65
    config.primer_annealing_prop = 10

    pm = ProgressManager()
    msa_obj = MSA(
        "example",
        pathlib.Path(
            "/Users/kentcg/primerschemes/primerschemes/artic-measles/400/v1.0.0/work/all_genomes.align.ds.align.repaired.fasta"
        ),
        1,
        "first",
        pm,
        config=config,
    )

    r = msa_obj.digest_f_to_count(config, [100])

    for i, drs in r:
        g = nx.DiGraph()

        # Check that the digested errors are not massive
        hard_errors = 0
        for dr in drs:
            print(dr.count, dr.result, dr.error)

        for dr in drs:
            for dr2 in drs:
                if dr != dr2:
                    ka = calc_annealing_hetro(dr.seq, dr2.seq, config)
                    g.add_edge(dr, dr2, weight=ka)
