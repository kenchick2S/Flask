from flask import Flask, render_template, request, session, json, redirect, url_for
import os
import time
import cv2
import numpy as np

# import photo_process

app=Flask(__name__)
app.secret_key= b'123456'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',methods=['POST','GET'])
def register():
	with open('./static/member.json','r') as file_object:
		member = json.load(file_object)
	if request.method=='POST':
		if request.values['send']=='送出':
			if request.values['userid'] in member:
				for find in member:
					if member[find]['nick']==request.values['username']:
						return render_template('register.html',alert='this account and nickname are used.')
				return render_template('register.html',alert='this account is used.',nick=request.values['username'])
			else:
				for find in member:
					if member[find]['nick']==request.values['username']:
						return render_template('register.html',alert='this nickname are used.',id=request.values['userid'],pw=request.values['userpw'])
				member[request.values['userid']]={'password':request.values['userpw'],'nick':request.values['username']}
				with open('./static/member.json','w') as f:
				    json.dump(member, f)
				basepath = os.path.join(os.path.dirname(__file__), 'static','uploads')
				os.mkdir(os.path.join(basepath,request.values['userid']))
				return render_template('index.html')
	return render_template('register.html')

@app.route('/login',methods=['GET','POST'])
def login():

	if request.method== 'POST' :

		session['width']=request.values['bodywidth']
		session['edit']=False

		with open('./static/member.json','r') as file_object:
			member = json.load(file_object)

		if request.values['userid'] in member:
			if member[request.values['userid']]['password']==request.values['userpw']:
				session['username']=request.values['userid']
				return redirect ( url_for ( 'index' ))
			else:
				return render_template('login.html',alert="Your password is wrong, please check again!")
		else:
			return render_template('login.html',alert="Your account is unregistered.")
	return render_template('login.html')

@app.route('/logout',methods=['GET','POST'])
def logout ():
	if request.method=='POST':
		if request.values['send']=='確定':
			# session.pop('username',None)
			session['username'] = False
		return redirect(url_for('index'))
	return render_template('logout.html')

@app.route('/upload/',methods=['GET','POST'])
def upload():

	basepath = os.path.join(os.path.dirname(__file__), 'static','uploads')
	dirs=os.listdir(os.path.join(basepath,session.get('username')))
	dirs.insert(0,'New Folder')
	dirs.insert(0,'Not Choose')

	if request.method == 'POST':
		flist = request.files.getlist("file[]")
		
		for f in flist:
			try:
				# basepath = os.path.join(os.path.dirname(__file__), 'static','uploads')
				basepath = "./static/uploads"
				format=f.filename[f.filename.index('.'):]
				fileName=time.time()
				if format in ('.jpg','.png','.jpeg','.HEIC','.jfif'):
					format='.jpg'
				else:
					format='.mp4'
					

				if request.values['folder']=='0':
					return render_template('upload.html',alert='Please choose a folder or creat a folder',dirs=dirs)

				elif request.values['folder']=='1':
					if not os.path.isdir(os.path.join(basepath,session.get('username'),request.values['foldername'])):
						os.mkdir(os.path.join(basepath,session.get('username'),request.values['foldername']))
						os.mkdir(os.path.join(basepath,session.get('username'),request.values['foldername'],'video'))
						os.mkdir(os.path.join(basepath,session.get('username'),request.values['foldername'],'photo'))
						os.mkdir(os.path.join(basepath,session.get('username'),request.values['foldername'],'album'))
						os.mkdir(os.path.join(basepath,session.get('username'),request.values['foldername'],'album','video'))
						os.mkdir(os.path.join(basepath,session.get('username'),request.values['foldername'],'album','photo'))

					if format == '.mp4':
						upload_path = os.path.join(basepath,session.get('username'),request.values['foldername'],'video',str(fileName).replace('.','')+str(format))
						album_path = os.path.join(basepath,session.get('username'),request.values['foldername'],'album','video',str(fileName).replace('.','')+'.jpg')
						
					else:
						upload_path = os.path.join(basepath,session.get('username'),request.values['foldername'],'photo',str(fileName).replace('.','')+str(format))
						album_path = os.path.join(basepath,session.get('username'),request.values['foldername'],'album','photo',str(fileName).replace('.','')+str(format))
											
				else:
					if format == '.mp4':
						upload_path = os.path.join(basepath,session.get('username'),dirs[int(request.values['folder'])],'video',str(fileName).replace('.','')+str(format))
						album_path = os.path.join(basepath,session.get('username'),dirs[int(request.values['folder'])],'album','video',str(fileName).replace('.','')+'.jpg')
					else:
						upload_path = os.path.join(basepath,session.get('username'),dirs[int(request.values['folder'])],'photo',str(fileName).replace('.','')+str(format))
						album_path = os.path.join(basepath,session.get('username'),dirs[int(request.values['folder'])],'album','photo',str(fileName).replace('.','')+str(format))
					
				f.save(upload_path)
				if format =='.mp4':
					video_photo(upload_path,album_path)
				else:
					image=cv2.imread(upload_path)
					fill_photo(image,album_path)

			except:
				return render_template('upload.html',alert='你沒有選擇要上傳的檔案',dirs=dirs)

		return redirect(url_for('upload'))
	return render_template('upload.html',dirs=dirs)

