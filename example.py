
class Annotation(object):
﻿  def __init__(self, pan, tilt, scale, image, parent):
﻿  ﻿  self.pan    = pan
﻿  ﻿  self.tilt   = tilt
﻿  ﻿  self.scale  = scale
﻿  ﻿  self.parent = parent
﻿  ﻿  self.create_button()
﻿  ﻿    
﻿  def create_button(self):
﻿  ﻿  self.button = Button(self.parent.button_frame, image=self.thumb, command=self.button_click)
﻿  ﻿  self.button.pack()
﻿  ﻿  
﻿  def button_click(self):
﻿  ﻿  threading.Thread(target=self.parent.ptz_goto, args=(self.pan, self.tilt, self.scale)).start()
﻿  ﻿  
class DemoGui(object):
﻿  pan   = 0
﻿  tilt  = 0
﻿  oldx  = 0
﻿  oldy  = 0
﻿  grabx = 0
﻿  graby = 0
﻿  panorama_inited = False
﻿  scanning_scene = False
﻿  
﻿  angular_res = 0.002
﻿  
﻿  bridge = CvBridge()
﻿  rospy.init_node('demogui')
﻿  root = Tk()
﻿  root.title('Autoparking for Social Robot')
﻿  root.geometry('+%d+%d' % (24*SCALE, 18*SCALE))
﻿  
﻿  canvas_frame = Frame(height=LIVE_SIZE[1]+PANORAMA_SIZE[1], width=PANORAMA_SIZE[0])
﻿  canvas_frame.pack(side=LEFT)

﻿  panorama_im     = Image.new('RGB', PANORAMA_SIZE, (0,0,0))
﻿  panorama        = ImageTk.PhotoImage(panorama_im)
﻿  panorama_canvas = Canvas(canvas_frame, width=PANORAMA_SIZE[0], height=PANORAMA_SIZE[1], cursor='cross')
﻿  panorama_canvas.create_image(0, 0, image=panorama, anchor=NW)
﻿  panorama_canvas.pack(anchor=NW)
﻿  panorama_images = [] 
﻿  
﻿  info = None
﻿  
﻿  image_lock = threading.Lock()
﻿  info_lock  = threading.Lock()
﻿  
﻿  ptu_client = actionlib.SimpleActionClient('SetPTUState', ptu_control.msg.PtuGotoAction)
﻿  
﻿  rospy.wait_for_service('/chat_cam/set_image_scale')
﻿  image_scale_proxy = rospy.ServiceProxy('/chat_cam/set_image_scale', SetImageScale)

﻿  lut = None

﻿  annotations = []
﻿  
﻿  cv_panorama_inited = False

﻿  def __init__(self):
﻿  ﻿  cv.NamedWindow('win')
﻿  ﻿  
﻿  ﻿  rospy.Subscriber('image', sensor_msgs.msg.Image, self.image_cb)
﻿  ﻿  rospy.Subscriber('camera_info', sensor_msgs.msg.CameraInfo, self.info_cb)
﻿  ﻿  self.ground_truth_pub = rospy.Publisher('ground_truth_pantilt', PanTilt)

