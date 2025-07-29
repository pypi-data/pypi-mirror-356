from AFL.automation.loading.SyringePump import SyringePump
from AFL.automation.loading.SerialDevice import SerialDevice
import time

class NE1kSyringePump(SyringePump):

    def __init__(self,port,syringe_id_mm,syringe_volume,baud=9600,daisy_chain=None,pumpid=None,flow_delay=5):
        '''
            Initializes and verifies connection to a New Era 1000 syringe pump.

            port = serial port reference

            syringe_id_mm = syringe inner diameter in mm, used for absolute volume. 
                            (will re-program the pump with this diameter on connection)

            syringe_volume = syringe volume in mL

            baud = baudrate for connection

            daisy_chain = used for the 'party-line' mode on these pumps where a string of pumps is on one serial port.
                            when setting up daisy chaining:
                                connect to the first pump on a port with daisy_chain = False
                                on subsequent pumps, set daisy_chain to the pump with a hardware connection (the first pump)
                                    or any other pump on the string.
                                note: when daisy chaining you should probably set pumpid explicitly rather than autodiscovering
                                    as most likely the autodiscovery will return the first pump id each time.

            pumpid = the ID configured in the pump firmware.  If not set, will attempt to auto-discover a pump.  
                    setting pumpid will save some time on connection and probably result in more reproducible 
                    behavior.  Practically mandatory for daisy chain mode.


        '''
        self.app = None
        self.name = 'NE1kSyringePump'
        self.pumpid = pumpid
        self.flow_delay = flow_delay
        if daisy_chain is not None:
            self.serial_device = daisy_chain.serial_device
        else:
            self.serial_device = SerialDevice(port,baudrate=baud,timeout=0.5)

        # try to connect

        if self.pumpid is None:
            for i in range(75):
                   if len(self.serial_device.sendCommand('%iADR\x0D'%i))>0:
                    self.pumpid = i
                    break
        else:
            if len(self.serial_device.sendCommand('%iADR\x0D'%self.pumpid))==0:
                raise NoDeviceFoundException


        assert self.pumpid is not None, "Error: no answer from any of the first 75 pumps.  Is speed correct?"
          # reset diameter
        self.syringe_id_mm = syringe_id_mm
        self.syringe_volume = syringe_volume

        self.stop()#stop the pump
        self.serial_device.sendCommand('%iDIA %.02f\x0D'%(self.pumpid,syringe_id_mm)) #set the diameter
        readback = self.serial_device.sendCommand('%iDIA\x0D'%self.pumpid) #readback
        dia = float(readback[4:-1])
        assert dia==syringe_id_mm, "Warning: syringe diameter set failed.  Commanded diameter "+str(syringe_id_mm)+", read back "+str(dia)

    def stop(self):
        '''
        Abort the current dispense/withdraw action. Equivalent to pressing stop button on panel.
        '''
        self.serial_device.sendCommand('%iSTP\x0D'%self.pumpid,questionmarkOK=True) 

    def withdraw(self,volume,block=True,delay=True):
        if self.app is not None:
            rate = self.getRate()
            self.app.logger.debug(f'Withdrawing {volume}mL at {rate} mL/min')

        self.serial_device.sendCommand('%iVOLML\x0D'%self.pumpid)
        self.serial_device.sendCommand('%iVOL %.03f\x0D'%(self.pumpid,volume))
        self.serial_device.sendCommand('%iDIRWDR\x0D'%self.pumpid)
        self.serial_device.sendCommand('%iRUN\x0D'%self.pumpid)
        if block:
            self.blockUntilStatusStopped()
        if delay:
            time.sleep(self.flow_delay)
        
    def dispense(self,volume,block=True,delay=True):
        if self.app is not None:
            rate = self.getRate()
            self.app.logger.debug(f'Dispensing {volume}mL at {rate} mL/min')
        self.serial_device.sendCommand('%iVOLML\x0D'%self.pumpid)
        self.serial_device.sendCommand('%iVOL%.03f\x0D'%(self.pumpid,volume))
        self.serial_device.sendCommand('%iDIRINF\x0D'%self.pumpid)
        self.serial_device.sendCommand('%iRUN\x0D'%self.pumpid)
        if block:
            self.blockUntilStatusStopped()
        if delay:
            time.sleep(self.flow_delay)
        
    def setRate(self,rate):
        if self.app is not None:
            self.app.logger.debug(f'Setting pump rate to {rate} mL/min')
        self.serial_device.sendCommand('%iRAT%.02fMM\x0D'%(self.pumpid,rate),debug=True)
        if self.getRate()!=rate:
            raise ValueError('Pump rate change failed')

    def getRate(self):
        output = self.serial_device.sendCommand('%iRAT\x0D'%self.pumpid)
        units = output[-3:-1]
        if units=='MM':
            rate = float(output[4:-3])
        elif units=='UM':
            rate = float(output[4:-3])/1000
        elif units=='MH':
            rate = float(output[4:-3])/60
        elif units=='UH':
            rate = float(output[4:-3])/60/1000
        else:
            raise ValueError(f'Rate units not supported in getRate: {units}')
        return rate

    def emptySyringe(self):
        self.dispense(self.syringe_volume*0.9)

    def blockUntilStatusStopped(self,pollingdelay=0.2):
        statuschar = 'X'
        while statuschar is not 'S':
            time.sleep(pollingdelay)
            statuschar = self.getStatus()[0]

    def getStatus(self):
        '''
        query the pump status and return a tuple of the status character, 
        infused volume, and withdrawn volume)
        '''

        dispensed = self.serial_device.sendCommand('%iDIS\x0D'%self.pumpid)
        # example answer: 10SI0.000W20.00ML
        statuschar = dispensed[3]
        infusedvol = float(dispensed[5:10])
        withdrawnvol = float(dispensed[11:16])

        return(statuschar,infusedvol,withdrawnvol)




