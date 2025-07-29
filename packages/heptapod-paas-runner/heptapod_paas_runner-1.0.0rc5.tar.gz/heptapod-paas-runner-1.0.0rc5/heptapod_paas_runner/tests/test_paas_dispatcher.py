# Copyright 2021-2023 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-3.0-or-later
import json
from overrides import overrides
import signal
import threading
import time

import pytest

from ..testing import RunnerForTests
from ..exceptions import (
    GitLabUnavailableError,
    GitLabUnexpectedError,
    JobLaunchTimeout,
    PaasProvisioningError,
    PaasResourceError,
)
from .. job import JobHandle
from ..paas_resource import PaasResource
from ..paas_dispatcher import (
    JobEventType,
    PaasDispatcher,
    main as dispatcher_main,
)
from ..testing import FlavorForTests

parametrize = pytest.mark.parametrize


class ApplicationForTests(PaasResource):
    """Mock application object, just storing details for assertions.
    """

    def __init__(self, runner_name, job_id, paas_secret,
                 service_based=False,
                 testing_behaviour=None,
                 standby_seconds_once_finished=0,
                 weight=1):
        self.runner_name = runner_name
        self.job_id = job_id
        self.app_id = 'app_%s_%d' % (runner_name, job_id)
        self.paas_secret = paas_secret
        self.weight = weight
        self.launched = False
        self.service_based = service_based
        self.testing_behaviour = testing_behaviour
        self.standby_seconds_once_finished = standby_seconds_once_finished

    def __eq__(self, other):
        self_dict = self.__dict__
        other_dict = other.__dict__
        del self_dict['testing_behaviour']
        other_dict.pop('testing_behaviour', None)

        return self_dict == other_dict

    def __hash__(self):
        return hash(self.app_id)

    def dump(self):
        return dict(runner_name=self.runner_name,
                    weight=self.weight,
                    job_id=self.job_id)

    def log_fmt(self):
        return repr(self)

    def wait_can_take_job(self, interruptible_sleep):
        beh = self.testing_behaviour['can_take_job']
        if beh == 'ok':
            return True
        if beh == 'interrupted':
            return False
        if beh == 'exception':
            raise RuntimeError("unexpected!")
        raise JobLaunchTimeout(98765)

    def launch(self, job_data):
        if not self.testing_behaviour['launch_ok']:
            raise PaasResourceError(self.app_id, 'executor',
                                    action='launch',
                                    code=123,
                                    transport_code=500,
                                    error_details="Launch failed")
        self.launched = True

    def finished_standby_seconds(self):
        return self.standby_seconds_once_finished


class Runner(RunnerForTests):

    executor = 'paas-test-docker'

    paas_secret = None
    """Model for an additional secret used with the PAAS API."""

    weighted = False
    """If True, job weight is set in place."""

    weight_requestable = False
    """If True, the runner is able to request jobs with a maximum weight."""

    request_job_errors = ()
    """If not empty, any request for jobs raises the first popped error."""

    service_based = False
    """If True, generate service based resources."""

    resource_standby_once_finished = 0

    def __init__(self, config):
        super(Runner, self).__init__(config)
        self.acquirable_jobs = []
        self.acquired_jobs = {}
        self.launched_jobs_resources = []
        self.progress_errors = {}  # used to trigger errors in job progress
        self.coord_reported_failed = []
        self.failing_decommissions = []
        self.successful_decommissions = []
        self.job_requests_count = 0
        self.job_traces = {}
        self.available_flavors = {'L': FlavorForTests(weight=4),
                                  'M': FlavorForTests(weight=2),
                                  }
        self.request_job_errors = []
        self.launch_times = {}

    def request_job(self, max_weight=None):
        self.job_requests_count += 1
        try:
            err = self.request_job_errors.pop()
        except IndexError:
            pass
        else:
            raise err

        if not self.acquirable_jobs:
            return None

        if max_weight is None or not self.weighted:
            job = self.acquirable_jobs[0]
        else:
            for job in self.acquirable_jobs:
                if job['weight'] <= max_weight:
                    break
            else:
                return None

        self.acquirable_jobs.remove(job)
        job_id = job['id']
        job.setdefault('job_info', {}).setdefault('project_id', 1049)
        job['status'] = 'acquired'
        self.acquired_jobs[job_id] = job
        return json.dumps(job)

    def expected_weight(self, job):
        if self.weighted:
            return job['weight']
        else:
            # covers default impl for Runners without weight handling
            return super(Runner, self).expected_weight(job)

    def provision(self, job):
        job_id = job['id']
        acquired = self.acquired_jobs[job_id]
        success = acquired['provision_ok']
        standby = self.resource_standby_once_finished
        if success:
            return ApplicationForTests(self.unique_name, job_id,
                                       self.paas_secret,
                                       weight=job.get('weight', 1),
                                       service_based=self.service_based,
                                       testing_behaviour=acquired,
                                       standby_seconds_once_finished=standby,
                                       )

        else:
            raise PaasProvisioningError(executor=self.executor,
                                        action='test-provision',
                                        code=321, transport_code=400,
                                        error_details="Read the doc!")

    def launch(self, app, job_data):
        if self.service_based:
            return app.launch(job_data)

        job = self.acquired_jobs[app.job_id]
        print("Launching job %r" % job)
        self.launch_times[app.job_id] = time.time()
        if not job['launch_ok']:
            if job.get('exc_kind') == 'unexpected':
                raise RuntimeError("did not see that coming")
            else:
                raise PaasResourceError(executor=self.executor,
                                        action='test-plaunch',
                                        resource_id='cloud51',
                                        code=196, transport_code=400,
                                        error_details="Famous last words")

        self.launched_jobs_resources.append((app, job_data))
        job['status'] = 'launched'

    def launch_reuse_resource(self, *a, **kw):
        new_jh = super(Runner, self).launch_reuse_resource(*a, **kw)
        if new_jh is not None:
            self.acquired_jobs[new_jh.job_id]['status'] = 'launched-reused'
        return new_jh

    def job_wait_trace(self, project_id, job_handle, interruptible_sleep):
        job_details = self.acquired_jobs[job_handle.job_id]
        print("job_wait_trace for %s, details=%r" % (job_handle, job_details))
        calls = job_details.get('wait_trace_calls', 0) + 1
        job_details['wait_trace_calls'] = calls

        call_nr, response = job_details.get('wait_trace_response',
                                            (1, 'success'))
        if calls >= call_nr:
            if response == 'success':
                return True
            if response == 'timeout':
                raise JobLaunchTimeout(
                    job_handle,
                    job_details.get('wait_trace_timeout_value', 10))

        return False  # interruption

    def is_job_finished(self, job_handle):
        job_id = job_handle.job_id
        error = self.progress_errors.get(job_id)
        if error:
            raise error
        else:
            return self.acquired_jobs[job_id]['status'] == 'finished'

    def job_append_trace(self, job_handle, message):
        self.job_traces.setdefault(job_handle, []).append(message)
        job_handle.trace_offset += len(message)

    def report_coordinator_job_failed(self, job_handle, reason):
        self.coord_reported_failed.append((job_handle, reason))

    def mark_job_finished(self, job_id):
        self.acquired_jobs[job_id]['status'] = 'finished'

    def decommission(self, paas_resource):
        rsc_id = paas_resource.app_id
        if rsc_id in self.failing_decommissions:
            raise PaasResourceError(rsc_id, self.executor,
                                    action='decom', code=1)
        self.successful_decommissions.append(rsc_id)

    @overrides
    def load_paas_resource(self, data):
        return ApplicationForTests(paas_secret=self.paas_secret, **data)


