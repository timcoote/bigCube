import pstats
p = pstats.Stats ('foo')
p.sort_stats ('cumulative').print_stats (10)
p.sort_stats ('time').print_stats (10)
