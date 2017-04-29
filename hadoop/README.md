# 18645_team030_project Hadoop Programs

## Term Project Specs

Java: 1.8
Hadoop version: 2.7.3
EMR: EMR 5.4.0


## Build instructions
	- go to directory with pom.xml
	- "mvn clean package" in your terminal


## Run Instructions
    Replace [xxxx] with relevant names to your use case
    Utilized tmpdir only when temporary intermediate steps are required
    - hadoop jar subredditRecommendor.jar -program [program name] -input [input_file/s] -output [output_directory] -tmpdir tmp