# 3D_Helios_UI
This project looks at developing a UI-based tool for using the Helios++ (https://github.com/3dgeo-heidelberg/helios) LiDAR simulation project for UAV task planning.

# Usage

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

# Running 3D_Helios_UI Using Docker

In the directory that contain the Dockerfile, run the following code
 
```
docker build -t 3dhelios .
docker run --rm -it -p 5000:5000 3dhelios
```

Open a web browser and run: localhost:5000
