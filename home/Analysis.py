def Analysis(str,url):
   count=0
   array=str.split(' ')
   for i in array:
       if i in url:
          count=count+1
   return count


