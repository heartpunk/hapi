import random

import simpy

MAX_TIME = 1000
WORKERS = 2750
RATE = WORKERS


def timing(env, start):
    now = env.now
    return "%.4f, %.4f after start" % (now, now - start)


def phase(now):
    TEST_TIME = 0.5 * MAX_TIME

    if now < TEST_TIME:
        return 'warmup'
    elif now < TEST_TIME + (MAX_TIME / 6.0):
        return 'steady'
    elif now < TEST_TIME + (2 * MAX_TIME / 6.0):
        return 'spike'
    else:
        return 'choke'


def scale(time):
    base_rate = RATE / 10.0
    if phase(time) in ('warmup', 'steady'):
        return base_rate
    if phase(time) == 'spike':
        return base_rate * 10
    if phase(time) == 'choke':
        return base_rate

def clients(count, env, resource, cur_phase):
    return [env.process(resource_user(env, resource, cur_phase)) for i in range(int(count))]


def resource_user(env, resource, cur_phase, retry=0):
    start = env.now
    if retry >= 9:
        return
    with resource.request() as request:
        yield env.timeout(random.uniform(0.0, 0.5)) # prevent retry storms
        ev = yield env.any_of([request, env.timeout(30)])
        if isinstance(list(ev.keys())[0], simpy.events.Timeout):
            print "failed to get resource at %s, %s" % (timing(env, start), cur_phase)
            resource.release(request)
            yield env.process(resource_user(env, resource, cur_phase, retry=retry+1))
        else:
            print "got resource at %s, %s" % (timing(env, start), cur_phase)
            yield env.timeout(.1)
            print "blocked for a second to simulate doing something at %s" % timing(env, start)
            resource.release(request)
            print "released resource at %s" % timing(env, start)


def loop(env, resource):
    cur_clients = []
    while True:
        print "queue length is %d" % len(resource.queue)
        cur_phase = phase(env.now)
        num_clients = int(scale(env.now))
        cur_clients = filter(lambda c: c.is_alive, cur_clients)
        cur_clients += clients(num_clients - len(cur_clients), env, resource, cur_phase)
        cur_clients = cur_clients[:num_clients]
        ev = yield env.any_of(cur_clients + [env.timeout(40)])
        print repr(ev)


env = simpy.Environment()
res = simpy.Resource(env, capacity=1)
env.process(loop(env, res))
env.run(until=MAX_TIME)
