How to add Standard Access Control Lists (ACLs) for VTY lines (Telnet or SSH)
=============================================================================

How to create a Extended Access Control List (ACL) using "access-list" IOS command to filter SSH and Telnet traffic
-------------------------------------------------------------------------------------------------------------------

**Extended Access List**

Extended IP access lists are almost identical to standard IP access lists in their use.
The difference between them is the variety of fields in the packet that can be compared for matching.
As with standard lists, extended access lists are enabled for packets entering or exiting an interface.
The list is walked sequentially, the first statement matched stops the search through the list and defines
the action to be taken. Extended access lists can match source and destination addresses as well as different TCP
and UDP ports. This gives greater flexibility and control over network access.

To configure extended access lists, the command is similar to standard access list, but with more options.

::

    router(config)# access-list {100-199} {permit | deny} protocol source-addr [source wildcard bits]
    [operator operand] destination-addr [destination wildcard bits] [operator operand] [established]


In this example we are going to permit SSH and Telnet only from the admin networks (10.10.10.0/24 and
172.16.0.0/24), so first of all we have to create the Access List

::

    router>enable
    router#configure terminal
    Enter configuration commands, one per line.  End with CNTL/Z.
    router(config)#access-list 101 permit tcp 10.10.10.0 0.0.0.255 any eq 22
    router(config)#access-list 101 permit tcp 10.10.10.0 0.0.0.255 any eq telnet
    router(config)#access-list 101 permit tcp 172.16.0.0 0.0.0.255 any eq 22
    router(config)#access-list 101 permit tcp 172.16.0.0 0.0.0.255 any eq telnet
    router(config)#access-list 101 deny ip any any
    router(config)#exit
    router#


Applying the Access Control Lists (ACL) to VTY lines to filter Telnet or SSH traffic
------------------------------------------------------------------------------------

The Exteded Access Control List created before can be applied to VTY lines using the IOS command ``access-class``:

::

    router>enable
    router#configure terminal
    Enter configuration commands, one per line.  End with CNTL/Z.
    router(config)#line vty 0 4
    router(config-line)#access-class 101 in
    router(config-line)#exit
    router(config)#line vty 5 15
    router(config-line)#access-class 101 in
    router(config-line)#end
    router#

Even, it's possible to create two ACL, one for SSH lines and other for Telnet lines

