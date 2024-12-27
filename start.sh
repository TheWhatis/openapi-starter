#!/usr/bin/sh
#==
#   NOTE      - start
#   Author    - Whatis
#
#   Created   - 2024.12.26
#   Github    - ...
#   Contact   - asdwdagwahwabe@gmail.com
#/

root=$(dirname $0);

openapiConfig="$root/openapi/openapi.yaml"
outputDir="$root/openapi/decomposed"
apiName=NO
decompose=YES
port=8080

while [[ $# -gt 0 ]]; do
    case $1 in
        -nd|--no-decompose)
            decompose=NO
            shift
            ;;
        -c|--config)
            openapiConfig="$2"
            shift
            shift
            ;;
        -o|--output)
            outputDir="$2"
            shift
            shift
            ;;
        --api)
            apiName="$2"
            shift
            shift
            ;;
        -p|--port)
            port="$2"
            shift
            shift
            ;;
    esac
done

if [ $decompose == YES ]; then
    sh "$root/split.sh" $openapiConfig $outputDir
fi

if [ $apiName == NO ]; then
    npm start -- --port=$port
else
    npm start $apiName -- --port=$port
fi
