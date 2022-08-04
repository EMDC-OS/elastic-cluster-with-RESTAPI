# ElasticHorovod-RESTAPI-tool

Elastic Horovod를 이용하여 분산 학습을 진행할 때 worker를 dynamic scaling in/out을 하기 위해 현재 동작 중인 Elastic Horovod의 상태를 파악해야 됩니다.

ElasticHorovod-RESTAPI-tool은 이를 동적으로 파악해서 보여주는 interface와 그 정보를 가지고 Elastic Horovod에서 여러 개의 node에서 학습하고 있는 worker의 수를 버튼 하나로 scaling in/out 할 수 있는 API를 제공합니다.

학습의 효율성을 높이기 위해 worker를 scaling in/out 하는 시기를 결정하는 알고리즘을 연구하는데 해당 tool을 사용할 수 있습니다. 이를 통해 분산 학습 클라우드를 효과적으로 관리할 수 있는 platform을 만들 수 있을 것으로 기대하고 있습니다.  

## Setting

해당 tool을 이용하려면 Elastic Horovod를 이용할 수 있는 환경과 여러 Python 라이브러리의 설치가 필요합니다.

1. [Elastic Horovod](https://horovod.readthedocs.io/en/stable/elastic_include.html)  
tool을 개발하며 Elastic Horovod가 설치된 docker image를 이용하여 docker container 환경에서 작업하였습니다. 기존에 Elastic Horovod를 이용하여 연구를 진행하셨던 CSL 김경록님께서 정리해놓으신 notion 링크를 첨부하겠습니다. 해당 링크의 내용을 참고한다면 쉽게 환경을 설정할 수 있습니다.
>+ [notion link](https://discreet-file-a73.notion.site/Elastic-Horovod-6ae5f2c3dac04b62b0f4605cf65b0d36)

2. Python 라이브러리 설치  
REST-API를 이용하기 위해 몇 가지 파이썬 라이브러리가 필요합니다. 필요한 라이브러리와 설정 방법은 다음과 같습니다.  
+ Flask  
+ uwsgi  
+ nginx  

## How to Run

Elastic Horovod가 학습하는 동안 Web Server와 지속적으로 상호작용을 해야 합니다.
따라서, 해당 tool을 사용하기 위해서는 Web Server가 우선 실행되어 Web page를 띄워주고 horovodrun 명령어를 통해 Elastic Horovod가 학습을 시작한 뒤 Web page와 상호작용 합니다.
이와 같은 실행 과정을 순서대로 설명하면 다음과 같

우선, Web Server를 실행하는 방법에 대해 설명하겠습니다.

1. uwsgi

```sh
uwsgi --ini <path-to-uwsgi.ini>
```

2. nginx

```sh
nginx
```

3. run.sh

```sh
horovodrun -p <SSH port number> --network-interface <nic> -np <num_proc> --min-np <min_num> --max-np <max_num> --host-discovery-script <path-to-script> python <path-to-run-script>
```

## Result
