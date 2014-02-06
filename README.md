Installation:

install PyWPS
   I use version 3.2
   See http://pywps.wald.intevation.org/

Update python
   a recent version of the requests library is needed

Edit the Makefile 

Edit wps/pywps.cfg
   The line "serveraddress" need to match your server name and the WEB_PATH in the Makefile

sudo make install

Test the installation with the provided test-pages.
   http://crisma.ait.ac.at/models/



