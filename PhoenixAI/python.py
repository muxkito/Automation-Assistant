try:
   f = open("C:\\Users\\Administrator\\Desktop\\line.txt", "r")
   f.write("This is the test file for exception handling!!")
except IOError:
   print ("content is written in the file successfully")