Runner.register()


class WeightedRunner(Runner):
    executor = 'paas-test-weighted'


WeightedRunner.register()


def make_job_handle(runner, job_id, token,
                    expected_weight=1,
                    actual_weight=1,
                    service_based=False,
                    with_resource=True):
    handle = JobHandle(runner.unique_name, job_id, token,
                       expected_weight=expected_weight)
    if with_resource:
        handle.paas_resource = ApplicationForTests(
            runner.unique_name,
            job_id,
            runner.paas_secret,
            weight=actual_weight,
            service_based=service_based,
        )

    return handle


DEFAULT_QUOTA_CONFIG = dict(reference_runner='testrunner',
                            reference_flavor='L',
                            reference_jobs_count=3,
                            )
"""Used when it doesn't matter much.

Tests about the quota would typically force it anyway.
Needs obviously a runner with human-readable name 'testrunner'.
"""


def dispatcher_config(nb_runners=1):
    def numbered(s, i):
        if not i:
            return s
        return s + str(i + 1)

    return dict(
        concurrent=5,
        check_interval=0.01,
        job_progress_poll_interval=0.02,
        quota_computation=DEFAULT_QUOTA_CONFIG,
        runners=[dict(executor=Runner.executor,
                      name=numbered('testrunner', i),
                      url='http://heptapod.test',
                      token=numbered('secret', i))
                 for i in range(nb_runners)]
    )


@pytest.fixture
def paas_dispatcher():
    dispatcher = PaasDispatcher(dispatcher_config())
    dispatcher.start_event_processing_thread()
    yield dispatcher

    dispatcher.shutdown_required = True


@pytest.fixture
def single_runner_dispatcher(paas_dispatcher):
    assert len(paas_dispatcher.runners) == 1
    runner_name, runner = next(iter(paas_dispatcher.runners.items()))
    yield paas_dispatcher, runner, runner_name


@pytest.fixture
def dual_runner_dispatcher():
    dispatcher = PaasDispatcher(dispatcher_config(2))
    dispatcher.start_event_processing_thread()
    yield dispatcher

    dispatcher.shutdown_required = True


def wait_until(condition, timeout=10, tick=0.1, do_assert=False):
    start = time.time()
    while not condition() and time.time() - start < timeout:
        time.sleep(tick)
    if do_assert:
        assert condition()


def test_decommission_bogus(single_runner_dispatcher):
    dispatcher, _, runner_name = single_runner_dispatcher
    handle = JobHandle(runner_name=runner_name, job_id=23, token='jt23')
    # doesn't make sense without a PAAS resource, yet no crash occurs
    dispatcher.decommission(handle)
    # and no event was sent (probability of a blocked put is very low)
    assert dispatcher.reporting_queue.empty()


def test_decommission_full(single_runner_dispatcher):
    dispatcher, runner, runner_name = single_runner_dispatcher
    handle = make_job_handle(runner, 87, token='jt87')
    dispatcher.to_decommission.add(handle)
    dispatcher.decommission(handle)
    wait_until(lambda: not dispatcher.to_decommission, do_assert=True)
    assert runner.successful_decommissions == [handle.paas_resource.app_id]


@parametrize('interrupt', ('in-delay', 'in-pause'))
def test_decommission_interruption(single_runner_dispatcher, interrupt):
    dispatcher, runner, runner_name = single_runner_dispatcher
    runner = dispatcher.runners[runner_name]
    handle = make_job_handle(runner, 87, token='jt87')
    dispatcher.to_decommission.add(handle)
    if interrupt == 'in-delay':
        after_seconds = 10
    else:
        # happens when trying to reuse resources
        dispatcher.decommissions_paused = True
        after_seconds = 0
    dispatcher.interruptible_sleep = lambda _duration: True

    dispatcher.decommission(handle, after_seconds=after_seconds)
    wait_until(lambda: dispatcher.reporting_queue.empty(), do_assert=True)
    assert not runner.successful_decommissions


def test_already_decommissionned(single_runner_dispatcher):
    # if a resource was scheduled to be decommissionned after a delay,
    # allowing for reuse. It is possible that an immediate decommission
    # to free the quota happens before that (if reuse was not possible)
    dispatcher, runner, runner_name = single_runner_dispatcher
    runner = dispatcher.runners[runner_name]
    handle = make_job_handle(runner, 87, token='jt87')
    dispatcher.to_decommission.add(handle)

    dispatcher.schedule_decommission(handle, after_seconds=0.2)
    dispatcher.decommission(handle, after_seconds=0)
    wait_until(lambda: not dispatcher.to_decommission)

    assert runner.successful_decommissions == [handle.paas_resource.app_id]
    # give the (daemon) thread enough time to actually run
    time.sleep(0.2)


