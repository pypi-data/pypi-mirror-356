# romscom/romscom.py

"""**ROMS Communication Module primary functions**

This module holds the primary functions expected to be called by end-users in a
typical romscom workflow, which includes importing ROMS parameters from .yaml files,
manipulating values as needed for an experiment, and then exporting to ROMS .in
files:

- `readparamfile(filename,...)` reads a parameter YAML file into an ordered
  dictionary
- `stringifyvalues(d,...)` reformats the values in a parameter dictionary to
  ROMS syntax strings
- `dict2standardin(d,...)` converts a parameter dictionary to standard input
  text, and optionally writes to file
- `converttimes(d,direction)` converts time-related parameter fields between ROMS
  format and datetimes/timedeltas.

Additional functions focus on a specific ROMS workflow; this includes a standard
folder setup and file-naming conventions that facilitate robust automation of
simulations.

- `runtodate(ocean,simdir,simname,enddate,...)` sets up I/O and runs ROMS
  simulation through indicated date, with options to restart and work past
  blowups
- `simfolders(simdir)` generates folder path names for, and optionally creates,
  the 3 I/O folders used by runtodate
- `setoutfilenames(ocean,base,...)` resets the values of output file name
  parameters in a ROMS parameter dictionary to use a systematic naming scheme
"""

import copy
import csv
import glob
import math
import os
import subprocess
from datetime import datetime, timedelta
import warnings

import netCDF4 as nc

import romscom.rcutils as r


def readparamfile(filename, tconvert=False):
    """
    Reads parameter YAML file into an ordered dictionary

    Args:
        filename (string): name of parameter file
        tconvert (logical, optional): True to convert time-related fields to 
            datetimes and timedeltas, False (default) to keep in native ROMS 
            format.

    Returns:
        (OrderedDict): ROMS parameter dictionary
    """

    with open(filename, 'r') as f:
        d = r.ordered_load(f)

    if tconvert:
        converttimes(d, "time")

    return d

def stringifyvalues(d, compress=False):
    """
    Formats all dictionary values to ROMS standard input syntax

    This function converts values to the Fortran-ish syntax used in ROMS
    standard input files.  Floats are converted to the double-precision format
    of Fortran read/write statements, booleans are converted to T/F, integers
    are converted straight to strings, and lists are converted to space-
    delimited strings of the above (compressed using * for repeated values where
    applicable).  Values corresponding to a few special KEYWORDS (e.g., the
    'POS' station table, multi-file parameters, 'LBC' boundary conditions)
    receive the appropriate formatting

    Args:
        d (dict): ROMS parameter dictionary compress (logical, optional): True
            to compress repeated values (e.g., T T T -> 3*T), False (default) to
            leave as is.

    Returns:
        (dict): deep copy of d with all values replaced by ROMS-formatted
            strings
    """

    if compress:
        consecstep = 0
    else:
        consecstep=-99999

    newdict = copy.deepcopy(d)

    for x in newdict:

        # Start by checking for special cases

        if x == "no_plural":
            pass
        elif x == 'POS':
            # Stations table
            tmp = newdict[x]
            for idx in range(0,len(tmp)):
                if tmp[idx][1] == 1: # lat/lon pairs
                    tmp[idx] = '{:17s}{:4d} {:4d} {:12f} {:12f}'.format('', *tmp[idx])
                elif tmp[idx][1] == 0: # I/J pairs
                    tmp[idx] = '{:17s}{:4d} {:4d} {:12d} {:12d}'.format('', *tmp[idx])

            tablestr = '{:14s}{:4s} {:4s} {:12s} {:12s} {:12s}'.format('', 'GRID','FLAG', 'X-POS', 'Y-POS', 'COMMENT')
            tmp.insert(0, tablestr)

            newdict[x] = '\n'.join(tmp)

        elif x in ['BRYNAME', 'CLMNAME', 'FRCNAME']:
            # Multi-file entries (Single file strings are not modified)
            if isinstance(newdict[x], list):
                newdict[x] = r.multifile2str(newdict[x])

        elif x.endswith('LBC'):
            # LBC values are grouped 4 per line
            for k in newdict[x]:
                if len(newdict[x][k]) > 4:
                    nline = len(newdict[x][k])//4
                    line = []
                    for ii in range(0,nline):
                        s = ii*4
                        e = ii*4 + 4
                        line.append(' '.join(newdict[x][k][s:e]))
                    delim = f" \\\n"
                    newdict[x][k] = delim.join(line)
                else:
                    newdict[x][k] = ' '.join(newdict[x][k])
        elif x in ['fsh_age_offset', 'fsh_q_G', 'fsh_q_Gz', 'fsh_alpha_G', 
                   'fsh_alpha_Gz', 'fsh_beta_G', 'fsh_beta_Gz', 'fsh_catch_sel', 
                    'fsh_catch_01', 'fsh_catch_99']:
            # FEAST parses arrays via repeated keywords
            tmp = newdict[x]
            for ii in range(0,len(tmp)):
                tmp[ii] = r.list2str(tmp[ii], consecstep=-99999)
                if ii > 0:
                    tmp[ii] = f"{x} == {tmp[ii]}"
            newdict[x] = '\n'.join(tmp)
        else:
            if isinstance(newdict[x], float):
                newdict[x] = r.float2str(newdict[x])
            elif isinstance(newdict[x], bool):
                newdict[x] = r.bool2str(newdict[x])
            elif isinstance(newdict[x], int):
                newdict[x] = '{}'.format(newdict[x])
            elif isinstance(newdict[x], list):
                tmp = newdict[x]
                if isinstance(tmp[0], list):
                    newdict[x] = [r.list2str(i, consecstep=consecstep) for i in tmp]
                else:
                    newdict[x] = r.list2str(tmp, consecstep=consecstep)
            elif isinstance(newdict[x], dict):
                    newdict[x] = stringifyvalues(newdict[x], compress=compress)

    return newdict

