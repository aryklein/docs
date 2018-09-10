systemd Timers
==============

Timers are systemd unit files that end with .timer. They control .service files or events. Timers can be used as
an alternative to cron.

Type of Timers
--------------

Timers are systemd unit files with a suffix of ``.timer``. They include a ``[Timer]`` section which defines when
and how the timer activates.

- **Monotonic timers**: relative to different starting point.
- **Realtime timers**: activate on a calendar event, the same way that cronjobs do.

Timer units
-----------

For each ``.timer`` file, a matching ``.service`` file should exist. For example for a ``foo.timer`` timer
a ``foo.service`` should exist. The ``.timer`` file activates and controls the ``.service`` file.
The ``.service`` does not require an ``[Install]`` section as it is the timer units that are enabled.

It is possible to control a different named unit using the ``Unit=`` option in the ``[Timer]`` section.

systemd timers as a cron alternative
------------------------------------

Timers work directly with services units. So we have to create the service unit in the ``/etc/systemd/system/``
directory. For example, create the file ``/etc/systemd/system/date.service``:

.. code-block:: bash

    [Unit]
    Description=Prints date into /tmp/date file
    
    [Service]
    Type=oneshot
    ExecStart=/usr/bin/bash -c '/usr/bin/date >> /tmp/date'
    User=ary

Now we have to define in the same directory (``/etc/systemd/system``) the timer:

.. code-block:: bash

    [Unit]
    Description=Daily prints of date into /tmp/date file
        
    [Timer]
    OnCalendar=*-*-* 01:05:00
    
    [Install]
    WantedBy=timers.target

Then run:

.. code-block:: bash

    $ sudo systemctl daemon-reload

To use the *timer unit* enable and start it, like any other unit but using the ``.timer`` sufix.
This config will run our ``date.service`` all days at 1:05am. We can check the timer running on a system with:

.. code-block:: bash

    $ sudo systemctl list-timers
    $ sudo systemctl list-timers --all

In Archlinux, you can check as an example the logrotate's timer:

.. code-block:: bash

    $ cat /usr/lib/systemd/system/logrotate.timer
    [Unit]
    Description=Daily rotation of log files
    Documentation=man:logrotate(8) man:logrotate.conf(5)
    
    [Timer]
    OnCalendar=daily
    AccuracySec=12h
    Persistent=true
    
    [Install]
    WantedBy=timers.target
    
    $ cat /usr/lib/systemd/system/logrotate.service
    [Unit]
    Description=Rotate log files
    Documentation=man:logrotate(8) man:logrotate.conf(5)
    ConditionACPower=true
    
    [Service]
    Type=oneshot
    ExecStart=/usr/sbin/logrotate /etc/logrotate.conf
    
    # performance options
    Nice=19
    IOSchedulingClass=best-effort
    IOSchedulingPriority=7
    
    # hardening options
    #  details: https://www.freedesktop.org/software/systemd/man/systemd.exec.html
    #  no ProtectHome for userdir logs
    #  no PrivateNetwork for mail deliviery
    #  no ProtectKernelTunables for working SELinux with systemd older than 235
    MemoryDenyWriteExecute=true
    PrivateDevices=true
    PrivateTmp=true
    ProtectControlGroups=true
    ProtectKernelModules=true
    ProtectSystem=full
    RestrictRealtime=true