def test_one_cycle(single_runner_dispatcher):
    dispatcher, runner, runner_name = single_runner_dispatcher

    runner.acquirable_jobs.extend((
        dict(id=12, token='jobtok12', provision_ok=True, launch_ok=True),
        dict(id=13, token='jobtok13', provision_ok=False),
        dict(id=14, token='jobtok14', provision_ok=True, launch_ok=False),
        dict(id=15, token='jobtok15', provision_ok=True, launch_ok=True),
        dict(id=16, token='jobtok16', provision_ok=True,
             launch_ok=False, exc_kind='unexpected'),
    ))

    dispatcher.poll_all_launch()
    wait_until(lambda: dispatcher.total_job_launches >= 5)
    wait_until(lambda: len(dispatcher.launch_errors) >= 3)

    # reports about launch attempts can arrive in any order
    assert set(jh.full_id for jh in dispatcher.launch_errors) == {
        (runner_name, 13),
        (runner_name, 14),
        (runner_name, 16),
    }
    assert set(jh.full_id for jh in dispatcher.launched_jobs) == {
        (runner_name, 12),
        (runner_name, 15),
    }

    # testing runner has more details about jobs
    launched = runner.launched_jobs_resources
    assert len(launched) == 2
    assert set(job[0] for job in launched) == {
        ApplicationForTests(runner.unique_name, 12, None),
        ApplicationForTests(runner.unique_name, 15, None)
    }

    # cover debug log dumps
    dispatcher.log_state_signal(signal.SIGUSR1, None)


def test_launch_delay(single_runner_dispatcher):
    dispatcher, runner, runner_name = single_runner_dispatcher

    # half a second total should be plenty enough to avoid false success
    # and still bearable in tests latency
    min_time = 0.25
    dispatcher.min_time_between_launches = min_time
    runner.acquirable_jobs.extend((
        dict(id=12, token='jobtok12', provision_ok=True, launch_ok=True),
        dict(id=13, token='jobtok13', provision_ok=True, launch_ok=True),
        dict(id=14, token='jobtok14', provision_ok=True, launch_ok=True),
    )),

    start = time.time()
    dispatcher.poll_all_launch()
    wait_until(lambda: dispatcher.total_job_launches >= 3)

    # reports about launch attempts can arrive in any order
    assert set(jh.full_id for jh in dispatcher.launched_jobs) == {
        (runner_name, 12),
        (runner_name, 13),
        (runner_name, 14),
    }
    # the second and third job got delayed, the third further than the second
    assert time.time() - start >= min_time * 2
    # really making sure that we really scheduled the jobs in a spread way
    for job1, job2 in ((12, 13), (13, 14)):
        time_delta = runner.launch_times[job2] - runner.launch_times[job1]
        # we need a small rounding up, here as the times reported from
        # the launching thread are a bit skewed by its own processing until
        # it calls `runner.launch()`.
        assert time_delta + 0.02 >= min_time


def test_request_job_errors(single_runner_dispatcher):
    dispatcher, runner, runner_name = single_runner_dispatcher

    runner.request_job_errors.extend((
        GitLabUnavailableError(url='http://coord.test',
                               message="connection refused"),
        GitLabUnavailableError(status_code=502,
                               url='http://coord.test',
                               message="connection refused"),
    ))

    # no error is raised
    dispatcher.poll_all_launch()
    dispatcher.poll_all_launch()
    assert not runner.request_job_errors  # consistency check


@parametrize('outcome',
             ('can_take_job:timeout',
              'can_take_job:interrupted',
              'can_take_job:exception',
              'all_ok',
              'launch_error',
              ))
def test_launch_job_service(single_runner_dispatcher, outcome):
    if outcome.startswith('can_take_job:'):
        can_take_job = outcome.split(':')[1]
    else:
        can_take_job = 'ok'
    launch_ok = outcome != 'launch_error'

    dispatcher, runner, runner_name = single_runner_dispatcher
    runner.service_based = True
    jh = make_job_handle(runner, 567, 'job-567', with_resource=False)
    job_data = dict(id=jh.job_id,
                    job_info=dict(project_id=383))
    runner.acquired_jobs[567] = dict(provision_ok=True,
                                     can_take_job=can_take_job,
                                     launch_ok=launch_ok,
                                     )
    dispatcher.launch_job(jh, job_data)
    if can_take_job != 'interrupted':
        wait_until(lambda: dispatcher.total_job_launches >= 1)

    if outcome == 'all_ok':
        assert dispatcher.launched_jobs == {jh}
        resource = jh.paas_resource
        assert resource.service_based
        assert resource.launched
    if can_take_job in ('timeout', 'exception') or not launch_ok:
        assert dispatcher.launch_errors == [jh]


def test_failure_coordinator_report_failure(monkeypatch,
                                            single_runner_dispatcher):
    dispatcher, runner, runner_name = single_runner_dispatcher

    # no need to wait for good in tests
    from .. import paas_dispatcher
    monkeypatch.setattr(paas_dispatcher,
                        'COORDINATOR_REPORT_LAUNCH_FAILURES_RETRY_DELAY',
                        0.1)

    attempts = []

    def report_coordinator(*a, **kw):
        attempts.append((a, kw))
        raise RuntimeError("Failed to report failure to coordinator")

    runner.report_coordinator_job_failed = report_coordinator
    runner.acquirable_jobs.append(
        dict(id=17, token='jobtok17', provision_ok=False))

    dispatcher.poll_all_launch()
    wait_until(lambda: dispatcher.total_job_launches >= 1)

    # all exception were catched, we had the expected amount
    # of attempts at reporting to coordinator.
    assert len(attempts) == 3

    attempts.clear()
    wait_until(lambda: not dispatcher.pending_jobs, do_assert=True)
    wait_until(lambda: not dispatcher.to_decommission, do_assert=True)

    assert dispatcher.decommission_launch_failures
    assert dispatcher.potential_concurrency == 0
    assert dispatcher.potential_weight == 0


