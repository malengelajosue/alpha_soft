import  os


longitude ='1140.8688S'
latitude='02727.9781E'
altitude='1212.9M'

#convert dd mm.mmm to dd.ddd =dd +mm/60 +mmm/60

newLong = longitude

coord=newLong.split('.')

mmmList=coord[1]
print(coord[1])
mmm = mmmList[:-1]

signe=mmmList[-1:]
ddmm=list(coord[0])
print(''.join(ddmm[0:1]))
if int(''.join(ddmm[0:1]))!=0:
    dd = ''.join(ddmm[0:2])
    mm = ''.join(ddmm[2:])
else:
    dd = ''.join(ddmm[1:3])
    mm = ''.join(ddmm[3:])



print(str(dd)+' '+str(mm)+' '+str(mmm)+' '+str(signe) +' len'+str(len(mmm)))

conver =int(dd) + (int(mm)/60) +(int(mmm)/(60*(10** len(mmm))))
if signe=='S' or signe=='W':
    conver *=-1

print(format(conver,'4f'))