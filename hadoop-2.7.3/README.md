# 18645_team030_project Hadoop Programs

## Term Project Specs

Java: 1.8
Hadoop version: 2.7.3
EMR: EMR 5.4.0


## Build instructions
- go to directory with pom.xml
- `mvn clean package` in your terminal


## Run Instructions

#### If you are using Mac OS follow these instructions first
- `zip -d subredditRecommendor.jar META-INF/LICENSE`
- `jar -tvf subredditRecommendor.jar | grep META-INF/LICENSE`

#### To run the jar

Replace [xxxx] with relevant names to your use case.

Utilized tmpdir only when temporary intermediate steps are required.
- `hadoop jar subredditRecommendor.jar -program [program name] -input [input_file/s] -output [output_directory] -tmpdir tmp`

Two programs exist:
- "processData"
- "allPairs"

#### How to run on AWS EMR in general
`aws emr create-cluster --name "Test cluster Process Reddit Data" --release-label emr-5.4.0 \
--service-role EMR_DefaultRole --ec2-attributes InstanceProfile=EMR_EC2_DefaultRole \
--log-uri s3://team030.output.reddit --enable-debugging \
--instance-groups
InstanceGroupType=MASTER,InstanceCount=1,InstanceType=c1.xlarge
InstanceGroupType=CORE,InstanceCount=4,InstanceType=c1.xlarge \
--steps Type=CUSTOM_JAR,Jar=s3://team030.fastcode/subredditRecommendor.jar,Args=["-
input","s3://team030.rc-2015-01/rc_2015_01","-output","s3://team030.output/rc-2015-01","-
program","processData","-tmpdir","tmp"] \
--auto-terminate`