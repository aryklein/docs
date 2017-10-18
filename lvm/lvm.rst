LVM cheat sheet
===============

Find free space in a Volume Group in LVM
----------------------------------------

Execute the command vgdisplay to get information of all volume groups on the system.

::

  # vgdisplay
  
Example output is given below. The line “Free PE / Size” indicates the free physical extents in the VG and
free space available in the VG respectively.

The physical extent in LVM is the blocksize that physical volumes are using. The default physical extent is
4MB but can range from 8kB up to 16GB (using powers of 2). Logical volumes are made up from logical extents
having the same size as the physical extents.

Example:

::

  # vgdisplay
  ......
    --- Volume group ---
    VG Name               vg_os2
    System ID
    Format                lvm2
    Metadata Areas        1
    Metadata Sequence No  9
    VG Access             read/write
    VG Status             resizable
    MAX LV                0
    Cur LV                5
    Open LV               5
    Max PV                0
    Cur PV                1
    Act PV                1
    VG Size               558.88 GiB
    PE Size               4.00 MiB
    Total PE              143072
    Alloc PE / Size       102400 / 400.00 GiB
    Free  PE / Size       40672 / 158.88 GiB
    VG UUID               BXrCkO-bip9-fqjB-h4yd-JdNL-fUEq-Vsh6cq


From the example above there are 40672 available PEs or 158.88 GiB of free space.

And ``162688 MiB to GiB = 158.875 GiB``


Create a new Physical Volume
----------------------------

::

  # pvcreate /dev/sdb1

Extend a Volume Group
---------------------

::

  # vgextend vg_main /dev/sdb1


Extend a LVM
------------

Extend the size of your LVM by the amount of free space on PV:

::

  # lvextend /dev/vg_main/lv_root /dev/sdb1

Extend with a given size (add 10G):

::

  # lvextend -L +10G /dev/vg_main/lv_root


Extend to a given size (to 12 GB)

::

  # lvextend -L 12G /dev/vg_main/lv_root
  

Resize the file system online
-----------------------------

Without umounting the filesystem, you can run:

::

  # resize2fs /dev/vg_main/lv_root

