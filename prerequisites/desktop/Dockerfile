FROM ubuntu:16.10

MAINTAINER Thomas Kroes <t.kroes@lumc.nl>

ENV DEBIAN_FRONTEND noninteractive

ENV HOME /home/ubuntu

RUN apt-get update
RUN apt-get upgrade -y

# Add linux-mint dependencies and update packages
#RUN apt-key adv --recv-key --keyserver keyserver.ubuntu.com "3EE67F3D0FF405B2"
#RUN echo "deb http://packages.linuxmint.com/ rafaela main upstream import" >> /etc/apt/sources.list.d/mint.list
#RUN echo "deb http://extra.linuxmint.com/ rafaela main " >> /etc/apt/sources.list.d/mint.list

# Package management
RUN apt-get install python-software-properties -y
RUN apt-get install software-properties-common -y

RUN apt-get update

# Install xfce and vnc
RUN apt-get install xfce4 -y
RUN apt-get install xfce4-goodies -y
RUN apt-get install x11vnc -y
RUN apt-get install xvfb -y

# Miscellaneous tools
RUN apt-get install wget -y
RUN apt-get install curl -y
RUN apt-get install gedit -y
RUN apt-get install supervisor -y
RUN apt-get install openssh-server -y

# Screensaver uses too much resources so remove it
RUN apt-get remove xscreensaver -y

# Change to xfce terminal emulator
RUN apt-get install xfce4-terminal -y
RUN echo 4 | update-alternatives --config x-terminal-emulator

# Install firefox
RUN apt-get install firefox -y

# Cleanup
RUN apt-get autoclean -y
RUN apt-get autoremove -y
RUN rm -rf /var/lib/apt/lists/*

# Add startup script and supervisor configuration file
ADD startup.sh /root
ADD supervisord.conf /root

# Add configuration files for vnc and xfce
ADD .vnc /root/.vnc
ADD .config /root/.config

# Handle configuration files permissions
RUN chmod +x /root/.vnc/xstartup /etc/X11/xinit/xinitrc

# Expose ports for vnc and ssh
EXPOSE 5900
EXPOSE 22

# Launch startup script when container is started
ENTRYPOINT ["/root/startup.sh"]
