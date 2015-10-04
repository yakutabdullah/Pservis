


import PyQt4
from PyQt4.Qt import QLabel, QTextEdit, QWidget, QPixmap, QBoxLayout, \
    QHBoxLayout
from PyQt4.QtGui import QDialog, QPushButton, QGridLayout, QApplication, QTextBlock, QTextFormat
import commands
import os
from os.path import join
import pip
import pkg_resources
import subprocess

import netifaces as ni


class ServiceControl(QDialog):
    SSHcnt =0
    HTTPcnt =0
    FTPcnt =0
    ip =''     

    
    def __init__(self, parent=None): 
        
        
        self.ip=''
        
        super(ServiceControl, self).__init__(parent)
        try:
            self.ip = ni.ifaddresses('eth0')[2][0]['addr']
            
            
        except:
            self.ip = 'No Network '
            
        

# servis etiketleri...........................        
        SSHLabel = QLabel('<center><font color="#2980B9" size="4"> SSH </font></center>')
        HTTPLabel = QLabel('<center><font color="#2980B9" size="4"> HTTP </font></center>')
        FTPLabel = QLabel('<center><font color="#2980B9" size="4"> FTP </font></center>')
        
# servis calisiyor etiketleri ..............................     
     
        self.SSHRLabel = QLabel()
        self.HTTPRLabel =QLabel()
        self.FTPRLabel =QLabel()
        
# servis Buttonlari.....................................        
        self.SSHBtn=QPushButton()
        self.HTTPBtn=QPushButton()
        self.FTPBtn=QPushButton()
        
# servis Buttonlarina tiklandigi zaman gidecekleri fonsiyonlar...................       
        
        self.SSHBtn.clicked.connect(self.SSH_Change)
        self.HTTPBtn.clicked.connect(self.HTTP_Change)
        self.FTPBtn.clicked.connect(self.FTP_Change)        
        
        self.HTTPRestart = QPushButton('Restart')       
        self.FTPRestart = QPushButton('Restart')        
        self.SSHRestart = QPushButton('Restart')
        
        self.SSHRestart.clicked.connect(self.SSH_Restart)
        self.HTTPRestart.clicked.connect(self.Http_Restart)
        self.FTPRestart.clicked.connect(self.Ftp_Restart) 
        
        
        
# logo...................................
        self.label = QLabel()
        self.pixmap = QPixmap(os.getcwd() + '/p2.png')
        self.label.setPixmap(self.pixmap)
    
        
       
        
# ssh kapaliysa kapali yaz... 

        Stringssh = commands.getoutput('/etc/init.d/ssh status')        
        Stringhttp = commands.getoutput('/etc/init.d/lighttpd status')
        Stringftp = os.system('/etc/init.d/vsftpd status')
        
        StringCheck = 'Active: inactive'

        Cssh = Stringssh.find('Active: active')
        Chttp = Stringhttp.find('Active: active')
        Cftp = Stringssh.find('Active: active')

    
        
        if Cssh != -1:
            self.SSHBtn.setText('DURDUR')
            self.SSHRLabel.setText('<center><font color="#2980B9" size="2"> Runing... </font></center>')
            print('Aktif')
    
        else:
            self.SSHBtn.setText('BASLAT')
                       
            
        if Chttp !=-1:
            self.HTTPBtn.setText('DURDUR')
            self.HTTPRLabel.setText('<center><font color="#2980B9" size="2"> Runing... </font></center>')
            print('Aktif')
        else:
            self.HTTPBtn.setText('BASLAT')
            
            
        if Cftp !=-1:
            self.FTPBtn.setText('DURDUR')
            self.FTPRLabel.setText('<center><font color="#2980B9" size="2"> Runing... </font></center>')
            print('Aktif')
        else:
            self.FTPBtn.setText('BASLAT')


    
# alt kisim. ip ve kernel surumleri.............

        self.Text = QTextEdit()
        self.Text.setText('Pardus ARM Servis Kontrol'+'\n'+
                          'Host Name  : ' +
                          str(commands.getoutput("hostname")) + '\n'+
                          'Kernel  : '+
                          str(commands.getoutput("uname -r")) +'\n' 
                          +'IP Adress  : '+ self.ip)
        self.Text.setReadOnly(True)
        
        
        
# grid layout etiketleri ve buttonlari ekliyoruz.....................

        kutu = QHBoxLayout()
        kutu.addStretch(1)
        kutu.addWidget(self.label)
        
        
        grid = QGridLayout()
      #  grid.addWidget(kutu,3,0,0,0)
        grid.addWidget(self.label,3,0,4,4)
        
        grid.addWidget(SSHLabel,3,1)
        grid.addWidget(HTTPLabel,4,1)
        grid.addWidget(FTPLabel,5,1)
        
        grid.addWidget(self.SSHRLabel,3,2)
        grid.addWidget(self.HTTPRLabel,4,2)
        grid.addWidget(self.FTPRLabel,5,2)
        
        grid.addWidget(self.SSHBtn,3,3)
        grid.addWidget(self.HTTPBtn,4,3)
        grid.addWidget(self.FTPBtn,5,3)
        
        grid.addWidget(self.SSHRestart,3,4)
        grid.addWidget(self.HTTPRestart,4,4)
        grid.addWidget(self.FTPRestart,5,4)
        
        
        grid.addWidget(self.Text, 8, 0, 7, 4)      
        
        self.setLayout(grid)        
        self.setWindowTitle('Pardus Servis Control')
        self.setFixedSize(650, 350)
        
        
    def SSH_Change(self):
   
        if(self.SSHBtn.text()=='BASLAT'):
            os.system('/etc/init.d/ssh start')
            self.SSHBtn.setText('DURDUR')
            self.SSHRLabel.setText('<center><font color="#2980B9" size="2"> Runing... </font></center>') 
            
                       
            
        else:
            os.system('/etc/init.d/ssh stop')
            self.SSHRLabel.setText('')            
            self.SSHBtn.setText('BASLAT')
            print('kapandi') 
            
    
    def HTTP_Change(self):
          
        if(self.HTTPBtn.text()=='BASLAT'):
            os.system('/etc/init.d/lighttpd start')
            self.HTTPBtn.setText('DURDUR')
            self.HTTPRLabel.setText('<center><font color="#2980B9" size="2"> Runing... </font></center>') 
                        
            
        else:
            os.system('/etc/init.d/lighttpd stop') 
            self.HTTPBtn.setText('BASLAT')
            self.HTTPRLabel.setText('')
            print('kapandi') 
            
    def FTP_Change(self):
          
        if(self.FTPBtn.text()=='BASLAT'):
            os.system('/etc/init.d/vsftpd start')
            self.FTPBtn.setText('DURDUR')
            self.FTPRLabel.setText('<center><font color="#2980B9" size="2"> Runing... </font></center>') 
            print('acildi')                 
            
        else:
            os.system('/etc/init.d/vsftpd stop') 
            self.FTPBtn.setText('BASLAT')
            self.FTPRLabel.setText('')
            print('kapandi')         

            
            
    def SSH_Restart(self):
        os.system('/etc/init.d/ssh restart') 
        
    def Http_Restart(self):
        os.system('/etc/init.d/lighttpd restart')
        
    def Ftp_Restart(self):
        os.system('/etc/init.d/vsftpd restart')  

    def Close(self):
        
        self.close()
        

uygulama = QApplication([])


pencer = ServiceControl()
pencer.show()  


uygulama.exec_()

"""
if (str1.find(str2)>=0):
  print("True")
else:
  print ("False")
"""      
   # os.system("sudo start ssh")
