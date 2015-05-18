What is [Hapi](http://en.wikipedia.org/wiki/Hapi_%28Nile_god%29)?
===========

Hapi is a proof of concept for a relatively simple idea, related to (maybe even the same as, I'm not sure) [congestion collapse](http://en.wikipedia.org/wiki/Network_congestion#Congestive_collapse). The idea is that in queuing systems, one only has to get _barely_ over capacity to have a sustained outage, even if load subsequently falls dramatically. If there's already equivalent work out there, I apologize for not citing it. I tried to find something like this and couldn't. Seeing the gap, and not having taken the time to more than trivially understand the surrounding literature, I decided to demonstrate to myself at least the possibility of the correctness of the idea. Please inform me of any related works, and I will gladly list them here.

Usage
-----

```
pip install -r requirements.txt
sh run_sim.sh
```

Somewhat detailed logs will be output to `simulation_output`.

What's Here Now?
----------------

`simulation.py` is a rough proof of concept that simulates a queueing system:

1. Warming up (with no or trivial numbers of failed requests).
2. Running at steady state (again, almost no failed requests).
3. Bumping to a slightly higher rate (all requests fail).
4. Dropping to a _lower_ rate than the previous steady state, yet all requests still fail.

What's Coming?
--------------

I hope to demonstrate this against real world software, to prove to myself and others whether this concept applies to systems like web servers.

Got Feedback?
-------------

Please, create an issue, email me at [tehgeekemister@gmail.com](mail:tehgeekmeister@gmail.com), or get me at [@tehgeekmeister](http://twitter.com/tehgeekmeister). I'd love to hear why my simulation is too simplistic, or anything else related to this.

License
-------

MIT. Please submit pull requests!
