import sys, subprocess
import json

is_master = subprocess.check_output(['cat /emr/instance-controller/lib/info/instance.json | jq .isMaster'],
                                    shell=True).strip()

if is_master == "true":
    public_ip = str(sys.argv[1])
    instance_id = subprocess.check_output(['/usr/bin/curl -s http://169.254.169.254/latest/meta-data/instance-id'],
                                          shell=True)
    subprocess.check_call(['aws ec2 associate-address --instance-id %s --public-ip %s' % (instance_id, public_ip)],
                          shell=True)
else:
    instance_id = subprocess.check_output(['/usr/bin/curl -s http://169.254.169.254/latest/meta-data/instance-id'],
                                          shell=True)
    print("Not the master node")

    p = subprocess.Popen(["aws", "emr", "list-clusters", "--active"], stdout=subprocess.PIPE)
    out, err = p.communicate()

    out = out.decode("utf-8")
    out = json.loads(out)

    print(out['Clusters'][0]['Id'])

    p = subprocess.Popen(["aws", "emr", "list-instances", "--cluster-id", out['Clusters'][0]['Id']],
                         stdout=subprocess.PIPE)
    out2, err = p.communicate()

    out2 = out2.decode("utf-8")
    print(out2)
    id_list = []
    for x in json.loads(out2)['Instances']:
        print(x['Ec2InstanceId'])
        id_list.append(x['Ec2InstanceId'])

    print(id_list)
    id_list.pop()
    ip_list = ['ip1', 'ip2', 'ip3']
    d = dict(zip(id_list, ip_list))
    subprocess.check_call(['aws ec2 associate-address --instance-id %s --public-ip %s' % (instance_id, d[instance_id])],
                          shell=True)
