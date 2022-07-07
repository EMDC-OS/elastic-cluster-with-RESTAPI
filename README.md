# ElasticHorovod-RESTAPI-tool

Elastic Horovod를 이용하여 분산 학습을 진행할 때 worker를 dynamic scaling in/out을 하기 위해 현재 동작 중인 Elastic Horovod의 상태를 파악해야됩니다.

ElasticHorovod-RESTAPI-tool은 이를 동적으로 파악해서 보여주는 interface와 그 정보를 가지고 Elastic Horovod에서 학습하고 있는 worker의 수를 버튼 하나로 scaling in/out 할 수 있는 API를 제공합니다.

학습의 효율성을 높이기 위해 worker를 scaling in/out 하는 시기를 결정하는 알고리즘을 연구하는데 해당 tool을 사용할 수 있습니다. 이를 통해 분산 학습 클라우드를 효과적으로 관리할 수 있는 platform을 만들 수 있을 것으로 기대하고 있습니다.

### Prerequisites

### How to Build
