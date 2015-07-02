execfile("StrokeHmm.py") 
x = StrokeLabeler() 
x.trainHMMDir("../trainingFiles/") 

# [strokes, labels] = x.loadLabeledFile('../trainingFiles/0128_1.6.1.labeled.xml')
# x.labelFile("../trainingFiles/0128_1.6.1.labeled.xml", "results.txt") 
# print strokes
# print labels
# print len(strokes), len(labels)

# x.labelStrokes(strokes)

lTrueLabels, lPredictLabels = x.findConfusionData()
B = x.confusion(lTrueLabels, lPredictLabels)
print B