def test_launcher_thread_shutdown_between_retries(single_runner_dispatcher):
    dispatcher, runner, _ = single_runner_dispatcher
    attempts = []

    def report_coordinator(*a, **kw):
        attempts.append((a, kw))
        raise RuntimeError("Failed to report failure to coordinator")

    runner.report_coordinator_job_failed = report_coordinator
    runner.acquirable_jobs.append(
        dict(id=18, token='jobtok18', provision_ok=False))

    dispatcher.poll_all_launch()

    # with the standard retry delay, we'll detect the first attempt way
    # before the first actual retry.
    wait_until(lambda: attempts)
    dispatcher.shutdown_signal(signal.SIGTERM, None)
    assert dispatcher.shutdown_required

    # take the opportunity to test shutdown-reentrance
    dispatcher.shutdown()

    assert len(dispatcher.pending_jobs) == 1
    job_handle = list(dispatcher.pending_jobs)[0]
    assert job_handle.job_id == 18

    queue = dispatcher.reporting_queue
    # the queue can be not empty (POLL_CYCLE_FINISHED actually seen to
    # be in there). Asserting that would make the test flaky.
    # This doesn't happen often, so we must exclude the loop from coverage.
    while not queue.empty():  # pragma: no cover
        msg = queue.get()
        assert msg != (job_handle, JobEventType.LAUNCH_FAILED)


def test_timed_out_job_trace_appending_failure(single_runner_dispatcher):
    dispatcher, runner, _ = single_runner_dispatcher
    append_attempts = []

    def job_append_trace(*a, **kw):
        append_attempts.append((a, kw))
        raise RuntimeError("Failed to append to coordinator job trace")

    def job_wait_trace(project_id, job_handle, **kw):
        raise JobLaunchTimeout(job_handle, 1)

    runner.job_append_trace = job_append_trace
    runner.job_wait_trace = job_wait_trace

    pending_jh = make_job_handle(runner, 257, 'pj257',
                                 with_resource=True)
    pending_jh.paas_resource.launched = True
    pending_data = dict(id=pending_jh.job_id,
                        job_info=dict(project_id=383))

    dispatcher.pending_jobs[pending_jh] = pending_data
    dispatcher.potential_concurrency = 1
    dispatcher.potential_weight = pending_jh.paas_resource.weight

    dispatcher.launch_job(pending_jh, pending_data)
    wait_until(lambda: not dispatcher.pending_jobs, do_assert=True)
    wait_until(lambda: not dispatcher.to_decommission, do_assert=True)

    assert dispatcher.potential_concurrency == 0
    assert dispatcher.potential_weight == 0


def test_wait_job_trace_recovery(single_runner_dispatcher):
    dispatcher, runner, _ = single_runner_dispatcher

    def job_wait_trace(project_id, job_handle, **kw):
        raise GitLabUnexpectedError(url='http://heptapod.example',
                                    status_code=415,
                                    params=None,
                                    message="Zombie job")

    runner.job_wait_trace = job_wait_trace

    pending_jh = make_job_handle(runner, 258, 'pj258',
                                 with_resource=True)
    pending_jh.paas_resource.launched = True
    pending_data = dict(id=pending_jh.job_id,
                        job_info=dict(project_id=383))

    dispatcher.pending_jobs[pending_jh] = pending_data
    dispatcher.potential_concurrency = 1
    dispatcher.potential_weight = pending_jh.paas_resource.weight

    dispatcher.launch_job(pending_jh, pending_data)
    wait_until(lambda: not dispatcher.pending_jobs, do_assert=True)
    wait_until(lambda: not dispatcher.to_decommission, do_assert=True)

    assert dispatcher.potential_concurrency == 0
    assert dispatcher.potential_weight == 0


def test_launch_progress_max_pending(single_runner_dispatcher):
    dispatcher, runner, _ = single_runner_dispatcher
    dispatcher.max_pending_jobs = 2

    def pending_jobs():
        return set(jh.job_id for jh in dispatcher.pending_jobs)

    def launch_failures():
        return set(jh.job_id for jh in dispatcher.launch_errors)

    def launched_jobs():
        return set(jh.job_id for jh in dispatcher.launched_jobs)

    def wait_trace_counts():
        return {job_id: details.get('wait_trace_calls', 0)
                for job_id, details in runner.acquired_jobs.items()
                }

    # wait_trace on the first two jobs gives an interruption,
    # which stops the launching thread, as if a general shutdown had
    # been signaled.
    runner.acquirable_jobs.extend((
        dict(id=12, token='jobtok12', provision_ok=True, launch_ok=True,
             wait_trace_response=(2, 'success')),
        dict(id=13, token='jobtok13', provision_ok=True, launch_ok=True,
             wait_trace_response=(2, 'timeout')),
        dict(id=14, token='jobtok14', provision_ok=True, launch_ok=True),
    ))

    dispatcher.poll_all_launch()
    # the test depends on the fact that poll_all_launch() repolls a runner
    # immmediately if it gave a job unless limits are reached.
    wait_until(lambda: len(dispatcher.pending_jobs) >= 2
               and list(wait_trace_counts().values()) == [1, 1])
    assert runner.job_requests_count == 2
    assert pending_jobs() == {12, 13}
    # cover debug log dumps with pending jobs
    dispatcher.log_state_signal(signal.SIGUSR1, None)

    # provisioning has been called for the pending jobs, make sure it
    # won't be called again by adding an assertion in the provisioning method
    provision = runner.provision

    def no_reprovision(job_data):
        assert job_data['id'] not in (12, 13)
        return provision(job_data)

    runner.provision = no_reprovision

    # resuming as if loading state (TODO actually dump/load state?)
    # job 12 will launch successfully,
    # job 13 will have a trace timeout -> launch failure
    dispatcher.start_initial_threads()
    wait_until(lambda: len(pending_jobs()) == 0)
    assert launched_jobs() == {12}
    assert launch_failures() == {13}

    # polling again will launch job 14 successfully
    dispatcher.poll_all_launch()
    wait_until(lambda: len(dispatcher.launched_jobs) >= 2)
    assert launched_jobs() == {12, 14}