def dict2standardin(d, compress=False, file=None):
    """
    Converts a parameter dictionary to standard input text, and optionally
    writes to file

    Args:
        d (dict): parameter dictionary compress (logical, optional): True to
            compress repreated values (e.g., T T T -> 3*T), False (default) to
            leave as is.
        file (string or None): name of output file.  If None (default), text is 
            returned; otherwise, text will be printed to file indicated

    Returns:
        (string): standard input text (only if output file not provided)

    """
    if 'DT' in d:
        istime = r.fieldsaretime(d)
    else:
        istime = False
    if istime:
        converttimes(d, "ROMS")
    dstr = stringifyvalues(d, compress)
    no_plural = dstr.pop('no_plural')
    txt = []
    for ky in dstr:
        if isinstance(dstr[ky], list):
            for i in dstr[ky]:
                txt.append(r.formatkeyvalue(ky, i, no_plural))
        elif isinstance(dstr[ky], dict):
            for i in dstr[ky]:
                newkey = '{}({})'.format(ky,i)
                txt.append(r.formatkeyvalue(newkey, dstr[ky][i], no_plural))
        else:
            txt.append(r.formatkeyvalue(ky, dstr[ky], no_plural))

    delim =  ''
    txt = delim.join(txt)

    if istime:
        converttimes(d, "time")

    if file is None:
        return txt
    else:
        with open(file, 'w') as f:
            f.write(txt)

