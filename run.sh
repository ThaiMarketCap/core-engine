docker stop thcap1
docker rm thcap1

# Run interactive (debug)
# docker run -it --name thcap1 -p 4017:5000 optjar/thcap

# Run as daemon
docker run -d --name thcap1 -e "TZ=Asia/Bangkok" -p 4017:5000 optjar/thcap