def test_jobs_progress_max_concurrency(single_runner_dispatcher):
    dispatcher, runner, _ = single_runner_dispatcher
    dispatcher.max_concurrency = 2

    def launched_jobs():
        return set(jh.job_id for jh in dispatcher.launched_jobs)

    def to_decommission_jobs():
        return set(jh.job_id for jh in dispatcher.to_decommission)

    runner.acquirable_jobs.extend((
        dict(id=12, token='jobtok12', provision_ok=True, launch_ok=True),
        dict(id=13, token='jobtok13', provision_ok=True, launch_ok=True),
        dict(id=14, token='jobtok14', provision_ok=True, launch_ok=True),
    ))
    dispatcher.poll_all_launch()
    # the test depends on the fact that poll_all_launch() repolls a runner
    # immmediately if it gave a job unless max concurrency is reached.
    assert runner.job_requests_count == 2
    wait_until(lambda: dispatcher.total_job_launches >= 2)

    assert launched_jobs() == {12, 13}

    dispatcher.poll_launched_jobs_progress_once()
    assert launched_jobs() == {12, 13}

    runner.mark_job_finished(13)
    dispatcher.poll_launched_jobs_progress_once()
    wait_until(lambda: 13 not in launched_jobs())
    wait_until(lambda: 13 not in to_decommission_jobs())

    dispatcher.poll_all_launch()
    wait_until(lambda: dispatcher.total_job_launches >= 3)
    assert launched_jobs() == {12, 14}

    # covering decommissionning error while we're at it
    runner.failing_decommissions.append(
        ApplicationForTests(runner.unique_name, 12, None).app_id)
    runner.mark_job_finished(12)
    dispatcher.poll_launched_jobs_progress_once()

    wait_until(lambda: len(launched_jobs()) <= 1)
    assert launched_jobs() == {14}


def test_runner_by_human_name(single_runner_dispatcher):
    dispatcher, runner, _ = single_runner_dispatcher
    assert dispatcher.runner_by_human_name('testrunner') is runner

    with pytest.raises(KeyError) as exc_info:
        dispatcher.runner_by_human_name('foo')

    assert exc_info.value.args == ('foo', )


def test_init_max_concurrency(single_runner_dispatcher):
    dispatcher, runner, _ = single_runner_dispatcher
    dispatcher.init_max_concurrency(
        dict(quota_computation=DEFAULT_QUOTA_CONFIG,
             concurrent=25,
             ))
    assert dispatcher.max_concurrency == 25
    assert dispatcher.weighted_quota == 12


@parametrize('weight_requestable', ['requestable', 'non_requestable'])
def test_jobs_weighing(single_runner_dispatcher, weight_requestable):
    dispatcher, runner, _ = single_runner_dispatcher
    runner.weighted = True
    dispatcher.weighted_quota = 100
    dispatcher.max_concurrency = 10000  # infinite

    weight_requestable = runner.weight_requestable = (
        weight_requestable == 'requestable')

    runner.min_requestable_weight = 30 if weight_requestable else 80

    def launched_jobs():
        return set(jh.job_id for jh in dispatcher.launched_jobs)

    def to_decommission_jobs():
        return set(jh.job_id for jh in dispatcher.to_decommission)

    runner.acquirable_jobs.extend((
        dict(id=12, token='jobtok12', provision_ok=True, launch_ok=True,
             weight=50),
        dict(id=13, token='jobtok13', provision_ok=True, launch_ok=True,
             weight=60),
        dict(id=14, token='jobtok14', provision_ok=True, launch_ok=True,
             weight=30),
    ))

    def poll_assert_launched_jobs(expected):
        # the test depends on the fact that poll_all_launch() repolls a runner
        # immmediately if it gave a job unless max concurrency is reached.
        prev_requests = runner.job_requests_count
        prev_launches = dispatcher.total_job_launches
        expected_new = len(expected - launched_jobs())
        expected_total_launches = expected_new + prev_launches

        dispatcher.poll_all_launch()

        assert runner.job_requests_count == expected_new + prev_requests
        wait_until(
            lambda: dispatcher.total_job_launches >= expected_total_launches)

        assert launched_jobs() == expected

    # If the runner is able to request a small job, then it will take
    # job 14, otherwise the weight of job 12 is already too close to the
    # limit to take the risk of obtaining a job since it could weigh as much
    # as 80.
    poll_assert_launched_jobs({12, 14} if weight_requestable else {12})
    dispatcher.poll_launched_jobs_progress_once()

    runner.mark_job_finished(12)
    dispatcher.poll_launched_jobs_progress_once()
    wait_until(lambda: 12 not in launched_jobs())
    wait_until(lambda: 12 not in to_decommission_jobs())

    # In requestable case, 14 is already running, and we can request
    # a weight at most 70, which matches job 13.
    # In the non requestable case, the next to launch is 13, leaving
    # again not enough headroom for the potential weight of 80
    poll_assert_launched_jobs({13, 14} if weight_requestable else {13})

    # Note that in the requestable case, no further request has been
    # issued because we are at weight 90 and the minimal (requestable)
    # job weight is 30. Let's change that and retry.
    if weight_requestable:
        runner.min_requestable_weight = 5
        prev_req_count = runner.job_requests_count
        runner.acquirable_jobs.append(
            dict(id=15, token='jobtok15', provision_ok=True, launch_ok=True,
                 weight=20)
        )

        dispatcher.poll_all_launch()

        # there was a new request, but it found no suitable job
        assert runner.job_requests_count == prev_req_count + 1
        wait_until(lambda: dispatcher.reporting_queue.empty())
        assert 15 not in launched_jobs()


