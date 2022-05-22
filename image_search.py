from google_images_download import google_images_download

#instantiate the class
response = google_images_download.googleimagesdownload()
arguments = {"keywords":"aeroplane, school bus, dog in front of house",
             "limit":10,"print_urls":False}
paths = response.download(arguments)

#print complete paths to the downloaded images
print(paths)