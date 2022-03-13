Cont. static analysis project 
Done by:
- M. Fatih Öztank 25060
- Arca Özkan 25524

dependency analysis reports are already provided in elassticsearchReports for convenience
but if you want to generate those reports from scratch you need to clone the elasticsearch repository
from github into this folder.

git clone https://github.com/elastic/elasticsearch.git

elasticsearch_test.py: Builds the software and generates the dependency analysis reports for server. You don't 
need to run this if you don't wish to generate dependency analysis reports from scratch. If 
your java version is not compatible with that release's gradle this program fails. Using an appropriate java
version fixes the problem.

GraphClass.py: No need to run this file specificly, it is a class implementation for jdepsReader.py

jdepsReader.py: By using the reports in the elasticsearchReports folder, it generates the dependency graphs 
and converts graphs into embeddings. It clusters each release according to the class defined in classname parameter.
depth can be choosen as 2 or 3. Picking a depth value larger than 3 showed no noticable impact in the results. So using 2 or
3 as depth value is optimal.


required python version: python3.9

required python packages: networkx, karateclub, scikit-learn, glob, numpy, abc