def test_resource_reuse_same_runner(single_runner_dispatcher):
    dispatcher, runner, _ = single_runner_dispatcher
    runner.weighted = True
    runner.service_based = True
    runner.resource_standby_once_finished = 3600  # infinite in unit tests
    dispatcher.weighted_quota = 50
    dispatcher.max_concurrency = 10000  # infinite

    runner.weight_requestable = False
    runner.min_requestable_weight = 15

    def launched_jobs():
        return {jh.job_id: jh for jh in dispatcher.launched_jobs}

    def to_decommission_jobs():
        return set(jh.job_id for jh in dispatcher.to_decommission)

    def poll_assert_launched_jobs(expected):
        # the test depends on the fact that poll_all_launch() repolls a runner
        # immmediately if it gave a job unless max concurrency is reached.
        prev_requests = runner.job_requests_count
        prev_launches = dispatcher.total_job_launches
        expected_new = len(expected - set(launched_jobs()))
        expected_total_launches = expected_new + prev_launches

        dispatcher.poll_all_launch()

        assert runner.job_requests_count == expected_new + prev_requests
        wait_until(
            lambda: dispatcher.total_job_launches >= expected_total_launches)

        assert set(launched_jobs()) == expected

    runner.acquirable_jobs.extend((
        dict(id=12, token='jobtok12', provision_ok=True, launch_ok=True,
             can_take_job='ok',
             weight=20),
        dict(id=13, token='jobtok13', provision_ok=True, launch_ok=True,
             can_take_job='ok',
             weight=30),
        dict(id=14, token='jobtok14', provision_ok=True, launch_ok=True,
             can_take_job='ok',
             weight=20),
        dict(id=15, token='jobtok15', provision_ok=True, launch_ok=True,
             can_take_job='ok',
             weight=28),
        dict(id=16, token='jobtok16', provision_ok=True, launch_ok=True,
             can_take_job='ok',
             weight=40),
    ))

    poll_assert_launched_jobs({12, 13})
    assert dispatcher.potential_weight == 50
    dispatcher.poll_launched_jobs_progress_once()

    # Job 12 is finished, resource is not decommissioned yet and the
    # weight has not changed, yet job 14 can be launched with reuse
    runner.mark_job_finished(12)
    dispatcher.poll_launched_jobs_progress_once()
    wait_until(lambda: 12 not in launched_jobs())
    wait_until(lambda: 12 in to_decommission_jobs(), do_assert=True)
    assert dispatcher.potential_weight == 50
    assert len(runner.standby_job_handles) == 1
    assert runner.standby_weight() == 20
    reusable = runner.standby_job_handles[0].paas_resource

    poll_assert_launched_jobs({13, 14})
    assert launched_jobs()[14].paas_resource == reusable
    wait_until(lambda: not to_decommission_jobs(), do_assert=True)
    assert dispatcher.potential_weight == 50

    # Once resource with weight 30 is available for reuse.
    # Although job 15 is slightly smaller, the resource of job 13
    # is picked to run it
    runner.mark_job_finished(13)
    dispatcher.poll_launched_jobs_progress_once()
    wait_until(lambda: 13 not in launched_jobs())
    assert runner.standby_weight() == 30
    reusable = runner.standby_job_handles[0].paas_resource
    assert reusable.job_id == 13
    poll_assert_launched_jobs({14, 15})
    assert launched_jobs()[15].paas_resource == reusable
    assert dispatcher.potential_weight == 50

    runner.mark_job_finished(14)
    runner.mark_job_finished(15)
    dispatcher.poll_launched_jobs_progress_once()
    wait_until(lambda: not launched_jobs())
    wait_until(lambda: to_decommission_jobs() == {14, 15}, do_assert=True)

    # acquiring job 16 will trigger immediate decommission for
    # the two standby resources
    assert len(runner.standby_job_handles) == 2
    assert runner.standby_weight() == 50
    poll_assert_launched_jobs({16})
    wait_until(lambda: not to_decommission_jobs(), do_assert=True)
    # job 16 is really on a new resource
    assert launched_jobs()[16].paas_resource.app_id == 'app_secret_16'
    assert dispatcher.potential_weight == 40


@parametrize('how', ('actual-reuse', 'decommission'))
def test_resource_reuse_stealing(dual_runner_dispatcher, how):
    dispatcher = dual_runner_dispatcher
    by_decommission = how == 'decommission'
    for runner in dispatcher.runners.values():
        runner.weighted = True
        runner.service_based = True
        runner.resource_standby_once_finished = 3600
        runner.weight_requestable = False
        runner.min_requestable_weight = 15

    dispatcher.weighted_quota = 50
    dispatcher.max_concurrency = 10000  # infinite
    runner1 = dispatcher.runners['secret']
    runner2 = dispatcher.runners['secret2']

    def launched_jobs():
        return {jh.job_id: jh for jh in dispatcher.launched_jobs}

    def to_decommission_jobs():
        return set(jh.job_id for jh in dispatcher.to_decommission)

    def poll_assert_launched_jobs(expected):
        all_expected = {job for (_, jobs) in expected for job in jobs}
        # the test depends on the fact that poll_all_launch() repolls a runner
        # immmediately if it gave a job unless max concurrency is reached.
        prev_launches = dispatcher.total_job_launches
        all_expected_new = len(all_expected - set(launched_jobs()))
        expected_total_launches = all_expected_new + prev_launches

        dispatcher.poll_all_launch()

        wait_until(
            lambda: dispatcher.total_job_launches >= expected_total_launches)

        launched = launched_jobs()
        assert set(launched) == all_expected
        for runner, job_ids in expected:
            for job_id in job_ids:
                assert launched[job_id].runner_name == runner.unique_name

    runner1.acquirable_jobs.extend((
        dict(id=12, token='jobtok12', provision_ok=True, launch_ok=True,
             can_take_job='ok',
             weight=20),
        dict(id=13, token='jobtok13', provision_ok=True, launch_ok=True,
             can_take_job='ok',
             weight=30)
    ))

    poll_assert_launched_jobs(((runner1, {12, 13}), (runner2, {})))
    assert dispatcher.potential_weight == 50
    dispatcher.poll_launched_jobs_progress_once()

    # Job 12 is finished, resource is not decommissioned yet and the
    # weight has not changed, yet job 14 can be launched with reuse
    runner1.mark_job_finished(12)
    dispatcher.poll_launched_jobs_progress_once()
    wait_until(lambda: 12 not in launched_jobs())
    wait_until(lambda: 12 in to_decommission_jobs(), do_assert=True)
    assert dispatcher.potential_weight == 50
    assert len(runner1.standby_job_handles) == 1
    assert runner1.standby_weight() == 20
    reusable = runner1.standby_job_handles[0].paas_resource

    runner2.acquirable_jobs.append(
        dict(id=14, token='jobtok14', provision_ok=True, launch_ok=True,
             can_take_job='ok',
             # 5 is way too small, it should force decommission.
             # In some future this might not be the case: we may introduce
             # the possibility to run several smaller jobs on a single
             # resource.
             weight=5 if by_decommission else 20)
    )
    poll_assert_launched_jobs(((runner1, {13}), (runner2, {14})))
    rsc14 = launched_jobs()[14].paas_resource
    wait_until(lambda: not to_decommission_jobs(), do_assert=True)
    if by_decommission:
        assert rsc14 != reusable
        assert dispatcher.potential_weight == 35
    else:
        assert rsc14 == reusable
        assert dispatcher.potential_weight == 50


