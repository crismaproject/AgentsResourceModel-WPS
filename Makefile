############################################################
# /home/peter/_work/CRISMA-sw/indicators-py/Makefile
# Peter Kutschera, Thu Feb  6 12:42:00 2014
# Time-stamp: "2014-02-06 13:55:42 peter"
# 
# Peter.Kutschera@ait.ac.at
# © Peter Kutschera
#############################################################

WPS_DIR = /usr/local/wps/models
WEB_DIR = /home/crisma/public_html/models

install: install_wps install_web

install_wps:
	@echo "Setup WPS processes"
	[ -d $(WPS_DIR) ] || mkdir $(WPS_DIR)
	[ -d $(WPS_DIR)/processes ] || mkdir $(WPS_DIR)/processes
	install -p wps/pywps.cfg $(WPS_DIR)
	install -p wps/processes/__init__.py $(WPS_DIR)/processes
	install -p wps/processes/AgentsResourceModel.py $(WPS_DIR)/processes

install_web:
	@echo "Setup web page"
	[ -d $(WEB_DIR) ] || mkdir $(WEB_DIR)
	install -p web/pywps.cgi $(WEB_DIR)
	install -p web/jquery-1.10.2.min.js $(WEB_DIR)
	install -p web/AgentsResourceModel.html $(WEB_DIR)

clean:
	rm -rf $(WPS_DIR) $(WEB_DIR)

.PHONY: install clean
