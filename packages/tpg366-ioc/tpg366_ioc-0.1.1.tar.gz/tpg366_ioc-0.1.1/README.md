IOC for the Pfefiffer TPG-366 Pressure Gauge
============================================

This in an unofficial, as-simple-as-it-gets IOC for the Pfeiffer TPG-366
pressure gauge.

It does nothing else except reading out temperatrue and status
data, publishing them via PV suffixes `.VALUE` and `.STATUS` for
each gauge. The exact format of the PVs is `{prefix}G{cnt}:STATUS`,
respectively `{prefix}G{gauge}:VALUE` with `{prefix}` as the EPICS
prefix (e.g. "DOODLE:") and `{cnt}` as the gauge counter, starting
at 1. For instance:

 - `DOODLE:G1:VALUE`
 - `DOODLE:G1:STATUS`
 - `DOODLE:G2:VALUE`
 - `DOODLE:G2:STATUS` ...

Obtaining & Running
-------------------

Via Pip:
```
$ pip install tpg366-ioc
$ export PFEIFFER_EPICS_PREFIX=DOODLE:
$ export PFEIFFER_VISA_DEVICE=TCPIP::192.168.1.17::8000::SOCKET
$ tpg-366-ioc
```

Or via Podman:
```
$ podman run -ti --rm \
     -e PFEIFFER_EPICS_PREFIX=DOODLE: \
     -e PFEIFFER_VISA_DEVICE=TCPIP::192.168.1.17::8000::SOCKET
     registry.gitlab.com/kmc3-xpp/tpg366-ioc:latest
```

Or directly from source, via git clone:
```
$ git clone https://gitlab.com/kmc3-xpp/tpg366-ioc
$ pip install -e tpg366-ioc[all]
$ export PFEIFFER_EPICS_PREFIX=DOODLE:
$ export PFEIFFER_VISA_DEVICE=TCPIP::192.168.1.17::8000::SOCKET
$ tpg-366-ioc
```

Environment Variables
---------------------

TPG-IOC is controlled via environment variables:

- `PFEIFFER_EPICS_PREFIX` EPICS prefix including the trailing ":"
- `PFEIFFER_VISA_DEVICE` VISA device address specification. Note that
  anything other than TCPIP-schemes may cause problems currently.
  Typically, the default port for these devices is 8000, so your TCP/IP
  VISA device would be something like: "TCPIP::\<host\>::8000::SOCKET".
- `PFEIFFER_VISA_RMAN` VISA resource manager, defaults to "@py"
- `PREIFFER_NR_GAUGES` number of gauges to query / display, defaults
  to 6.


Bugs & Caveats
--------------

Async operation, which the EPICS PV part depends on, only seems
to work fine with TCP/IP VISA devices. This is owing to bugs
within the VISA framework. Could be worked around, but it isn't
a priority currently (contact us if you have a use case).

The IOC is very, *very* simple -- just reading pressure values.
No configuration, no advaced features.

Normally there would be unit tests and a sim-mode prior to building
the image -- this time there aren't. Eventually they'll get
retrofitted (there is a test harness in place). But for now,
be careful with upgrades.