def test_jobs_progress_errors(single_runner_dispatcher):
    dispatcher, runner, runner_name = single_runner_dispatcher

    url = 'https://heptapod.test/api/v4/job'
    runner.progress_errors = {
        5: GitLabUnavailableError(message='Rebooting', url=url),
        6: GitLabUnexpectedError(message="I'm a teapot",
                                 status_code=418,
                                 params=None,
                                 url=url,
                                 ),
        7: RuntimeError("Something went baaad"),
        }

    def launched_jobs():
        return set(jh.job_id for jh in dispatcher.launched_jobs)

    runner.acquirable_jobs.extend((
        dict(id=5, token='jobtok5', provision_ok=True, launch_ok=True),
        dict(id=6, token='jobtok6', provision_ok=True, launch_ok=True),
        dict(id=7, token='jobtok7', provision_ok=True, launch_ok=True),
    ))
    dispatcher.poll_all_launch()
    wait_until(lambda: len(launched_jobs()) >= 3, do_assert=True)

    dispatcher.poll_launched_jobs_progress_once()


def test_save_load_state(tmpdir):
    dual_config = dispatcher_config(2)
    dual_config['state_file'] = tmpdir / 'paas-dispatcher.json'

    dispatcher = PaasDispatcher(config=dual_config)
    assert not dispatcher.state_file_path.exists()  # checking test assumption
    dispatcher.load_state()
    assert not dispatcher.launched_jobs

    runner1 = dispatcher.runners['secret']
    runner2 = dispatcher.runners['secret2']
    runner1.paas_secret = 'before-save-load'

    launched_jobs = {
        make_job_handle(runner1, 956, 'job-token-1',
                        expected_weight=5,
                        actual_weight=17),
        # make sure the process does not fail if PAAS resource is missing
        # even though that should not happen for launched jobs!
        make_job_handle(runner2, 957, 'job-token-2',
                        expected_weight=13,
                        with_resource=False),
    }
    # since we don't have a running polling loop, the pending jobs
    # will stay inert.
    pending_job_handle = make_job_handle(runner1, 54, 'pendingtok1',
                                         actual_weight=10)
    pending_jobs = {pending_job_handle: dict(id=54,
                                             job_info=dict(project_id=383),
                                             ),
                    }

    dispatcher.launched_jobs = launched_jobs
    dispatcher.pending_jobs = pending_jobs

    to_decom_job_handle = make_job_handle(runner2, 955, 'prev-token',
                                          actual_weight=7)

    runner2.standby_job_handles.append(to_decom_job_handle)
    dispatcher.to_decommission = [to_decom_job_handle]
    dispatcher.save_state()
    assert dispatcher.state_file_path.exists()

    dispatcher = PaasDispatcher(config=dual_config)
    assert not dispatcher.launched_jobs
    runner1 = dispatcher.runners['secret']
    runner1.paas_secret = 'after-save-load'
    runner2 = dispatcher.runners['secret2']
    assert not runner2.standby_job_handles

    dispatcher.load_state()
    # quick assertion on runner_name and job_id
    assert dispatcher.launched_jobs == launched_jobs

    # job limits (notice how actual weight took precedence over
    # expected weight). The CleverApplications will use the just reloaded
    # flavors instead of serializing the weight.
    assert dispatcher.potential_concurrency == 4
    # there is no point using the original dispatcher's weight as it is 0,
    # as accounting is normally done by the polling and event threads.
    # The pending job is worth its expected weight (1)
    assert dispatcher.potential_weight == 38  # 17 + 13 + 1 + 7

    # details of job handles and PAAS resources
    handles_by_id = {jh.job_id: jh for jh in dispatcher.launched_jobs}
    jh1 = handles_by_id[956]
    rsc1 = jh1.paas_resource
    assert rsc1 is not None
    assert rsc1.paas_secret == 'after-save-load'

    assert handles_by_id[957].paas_resource is None
    # standby resources
    assert {jh.job_id for jh in runner2.standby_job_handles} == {955}
    assert {jh.job_id for jh in dispatcher.to_decommission} == {955}
    # pending jobs
    assert dispatcher.pending_jobs == pending_jobs

    # telling the testing runner that provision/launch should work
    # for the pending job.
    runner1.acquired_jobs[54] = dict(provision_ok=True, launch_ok=True)
    # standby resources
    assert {jh.job_id for jh in runner2.standby_job_handles} == {955}

    dispatcher.start_initial_threads()
    dispatcher.start_event_processing_thread()
    wait_until(lambda: not dispatcher.pending_jobs, do_assert=True)
    assert pending_job_handle in dispatcher.launched_jobs

    wait_until(lambda: not dispatcher.to_decommission, do_assert=True)
    # we keep the expected weight for the handle that does not have resource
    # because the resource might actually exist and would be kept forever
    # The job that was just launched now counts as its actual weight (10)
    assert dispatcher.potential_weight == 40  # 17 + 13 + 10


def test_load_standby_resources_corner_cases(tmpdir):
    state_path = tmpdir / 'paas-dispatcher.json'
    config = dict(
        state_file=str(state_path),
        quota_computation=DEFAULT_QUOTA_CONFIG,
        runners=[dict(executor=Runner.executor,
                      name='testrunner',
                      url='http://heptapod1.test',
                      token='secret1'),
                 ])
    dispatcher = PaasDispatcher(config=config)
    assert not dispatcher.state_file_path.exists()  # checking test assumption

    # state file with standbys for an unknown runner
    handle_with_unknown = JobHandle('unknown', 286, 'jobtok',
                                    expected_weight=13)
    with open(state_path, 'w') as statef:
        json.dump(dict(launched=[],
                       pending=[],
                       standby_resources=[handle_with_unknown.dump()],
                       ),
                  statef)
    dispatcher.load_state()


