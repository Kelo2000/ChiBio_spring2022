# Chio_bio
This fork of [Chi.Bio](https://github.com/HarrisonSteel/ChiBio) code file `app.py` implements some more useful functionality.

## Toggle pumps during experiments
### Usage
At the top of `app.py`, in `sysDefault` you can change the default pumps for each reactor. The `default_inputPump` and
`default_outputPump` are the ones will be used when the experiment starts, and the code will toggle back and forth
between the `default_inputPump` and the `toggled_inputPump` during the experiment. 

To specify the toggle times, please add a `.csv` file for each of the reactor with the file name syntax:
`PumpToggleTimes_<reactor>.csv` next to the `app.py`. This repository comes with a sample file for reactor M0 which you
can modify for the other reactors. Each cell/data contains the minutes from experiment start the program will toggle the
pumps. The example file tells the program to switch input pumps after 1.5, 2.5 and 3.5 minutes.

The program might not work properly if the times are too close to each other (within the same minute) or there is a
zero (as it cannot toggle on start). For it to work well you might need to space out the times a bit and also avoid
toggling right after experiment start. The program will notify on terminal if there is a pump switch, an error or if
pump switching has ended.

### Code changes
@Quan: I edited a lot of references to `'Pump1'` and `'Pump2'` in the original code to reference `inputPump` and
`outputPump` instead, so that these can be changed during runtime. The `TogglePumps` function was added to toggle the
pumps and wait on a separate thread. Inside the `ExperimentStartStop` I also added some code to check if the `.csv` file
is there, and if yes proceed with the pump toggling.

@Malak & Lukelo: 

Task1:Delay the switching on of Pump2 to work after pump1 is on. Currently when we switch on 'OD Regulation', outlet pump 2 turns on immediately even if the OD is below the target. Since switching it on very early in the experiment is unnecessary and leads to waring out the tubings quicker, it would be best if it switched on once the OD goes above the limit (after Pump1 is switched on).
Changes made:- Line 1960(Original file) and 1997(Quran’s file): changed 15 to 0 so that pump1 turns on from the beginning 

Task3: Get rid of the normalization of fluorescence over time. This can be seen in the real time fluorescence graph 'Normalized FP Emission' Vs. 'Time'. The code calculates Real time fluorescence as  FP_Emit / FP_base. Hence “Normalized Emission values” on the Y-Axis. If we can get rid of this division/normalization would be great. Maybe through adding an “OFF” selection under baseband dropdown list on the GUI (the default is clear), or removing the division altogether.
Changes made: Line 1639 and 1640 (in original file) and 1669 and 1670 (Quan’s file): remove the denominator completely
