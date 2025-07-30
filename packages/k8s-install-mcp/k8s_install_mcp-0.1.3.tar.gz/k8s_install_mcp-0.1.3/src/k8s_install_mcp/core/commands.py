class InstallCommands:

    def __init__(self):
        self.setting_commands = [
            'sudo setenforce 0',
            "sudo sed -i \'s/SELINUX=enforcing/SELINUX=disabled/g\' /etc/selinux/config",
            'sudo systemctl stop firewalld; sudo systemctl disable firewalld',
            "sudo swapoff -a && sudo sed -i \'/ swap / s/^/#/\' /etc/fstab",
            """cat <<EOF | sudo tee /etc/sysctl.d/99-kubernetes-cri.conf
net.bridge.bridge-nf-call-iptables  = 1
net.ipv4.ip_forward                 = 1
net.bridge.bridge-nf-call-ip6tables = 1
EOF""",
            "sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo",
            'sudo dnf install -y containerd.io iproute-tc',
        ]

        self.master_install_commands = [
            # linux settings
            """cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://pkgs.k8s.io/core:/stable:/v1.29/rpm/
enabled=1
gpgcheck=1
gpgkey=https://pkgs.k8s.io/core:/stable:/v1.29/rpm/repodata/repomd.xml.key
EOF""",
            'sudo dnf install -y kubelet kubectl kubeadm',
            'sudo systemctl start kubelet; sudo systemctl enable kubelet',

            # k8s settings
            'sudo modprobe br_netfilter',
            'sudo modprobe overlay',
            'sudo sysctl --system',
            'sudo systemctl start containerd; sudo systemctl enable containerd',
            'sudo rm /etc/containerd/config.toml',
            'sudo containerd config default | sudo tee /etc/containerd/config.toml',
            'sudo systemctl restart containerd',
            'sudo ip route del 10.0.0.0/8; sudo ip route add 10.0.0.0/16 dev enp0s3; sudo systemctl restart NetworkManager',
            "sudo kubeadm init --pod-network-cidr=10.244.0.0/16 | tail -n 2 > token.txt",
            'mkdir -p $HOME/.kube',
            'sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config',
            'sudo chown $(id -u):$(id -g) $HOME/.kube/config',
            'export KUBECONFIG=$HOME/.kube/config',
            'source ~/.bashrc',
            'kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml'
        ]

        self.client_install_commands = [
             """cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://pkgs.k8s.io/core:/stable:/v1.29/rpm/
enabled=1
gpgcheck=1
gpgkey=https://pkgs.k8s.io/core:/stable:/v1.29/rpm/repodata/repomd.xml.key
EOF""",
            'sudo dnf install -y kubelet kubectl kubeadm',
            'sudo systemctl start kubelet; sudo systemctl enable kubelet',

            # k8s settings
            'sudo modprobe br_netfilter',
            'sudo modprobe overlay',
            'sudo sysctl --system',
            'sudo systemctl start containerd; sudo systemctl enable containerd',
            'sudo rm /etc/containerd/config.toml',
            'sudo containerd config default | sudo tee /etc/containerd/config.toml',
            'sudo systemctl restart containerd',
            'sudo ip route del 10.0.0.0/8; sudo ip route add 10.0.0.0/16 dev enp0s3; sudo systemctl restart NetworkManager'
        ]



install_commands = InstallCommands()