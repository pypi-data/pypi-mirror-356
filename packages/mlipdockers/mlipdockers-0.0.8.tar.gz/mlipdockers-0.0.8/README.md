A docker socket allowing for multiple MLIP usages within the same python environment.  
`mlipdockers`是一个实现在同一个python环境中使用不同机器学习原子间势（MLIP）的docker接口。

Install: `pip install mlipdockers`

Integrated machine learning interatomic potentials (MLIPs) including `grace-2l` `chgnet` `mace` `orb-models` `sevenn` `eqv2`. Details can be find in https://matbench-discovery.materialsproject.org/

Our images are uploaded in the Alibaba Cloud. Therefore, to use our package, you need to register an Alibaba Cloud account at https://account.alibabacloud.com/ and install docker.  
docker镜像上传在阿里云，因此需要注册阿里云账号才能使用。

After you register your Alibaba Cloud account, go to the `Container Registry/Instances` page, follow the instruction to register for a totally free `Instance of Personal Edition`, and get your countainer registry [username] and [password] which you will need to login in to the docker registry.  
注册账号以后，进入`容器镜像服务`页面，根据提示注册免费的`个人实例`，在`个人实例`-`访问凭证`获得`docker login ...`命令，复制到本地运行进行登录便获得了访问阿里云上公开镜像的权限。

![image](https://github.com/user-attachments/assets/bd4240f8-f9d2-4f36-990b-579963a7462a)

Finally, execute the `docker login` command provided in your own `Container Registry/Instances` page, and try to run tutorial.ipynb.

Try [examples](https://github.com/HouGroup/mlipdockers/tree/main/examples) now!
