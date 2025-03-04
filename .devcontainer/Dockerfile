FROM ubuntu:jammy-20240627.1

# Set Non-Interactive Mode
ARG DEBIAN_FRONTEND=noninteractive

# Set Timezone
ARG TZ="America/Chicago"
RUN echo "${TZ}" > /etc/localtime && \
    echo "${TZ}" > /etc/timezone

# Install Required Ubuntu Packages
RUN apt-get update && apt-get install --no-install-recommends -y dotnet-sdk-8.0 \
    python3 \ 
    python-is-python3 \
    python3-pip \
    gnome-keyring \
    sqlite3 \ 
    nano \ 
    net-tools \ 
    git \ 
    ssh \
    git-lfs \
    libexpat1 \ 
    apt-transport-https \ 
    software-properties-common \ 
    wget \ 
    unzip \ 
    ca-certificates \ 
    build-essential \ 
    cmake \ 
    libtbb-dev \ 
    libatlas-base-dev \ 
    libgtk2.0-dev \ 
    libavcodec-dev \ 
    libavformat-dev \ 
    libswscale-dev \ 
    libdc1394-dev \ 
    libxine2-dev \ 
    libv4l-dev \ 
    libtheora-dev \ 
    libvorbis-dev \ 
    libxvidcore-dev \ 
    libopencore-amrnb-dev \ 
    libopencore-amrwb-dev \ 
    x264 \ 
    libtesseract-dev \ 
    libgdiplus

# Install required python libraries
RUN pip install matplotlib \
    numpy \
    noise

# Set Labels
LABEL authors="WAW"
LABEL maintainer="willweidler@mst.edu"
LABEL org.opencontainers.image.source=https://github.com/wiidler/DigginDeepApp
LABEL org.opencontainers.image.licenses=GPL-3.0-only
LABEL org.opencontainers.image.version="v0.0.1"
LABEL org.opencontainers.image.description="Docker Image for Ubuntu Blazor Server Development"
