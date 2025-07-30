import pytest
from click.testing import CliRunner

from shephex.cli.slurm.open import open_slurm

# 1. 'sacct', '-j', job_id, '--format', 'state, JobName', '--noheader'
# 2. "scontrol", "show", "job", job_id
# 3. 'sacct', '-j', job_id, '--format', 'workdir%-1000', '--noheader'
# 4. 'sacct', '-B', '-j', job_id


output1=b"""RUNNING submit_1.+ 
   RUNNING      batch 
   RUNNING     extern
"""

output2=b"""
JobId=19834435 ArrayJobId=19834435 ArrayTaskId=0 ArrayTaskThrottle=1 JobName=submit_1.sh
   UserId=XXX(1172) GroupId=XXX(512) MCS_label=N/A
   Priority=26687 Nice=0 Account=XXX QOS=normal
   JobState=RUNNING Reason=None Dependency=(null)
   Requeue=1 Restarts=0 BatchFlag=1 Reboot=0 ExitCode=0:0
   RunTime=00:04:39 TimeLimit=1-00:00:00 TimeMin=N/A
   SubmitTime=2025-02-27T21:25:16 EligibleTime=2025-02-27T21:25:20
   AccrueTime=2025-02-27T21:25:16
   StartTime=2025-02-27T21:25:20 EndTime=2025-02-28T21:25:20 Deadline=N/A
   SuspendTime=None SecsPreSuspend=0 LastSchedEval=2025-02-27T21:25:20 Scheduler=Main
   Partition=q48 AllocNode:Sid=s41n24.grendel.cscaa.dk:586257
   ReqNodeList=(null) ExcNodeList=s41n01,s41n0[2-3]
   NodeList=s41n13
   BatchHost=s41n13
   NumNodes=1 NumCPUs=1 NumTasks=1 CPUs/Task=1 ReqB:S:C:T=0:0:*:*
   ReqTRES=cpu=1,mem=6G,node=1,billing=1
   AllocTRES=cpu=1,mem=6G,node=1,billing=1
   Socks/Node=* NtasksPerN:B:S:C=0:0:*:* CoreSpec=*
   MinCPUsNode=1 MinMemoryCPU=6G MinTmpDiskNode=0
   Features=(null) DelayBoot=00:00:00
   OverSubscribe=OK Contiguous=0 Licenses=(null) Network=(null)
   Command=submit_1.sh
   WorkDir=slurm
   StdErr=slurm-12345_0.out
   StdIn=/dev/null
   StdOut=slurm-12345_0.out
   TresPerTask=cpu=1
"""

output3=b"""slurm
"""

output4=b"""#!/bin/sh
#SBATCH --partition=q48,q40,q36
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=6G
#SBATCH --time=24:00:00
#SBATCH --array=0-0%1

directories=(
        /mnt/lustre/grnfs0/users/machri/projects/shephex/examples/slurm_profiles/shephex/G7YccTHWfiaiMbbc5jdnxj-exp
)
identifiers=(
        G7YccTHWfiaiMbbc5jdnxj
)
ulimit -Su 8000
hex slurm add-info -d ${directories[$SLURM_ARRAY_TASK_ID]} -j "${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}"
hex execute ${directories[$SLURM_ARRAY_TASK_ID]}"""

def test_cli_slurm_open(mocker) -> None:
    output_list = [output1, output2, output3, output4]
    mocker.patch('subprocess.check_output', side_effect=lambda *args, **kwargs: output_list.pop(0))
    runner = CliRunner()
    result = runner.invoke(open_slurm, ['12345', '-p'])
    assert result.exit_code == 0
    assert 'slurm-12345_0.out' in result.output

def test_cli_slurm_open2(mocker) -> None:
    output_list = [output1, output2, output3, output4]
    mocker.patch('subprocess.check_output', side_effect=lambda *args, **kwargs: output_list.pop(0))
    mocker.patch('subprocess.call', 0)
    runner = CliRunner()
    result = runner.invoke(open_slurm, ['12345', '-p'])
    assert result.exit_code == 0


def test_cli_slurm_open_help() -> None:
    runner = CliRunner()
    result = runner.invoke(open_slurm, ['--help'])
    assert result.exit_code == 0


