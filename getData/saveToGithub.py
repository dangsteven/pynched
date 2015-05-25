import os
from datetime import date

os.system("git add prices.dat")
os.system('git commit -m "prices.date update on %s' % str(date.today()))
os.system("git push")