def runtodate(ocean, simdir, simname, enddate, dtslow=None, addcounter="most",
               compress=False, romscmd=["mpirun","romsM"], dryrunflag=True,
               permissions=0o755, count=1, runpastblowup=True):
    """
    Sets up I/O and runs ROMS simulation through indicated date
               
    This function provides a wrapper to set up a ROMS simulation and run through
    the desired date, allowing for robust restarts when necessary. It organizes
    ROMS I/O under a 3-folder system (under the user-specified simdir folder): 
    
    - <simdir>/In: holds all stardard input (.in) files for the simulation
    - <simdir>/Log: holds standard output and standard error files (redirected
        to file from the call to ROMS) as well as step-size tracking to support
        this function's runpastblowup option
    - <simdir>/Out: holds all netCDF output files from the ROMS simulation

    Before calling the ROMS executable, this function looks for an
    appropriately-named restart file under the <simdir>/Out subfolder. If found,
    it uses this restart file to initialize a run with NRREC=-1; otherwise, it
    will use the user-provided ININAME and NRREC values. It also adjusts the
    NTIMES field to reach the requested end date.
               
    This procedure allows a simulation to be restarted using the same call to
    runtodate regardless of whether it has been partially completed or not; this
    can be useful when running simulations on computer clusters where jobs may
    be cancelled and resubmitted for various queue management reasons, or to
    extend existing simulations with new forcing.
               
    This function also provides the option to work through ROMS blowups. These
    occur when physical conditions lead to numeric instabilities. Blowups can
    sometimes be mitigated by reducing the model time step. When the
    runpastblowup option is True and runtodate encounters a blowup, it will
    adjust the DT parameter to the user-provided slow time step, restart the
    simulation from the last history file, and run for 30 days.  It will then
    return to the original time step and resume. Note that this time step
    reduction will only be attempted once; if the model still blows up, the
    simulation will exit and the user will need to troubleshoot the situation.
               
    Each time the model is restarted, output file counters are incremented as
    specified by the addcounter option.  This preserves output that would
    otherwise be overwritten on restart with the same simulation name.  By
    default, the counter is only added to file types that modern ROMS does not
    check for on restart.

    Args:
        ocean (dict): ROMS parameter dictionary for standard input simdir
        (string): folder where I/O subfolders are found/created simname
        (string): base name for simulation, used as prefix for 
            auto-generated input, standard output and error files, and .nc
            output.
        enddate (datetime):    datetime, simulation end date dtslow (timedelta,
        optional): length of time step used during 
            slow-stepping (blowup) periods. If None (default), this will be set
            to half the primary (i.e., ocean['DT']) time step
        addcounter (string or list of strings, optional): list of output 
            filename prefixes corresponding to those where a counter index
            should be added to the name, or one of the following special strings

            - 'all': add counter to all output types
            - 'most': add counter only to output types that do not have
                    the option of being broken into smaller files on output
                    (i.e. those that do not have an NDEFXXX option)
            - 'none': do not add counter to any (default)
        compress (logical, optional): True to compress repreated values (e.g., 
            T T T -> 3*T), False (default) to leave as is.
        romscmd (list of strings, optional): components of command used to call 
            the ROMS executable (see subprocess.run).  Default is
            ["mpirun","romsM"], which would be  appropriate to call a
            compiled-for-parallel ROMS executable via MPI.
        dryrunflag (logical, optional): True to perform a dry run, where I/O is 
            prepped but the ROMS executable is not called, False to call ROMS.
            Defaults to True
        permissions (octal, optional): folder permissions applied to I/O 
            subfolders if they don't already exist (see os.chmod). Default is
            0o755
        count (int, optional): Starting index for file counter. runpastblowup
        (logical,optional): True to attempt time step reduction if the
            model blows up, false otherwise
               
    Returns:     
        (string): indicator of ROMS simulation results, will be one of:

            - 'dryrun': dryrunflag was True, no simulation was attempted
            - 'blowup': simulation blew up (either with runpastblowup off, or 
               reduction of time step did not mitigate blowup)
            - 'error': simulation encountered an error other than a blowup
            - 'success': simulation completed successfully
    """

    # Get some stuff from dictionary, before we make changes

    converttimes(ocean, "time") # make sure we're in datetime/timedelta mode
    inifile = ocean['ININAME']
    dt = ocean['DT']
    drst = ocean['NRST']
    nrrec = ocean['NRREC']
    if dtslow is None:
        dtslow = dt/2

    # Set up input, output, and log folders

    fol = simfolders(simdir, create=True, permissions=permissions)

    # Initialization file: check for any existing restart files, and if not
    # found, start from the initialization file

    rstinfo = r.parserst(os.path.join(fol['out'], simname))
    if rstinfo['lastfile']:
        cnt = rstinfo['count']
        ocean['ININAME'] = rstinfo['lastfile']
        ocean['NRREC'] = -1
    else:
        cnt = count
        ocean['ININAME'] = inifile
        ocean['NRREC'] = nrrec

    # Check that all input files exist (better to do this here than let ROMS try and fail)

    flag = r.inputfilesexist(ocean)
    if not flag:
        Exception("Input file missing, exiting")
    
    # Get starting time from initialization file
    # TODO: Eventually would like to support other ROMS-supported calendar 
    # options (e.g., 360_day) but it would require tracking the TIME_REF flags 
    # after converting to datetime
    # TODO: Would also like to add some checks to ensure files that include 
    # calendar info and/or reference dates in their time attributes are properly
    # synced with the TIME_REF parameter

    f = nc.Dataset(ocean['ININAME'], 'r')
    tunit = f.variables['ocean_time'].units

    if "day" in tunit:
        tunit = "days"
    elif "second" in tunit:
        tunit = "seconds"
    else:
        warnings.warn("Your initialization time unit will be interpreted by ROMS as seconds")
        tunit = "seconds"
    tunit = f"{tunit} since {ocean['TIME_REF'].strftime("%Y-%m-%d %H:%M:%S")}"        
    tini = max(nc.num2date(f.variables['ocean_time'][:], units=tunit, calendar='proleptic_gregorian'))

    # Create log file to document slow-stepping time periods

    steplog = os.path.join(fol['log'], f"{simname}_step.txt")

    if not os.path.isfile(steplog):
        fstep = open(steplog, "w+")
        fstep.close()

    # Run sim

    while tini < (enddate - drst):

        # Set end date as furthest point we can run.  This will be either
        # the simulation end date  or the end of the slow-stepping period (if we
        # are in one), whichever comes first

        # Check if in slow-stepping period

        endslow = enddate
        ocean['DT'] = dt
        with open(steplog) as fstep:
            readCSV = csv.reader(fstep, delimiter=',')
            for row in readCSV:
                t1 = datetime.strptime(row[0], '%Y-%m-%d-%H-%M:%S')
                t2 = datetime.strptime(row[1], '%Y-%m-%d-%H-%M:%S')
                if (tini >= t1) & (tini <= (t2-drst)): # in a slow-step period
                    endslow = t2
                    ocean['DT'] = dtslow

        tend = min(enddate, endslow)
        # ocean['NTIMES'] = tend - ocean['DSTART']
        ocean['NTIMES'] = tend - tini

        # Set names for output files

        setoutfilenames(ocean, os.path.join(fol['out'], simname), cnt, addcounter=addcounter)

        # Names for standard input, output, and error

        standinfile  = os.path.join(fol['in'],  f"{simname}_{cnt:02d}_ocean.in")
        standoutfile = os.path.join(fol['log'], f"{simname}_{cnt:02d}_log.txt")
        standerrfile = os.path.join(fol['log'], f"{simname}_{cnt:02d}_err.txt")

        # Export parameters to standard input file

        converttimes(ocean, "ROMS")
        dict2standardin(ocean, compress=compress, file=standinfile)
        converttimes(ocean, "time")

        # Print summary

        cmdstr = ' '.join(romscmd)

        print("Running ROMS simulation")
        print(f"  Counter block:   {cnt}")
        print(f"  Start date:      {tini.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  End date:        {tend.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  ROMS command:    {cmdstr}")
        print(f"  Standard input:  {standinfile}")
        print(f"  Standard output: {standoutfile}")
        print(f"  Standard error:  {standerrfile}")

        if dryrunflag:
            print("Dry run")
            return 'dryrun'
        else:
            with open(standoutfile, 'w') as fout, open(standerrfile, 'w') as ferr:
                subprocess.run(romscmd+[standinfile], stdout=fout, stderr=ferr)

        rsim = r.parseromslog(standoutfile)

        # Did the run crash (i.e. anything but successful end or blowup)? If
        # so, we'll exit now

        if (not rsim['cleanrun']) & (not rsim['blowup']):
            print('  Simulation block terminated with error')
            return 'error'

        # Did it blow up?  If it did so during a slow-step period, we'll exit
        # now.  If it blew up during a fast-step period, set up a new
        # slow-step period and reset input to start with last history file.
        # If it ran to completion, reset input to start with last restart
        # file

        rstinfo = r.parserst(os.path.join(fol['out'], simname))
        cnt = rstinfo['count']

        if rsim['blowup']:
            if not runpastblowup:
                print('  Simulation block blew up')
                return 'blowup'
                
            if ocean['DT'] == dtslow:
                print('  Simulation block blew up in a slow-step period')
                return 'blowup'

            # Find the most recent history file written to
            hisfile = rsim['lasthis']

            if not hisfile: # non-clean blowup, no his file defined
                allhis = sorted(glob.glob(os.path.join(fol['out'], simname + "*his*.nc")))
                hisfile = allhis[-1]

            fhis = nc.Dataset(hisfile)
            if len(fhis.variables['ocean_time']) == 0:
                allhis = glob.glob(os.path.join(fol['out'], simname + "*his*.nc"))
                allhis = sorted(list(set(allhis) - set([hisfile])))
                hisfile = allhis[-1]

            ocean['ININAME'] = hisfile
            ocean['NRREC'] = -1

            f = nc.Dataset(ocean['ININAME'], 'r')
            tunit = f.variables['ocean_time'].units
            tcal = f.variables['ocean_time'].calendar
            tini = max(nc.num2date(f.variables['ocean_time'][:], units=tunit, calendar=tcal))

            t1 = tini.strftime('%Y-%m-%d-%H-%M:%S')
            t2 = (tini + timedelta(days=30)).strftime('%Y-%m-%d-%H-%M:%S')
            fstep = open(steplog, "a+")
            fstep.write('{},{}\n'.format(t1,t2))
            fstep.close()

        else:
            ocean['ININAME'] = rstinfo['lastfile']
            ocean['NRREC'] = -1

            f = nc.Dataset(ocean['ININAME'], 'r')
            tunit = f.variables['ocean_time'].units
            tcal = f.variables['ocean_time'].calendar
            tini = max(nc.num2date(f.variables['ocean_time'][:], units=tunit, calendar=tcal))

    # Print completion status message

    print('Simulation completed through specified end date')
    return 'success'

