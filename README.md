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