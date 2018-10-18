## Description

In this lab I had to transfer multiple files using threads and avoiding race
conditions. This was accomplished by sending different files and storing them
under the same name and avoiding an output file which contains a mixed up
combination of both original files.


## Code

The code for this lab is seperated into different files. The
server(framedThreadServer) and the client(framedThreadClient) both create a
class of serverThread and clientThread respectively. The framedSock file has
the framedSockThread which crates a class which has all the functions to send
and receive messages over the socket. In the server file, I determine if the
sent file can be stored under the specified name, if it can then it is simply
stored under the provided name otherwise, I put a number in front of the
provided fileName. All this searching and storing(receivemsg) is done within a
lock which will stop a race condition from happening. Only after the lock is
realeased can the next server thread search and determine if fileName already
exists.


## How to Run

To run program...

```
1. C-x 2 (split screen horizontally)
2. Create 2 shells. One named client and one named server (M-x rename-buffer)
3. python3 framedThreadServer.py on the server shell
4. python3 framedThreadClient.py on the client shell
5. ls to list newly created files
6. cat all files to check everything saved correctly
7. All this can be ran along with the srammer proxy. Simply open another shell
for stammerProxy.py(run using python3 stammerProxy.py)
To terminate simply C-x C-c
```
## Bugs
I create a total of 10 client threads all storing two different files under
the same name. All the files are created correctly and stored by server. But
for some reason I get print statements that say theres trouble connecting. I
dont understand why I am getting these messages if the program is running as
it should.