def simfolders(simdir, create=False, permissions=0o755):
    """
    Generate path names for, and if requested, create folders for the the 3 I/O
    folders used by runtodate (<simdir>/In, <simdir>/Log, and <simdir>/Out).  

    Args:
        simdir (string): path to location where folders will be located. 
        create (logical, optional): True to create the folders if they do not 
            exist.  Defaults to False
        permissions (octal, optional): folder permissions applied to I/O 
            subfolders if they don't already exist (see os.chmod). Default is
            0o755
    
    Returns:
        (dict): with the following fields:

            Key        |Value type|Value description
            -----------|----------|-----------------
            `out`      |`string`  | path to folder where ROMS netCDF output will be placed
            `in`       |`string`  | path to folder for romscom-generated ROMS text input files
            `log`      |`string`  | path to folder for standard error and standard output files
    """

    outdir = os.path.join(simdir, "Out")
    indir  = os.path.join(simdir, "In")
    logdir = os.path.join(simdir, "Log")

    if create:
        if not os.path.exists(indir):
            os.makedirs(indir, permissions)
            os.chmod(indir, permissions)
        if not os.path.exists(outdir):
            os.makedirs(outdir, permissions)
            os.chmod(outdir, permissions)
        if not os.path.exists(logdir):
            os.makedirs(logdir, permissions)
            os.chmod(logdir, permissions)

    return {"out": outdir, "in": indir, "log": logdir}

