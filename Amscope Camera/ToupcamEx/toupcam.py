from camera import ToupCamCamera
import os

class UserCamera():

	def __init__(self, root_dir):
		self.initializeMicroscopeCam()
		self.root_dir=root_dir
	
	def initializeMicroscopeCam(self):
		try:
		    cam = ToupCamCamera(resolution=3)
		    cam.open()
		    cam.set_auto_exposure(False)
		    cam.set_exposure_time(200000)
		    cam.set_gain(200)
		    self.microscope_cam = cam
		except:
		    raise RuntimeError("Unable to initialize microscope camera")
		    
	def isMicroscopeCamActive(self):
		return self.microscope_cam is not None
		
	def takeImage(self, foram_num, light_dir, focal_plane, orientation_id):
		if self.isMicroscopeCamActive():
		    base_dir = os.path.join(self.root_dir, foram_num, orientation_id)
		    os.makedirs(base_dir, exist_ok=True)
		    save_loc = os.path.join(base_dir,'{}_{}.tiff'.format(light_dir,focal_plane))
		    im = self.microscope_cam.get_save_tiff(save_loc)
		    
            
if __name__=='__main__':
	#SET THE ROOT_DIR TO WHERE YOU WANT THE IMAGES SAVED
	#my root dir is populated with the current date format as the last folder
	#yyyymmdd_HHMM
	#I just use the python fn: datetime.datetime.now().strftime('%Y%m%d_%H%M')
	
	#root_dir = 
	cam = UserCamera( root_dir)
	cam.takeImage('0','0','0','0')