@app.route('/album/', methods=['POST', 'GET'])
def album():

	colspan=int(int(session.get('width'))/150)
	if colspan>7:
		colspan=7
	# basepath = os.path.join(os.path.dirname(__file__), 'static','uploads')
	basepath = "./static/uploads"
	dirs=os.listdir(os.path.join(basepath,session.get('username')))
	dirs.insert(0,'ALL')
	dirs.insert(0,'')

	dict2={} #record all folder has what number name

	for dir in dirs:
		if dir == "ALL" or dir == '':
			continue
		dict2[dir]={'photo':[],'video':[]}
		path=os.path.join(basepath,session.get('username'),dir,'photo')
		for lists in os.listdir(path):
			dict2[dir]['photo'].append(lists)
		path=os.path.join(basepath,session.get('username'),dir,'video')
		for lists in os.listdir(path):
			dict2[dir]['video'].append(lists)
	if request.method == 'POST':
		if request.values['folder']!='0' and request.values['folder']!='1':
			return render_template('album.html',dirs=dirs,colspan=colspan, \
				filefolder=[dirs[int(request.values['folder'])]],files=dict2,username=session.get('username'))
		elif request.values['folder'] =='1':
			return render_template('album.html',dirs=dirs, colspan=colspan,\
				filefolder=dirs[2:],files=dict2,username=session.get('username'))
	return render_template('album.html',dirs=dirs, files=dict2, filefolder=dirs[2:],colspan=colspan,username=session.get('username'))

@app.route('/stream/<folder>/<name>',methods=['GET','POST'])
def stream(folder,name):
	# basepath = os.path.join(os.path.dirname(__file__),'static','uploads')
	basepath = "./static/uploads"

	dirs=os.listdir(os.path.join(basepath,session.get('username')))
	dirs.insert(0,'')

	fileName=[]
	for lists in os.listdir(os.path.join(basepath,session.get('username'),folder,'photo')):
		sub_path = os.path.join(os.path.join(basepath,session.get('username'),folder,'photo'),lists)
		fileName.append(lists)
	for lists in os.listdir(os.path.join(basepath,session.get('username'),folder,'video')):
		sub_path = os.path.join(os.path.join(basepath,session.get('username'),folder,'video'),lists)
		fileName.append(lists)

	if request.method=='POST':
		if request.values['folder'] !='0':
			folder=dirs[int(request.values['folder'])]
			fileName.clear()
			fileName=[]
			for lists in os.listdir(os.path.join(basepath,session.get('username'),folder,'photo')):
				sub_path = os.path.join(os.path.join(basepath,session.get('username'),folder,'photo'),lists)
				fileName.append(lists)
			for lists in os.listdir(os.path.join(basepath,session.get('username'),folder,'video')):
				sub_path = os.path.join(os.path.join(basepath,session.get('username'),folder,'video'),lists)
				fileName.append(lists)
			name=fileName[0]
		elif request.values['next']=='往前':
			name=fileName[(fileName.index(name))-1]
		elif request.values['next']=='往後':
			name=fileName[(fileName.index(name))+1]
		return redirect(url_for('stream',folder=folder,name=name))
	return render_template('stream.html',dirs=dirs,name=name,folder=folder,fileName=fileName,username=session.get('username'))
#=======================================================
def video_photo(video_path,out_path):
	max_width=150

	cap = cv2.VideoCapture(video_path)
	video_width = int(cap.get(3))

	ratio = max_width * 1.0 / video_width

	ret, frame = cap.read()
	image=cv2.resize(frame, None, fx=ratio, fy=ratio)
	cap.release()

	fill_photo(image,out_path)

def fill_photo(img,out_path):

	h,w=img.shape[0],img.shape[1]
	side=max(h,w)
	new = np.zeros((side,side,3), np.uint8)
	new.fill(255)
	if w>h:
		center=((side-h)/2.0)
		for i in range(img.shape[0]):
			for j in range(img.shape[1]):			
				new[int(i+center),j]=img[i,j]
	else:
		center=((side-w)/2.0)
		for i in range(img.shape[0]):
			for j in range(img.shape[1]):			
				new[i,int(j+center)]=img[i,j]

	print("save video")
	cv2.imwrite(out_path, new)

if __name__ == '__main__':
	app.run(host='0.0.0.0',port='5000',debug=True)