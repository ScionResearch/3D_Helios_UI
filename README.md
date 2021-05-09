# 3D_Helios_UI
This project looks at developing a UI-based tool for using the Helios++ (https://github.com/3dgeo-heidelberg/helios) LiDAR simulation project for UAV task planning.

The Helios++_UI is delivered to you in a zipped folder, unzip the folder to your working directory. This folder contains Dockerfile to build the docker image for running 
this project. The folder also contains some predefined scanners and platform settings and definitions **(please do not modify these files!!!)**. The predefined scanners and platforms are available on the front end for editing and working with. You can add new scanners and platforms from the front-end as well as modify exisiting scanner and platform settings. More information is available on the wiki.
Finally, the whole GUI code is written across several files and folders in this directory.

# Running 3D_Helios_UI Using Docker

In the directory (base directory) that contain the Dockerfile, run the following code
 
```
docker build -t 3dhelios .
docker run --rm -it -p 5000:5000 3dhelios
```

Open a web browser and run: 
```
localhost:5000
```
# Usage
You can select from the predefined scanner and platforms that comes with the Helios++_UI or you can define a new scanner or platform. You can also modify exisiting scanner and platform settings/definitions. The information below is for adding new scanner and platform.

### Filling the Scanner and Platform Information
Refer to Helios++ repository for a full definition of each of the parameters needed. 

The scanner settings information is available at https://github.com/3dgeo-heidelberg/helios/wiki/Scanners#scanner-settings

The platform settings information is available at https://github.com/3dgeo-heidelberg/helios/wiki/Platforms

### Filling the Survey
Additional information on the individual parameters of the survey is available at: https://github.com/3dgeo-heidelberg/helios/wiki/Survey

### Scene Upload
Using the blender2helios addon in blender, perform the following steps:

Helios Base Directory:

Create a directory called new_blender2helios_scene

Create a directory called data inside new_blender2helios_scene

Create two directories inside data called screens and screenparts

In blender2helios: provide  new_blender2helios_scene as the helios base directory

Zip data and upload to web-helios++


#### Scene Upload Folder Structure

```
src
|
 |--data
     |--screens
     |--screenparts

```

# Output
The Download button will become active when Helios have finish running. Download the output to have access to the results. The format and explanation of the output is available at https://github.com/3dgeo-heidelberg/helios/wiki/Output

The output point clouds and (optionally) the full waveform and the trajectory files are stored in
```
[survey_name]opt/gui-helios/helios-plusplus/output/Survey Playback/[name of survey as defined in survey.xml]/[time stamp of simulation start]/points/[number of scan position].

[xyz|las] e.g. TLS Arbaro\opt\gui-helioshelios-plusplus/output/Survey Playback/TLS Arbaro/2016-09-28_15-17-52/points/leg000_points.xyz
```
