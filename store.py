#coding=UTF-8
import shutil
import os
from pyspark.mllib.feature import HashingTF
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.classification import NaiveBayes
from pyspark import SparkContext, SparkConf
from sklearn.metrics import classification_report

### Spark Config ###
conf = SparkConf().setAppName("All group").setMaster("local").set("spark.executor.memory", "20g")
sc = SparkContext(conf=conf)

### file config ###
f_base = "/home/nctuteam/store/"
f_train = "train.txt"
f_test = "test.txt"
f_category = "group_list.txt"
f_result = "result.txt"

### Open result file for logging ###
res = open( f_base + f_result ,"w+")

### Hashing function to convert word to int limit to 70001(prime larger than 66K) words ###
htf = HashingTF(70001)

### tokenize sentences and transform them into vector space model ###
Data = sc.textFile( f_base + f_train )
data = Data.map(lambda text: LabeledPoint(int(text.split(",")[0]), htf.transform(text.split(",")[1].split(" "))))
res.write("No. of Training data: " + str(data.count())+"\n")
data.persist()

Test = sc.textFile( f_base + f_test )
test = Test.map(lambda text: LabeledPoint(int(text.split(",")[0]), htf.transform(text.split(",")[1].split(" "))))
res.write("No. of Testing data: " + str(test.count())+"\n")
test.persist()

### Get all category names ###
target_names = []
names = open( f_base + f_category ,"r")
for name in names:
    target_names.append(name.replace("\n",""))

### Train a Naive Bayes model on the training data ###
model = NaiveBayes.train(data)

### Compare predicted labels to actual labels ###
prediction_and_labels = test.map(lambda point: (model.predict(point.features), point.label, point.features))

### Filter to only correct predictions ###
correct = prediction_and_labels.filter(lambda (predicted, actual, text): predicted == actual)

### Calculate and print accuracy rate ###
accuracy = correct.count() / float(test.count())
res.write("Correct count out of test count: "+str(correct.count())+" "+str(test.count())+"\n")
res.write("Classifier correctly predicted category " + str(accuracy * 100) + " percent of the time"+"\n")

### Get precision and recall and f1 value ###
y_true = []
y_pred = []
for x in prediction_and_labels.collect():
    xx = list(x)
    try:
        tt = int(xx[1])
        pp = int(xx[0])
        y_true.append(tt)
        y_pred.append(pp)
    except:
        continue        

res.write(classification_report(y_true, y_pred, target_names=target_names))


