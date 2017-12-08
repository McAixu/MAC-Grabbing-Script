import os
import subprocess
import sys

filedest = os.getcwd() + '\\arpfiles\\arptesting%d.txt'
subnet = sys.argv[0]
netmask = sys.argv[1]

if 'arpfiles' not in os.listdir():
	os.mkdir('arpfiles')
	
def network_octs(subnet):
#Just getting octets based on network class
# To do: use netmask to find actual IP range for subnet
	netprefix = int(subnet[:3].split('.')[0])
	if 0 < netprefix < 127:
		netclass = 0
	elif 127 < netprefix < 192:
		netclass = 1
	else:
		netclass = 2
	octs = ''
	for x in range(0,netclass+1):
		octs += subnet.split('.')[x] + '.'
	return octs
	
####################### GET MAC LIST BELOW #######################
def save_arp_file(clickindex):
	clickindex += 1
	return clickindex
	
def get_lines(filedest):
	f = open(filedest, 'r')
	lines = f.readlines()
	f.close
	return lines


def get_MAC_lines(octets, lines):
#Returns a tuple with the line and its index in the file
	interfaceline = 'Interface: ' + octets
	y = [x for x in lines if x[:(11 + len(octets))]==interfaceline]
	startind = lines.index(y[0])
	z = [x for x in lines if x[:10] == 'Interface:']
	indexlist = [lines.index(x) for x in z]
	indexlist.sort()
	endind = 0
	if indexlist.index(index) == indexlist.index(max(indexlist)):
		endind = len(lines)
	else:
		endind = indexlist(indexlist.index(startind)+1)
	return startind, endind
	
def get_MACs(lines, start, end):
	usefullines = lines[start+2:end]
	t = [x[24:41].split(' ')[0] for x in usefullines if len(x[24:41]) == 17]
	t = [x.replace('-',':') for x in t]
	return t
	
def main():
	octets = network_octs(subnet)
	clickindex = 0
	MACs = []
	x = ''
	while x != 'done':
		x = input()
		if x == '':
			file = filedest%clickindex
			f = open(file,'w')
			subprocess.call('arp -a', stdout = f)
			#Can just store this as a list directly with subprocess.Popen rather than save first.
			#put on the to do list.
			f.close()
			clickindex += 1
			lines = get_lines(file)
			startind, endind = get_MAC_lines(octets,lines)
			MACstoAppend = get_MACs(lines, startind, endind)
			MACs += MACstoAppend
		elif x == 'done':
			#need to remove duplicate MACs here
			f = open('MACoutput.txt','w')
			for x in MACs:
				f.write(x+'\n')
			f.close()
		
		else:
			print('Prese enter to grab another set of MACs.')
			print('Otherwise, enter "done" to finish program.')
		
if __name__ == '__main__':
	main()