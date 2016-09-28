import os, errno, sys, time, shutil
import shlex, subprocess, math
import multiprocessing as mp
import numpy as np

def median(list):
    return np.median(np.array(list)).tolist()

def get_stats(data, Z=1.96):
    mean = np.mean(data , dtype=np.float32)
    std = np.std(data, dtype=np.float32, ddof=1)
    CI = Z * (std / math.sqrt(len(data)))

    return (mean , CI)


def countdown(t): # in seconds
    for i in range(t,0,-1):
        print 'Simulation will start in: %d seconds\r' % i,
        sys.stdout.flush()
        time.sleep(1)

def start_process():
    print 'Worker ready to work: ', mp.current_process().name


def mkdir(path, remove=False):
    try:
        os.makedirs(path)
        return ("%s : OK" % (path))
    except OSError as exc:  
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            if remove: 
                shutil.rmtree(path)
                os.makedirs(path)
                return ("%s : Removed and created again" % (path))
            else:
                return ("%s : Exist" % (path))
        else:
            raise

    return ("%s : Fail" % (path))

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


def optionizer(arg):
    # warning!!! ...  hack 
    # break the string args into a dict like {parameter: value}
    return dict(zip(arg[::2], arg[1::2]))


def create_output_directory(dirs):

    results = map(lambda x: '>>> creating '+ mkdir(x), dirs)

    print "mkdir results: "
    print ("\n".join(results))




def call_java(xms, xmx, cplex, jar, java, args):

    # splitting the args 
    command = shlex.split(args)

    # hack to a dict
    options = optionizer(command)

    # add extra java parameters
    command[0:0] = [java, cplex,  '-Xmx%dg' % (xmx), '-Xms%dg' % (xms),'-XX:-UseGCOverheadLimit', '-jar', jar]


    # creating files for stdout and stderr of each java called by the worker's children process
    path = options['--output'].replace('/results','/runners')
    mkdir(path)

    filename = options['--outputFilenamePrefix']

    stdout = '%s/%s.out.running' % (path, filename)
    stderr = '%s/%s.err.running' % (path, filename)


    with open(stdout,'w+') as out, open(stderr,'w+') as err:

        p = subprocess.Popen(['echo', str(command)+'\n'], stdout=out, stderr=err)
        p.wait()

        print ("Worker PID = %d running: %s\n") % (os.getpid(), command)

        # run the command by the worker's children process and wait to finish 
        p = subprocess.Popen(command, stdout=out, stderr=err)
        p.wait()


    # rename the filenames of the stdout and stderr
    mv_out = subprocess.Popen(['mv', stdout, stdout.replace('.running', '')])
    mv_err = subprocess.Popen(['mv', stderr, stderr.replace('.running', '')])
    
    mv_out.wait()
    mv_err.wait();

    return os.getpid()