def test_save_load_decommission_state(tmpdir, monkeypatch):
    state_path = tmpdir / 'paas-dispatcher.json'
    config = dict(
        state_file=str(state_path),
        quota_computation=DEFAULT_QUOTA_CONFIG,
        runners=[dict(executor=Runner.executor,
                      name='testrunner',
                      url='http://heptapod1.test',
                      token='secret1'),
                 ])
    dispatcher = PaasDispatcher(config=config)
    assert not dispatcher.state_file_path.exists()  # checking test assumption

    # state file without decommission info
    with open(state_path, 'w') as statef:
        json.dump(dict(launched=[], pending=[]), statef)
    dispatcher.load_state()
    assert not dispatcher.to_decommission

    runner = dispatcher.runners['secret1']

    # since we don't have a running polling loop, the jobs to decommisson
    # will stay inert.
    to_decomm_jobs = {
        make_job_handle(runner, 736, 'job-token-1'),
        # make sure the process does not fail if PAAS resource is missing
        # even though that should not happen for launched jobs!
        make_job_handle(runner, 737, 'job-token-2', with_resource=False),
    }

    dispatcher.to_decommission = to_decomm_jobs
    assert not state_path.exists()
    dispatcher.save_state()
    assert state_path.exists()

    # New Dispatcher and Runner instances
    dispatcher = PaasDispatcher(config=config)
    runner = dispatcher.runners['secret1']
    assert not dispatcher.to_decommission

    dispatcher.load_state()
    # quick assertion on runner_name and job_id
    assert dispatcher.to_decommission == to_decomm_jobs

    # details of job handles and PAAS resources
    handles_by_id = {jh.job_id: jh for jh in dispatcher.to_decommission}
    jh1 = handles_by_id[736]
    rsc1 = jh1.paas_resource
    assert rsc1 is not None
    assert handles_by_id[737].paas_resource is None

    monkeypatch.setattr(JobHandle, 'finished_standby_seconds', lambda _: 0.2)
    dispatcher.start_initial_threads()
    dispatcher.start_event_processing_thread()
    time.sleep(0.1)
    assert len(dispatcher.to_decommission) == 2  # still in standby time
    wait_until(lambda: len(dispatcher.to_decommission) < 2)

    # runner.decommission was called
    assert runner.successful_decommissions == [rsc1.app_id]
    # succesful decommission event sent and processed
    assert len(dispatcher.to_decommission) == 1
    assert dispatcher.to_decommission.pop().job_id == 737


@parametrize('saturation', ('concurrency', 'weight'))
def test_poll_loop(saturation):
    dispatcher = PaasDispatcher(dict(
        concurrent=17,
        check_interval=0.01,
        job_progress_poll_interval=0.02,
        quota_computation=DEFAULT_QUOTA_CONFIG,
        runners=[dict(executor=Runner.executor,
                      name='testrunner',
                      token='some-secret',
                      url='http://heptapod.test'
                      )
                 ]))

    cycles_done = dispatcher.poll_loop(max_cycles=2)
    assert cycles_done == 2

    if saturation == 'concurrency':
        dispatcher.potential_concurrency = 17
    elif saturation == 'weight':
        dispatcher.potential_weight = dispatcher.weighted_quota

    cycles_done = dispatcher.poll_loop(max_cycles=2)
    # we're still making cycles, even though new jobs won't be
    # requested.
    assert cycles_done == 2

    # Graceful shutdown. Running the loop in a separate thread for testing
    # purposes
    # TODO change the interruptible sleep step
    poll_thread = threading.Thread(target=lambda: dispatcher.poll_loop(),
                                   daemon=True)
    poll_thread.start()
    dispatcher.shutdown_required = True
    poll_thread.join(timeout=10)
    assert not poll_thread.is_alive()


def test_main(tmpdir, monkeypatch):
    config_path = tmpdir / 'runner.toml'
    state_file_path = tmpdir / 'paas_dispatcher_state.json'
    config_path.write_text('\n'.join((
        'concurrent = 17',
        'state_file = "%s"' % state_file_path,
        '',
        '[quota_computation]',
        '  reference_runner = "testrunner"',
        '  reference_flavor = "L"',
        '  reference_jobs_count = 5',
        '',
        '[[runners]]',
        '  executor = "%s"' % Runner.executor,
        '  name = "testrunner"',
        '  token = "toml-secret"',
        '  url = "http://heptapod.test"',
    )), 'ascii')
    dispatcher_main(
        raw_args=['--poll-interval', '0',
                  '--poll-cycles', '2',
                  '--job-progress-poll-interval', '0',
                  '--debug-signal',
                  str(config_path)])

    def raiser(dispatcher, *a, **kw):
        raise RuntimeError("panic, panic, panic!")

    monkeypatch.setattr(PaasDispatcher, 'poll_loop', raiser)
    assert dispatcher_main(raw_args=[str(config_path)]) == 1


def test_main_missing_quota_config(tmpdir):
    config_path = tmpdir / 'runner.toml'
    state_file_path = tmpdir / 'paas_dispatcher_state.json'
    config_path.write_text('\n'.join((
        'concurrent = 17',
        'state_file = "%s"' % state_file_path,
        '',
        '[[runners]]',
        '  executor = "%s"' % Runner.executor,
        '  name = "testrunner"',
        '  token = "toml-secret"',
        '  url = "http://heptapod.test"',
    )), 'ascii')
    assert dispatcher_main(raw_args=[str(config_path)]) == 2


def test_wait_threads_failure(paas_dispatcher):
    test_finished = False

    def long_wait():
        """Sleeping forever until the end of the test.

        Stopping at some point is still necessary!
        """
        while not test_finished:
            time.sleep(0.1)

    thread = threading.Thread(target=long_wait)
    thread.name = 'test-wait-threads-failure'
    paas_dispatcher.launched_jobs_progress_thread = thread
    thread.start()

    paas_dispatcher.shutdown_required = True
    paas_dispatcher.wait_all_threads(timeout=0.1)
    # we went through the error case, TODO assert on warning log.
    assert thread.is_alive()
    # TODO we don't have the means to make the event processing thread
    # stop if it is waiting for a message in the queue yet

    test_finished = True
    thread.join()
