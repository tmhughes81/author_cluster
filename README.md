# author_cluster
WebApp to visualize clusters of authors utilizing TF-IDF

## Development Status
**Minimal Development Completed**!  As of this update, this project only deploys
a basic Django shell, with no internals.  Watch this space for updates on
development status.

# Deployment
There is no current publicly available running instance of this WebApp.  However, you
are free to deploy your own version of it to any hosting service that can take a
[Docker](https://www.docker.com) image.  The image is hosted on
[Docker Hub](https://hub.docker.com/r/tmhughes81/author_cluster/), and can be pulled
from the public repositories by pulling `tmhughes81/author_cluster`.

# Dependencies

* [Python](https://www.python.org/downloads/release/python-2713/) - 2.7.13

* [Django](https://www.djangoproject.com)

* (Optional) [Docker](https://www.docker.com)

# Environment Setup
For security reasons, a number of settings are set via environmental variables, and not
inside of settings.py.  If you are going to run your own copy of this software, you must
set the following environmental variables.


For security reasons, a number of settings are set via environmental variables, and not
inside of settings.py.  If you are going to run your own copy of this software, you must
set the following environmental variables.

* SECRET_KEY -- Django secret key
* GOOGLE_OAUTH2_CLIENT_SECRET -- Used for Google oauth2 authentication
* GOOGLE_OAUTH2_CLIENT_ID -- Used for Google oauth2 authentication
* DATABASE_PORT -- Port to access Django's MySQL Database
* DATABASE_HOST -- Host of Django's MySQL Database
* DATABASE_PASSWORD -- Password to access Django's MySQL Database
* DATABASE_USER -- User to access Django's MySQL Database
* DATABASE_NAME -- Name of Django's MySQL Database

# Licenses
## Visualizations
The visualizations from this program are available under 
[Creative Commons Attribution 2.0](https://creativecommons.org/licenses/by/2.0/legalcode).
A summary of the license is available [here](https://creativecommons.org/licenses/by/2.0/).

## Code
### New BSD License

Copyright (c) 2017, Thomas M Hughes
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of 
conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this list 
of conditions and the following disclaimer in the documentation and/or other materials 
provided with the distribution.

* Neither the name of Thomas M Hughes nor the names of any contributors may be used to 
endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THOMAS M HUGHES BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
