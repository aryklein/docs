My personal lab Running on AWS
==============================

In this document I will add personal notes about how to deploy my personal lab on AWS for testing purpose.
This document is not itended to be an AWS tutorial. The offical AWS's documentation is really good.

1) Create a new VPC
-------------------

For my personal lab, I will create a new VPC with two subnets: a public subnet (for instances that need to be reachable
from Internet) and a private subnet (for instances that don't need to be reachable from Internet but need Internet access)

In the VPC menu, start the **VPC Wizard** and select the **VPC with Public and Private Subnets**. It will create a /16
network with two /24 subnets. Public subnet instances use Elastic IPs to access the Internet. Private subnet instances
access the Internet via Network Address Translation (NAT). You can ue the AWS NAT gateway or use a NAT instance.

To use a NAT instance is a cheaper option because AWS NAT gateway has extra charges, but a little bit more complicated.

In my case, my private subnet will reach Internet thru a NAT instance running in the public subnet. So I will choose 
**"Use a NAT gateway instead"** option.

After this, the wizard will deploy a new VPC with two subnets and a NAT instance. I will destroy this instance because
it's a *m1.small* instance (too big for my lab) and instead of this, I will create my personal NAT instance based on
Ubuntu 16.04.

2) Create an EC2 NAT instance
-----------------------------

In the EC2 section hit **Lanuch instance** and select *Ubuntu Server 16.04 LTS*. For my small lab I use **t2.nano**
but you can use another instance flavor. In the next step you should select the new VPC as a network, the public subnet,
Auto-assign public IP (enable) and in **Advanced Details** -> **User data** you should use this cloudl-init
configuration file to auto-deploy the NAT instance: 

https://raw.githubusercontent.com/aryklein/docs/master/AWS/cloud-config-nat.txt

This cloud-config updates all packages, creates a new user, creates a new systemd unit that will run a oneshoot script
that will set up the instance as a NAT instance. Besides it changes the SSH configuration and it enables the new 
systemd unit.


