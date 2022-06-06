% Chromebooks for Serious Use Finally Makes Sense
10 Nov 2018
T3

![](./images/chromebook.jpg)

For a very long time, I've criticized Chromebooks as a serious option for a laptop.

I still partially feel this way to most new laptops because of how easy it is to acquire cheap second-hand laptops with equivalent or better specs for the same price. I know this because I have purchased lots of cheap Thinkpads on eBay ([Useful Price Guide](https://www.truefla.me/free-stuff/used-thinkpad-buyers-guide)).

And similarly, this is where most of my loathing for MacBooks comes from: comparably poor price-to-performance efficiency.

For day-to-day productivity, cheaper cost efficient laptops are great. I used a  Thinkpad, that was at least 7 years old with SSD and RAM upgrades as my daily driver since the start of Grade 10 up until last month in my second year of university.

The primary reason I switched was that I wanted a machine that could play video games really well and increase my local power for running virtual machines and compute heavy programming environments since we started using RAM heavy IDEs such as IntelliJ and Android Studio.

These reasons guided my purchasing decision, but if I didn't care as much about gaming use, and even then, there may have been a better option.

### Enter Cloud Computing

### ![](./images/gcp.png)

Funnily enough, I stumbled upon it when looking to see if there was a way to offload a video game's GPU demand to a powerful computer and stream the result ([Gaming on an EC2 Blog Post](https://nexus.vert.gg/gaming-on-amazon-s-ec2-83b178f47a34)).

Now what if you wanted to offload, everything; your whole desktop environment? VNC/SSH into a cloud desktop with just enough cores and RAM from any PC including your low-power laptop.

Obviously you don't need cloud computing to do this; you could own a powerful PC and use it as a server and VNC over the internet etc. But cloud computing platforms make it more accessible and (possibly) more cost-effective.

The biggest drawback to this is the always online requirement to achieve most of the functionality on your low-power client.

Maybe, you get a low power laptop with a decent amount storage space to backup your most essential work folders so you can at least do some things offline like editing, and when you gain re-connection, you can push it for compiling, etc.

### Cost efficient?

Just for a quick cost comparison, let's say you have a $1600 CAD budget for a new laptop and you want to be able to do some medium-heavy computation with it. At this price point, you should be able to get an i7 8750H 6 core CPU with 16GiB and probably a decent GPU as well.

At the time of writing, an 8 core 30GiB RAM VM instance on Google Cloud Platform costs \~$0.267 CAD per hour (not counting extra disks and storage).

At 6 hours a day (generous) * 7 days a week (also generous) * 4 weeks * 12 months = \~2000 hrs/yr of compute time, or \~534 CAD/yr.

And if you make it preemptible, meaning that you are put into a lower priority and can get booted off by other higher paying customers, you can take that price down to \~$0.081 CAD per hour or \~$162/yr

Not bad.

Some major benefits to the cloud computing option are:

* uptime
* reliability/redundancy options
* easy to drop into more advanced cloud computing activity
* encouragement to gain cloud platform experience

The major con is of course that an internet connection is always required.

### Should you give it a try?

Google Cloud Platform offers $300 USD of credit that expires after 12 months with every new account that signs up.

That is far more than enough to run a powerful preemptible VM for ~2000 hrs.

So, no matter what kind of PC you have, go and try it.

And don't stop there. Check out AWS and Azure, though GCP has become my personal go-to and favorite.

Maybe you can put off spending a lump sum on a flashy new laptop, _and_ still get serious work done!
