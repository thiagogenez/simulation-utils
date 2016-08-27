import os, errno, sys, time, shutil

def countdown(t): # in seconds
	for i in range(t,0,-1):
		print 'Simulation will start in: %d seconds\r' % i,
		sys.stdout.flush()
		time.sleep(1)


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