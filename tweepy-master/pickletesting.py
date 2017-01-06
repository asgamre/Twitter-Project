# This Python file uses the following encoding: utf-8
import pickle

a = ['test value','test value 2','test value 3']
print a

file_Name = "testfile"
# open the file for writing
fileObject = open(file_Name,'wb') 

# this writes the object a to the
# file named 'testfile'
pickle.dump(a,fileObject)   

#here we close the fileObject
fileObject.close()
#we open the file for reading
fileObject = open(file_Name,'r')  
#load the object from the file into var b
b = pickle.load(fileObject)  
print b