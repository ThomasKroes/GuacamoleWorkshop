FROM gw_desktop

MAINTAINER Thomas Kroes "t.kroes@lumc.nl"

ENV DEBIAN_FRONTEND noninteractive

# Install blender
RUN apt-get update
RUN apt-get install blender -y

# Remove xfce panels and run blender maximized
RUN apt-get remove xfce4-panel -y
RUN apt-get install maximus -y

# Install unzipper
RUN apt-get install unzip -y

# Make data dir for the sample data sets
RUN cd /home/ && mkdir data

# Download sample data (obj models courtesy of http://www.oyonale.com/modeles.php?lang=en&page=58)
RUN cd /home/data && wget https://github.com/ThomasKroes/GuacamoleWorkshop/raw/master/watering_can.blend;
RUN cd /home/data && wget https://github.com/ThomasKroes/GuacamoleWorkshop/raw/master/fire_extinguisher.blend;
RUN cd /home/data && wget https://github.com/ThomasKroes/GuacamoleWorkshop/raw/master/shopping_cart.blend;

# Start blender with desktop
COPY blender.desktop /etc/xdg/autostart/
COPY blender.sh /etc/xdg/autostart/