def setoutfilenames(ocean, base, cnt=1, outtype="all", addcounter="none"):
    """
    Resets the values of output file name parameters in a ROMS parameter dictionary

    This function systematically resets the output file name values using the
    pattern `{base}_{prefix}.nc`, where prefix is a lowercase version of the 3- or
    4-letter prefix of the various XXXNAME parameters, e.g. `ocean['AVGNAME'] = 'base_avg.nc'`.
    Where specified, a 2-digit counter may also be added, e.g. `ocean['STANAME'] = 'base_01_sta.nc'`.
    Note that these extra counters apply an additional increment beyond those that ROMS
    itself applies to any file type with an NDEFXXX option; for example, history files are
    typically incremented internally, so `ocean['HISNAME'] = 'base_his.nc'` with `ocean['NDEFHIS'] > 0` 
    and `addcounter="none"` will still produce files named `<simdir>/Out/base_his_00001.nc`, 
    `<simdir>/Out/base_his_00002.nc`, etc.  

    Args:
        ocean (dict): parameter dictionary
        base (string): base name for output files (including path when 
            applicable)
        cnt (int): counter to be added to filenames, if requested.  Default = 1
        outtype (string or list of strings, optional): list of output filename 
            prefixes corresponding to those to be modified (e.g., 
            ['AVG', 'HIS']), or one of the following special strings:
            all:    modify all output types (default)
        addcounter (string or list of strings, optional): list of output 
            filename prefixes corresponding to those where a counter index 
            should be added to the name, or one of the following special strings:

            - all: add counter to all output types, equal to 
                   ['DAI', 'GST', 'RST', 'HIS', 'QCK', 'TLF', 'TLM', 'ADJ', 'AVG',
                    'HAR', 'DIA', 'STA', 'FLT', 'AVG2']
            - most: add counter only to output types that do not have
                    the option of being broken into smaller files on
                    output (i.e. those that do not have an NDEFXXX
                    option).  Includes all those listed in 'all' *except*
                    ['AVG', 'AVG2', 'HIS', 'DIA', 'TLM', 'ADJ']
            - none: do not add counter to any (default)
    """

    outopt = ['DAI', 'GST', 'RST', 'HIS', 'QCK', 'TLF', 'TLM', 'ADJ', 'AVG',
                'HAR', 'DIA', 'STA', 'FLT', 'AVG2']

    if isinstance(outtype, str):
        if outtype == "all":
            outtype = outopt

    if isinstance(addcounter, str):
        if addcounter == "none":
            addcounter = []
        elif addcounter == "most":
            default_nocount = ['AVG', 'AVG2', 'HIS', 'DIA', 'TLM', 'ADJ']
            addcounter = [x for x in outtype if x not in default_nocount]
        elif addcounter == "all":
            addcounter = outtype

    for fl in outtype:
        if fl in addcounter:
            ocean[fl+'NAME'] = f"{base}_{cnt:02d}_{fl.lower()}.nc"
        else:
            ocean[fl+'NAME'] = f"{base}_{fl.lower()}.nc"

