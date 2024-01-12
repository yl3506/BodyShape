from PIL import Image
import os

rootpath = '/Users/yichen/Downloads/images/' # image size 1000 W x 400 H
outpath = '/Users/yichen/Downloads/images_merged/'
left1, top1, right1, bottom1 = 100, 0, 600, 400
left2, top2, right2, bottom2 = 400, 0, 900, 400
filenames = [f for f in os.listdir(rootpath) if os.path.isfile(os.path.join(rootpath, f))]
initfilenames = [f for f in filenames if "_init.png" in f]
print(initfilenames)

for file in initfilenames:
	# load init and out image
	initimage = Image.open(os.path.join(rootpath, file))
	if "_no_change" in file: # nochange image's init and out are same
		outimage = Image.open(os.path.join(rootpath, file))
	else:
		outimage = Image.open(os.path.join(rootpath, file[:-8]+'out.png'))
	
	# crop init image and out image differently
	initcropped = initimage.crop((left1, top1, right1, bottom1))
	outcropped = outimage.crop((left2, top2, right2, bottom2))
	
	# merge the cropped image
	merged = Image.new(outcropped.mode, (outcropped.width * 2, outcropped.height))
	merged.paste(initcropped, (0, 0))
	merged.paste(outcropped, (outcropped.width, 0))
	merged.save(os.path.join(outpath, file[:-9]+'.png'))





