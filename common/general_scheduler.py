from common.executions.SchedulerExecutor import SchedulerExecutor


def schedule(period, task):
    return SchedulerExecutor(period, task)
