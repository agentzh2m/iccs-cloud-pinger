# Auto Instance Test

* The script will launch an instance at a time to save cost because launching five
instances at the same time is very expensive

* You need to install boto3 `pip install boto3`

* You should also install awscli `pip install awscli`

* then you configure it by running `aws configure` and then put in your
access credential id and secret key you can access from the credential detail when you click
on your account

* Go to the security group of all Asia region and then configure
the default security group to let
any ip in if you are scare we need ssh access from inbound and ping access
from outbound

* Furthermore add your public key to aws and name it whatever you want
then put that name in the keyname variable (do that for every asia region)

* Lastly to run the scipt `python main.py` for some machine that have both
python2 and python3 use `python3 main.py` because this is a python3
script if you run with python2 it will die a horrible death
