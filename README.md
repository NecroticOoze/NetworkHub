# NetworkHub
Repository for the NetworkHub project made by Blane Lysak. Essentially this is easy, cheap, efficient _(lol)_ LAN Storage.

## The problem
Basically, I wanted external storage that others on my network could access. At the same time,
I wanted everyone else to have something like this as well! This would be a cheap, at-home server.

For example, I can upload and share music, videos, pictures, PDF's, ebooks, database files, code, 
or zip files to the server and on a seperate device, I should be able to access it or view it or download it.

How can I allow everyone to have a cheap, in-house server?

## Hypothesis
If I use Flask to create an internal, network wide server,
I should be able to upload _any_ file and anyone on my network should be able to access it.

## My Solution: NetworkHub
NetworkHub started off as a small project, but now I want to see it through, to get it to every house and wifi.
Super simple GUI, the files are stored on the network, and if you want to disconnect it, you can!

**In a perfect world, this is how someone would set up NetworkHub:**
1. Get a Raspberry Pi
2. Get an external memory device, loaded with Ubuntu or some linux distro
3. Install Python3
4. Download NetworkHub
5. Use 'pip' to install requirements
6. Run application.py

NetworkHub would be broadcasted on the LAN, allowing anyone to gain access to the GUI by tuning into the IP of the Rasberry Pi.
It _should_ be that easy.

## Conclusion
Well, this is still a work-in-progress! I hope to add more functionality very soon.