def converttimes(d, direction):
    """
    Converts time-related parameter fields between ROMS format and
    datetimes/timedeltas.  The conversions apply to the following keys in
    the input dictionary d:

    |Key      | 'ROMS' format                      |'time' format
    |---------|------------------------------------|------------------------------
    |DSTART   | float, days since initialization   |datetime, starting date+time
    |TIME_REF | float, reference time (yyyymmdd.f) |datetime, reference date+time
    |NTIMES*  | integer, number of time steps in simulation |timedelta, duration of simulation
    |N###     | integer, number of time steps      |timedelta, length of time
    |NDEF###  | integer, number of time steps      |timedelta, length of time
    |DT:      | integer, number of seconds         |timedelta, length of time

    Args:
        d (dict): ROMS parameter dictionary
        direction (string): 'ROMS' to convert to ROMS standard input units or 'time' to 
            convert to datetime/timedelta values
    """

    timeflds = r.timefieldlist(d)
    istime = r.fieldsaretime(d)

    if not istime and direction == "time":
        # Convert from ROMS standard input units to datetimes and timedeltas

        if d['TIME_REF'] in [-1, 0]:
            Exception("360-day and 365.25-day calendars not compatible with this function")
        elif d['TIME_REF'] == -2:
            d['TIME_REF'] = datetime(1968,5,23)
        else:
            yr = math.floor(d['TIME_REF']/10000)
            mn = math.floor((d['TIME_REF']-yr*10000)/100)
            dy = math.floor(d['TIME_REF'] - yr*10000 - mn*100)
            dyfrac = d['TIME_REF'] - yr*10000 - mn*100 - dy
            hr = dyfrac * 24
            mnt = (dyfrac-math.floor(hr)/24)*60
            hr = math.floor(hr)
            sc = math.floor((mnt - math.floor(mnt)/60)*60) # Note: assuming no fractional seconds
            mnt = math.floor(mnt)

            d['TIME_REF'] = datetime(yr,mn,dy,hr,mnt,sc)

        d['DT'] = timedelta(seconds=d['DT'])

        d['DSTART'] = d['TIME_REF'] + timedelta(days=d['DSTART'])

        for fld in timeflds:
            d[fld] = d['DT']*d[fld]

    elif istime and direction == "ROMS":
        # Convert from datetimes and timedeltas to ROMS standard input units
        dfrac = (d['TIME_REF'] - datetime(d['TIME_REF'].year, d['TIME_REF'].month, d['TIME_REF'].day)).total_seconds()/86400.0
        datefloat = float('{year}{month:02d}{day:02d}'.format(year=d['TIME_REF'].year, month=d['TIME_REF'].month, day=d['TIME_REF'].day))

        d['DSTART'] = (d['DSTART'] - d['TIME_REF']).total_seconds()/86400.0

        d['TIME_REF'] = datefloat + dfrac

        for fld in timeflds:
            d[fld] = int(d[fld].total_seconds()/d['DT'].total_seconds())

        d['DT'] = d['DT'].total_seconds()