﻿  ﻿  self.panorama_canvas.bind('<Button-1>', self.click_event)
﻿  ﻿  self.panorama_canvas.bind('<Double-Button-1>', self.dbl_click_event)
﻿  ﻿  self.panorama_canvas.bind('<Double-Button-3>', self.dbl_rclick_event)
﻿  ﻿  self.panorama_canvas.bind('<Button-4>', lambda e: self.zoom_1(1))
﻿  ﻿  self.panorama_canvas.bind('<Button-5>', lambda e: self.zoom_1(-1))﻿  ﻿  
﻿  ﻿  
﻿  ﻿  self.live_canvas.bind('<Button-4>', lambda e: self.zoom_1(1))
﻿  ﻿  self.live_canvas.bind('<Button-5>', lambda e: self.zoom_1(-1))
﻿  ﻿  self.live_canvas.bind('<B1-Motion>', self.live_canvas_drag)
﻿  ﻿  self.live_canvas.bind('<ButtonRelease-1>', self.live_canvas_drag_end)
﻿  ﻿  self.live_canvas.bind('<Button-1>', self.live_canvas_drag_start)
﻿  ﻿  
﻿  ﻿  self.button_frame = Frame(height=18*SCALE, width=2*SCALE)
﻿  ﻿  self.button_frame.pack(side=TOP)
﻿  ﻿  
﻿  ﻿  scan_button = Button(self.button_frame, text="Scan Scene", command=self.scan_scene)
﻿  ﻿  scan_button.pack(fill=X, anchor=NW)
﻿  ﻿  
﻿  ﻿  annotate_button = Button(self.button_frame, text="Add Annotation", command=self.add_annotation)
﻿  ﻿  annotate_button.pack(fill=X, anchor=NW)
﻿  ﻿    ﻿  
﻿  ﻿  self.scale_widget = Scale(self.button_frame, from_=1, to=5, resolution=0.1, command=self.slider_event)
﻿  ﻿  
﻿  ﻿  self.root.bind_all('<Key>', self.keypress_event)
﻿  ﻿  
﻿  ﻿  # wait for camera info to be ready
﻿  ﻿  while not self.get_info() and not rospy.is_shutdown():
﻿  ﻿  ﻿  rospy.sleep(0.1)
﻿  ﻿  
﻿  ﻿  self.stitcher = PanoramaStitcher(self.get_info(), 0.002)
﻿  ﻿  
﻿  def start(self):
﻿  ﻿  self.root.mainloop()

﻿  def info_cb(self, info):
﻿  ﻿  with self.info_lock:
﻿  ﻿  ﻿  self.info = info

﻿  def get_info(self):
﻿  ﻿  with self.info_lock:
﻿  ﻿  ﻿  return self.info

﻿  def image_cb(self, msg):
﻿  ﻿  try:
﻿  ﻿  ﻿  with self.image_lock:
﻿  ﻿  ﻿  ﻿  self.last_im_time = msg.header.stamp
﻿  ﻿  ﻿  ﻿  in_im = self.bridge.imgmsg_to_cv(msg, "rgb8")
﻿  ﻿  ﻿  ﻿  self.cv_im = in_im
﻿  ﻿  except CvBridgeError, e:
﻿  ﻿  ﻿  rospy.logerr('Error converting image message to cv')
﻿  ﻿  ﻿  return
﻿  ﻿  ﻿  
﻿  ﻿    ﻿  
﻿  def keypress_event(self, event):
﻿  ﻿  if event.char in [str(n) for n in range(1,10)]:
﻿  ﻿  ﻿  num = int(event.char)
﻿  ﻿  ﻿  if len(self.annotations) >= num:
﻿  ﻿  ﻿  ﻿  self.annotations[num-1].button_click()
﻿  ﻿   ﻿  ﻿  
﻿  def dbl_click_event(self, event):
﻿  ﻿  self.zoom_1(10)
﻿  ﻿  self.click_event(event)
﻿  ﻿  
﻿  def dbl_rclick_event(self, event):
﻿  ﻿  self.zoom_1(-10)
﻿  ﻿  self.click_event(event)﻿  
﻿  ﻿  ﻿  
﻿  def click_event(self, event):
﻿  ﻿  threading.Thread(target=self.click_event_inner, args=(event,)).start()
﻿  ﻿  
﻿  def click_event_inner(self, event):
﻿  ﻿  pan, tilt = self.panorama_coords_to_pantilt(event.x, event.y)
﻿  ﻿  self.pan  = pan
﻿  ﻿  self.tilt = tilt
﻿  ﻿  self.ptu_client.send_goal(ptu_control.msg.PtuGotoGoal(pan=pan, tilt=tilt))
﻿  ﻿  rospy.sleep(2)
﻿  ﻿  # self.localize_in_panorama()
﻿    ﻿  
if __name__ == '__main__':
﻿  gui = DemoGui()
﻿  gui.start()
