1. python launch_one_run.py path/to/xxx.mc.conf
2. make run_mc
3. ./run_mc path/to/cppIn.txt
4. python check_after_one_run.py path/to/xxx.mc.conf

repeat the above steps until enough data points are collected

Note that the step length h should be large at first, then decrease the value
of h in later runs.
############################################
Alternatively, one may also compute without checking statistics.
The steps are:
1. python launch_one_run.py path/to/xxx.mc.conf
2. make run_mc
3. ./run_mc path/to/cppIn.txt
4. repeat the above steps until enough data points are collected
