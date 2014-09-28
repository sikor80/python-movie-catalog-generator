import os 
import json
import urllib
import webbrowser
import sys
import traceback

from media import *
from html import *


def main():
	try:
		default_source_dir = "movies"
		source_dir = raw_input("Enter directory / path: (default: %s):\n" % default_source_dir) or default_source_dir
		if not source_dir:
		    source_dir = default_source_dir

		default_output_file = "movies.html"
		output_file = raw_input("Enter name of output file (default: %s):\n" % default_output_file) or default_output_file
		if not output_file:
		    output_file = default_output_file

		movie_list = os.listdir(source_dir)
		movie_objects_list = []
		failed_movie_objects_list = []

		for movie in movie_list:
			title = movie[0:-7]
			year = movie[-6:][1:-1]
			try:
				## Using API from http://www.omdbapi.com/
				url = "http://www.omdbapi.com/?t=" + title + "&y=" + year
				## Now dowloading and parsing the results as json file so we can work on it locally 
				data = json.load(urllib.urlopen(url))

				try: 
					movie_imdbID = data["imdbID"] 
					## Adding .encode('utf8') otherwise, python errors out complaining about problems with parsing non-ascii chars 
					movie_title = data["Title"].encode('utf8') 
					movie_year = data["Year"]
					movie_director = data["Director"].encode('utf8')
					movie_actors = data["Actors"].encode('utf8')
					movie_plot = data["Plot"].encode('utf8')
					movie_poster = data["Poster"]
					movie_rating = data["imdbRating"]
					movie_object_name = "movie_" + movie_imdbID
					movie_object_name = Movie(movie_title, movie_year, movie_director, movie_actors, movie_plot, movie_poster, movie_rating)
					movie_objects_list.append(movie_object_name)
					print "Success - " + movie
				except:
					failed_movie_objects_list.append(movie)
					print "Failed - " + movie
					pass
			except:
				print "***** Error. Maybe try to run the script again but bit later? *****"
		    	
		try:


			## Opening and generating final html (for example movies.html) file 
			html_file = open(output_file,"w")
			html_file.write(header)

			for movie_object in movie_objects_list:	
				html_file.write('<div class="row">')
				html_file.write('<div class="col-md-4">')
				html_file.write('<div class="thumbnail">')
				html_file.write('<img src="' + movie_object.poster + '" />')
				html_file.write('</div></div>')
				html_file.write('<div class="col-md-8">')
				html_file.write('<h2>' + movie_object.title + ' (' + movie_object.year + ')' + '</h2>')
				html_file.write("<p><b>Plot:</b> " + str(movie_object.plot) + "</p>" )
				html_file.write("<p><b>Actors:</b> " + str(movie_object.actors) + "</p>" )
				html_file.write("<p><b>Director:</b> " + str(movie_object.director) + "</p>" )
				html_file.write("<p><b>Rating:</b> " + str(movie_object.rating) + "</p>" )
				html_file.write("</div></div>")

			## Generate some stats at on the bottom of the html page 
			html_file.write('<hr>')
			html_file.write('<p> Directory scanned: ' + str(os.getcwd()) + '/' + source_dir + '</p>')
			html_file.write('<p> Success entries: ' + str(len(movie_objects_list)) + '</p>')
			html_file.write('<p> Failed entries (below): ' + str(len(failed_movie_objects_list)) + '</p>') 
			html_file.write(str(failed_movie_objects_list))

			html_file.write(footer)
			html_file.close()

			## Opening the browser and presenting the summary html page 
			webbrowser.open('file://' + os.path.realpath(output_file))
		except Exception, e:	
			print e
			print "***** Error. Maybe try to run the script again but bit later? *****"    	
			sys.exit(0)	

    	
	except Exception, e:	
		print e
		print "***** Error. Maybe try to run the script again but bit later? *****"    	
		sys.exit(0)	





if __name__ == "__main__":
    main()





