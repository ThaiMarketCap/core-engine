docker stop thcap1
docker rm thcap1

# Run interactive (debug)
# docker run -it --name thcap1 -p 7342:8000 optjar/thcap

# Run as daemon
docker run -d --name thcap1 -e "TZ=Asia/Bangkok" -p 7349:8000 optjar/thcap
