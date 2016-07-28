Steps to install a LTSP server
==============================

1. Install a Ubuntu Desktop

2. Install LTSP on top of an already running desktop system:

   ``$ sudo apt-get install ltsp-server-standalone``

3. Create a thin-client environment on the server:

   ``$ sudo ltsp-build-client``

   If the thin-client has another architecture use the ``--arch`` option:

   ``$ sudo ltsp-build-client --arch i386``

4. Edit ``/etc/ltsp/dhcpd.conf`` and set the proper values according to the network 
   where the LTSP server is running. Change the architecture directory according to what you're using.

5. Chroot inside the thin client environment:
   
   ``$ sudo ltsp-chroot``

6. Inside the chroot environment, edit the file ``/etc/ltsp/update-kernels.conf``, add
   at the end of the file ``IPAPPEND=3`` and save it.

7. Inside the chroot environment, run:
   
   ``$ sudo dpkg-reconfigure linux-image-`uname -r```

8. Exit from the chroot

9. Generate a NBD image from the LTSP chroot:

   ``$ sudo ltsp-update-image``

10. Copy LTSP chroot kernels to TFTP directories:

    ``$ sudo ltsp-update-kernels``
