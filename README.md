# Elastic-Cluster-RESTAPI framework

Elastic Horovod를 이용하여 분산 학습을 진행할 때 GPU를 dynamic하게 scaling in/out을 하기 위해 현재 동작 중인 Elastic Horovod의 상태를 파악해야 됩니다.

Elastic-Cluster-Framework는 이를 동적으로 파악해서 보여주는 interface와 그 정보를 가지고 Elastic Horovod에서 여러 개의 node에서 학습하고 있는 worker의 수를 버튼 하나로 scaling in/out 할 수 있는 API를 제공합니다.
  
## Setting

해당 framework를 이용하기 위해 Elastic Horovod를 동작할 수 있는 환경 세팅과 여러 Python 라이브러리의 설치가 필요합니다.

1. [Elastic Horovod](https://horovod.readthedocs.io/en/stable/elastic_include.html)  
Framework를 개발하며 Elastic Horovod가 설치된 docker image를 이용하여 docker container 환경에서 작업하였습니다. 기존에 Elastic Horovod를 이용하여 연구를 진행하셨던 CSL 김경록님께서 정리해놓으신 notion 링크를 첨부하겠습니다. 해당 링크의 내용에는 Elastic Horovod를 설치 및 세팅하는 방법에 대해 자세히 설명되어 있습니다.
>+ [notion link](https://discreet-file-a73.notion.site/Elastic-Horovod-6ae5f2c3dac04b62b0f4605cf65b0d36)

2. Python 라이브러리 설치  
REST-API를 이용하기 위해 몇 가지 파이썬 라이브러리가 필요합니다. 필요한 라이브러리의 목록은 다음과 같습니다.  
+ Flask  
+ uwsgi  
+ nginx  
  
## How to Run

Elastic Horovod가 학습하는 동안 REST-API Server와 지속적으로 상호작용을 해야 합니다.
따라서, 해당 framework를 사용하기 위해서는 우선 REST-API Server가 실행되어 web page를 띄워준 뒤, horovodrun 명령어를 통해 Elastic Horovod가 학습을 시작한 뒤 REST-API를 통해 서로 상호작용 합니다.
이와 같은 실행 과정을 순서대로 설명하면 다음과 같습니다.

우선, REST-API Server를 실행하는 방법에 대해 설명하겠습니다. uwsgi.ini 파일은 /EC-MaS/REST-API-Server-pkg에 위치하고, nginx의 환경 설정을 위한 nginx.conf 파일은 해당 레포지토리 내부에 있습니다.

1. uwsgi

```sh
uwsgi --ini <path-to-uwsgi.ini>
```

2. nginx

```sh
nginx
```

3. horovodrun

```sh
horovodrun -p <SSH port number> --network-interface <nic> -np <num_proc> --min-np <min_num> --max-np <max_num> --host-discovery-script <path-to-job-script> sh <path-to-run-script>
```
  
## About EC-MaS(Elastic Cluster - Monitoring and Scaling)

앞서 framework의 동작 방법에 대해 설명했는데, 해당 파트에서는 소스 코드에 대해 자세히 설명하겠습니다.

1. GPU_monitoring   
해당 패키지는 GPU status를 확인하기 위해 생성되는 데몬을 생성하고 관리하는 역할을 합니다.
패키지 내부의 gpustat_daemon.py를 통해 데몬을 생성합니다.
해당 코드에서 gpustat 명령어를 통해 GPU status에 대한 정보를 얻는데. 해당 부분을 수정함으로써 원하는 경로로 설정할 수 있습니다.
```sh
...
gpustat_open_string = "SR-Elastic-Cluster-Framework/EC-MaS/Job_control/" + local_ip + "_gpustat.json"
gpustat_file_string = "gpustat --json > " + gpustat_open_string
...
```

2. Job_control  
해당 패키지는 job을 관리하는 역할을 합니다.
패키지 내부 hosts_scripts 디렉토리 내부에 위치한 script 파일은 각각 하나의 job을 나타냅니다.
script 파일을 통해 horovodrun 명령어를 이용하여 학습 job을 실행합니다.
파일의 형식은 다음과 같습니다.
```sh
echo 115.145.178.217:2
echo 115.145.178.218:3
```

다음으로 del_files.py의 역할은 이전 학습에서 사용된 log 파일을 삭제하는 것입니다.  
마지막으로, run.sh 파일에 포함된 내용은 앞서 설명한 del_files.py 및 rm 명령어를 통해 이전 학습에서 사용된 log 파일을 삭제하고, 메인 학습 코드를 실행합니다.
다양한 학습 코드에 해당 framework를 적용하려면 해당 부분을 수정해주면 됩니다.
해당 레포지토리에는 resnet50 모델을 예시로 사용하였습니다.
해당 framework의 최대 장점은 5줄의 코드 수정 만으로 기존 코드에 적용할 수 있다는 것입니다.
5줄의 코드 내부에 들어갈 인자는 간단한 소스 코드 수정을 통해 사용자의 필요성에 맞게 조정할 수 있습니다.
학습 코드에 추가해야하는 5줄의 코드는 다음과 같습니다.
```sh
from GPU_monitoring_daemon import gpustat_daemon as dmn
dmn.start_daemon(hvd.local_rank())
```

```sh
from Log_monitoring import log_control as lc
lc.local_log_save(...)
lc.web_post(...)
```
+) 해당 코드에서 import를 위해 sys.path에 패키지의 경로를 추가해야합니다.  

3. Log_monitoring  
해당 패키지는 학습 로그를 관리하는 역할을 합니다.
log_control.py 파일 내부에 학습 도중 로그를 출력하는 내용에 대한 코드가 작성되어 있습니다.
이를 학습 코드 callback 함수 내부에 추가하면 학습 도중에 로그를 출력하고 수집할 수 있습니다.
로컬에 로그를 저장하는 동작, REST-API 서버로 로그를 전달하는 역할 두 가지를 수행합니다.

4. REST_API_Server  
해당 패키지는 REST-API 서버 동작을 위해 필요한 코드를 포함하고 있습니다.
우선, static/js 디렉토리 내부에 위치한 javascript 파일은 GPU status와 로그를 웹 대시보드에서 그래프를 통해 보여주는 역할을 합니다.  
templates 내부에는 웹 대시보드 동작에 필요한 html 파일이 있습니다.  
다음으로는 서버 동작의 메인이라고 할 수 있는 dashboard_flask.py 파일입니다.
웹 대시보드에서 사용자가 요청하는 스케일링 정보를 처리하고, 현재 실행 중인 job / job 변경 로그 정보를 실시간으로 보여주는 역할 또한 수행하며 GPU status 및 로그 정보를 시각적으로 보여주는 그래프를 나타내는 역할을 합니다.

## horovodrun & Web Dashboard
아래 사진은 Elastic Horovod와 Web dashboard가 동작하는 것입니다.

![스크린샷, 2022-12-19 03-16-46](https://user-images.githubusercontent.com/30406090/208312830-7a2bac14-fd54-4e89-b171-e555cb15b904.png)  
![스크린샷, 2022-12-19 13-22-35](https://user-images.githubusercontent.com/30406090/208347088-73c31def-4b35-4980-b9bb-a99fe69d68aa.png)





