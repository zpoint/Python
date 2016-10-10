""""
cProfile:
python -m cProfile -s cumulative julia.py
python -m cProfile -o profile.stats julia.py

timeit:
python -m timeit -n 5 -r 5 -s "import julia" "julia.calc_pure_python(desired_width = 1000, max_iterations = 300)"
or inside Ipython
>>>z = 0 + 0j
>>>% timeit abs(z) < 2
 
line_profiler: #CPU USAGE
pip install line_profiler
"@profile" in your function
kernprof -l -v julia.py

memory_profiler #
pip install memory_profiler #in not unix os, psutil is required ,or it will raised NotImplementedError: The psutil module is required for non-unix platforms
python -m memory_profiler julia_memoryprofiler.py ##super slow, took i7 cpu about 1.5 hours


perf stat -e cycles,stalled-cycles-frontend,stalled-cycles-backend,instructions,cache-references,cache-misses,branches,branch-misses,task-clock,faults,minor-faults,cs,migrations -r 3 python3 diffusion_python_memory.py
"""
import pstats
p = pstats.Stats("profile.stats") //file name
p.sort_stats("cumulative")
p.print_stats()
p.print_callers()
p.print_callees()
