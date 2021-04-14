# Utility for finding the shift in synchronization
The two stereo videos must be synchronized to produce a 3D video. When syncing sound and video, a clap board is used, but with two video streams, a mobile clock displaying hundredths of a second is acceptable. 

The ```synchronize.py``` script takes the right and left videos as arguments and an optional shift _s_ argument that shifts the left video _s_ frames forward (a negative shift will freeze until the right video has reached frame _s_). The script is executed with the following command:
```python3 synchronize.py --right <path-to-file>/1.avi --left <path-to-file>2.avi [--shift <no-of-frames-to-shift>]```

Synchronize with the following steps.
1. Let the videos play until the right video has reached an easily identified moment in time, eg., a time on a mobile clock.
2. Toggle the pause with *space*.
3. Move both videos backward 10 frames with *V*, backward one frame with *B*, forward one frame with *N* and forward 10 frames with *M*. 
4. Find the corresponding frame in the left video by adjusting the _shift_ one frame at a time backward with *A* and forward with *S*.
5. Generate timealigned videos with *G*. The two videos will be saved in the same folder as the originial videos with ```_timealigned_``` attached to the names. 