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



#################
One may also use a script to do mc computations and check statiscs
1. set T value in exec_checking.py
2. python exec_checking.py


After mc computations end for all T, extract the effective data:
1. cd data2json/
2. python U_dist_data2json.py rowNum

To plot:
1. cd plt/
2. python V_inv_12_6_U_and_dist_json2plt.py rowNum

