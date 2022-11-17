import telnetlib
import time
import getpass
import sys

PASSWORD = b'1111111'
NEW_PASSWORD = b'1234567'


#IP = input('Device IP: ')
int_table = []
int_table_clear = []
d_interface = []
n_interface = []
arp_table = []
IP_list = []
Err_IP_list = []

text_file = open("IP.txt", "r")
IP_text = text_file.readlines()   ##Reading IP to list from file
text_file.close()

for i in range(len(IP_text)):
    IP_list.append(IP_text[i].rstrip('\n')) ##Clearing \n from IP list
print(IP_list)


for IP in IP_list:
    print()
    print('Connecting to device {}'.format(IP))
    try:
        with telnetlib.Telnet(IP) as t:
            print('Connected to device {}'.format(IP))
    
        
            output = t.read_until(b'Password: ')
            print(output)
            t.write(PASSWORD + b'\n')
            time.sleep(1)
            #output = t.read_until(b'Number')

            output = t.read_very_eager()
            if output.decode('utf-8').find('General') > 0:
                print ('Find General, password input correctly ')
            else:
                print('Cant find General')
                Err_IP_list.append(IP + ' Step 1 password input error')
                continue
            #print(output)
            
            
            t.write(b'23\n')               ##Select change pass item 23
            print('Select Item 23')
            time.sleep(1)
            output = t.read_very_eager()
            if output.decode('utf-8').find('Retype') > 0:
                print ('Find Retype, go to 23 success')
            else:
                print('Cant find Retype')
                Err_IP_list.append(IP + ' Step 2 error cant go to 23')
                continue
            


        
            t.write(PASSWORD + b'\n')      ##Input Old pass
            print('Old pass inserted')
            time.sleep(1)
            t.write(NEW_PASSWORD + b'\n')  ##Input New pass
            print('New pass inserted')
            time.sleep(1)
            t.write(NEW_PASSWORD + b'\n')  ##Retype new pass
            print('New pass repeated')
            time.sleep(1)
            t.write(b'\n')                 ##Input enter confirm
            print('Item 23 confirm')
            time.sleep(3)

            output = t.read_very_eager()
            if output.decode('utf-8').find('General') > 0:
                print ('Find General, password change correctly ')
            else:
                print('Cant find General')
                Err_IP_list.append(IP + ' Step 3 cant change password')
                continue
            #print(output)

    except Exception as err:
        print('Exception rised: ', err)
        Err_IP_list.append(IP + ' ' + str(err))
        continue
    ##    t.write(b'99\n')               ##exit
    ##    print('Exit telnet')
    
print()
for element in Err_IP_list:
     print(element)
f = open('IP_Err.txt', 'w')
for element in Err_IP_list:
    f.write(element + '\n')
f.close()    
    
    
