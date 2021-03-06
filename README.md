# CMU Interactive Data Science Final Project

* **Title**: Profiler
* **Online URL**: https://cmu-ids-2020.github.io/fp-profiler/ (Static demo without real back-end and call-graph support. Try it locally to see full functionality.)
* **Team members**:
  * Contact person: haonanw@andrew.cmu.edu
  * weiyizha@andrew.cmu.edu
  * lichenj@andrew.cmu.edu
  * yijiez2@andrew.cmu.edu
* **Track**: Interactive Visualization/Application
* **Video**: [here](https://drive.google.com/file/d/1HSFbZOKvZXDsIAktT9s-t5HH797ZDeJY/view?usp=sharing)
* **Report**: [here](https://github.com/CMU-IDS-2020/fp-profiler/blob/main/Report.pdf)

![Summary image](summary.gif)

## Abstract 

Programmers need to keep track of their programs' well-being and optimize the performance of their codes. Profilers are useful tools for experienced programmers to detect CPU bottlenecks and memory errors, but beginners may find it difficult both to use these tools and to interpret the raw text outputs of these tools. In this project, we build a user-friendly visualization for new programmers to conduct both CPU and memory analysis. 

There are three major components and all are highly interactive and easy to read. 
* **Call graph** gives users an overview of the program's structure and also supports free exploration into a small group of functions through expanding and collapsing operations. 
* **CPU linewise panel** allows users to detect in detail which lines of the code consumes most time. 
* **Memory linewise panel** enables users to detect possible memory bugs in each line of codes. 
  
Our application is lightweight and end-to-end. Users can spare the trouble of installing profiling tools, calling profilers and interpreting raw text outputs. All they need to do is to upload their codes or input through the editor. 

## Work distribution

Haonan Wang: Memory line-wise visualization and call graph interactive design.

Weiyi Zhang: Call graph visualization and interactive design.

Lichen Jin: CPU line-wise visualization, graph-line coordination, and the intergration.

Yijie Zhang: Front-end setup, user interface design and implementation.

## Deliverables

### Proposal

- [x] The URL at the top of this readme needs to point to your application online. It should also list the names of the team members.
- [x] A completed proposal. The contact should submit it as a PDF on Canvas.

### Design review

- [x] Develop a prototype of your project.
- [x] Create a 5 minute video to demonstrate your project and lists any question you have for the course staff. The contact should submit the video on Canvas.

### Final deliverables

- [x] All code for the project should be in the repo.
- [x] A 5 minute video demonstration.
- [x] Update Readme according to Canvas instructions.
- [x] A detailed project report. The contact should submit the video and report as a PDF on Canvas.

## Project setup

### Dependencies

Dependencies for back-end: Python, Flask, Pandas, Altair, binutils, valgrind.

Dependencies for front-end: Node.js and JavaScript libraries defined in frontend/profiler/package.json.

`linux-build.sh` contains the steps for setting up the development environment on Linux.

### Start front-end/back-end

The project consists of one back-end and one front-end. You can start the back-end under `backend/` with the following command:
```
flask run
```
This will start a dev server for back-end at localhost:5000.

You can start the front-end under `frontend/profiler/` with the following command:
```
npm install # install all dependencies locally
npm run serve
```
This will start a dev server for the application (front-end) at localhost:8080.

We provide `run.sh` which can start the back-end and front-end together.
