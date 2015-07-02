__author__ = 'xiaolin'
d = {9:2, 6:4, 3:1, 7:12}

for key, value in sorted(d.iteritems(), key = lambda (k,v):(v,k)):
	print key